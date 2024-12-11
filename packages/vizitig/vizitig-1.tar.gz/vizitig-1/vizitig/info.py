import argparse
import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import networkdisk as nd
from networkdisk.sqlite import DiGraph, Graph
from networkdisk.sqlite import sqlitedialect as sqlited
from tabulate import tabulate, tabulate_formats

from vizitig.cli import subparsers
from vizitig.errors import FileExists, NameAlreadyTaken, NoGraphException
from vizitig.metadata import GraphMetadata
from vizitig.paths import (
    graph_path_name,
    graphs_log,
    graphs_path,
    log_path_name,
)
from vizitig.types import Zero
from vizitig.utils import (
    SubLog,
    new_gid,
    number_fmt,
    sizeof_fmt,
)
from vizitig.utils import (
    vizitig_logger as logger,
)
from vizitig.env_var import VIZITIG_TMP_DIR

graphs = {}


def graphs_list() -> list[str]:
    # TODO: this is probably not portable
    graphs = set([f.stem for f in graphs_path.glob("*.db") if f.stem[0] != "."])
    return sorted(graphs)


def clean_log():
    if graphs_log.exists():
        shutil.rmtree(graphs_log)


def are_kmer_ingested(gname) -> bool:
    """We say yes if at least one value greater than 0 exists"""
    G = get_graph(gname)
    if not hasattr(G, "kmer_ingested"):
        try:
            next(iter(G.find_all_nodes(lambda e: e.gt(Zero()))))
            G.kmer_ingested = True
        except StopIteration:
            G.kmer_ingested = False
    return G.kmer_ingested


def create_graph(
    graph_name: str,
    kmer_size: int,
    output_path: Path,
    size: int,
    edge_size: int,
    sql_logger: bool = False,
    directed_edges: bool = True,
) -> DiGraph | Graph:
    GM = GraphMetadata(
        name=graph_name,
        k=kmer_size,
        size=size,
        edge_size=edge_size,
        gid=new_gid(),
    )
    graph_factory = Graph
    if directed_edges:
        graph_factory = DiGraph
    G = graph_factory(
        db=output_path,
        schema=dict(
            node="INT",
            node_datakey=f"VIZI_{GM.gid}",
            node_datavalue="JSON",
        ),
        sql_logger=sql_logger,
    )
    G.metadata = GM
    GM.commit_to_graph(G)
    return G


def regenerate_schema(graph):
    some_G = type(graph)(
        schema=dict(
            node="INT",
            node_datakey=f"VIZI_{graph.metadata.gid}",
            node_datavalue="JSON",
        ),
    )
    graph.master.delete_graph(masterid=1)
    graph.master.save_graph(some_G, masterid=1)


def rename_graph(old_name: str, new_name: str, replace: bool = False) -> None:
    L = graphs_list()
    if old_name not in L:
        raise NoGraphException(old_name)
    if new_name in L and not replace:
        raise NameAlreadyTaken(new_name)
    shutil.move(graph_path_name(old_name), graph_path_name(new_name))


def delete_graph(name: str) -> None:
    L = graphs_list()
    if name not in L:
        raise NoGraphException(name)
    os.unlink(graph_path_name(name))


def add_vizitig_graph(
    path: Path,
    name: str | None,
    replace: bool = False,
    check_compatibility: bool = False,
    copy=False,
) -> None:
    """Add an already existing graph to vizitig.
    Some issue with gid:
        to avoid issues, each graph should have a distinct gid.
        This is used to encode/decode metadata as networkdisk is too limited for now
        to do that in a flexible way.

        Hence, we need to regenerate the schema with type which depends of this gid.
    """
    if not path.exists():
        raise ValueError(f"Invalid {path}")
    if name is None:
        name = path.stem
    if name == "":
        raise ValueError("Graph name should be non empty")
    if name in graphs_list() and not replace:
        raise FileExists(f"{name} already exists")
    G = get_graph_from_path(path)
    GraphMetadata.set_metadata(
        G,
        check_compatibility=check_compatibility,
    )  # check compatibility mostly

    if copy:
        with tempfile.NamedTemporaryFile(prefix=VIZITIG_TMP_DIR, delete=False) as f:
            logger.info(f"Copy {path} to {f.name}")
            shutil.copy(path, f.name)  # this should happen info to log file eventually
            logger.info(f"mv {f.name} to {graph_path_name(name)}")
            shutil.move(f.name, graph_path_name(name))
    else:
        shutil.move(path, graph_path_name(name))

    new_G = get_graph_from_path(graph_path_name(name))
    GraphMetadata.set_metadata(new_G)
    new_G.metadata.gid = new_gid()  # refresh gid to avoid collision when dl/copying etc
    new_G.metadata.model_post_init(None)
    regenerate_schema(new_G)
    new_G.metadata.commit_to_graph(new_G)


def get_graph_from_path(
    path: Path,
    sql_logger=False,
    check_compatibility=True,
) -> DiGraph | Graph:
    master = sqlited.master.MasterGraphs(db=path)
    ## UGLY HACK
    # we can't know the gid of the graph before loading it
    # we can't load the graph without the gid because stored in the graph schema
    # we catch the gid with the key_error raise in the encoder function, set dummy function
    # and then build the metdata.
    key = None
    try:
        return master.load_graph()
    except KeyError as K:
        key = K.args[0]
        nd.utils.serialize.encoderFunctions[key] = (lambda e: e, lambda e: e)
        return master.load_graph()


def get_graph(name: str, sql_logger=False, check_compatibility=True) -> DiGraph | Graph:
    if name not in graphs:
        L = graphs_list()
        if name not in L:
            raise NoGraphException()
        if not name:
            raise ValueError
        G = graphs[name] = get_graph_from_path(graph_path_name(name))
        GraphMetadata.set_metadata(
            G, check_compatibility=check_compatibility, name=name
        )  # this should be safe to remove
        # once all graph in the wild have a metadata.name set
        # this is a quickfix to avoid a break in compatibility of old graph
    else:
        G = graphs[name]
    return G


def reload_graph(name: str) -> None:
    G = get_graph(name)
    G.helper.close()
    del graphs[name]
    del G
    return get_graph(name)


def graph_info(name: str, human_size: bool = False) -> dict[str, Any]:
    from vizitig.index import index_info  # avoiding circular import

    G = get_graph(name)
    f = graph_path_name(name)
    d = G.metadata.model_dump()
    d.update(
        dict(
            name=f.stem,
            file_size=f.stat().st_size,
            path=str(f),
            log_exists=log_path_name(name).exists(),
            index=index_info(name),
        ),
    )
    if human_size:
        d["file_size"] = sizeof_fmt(d["file_size"])
        d["node nb"] = number_fmt(d.pop("size"))
        d["edge nb"] = number_fmt(d.pop("edge_size"))
        d["index"] = [idx.model_dump() for idx in d["index"]]
        for idx in d["index"]:
            idx["size"] = sizeof_fmt(idx["size"])

    return d


def pretty_info(d: dict[str, Any]) -> dict[str, Any]:
    pretty_d = dict()
    for k, v in d.items():
        if isinstance(v, list):
            if len(v) > 3:
                pretty_d[k] = ", ".join(map(repr, v[:3] + [f"... ({len(v)})"]))
            else:
                pretty_d[k] = ", ".join(map(repr, v))
        else:
            pretty_d[k] = v
    for key in ("types_list", "vars_names", "vars_values", "filter_list", "log_exists"):
        pretty_d.pop(key)
    pretty_d["path"] = str(pretty_d["path"])
    pretty_d["index"] = ", ".join(
        map(lambda e: f'{e["type"]}({e["size"]})', d["index"]),
    )
    pretty_d["Viz Vers."] = pretty_d.pop("vizitig_version")
    pretty_d.pop("gid")
    return pretty_d


def main(args: argparse.Namespace) -> None:
    if args.format == "json":
        from json import dumps as jsondumps

        data = [graph_info(f) for f in graphs_list()]
        for d in data:
            d["index"] = [idx.model_dump() for idx in d["index"]]
        print(jsondumps(data))
    elif args.format in tabulate_formats:
        data = [pretty_info(graph_info(f, human_size=True)) for f in graphs_list()]
        print(tabulate(data, headers="keys", tablefmt=args.format))
    else:
        raise NotImplementedError(args.format)


@contextmanager
def GraphLogger(name: str, message: str | None = None):
    path = log_path_name(name)
    if message is None:
        message = name
    try:
        with SubLog(message, file=path):
            yield path
    finally:
        if path.exists():
            path.unlink()


OutputFormat = ["human", "json"]

parser = subparsers.add_parser(
    "info",
    help="get information about ingested graphs",
)

parser.add_argument(
    "--format",
    help=f"Output format, default is human readable text, choice: {OutputFormat}",
    metavar="output",
    type=str,
    choices=OutputFormat,
    default="simple",
)
parser.set_defaults(func=main)


def main_rename(arg: argparse.Namespace):
    rename_graph(arg.old_name, arg.new_name, replace=arg.replace)


parser = subparsers.add_parser(
    "rename",
    help="Rename a graph",
)

parser.add_argument(
    "old_name",
    help="Current graph name",
    type=str,
)

parser.add_argument(
    "new_name",
    help="New graph name",
    metavar="old_graph",
    type=str,
)

parser.add_argument(
    "-r",
    "--replace",
    help="Replace existing graph",
    action="store_true",
    default=False,
)

parser.set_defaults(func=main_rename)


def main_import(arg: argparse.Namespace):
    add_vizitig_graph(arg.path, name=arg.name, replace=arg.replace)


parser = subparsers.add_parser(
    "add",
    help="Add an already built Vizitig Graph",
)

parser.add_argument(
    "path",
    help="Path to the file",
    type=Path,
)

parser.add_argument(
    "-n",
    "--name",
    help="A name for the graph (default is the file name)",
    type=str,
)

parser.add_argument(
    "-r",
    "--replace",
    help="Replace existing graph",
    action="store_true",
    default=False,
)

parser.set_defaults(func=main_import)


parser = subparsers.add_parser(
    "rm",
    help="Remove an already built Vizitig Graph",
)

parser.add_argument(
    "name",
    help=f"The name of the graph: {graphs_list()}",
    type=str,
    metavar="name",
    choices=graphs_list(),
)


def main_delete(arg: argparse.Namespace):
    delete_graph(arg.name)


parser.set_defaults(func=main_delete)
