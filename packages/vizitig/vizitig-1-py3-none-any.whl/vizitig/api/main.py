import functools
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from uuid import uuid4

import networkx as nx
from fastapi import FastAPI, HTTPException, UploadFile, status

from vizitig.env_var import VIZITIG_TMP_DIR
from vizitig import query as vizquery
from vizitig import version as vizversion
from vizitig.api.async_utils import async_subproc
from vizitig.api.errors import (
    NodeNotFoundException,
    NoEmptyGraphNameAllowed,
    NoPathFoundException,
    UnknownFormat,
    UnsupportedExtension,
)
from vizitig.api.path import site
from vizitig.api.types import Alignment, AlignStrategy
from vizitig.errors import VizitigException
from vizitig.export import export_format, export_graph
from vizitig.generate_graph import generate_graph
from vizitig.index import (
    IndexInfo,
)
from vizitig.index import (
    build_kmer_index as base_build_kmer_index,
)
from vizitig.index import (
    drop_kmer_index as base_drop_kmer_index,
)
from vizitig.index import (
    index_info as base_index_info,
)
from vizitig.index import (
    index_types as base_index_types,
)
from vizitig.info import (
    add_vizitig_graph,
    get_graph,
)
from vizitig.info import (
    delete_graph as delete_graph_base,
)
from vizitig.info import (
    graph_info as base_graph_info,
)
from vizitig.info import (
    graphs_list as base_graphs_list,
)
from vizitig.info import (
    rename_graph as rename_graph_base,
)
from vizitig.metadata import GraphMetadata, NodeDesc
from vizitig.paths import graph_path_name, log_path_name, root
from vizitig.types import ESign

app = FastAPI()


def wrap_error(fct):
    """Wrap the Vizitig Error into HTTP Error"""

    @functools.wraps(fct)
    async def _fct(*args, **kwargs):
        try:
            return await fct(*args, **kwargs)
        except VizitigException as E:
            # This could be more efficient with an appropriate
            # layout of VizitiException.
            raise HTTPException(detail=f"{E!r}", status_code=400)

    return _fct


def get(*args, **kwargs):
    def ndec(f):
        f = wrap_error(f)
        return app.get(*args, operation_id=f.__name__, **kwargs)(f)

    return ndec


def post(*args, **kwargs):
    def ndec(f):
        f = wrap_error(f)
        return app.post(*args, operation_id=f.__name__, **kwargs)(f)

    return ndec


def patch(*args, **kwargs):
    def ndec(f):
        f = wrap_error(f)
        return app.patch(*args, operation_id=f.__name__, **kwargs)(f)

    return ndec


def delete(*args, **kwargs):
    def ndec(f):
        f = wrap_error(f)
        return app.delete(*args, operation_id=f.__name__, **kwargs)(f)

    return ndec


export_path = Path(root, "export")
if not export_path.exists():
    export_path.mkdir()


@get(
    path="/ryalive",
    status_code=status.HTTP_200_OK,
    description="Endpoint to check that server is online",
)
async def ryalive():
    return "yes master !!"


@get(
    path="/version",
    status_code=status.HTTP_200_OK,
    description="Endpoint to get the current vizitig version",
)
async def version() -> str:
    return vizversion


@get(
    path="/load_viz",
    status_code=status.HTTP_200_OK,
    description="Get the list of available visualisation",
)
async def load_viz() -> list[str]:
    return list(map(lambda e: e.stem, site.glob("js/viz/*.js")))


@get(
    path="/list_graphs",
    status_code=status.HTTP_200_OK,
    description="Get the list of available graphs",
)
async def graphs_list() -> dict[str, Any]:
    result = dict()
    for e in base_graphs_list():
        try:
            data = base_graph_info(e, human_size=True)
        except Exception as E:
            data = dict(error=str(E))
        result[e] = data
    return result


@get(
    path="/export_format",
    status_code=status.HTTP_200_OK,
    description="Get the list of available format to export some graph",
)
async def get_export_format() -> list[str]:
    return sorted(export_format)


@delete(
    path="/graphs/{name}",
    status_code=status.HTTP_200_OK,
    description="Delete the graph",
)
async def delete_graph(name: str) -> None:
    delete_graph_base(name)


@get("/log/{name}")
async def get_log(name: str) -> list[str]:
    try:
        with open(log_path_name(name)) as f:
            return list(f)
    except FileNotFoundError:
        return []


@post(
    path="/graph/{old_name}/{new_name}",
    status_code=status.HTTP_200_OK,
    description="Rename the graph",
)
async def rename_graph(old_name, new_name, replace: bool = False):
    rename_graph_base(old_name, new_name, replace=replace)


def fmt_name(name, idx):
    return f"{name}_copy_{idx}"


@get(
    path="/align/{gname}/{nid1}/{nid2}",
    status_code=status.HTTP_200_OK,
    description="Align the unit data of two nodes",
)
async def align(
    gname: str,
    nid1: int,
    nid2: int,
    strategy: AlignStrategy = "SW",
) -> Alignment:
    G = get_graph(gname)
    try:
        seq1 = G.nodes[nid1]["sequence"]
        seq2 = G.nodes[nid2]["sequence"]
    except KeyError as E:
        raise NodeNotFoundException(detail=E.args[0], status_code=404)
    return Alignment.from_seq(seq1, seq2, strategy=strategy)


@get(
    path="/index/{name}/info",
    status_code=status.HTTP_200_OK,
    description="Get info on the index of the graph",
)
async def index_info(name: str) -> list[IndexInfo]:
    return base_index_info(name)


@get(
    path="/index_types",
    status_code=status.HTTP_200_OK,
    description="Get info on the index of the graph",
)
async def index_types() -> list[str]:
    return base_index_types


@post(
    path="/index/{name}/{index_type}/drop",
    status_code=status.HTTP_200_OK,
    description="Drop indexes of the graph. If the index type is provided, drop only this type",
)
async def drop_index(name: str, index_type: str):
    if index_type is not None:
        base_drop_kmer_index(name, index_type)
    else:
        for idx in base_index_info(name):
            base_drop_kmer_index(name, idx.type)


@post(
    path="/index/{name}/build",
    status_code=status.HTTP_200_OK,
    description="Build an index for the graph. If no type is provided, the some index_type is selected somehow",
)
async def build_index(name: str, index_type: str | None = None):
    if index_type is None:
        index_type = base_index_types[-1]
    await async_subproc(base_build_kmer_index)(name, index_type)


@post(
    path="/duplicate/{name}",
    status_code=status.HTTP_200_OK,
    description="Duplicate the graph",
)
async def duplicate(name: str):
    L = set(base_graphs_list())
    path = graph_path_name(name)
    new_name = name
    idx = 0
    while fmt_name(new_name, idx) in L:
        idx += 1

    name = fmt_name(new_name, idx)
    await async_subproc(add_vizitig_graph)(path, name=name, replace=False, copy=True)


@post(
    path="/upload/{name}",
    status_code=status.HTTP_200_OK,
    description="""
    Upload a graph. 
    If replace is set to True, replace existing graph. 
    If check_compatibility is set to true, check is graph is compatible
    with the current vizitig version (default True)""",
)
async def upload_graph(file: UploadFile, name: str):
    assert file.filename is not None
    path = Path(file.filename)
    gname = path.stem
    if name != "":
        gname = name
    if name == "":
        raise NoEmptyGraphNameAllowed(status_code=402)

    if path.suffix in (".fa", ".gz", ".fasta"):
        try:
            tmp = NamedTemporaryFile(
                prefix=VIZITIG_TMP_DIR, delete=False, suffix=path.suffix
            )
            shutil.copyfileobj(file.file, tmp)  # type: ignore
            tmp_path = Path(tmp.name)
        finally:
            file.file.close()
        await async_subproc(generate_graph)(tmp_path, graph_path_name(name))
        tmp_path.unlink()
    elif path.suffix == ".db":
        try:
            with NamedTemporaryFile(
                prefix=VIZITIG_TMP_DIR, delete=False, suffix=".db"
            ) as tmp:
                shutil.copyfileobj(file.file, tmp)  # type: ignore
                tmp_path = Path(tmp.name)
        finally:
            file.file.close()
        await async_subproc(add_vizitig_graph)(
            tmp_path,
            name=gname,
            replace=False,
            check_compatibility=True,
        )
    else:
        raise UnsupportedExtension(extension=path.suffix, status_code=400)


@post(
    path="/graphs/{name}/export/{format}",
    status_code=status.HTTP_200_OK,
    description="Return a link to the exported file",
)
async def export_nodes(name: str, format: str, nodes: list[int]) -> str:
    """Exports the current nodes of the graph to a file"""
    # If the format is not supported, raise an error
    if format not in export_format:
        raise UnknownFormat(details=format, status_code=404)

    # Matches the export format of front with end
    # This calls the export_format dict from vizitig/export/__init__.py
    ext = export_format.get(format)

    # Generates a 128 bit random string that will serve as file name
    fname = f"{uuid4()}.{ext}"

    # Build the path
    target_path = Path(export_path, fname)

    await async_subproc(export_graph)(name, nodes, format, target_path)
    return f"export/{fname}"


@get(
    path="/graphs/{name}/info",
    status_code=status.HTTP_200_OK,
    description="Returns informations about the graph",
)
async def graph_info(name: str) -> GraphMetadata:
    return get_graph(name).metadata


def build_node_return(
    G,
    nodes: list[int],
) -> list[tuple[int, NodeDesc]]:
    nodes_with_data = G.subgraph(nodes).nodes(data=True)
    L: list[tuple[int, NodeDesc]] = []
    for x, d in nodes_with_data:
        neighbors: dict[int, ESign] = dict()
        adj = G._adj[x].fold()
        for y, od in adj.items():
            neighbors[y] = od.get("sign", None)
        L.append((x, G.metadata.to_nodedesc(d, neighbors)))
    return L


@get(
    path="/graphs/{name}/parse_query/{query}",
    status_code=status.HTTP_200_OK,
    description="Fetch all nodes with a query",
)
async def parse_query(name: str, query: str) -> vizquery.Term:
    return vizquery.parse(query)


@post(
    path="/graphs/{gname}/filters/{fname}/{filter}",
    status_code=status.HTTP_200_OK,
    description="Add a filter to the graph",
)
async def add_filter(gname: str, fname: str, filter: str):
    G = get_graph(gname)
    G.metadata.add_filter(fname, filter)
    G.metadata.commit_to_graph(G)


@post(
    path="/graphs/{gname}/filters/{fname}",
    status_code=status.HTTP_200_OK,
    description="Remove a filter from the graph",
)
async def remove_filter(gname: str, fname: str):
    G = get_graph(gname)
    G.metadata.remove_filter(fname)
    G.metadata.commit_to_graph(G)


@get(
    path="/graphs/{gname}/filters/",
    status_code=status.HTTP_200_OK,
    description="Get all filters of the graph",
)
async def list_filters(gname: str) -> list[tuple[str, str]]:
    G = get_graph(gname)
    return list(G.metadata.get_filters())


@get(
    path="/graphs/{name}/find/query/{query}",
    status_code=status.HTTP_200_OK,
    description="Fetch all nodes with a query",
)
async def find_with_query(name: str, query: str) -> list[tuple[int, NodeDesc]]:
    G = get_graph(name)
    nodes = await async_subproc(vizquery.search)(name, query)
    return build_node_return(G, list(nodes))


@post(
    path="/graphs/{name}/node_data",
    status_code=status.HTTP_200_OK,
    description="Get nodes data in argument (POST only)",
)
async def nodes_data(name: str, nodes: list[int]) -> list[tuple[int, NodeDesc]]:
    G = get_graph(name)
    return build_node_return(G, nodes)


@get(
    path="/graphs/{name}/{nid}",
    status_code=status.HTTP_200_OK,
    description="Get data from `nid`",
)
async def all_nid(name: str, nid: int) -> NodeDesc:
    G = get_graph(name)
    try:
        d = G.nodes[nid].fold()
        nd = G.metadata.to_nodedesc(d, [y for y in G[nid]])
        return nd
    except KeyError:
        raise NodeNotFoundException(detail=nid, status_code=404)


@get(
    path="/graphs/{name}/meta",
    status_code=status.HTTP_200_OK,
    description="Return the metadata information stored in the graph",
)
async def get_all_metadata(name: str) -> GraphMetadata:
    G = get_graph(name)
    return G.metadata


@get(
    path="/graphs/{name}/path/{source}/{target}",
    status_code=status.HTTP_200_OK,
    description="Get the path if it exists between `source` and `target`.",
)
async def get_path(name: str, source: int, target: int):
    G = get_graph(name)
    try:
        return nx.shortest_path(G, source, target)
    except nx.exception.NetworkXNoPath:
        return NoPathFoundException(detail=(source, target), status_code=404)
    except nx.exception.NodeNotFound:
        return NodeNotFoundException(detail=(source, target), status_code=404)
