import argparse
from pathlib import Path
from typing import Iterator, Mapping, MutableMapping, Tuple

from vizitig.cli import subparsers
from vizitig.errors import FileExists
from vizitig.info import GraphLogger, create_graph, graph_path_name
from vizitig.metadata import GraphMetadata
from vizitig.parsing import NodeHeader, parse, stat_bcalm
from vizitig.utils import (
    IteratableFromGenerator,
    SubLog,
    progress,
)
from vizitig.utils import (
    vizitig_logger as logger,
)


def nodes_iter_from_desc(
    it: Iterator[NodeHeader],
    k: int,
    graph_metadata: GraphMetadata,
    kmer_ingestion: bool,
) -> Iterator[Tuple[int, Mapping]]:
    for node in it:
        d: MutableMapping = dict(sequence=str(node.sequence))
        # HERE : add metadata
        if kmer_ingestion:
            for i, kmer in enumerate(node.sequence.enum_canonical_kmer(k)):
                d[kmer] = i
        if node.occurence:
            d["occurence"] = node.occurence
        # d must follow carefully the metadata data plan
        yield (node.node_id, d)


def generate_graph(
    path: Path,
    output_path: Path,
    name: str,
    k: int | None = None,
    kmer_ingestion: bool = False,
    buffsize: int = 10**6,  # Why this value ?
    parse_only: bool = False,
    sql_logger: bool = False,
    edge_annotation: bool = False,
    directed_edges: bool = True,
    raise_no_edges: bool = False,
) -> None:
    """Generate a graph file for vizitig to use"""
    if output_path.exists():
        raise FileExists()

    graph_name = output_path.stem
    with GraphLogger(graph_name):
        if parse_only:
            logger.info("Parse only execution")

        # Compute the number of nodes
        # Uses size_bcalm from vizitig/parsing
        logger.info("Computing some stat")
        size, edge_size, estimate_k = stat_bcalm(path, buffsize=buffsize)
        logger.info(
            f"found {size} nodes, {edge_size} edges and estimated k {estimate_k} ({k} provided)",
        )
        if edge_size == 0:
            msg = "No edge found -- is the input format BCALM?"
            if raise_no_edges:
                raise ValueError(msg)
            logger.info(msg)

        if k is None:
            k = estimate_k

        if not parse_only:
            G = create_graph(
                graph_name,
                k,
                output_path,
                size=size,
                edge_size=edge_size,
                sql_logger=sql_logger,
                directed_edges=directed_edges,
            )
            GM = G.metadata
            G.drop_index()
            G.helper.pragma_fk = False
        logger.info(f"Loading nodes, {kmer_ingestion=}")
        # Builds the list of node (nodeid, dict (canonical kmer, sequence))
        nodes_it = IteratableFromGenerator(
            lambda: progress(
                nodes_iter_from_desc(
                    parse(path, buffsize=buffsize),
                    k,
                    graph_metadata=GM,
                    kmer_ingestion=kmer_ingestion,
                ),
                total=size,
            ),
        )

        if not parse_only:
            with SubLog("node_ingestion"):
                G.add_nodes_from(nodes_it)

        GM.commit_to_graph(G)

        logger.info("Loading edges")
        desc = parse(path, buffsize=buffsize)
        if edge_annotation:

            def edges_it_annotate():
                return progress(
                    (
                        (node.node_id, f, {"sign": s.value})
                        for node in desc
                        for f, s in node.successors
                    ),
                    total=edge_size,
                )

            if not parse_only:
                with SubLog("edge_ingestion"):
                    G.add_edges_from(IteratableFromGenerator(edges_it_annotate))
        else:

            def edges_it():
                return progress(
                    ((node.node_id, f) for node in desc for f, _ in node.successors),
                    total=edge_size,
                )

            with SubLog("edge_ingestion"):
                G.add_edges_without_data_from(IteratableFromGenerator(edges_it))

        if not parse_only:
            with SubLog("indexing"):
                G.reindex()


def build_cli(args):
    """Builds a solid generate_graph call
    Tests if the args are correct and fetches the global variables such as path
    """
    # Name of the input
    input = Path(args.filename)

    # Raises an error if the file does not exist
    if not input.exists():
        raise ValueError(f"{input} is not a valid path to a file")

    name = args.name
    if not name:
        name = input.name

    output = graph_path_name(name)

    # Deletes the current output if already existants and erase = store_true
    # Raises an error otherwise
    if output.exists():
        if args.erase:
            output.unlink()
        else:
            raise FileExists()
    # Finally generate the graph
    with SubLog("build"):
        generate_graph(
            input,
            output,
            name,
            args.k,
            buffsize=args.buffer_size,
            parse_only=args.parse_only,
            kmer_ingestion=args.kmer_ingestion,
            sql_logger=args.sql_logger,
            directed_edges=args.directed_edges,
            edge_annotation=args.edge_annotation,
        )


build = subparsers.add_parser(
    "build",
    help="build a new graph from BCALM file",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
build.add_argument(
    "filename",
    help="A path to BCALM fize (gz compressed possibly)",
    metavar="filename",
    type=str,
)
build.add_argument(
    "-k",
    "--k",
    help="Size of the kmers used to build the graph. By default, the k is estimated from the input file",
    metavar="k",
    type=int,
)

build.add_argument(
    "-e",
    "--erase",
    help="Delete previous graph-file if it already exists",
    action="store_true",
)

build.add_argument(
    "-n",
    "--name",
    help="Set the name of the graph, default is input filename",
)

build.add_argument(
    "--sql-logger",
    help="display the SQL logger",
    action="store_true",
)

build.add_argument(
    "-p",
    "--parse-only",
    help="Simply parse the file and iterates through it without storing the result. For benchmarking purpose",
    action="store_true",
)

build.add_argument(
    "-b",
    "--buffer-size",
    help="A parameter used to bound the memory usage. In case of memory exhaustion, lower the value and increase it to get a faster processing",
    type=int,
    default=10**4,
)

build.add_argument(
    "-i",
    "--kmer-ingestion",
    help="Flag to ingestion kmers. Not ingesting kmers reduces the build time and the size of the vizitig graph, but make the fetching of kmer or require the build of an extra index",
    action="store_true",
    default=False,
)

build.add_argument(
    "--edge-annotation",
    help="Add sign annotation to edges (--, -+, +-, ++)",
    action="store_true",
    default=False,
)

build.add_argument(
    "-d",
    "--directed-edges",
    help="Store edge orientation",
    action="store_true",
    default=False,
)


build.set_defaults(func=build_cli)
