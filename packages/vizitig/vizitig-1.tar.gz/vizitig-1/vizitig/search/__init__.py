import gzip
from pathlib import Path
from typing import Callable, Iterable, Iterator, cast

from vizitig.cli import subparsers
from vizitig.errors import KmerIndexNeeded, NoIndex
from vizitig.export import export_format, export_graph
from vizitig.index import load_kmer_index
from vizitig.info import are_kmer_ingested, get_graph, graph_info, graphs_list
from vizitig.parsing import parse_fasta_dna
from vizitig.types import DNA, Kmer
from vizitig.utils import SubLog, progress
from vizitig.utils import vizitig_logger as logger
from vizitig.index import temporary_kmerset
from vizitig.env_var import VIZITIG_NO_TMP_INDEX

export_formats_str = ", ".join(sorted(export_format))


def fetch_nodes_by_dna(
    graph_name: str, dnas: Callable[[], Iterator[DNA]]
) -> Iterable[int]:
    """Will fetch the nodes that contain one of the provided kmers:"""
    G = get_graph(graph_name)
    k = G.metadata.k
    try:
        kmer_index = load_kmer_index(graph_name)
        logger.info(f"found index {type(kmer_index).__name__}")
        if not VIZITIG_NO_TMP_INDEX:
            index_set = temporary_kmerset(
                dnas, G.metadata.k, index_type=kmer_index.index_type.__name__
            )
            logger.info("index built")
            return kmer_index.intersection_index(index_set)
    except NoIndex:
        logger.warning("no index found, fall back to ingested kmer")

    def kmers():
        return (kmer for dna in dnas() for kmer in dna.enum_canonical_kmer(k))

    return fetch_nodes_by_kmers(graph_name, kmers)


def fetch_nodes_by_kmers(
    graph_name: str, kmers: Iterator[Kmer] | Callable[[], Iterator[Kmer]]
) -> Iterable[int]:
    """Will fetch the nodes that contain one of the provided kmers"""
    G = get_graph(graph_name)
    try:
        kmer_index = load_kmer_index(graph_name)
        logger.info(f"found index {type(kmer_index).__name__}")
        if not VIZITIG_NO_TMP_INDEX:
            kmers = cast(Callable[[], Iterator[Kmer]], kmers)
            index_set = temporary_kmerset(
                kmers, G.metadata.k, index_type=kmer_index.index_type.__name__
            )
            return kmer_index.intersection_index(index_set)
        else:
            if not hasattr(kmers, "__iter__"):
                kmers = cast(Callable[[], Iterator[Kmer]], kmers)
                return kmer_index.intersection(kmers())

            kmers = cast(Iterator[Kmer], kmers)
            return kmer_index.intersection(kmers)

    except NoIndex:
        logger.warning("no index found, fall back to ingested kmer")
    if not are_kmer_ingested(graph_name):
        raise KmerIndexNeeded()
    ## First we store kmers in a temporary table
    KmerTempTable = G.schema.schema.add_table("tmp_kmer", temporary=True)
    kmer_col = KmerTempTable.add_column("kmer", sqltype=G.schema.nodes[1].sqltype)
    G.helper.execute(KmerTempTable.create_query())
    q = KmerTempTable.insert_many()
    with SubLog("Indexing"):
        G.helper.execute(KmerTempTable.create_index_query((kmer_col,)))
    with SubLog("ingestion"):
        G.helper.executemany(q, map(lambda e: (e,), progress(kmers)))
    return G.find_all_nodes(lambda e: e.inset(KmerTempTable))


def fetch_nodes_by_gene(graph_name: str, gene: str) -> set[int]:
    """Will fetch all the nodes labeled by one gene"""
    G = get_graph(graph_name)
    return G.find_all_nodes(gene)


def main(args) -> None:
    info = graph_info(args.graph_name)
    k = info["k"]
    nodes_ids: set[int] = set()
    for kmer_file in args.kmer_files:
        openfile: Callable = open
        if kmer_file.suffix == ".gz":
            openfile = gzip.open

        def generator() -> Iterator[DNA]:
            with openfile(kmer_file) as f:
                yield from parse_fasta_dna(f, k)

        nodes_ids.update(fetch_nodes_by_dna(args.graph_name, generator))
    for node_file in args.node_files:
        with open(node_file) as f:
            nodes_ids.update(map(int, f.read().strip().split()))
    dnas = list(map(lambda e: DNA(e), args.dnas))
    nodes_ids.update(
        fetch_nodes_by_dna(
            args.graph_name,
            lambda: iter(iter(dnas)),
        )
    )
    nodes_ids.update(args.nodes_ids)
    for gene in args.genes:
        nodes_ids.update(fetch_nodes_by_gene(args.graph_name, gene))
    logger.info(f"Collected nodes: {len(nodes_ids)}")
    export_graph(args.graph_name, nodes_ids, args.export_format, args.output_file)


parser = subparsers.add_parser(
    "search",
    description=f"""
Find nodes according to various criteria and output the subgraph in various format.

The nodes can be selected by several means: (kmers in a fasta, unitig ids, genes).
If several options are selected, the results will be cumulative (a node is
selected if it satisified any of the condition.)

Result can be exported to any of the following format: {export_formats_str}.
The default is simply a node list. Most of the export relies on networkx to do the work.

- Pickle will allow to load the networkx graph in Python directly.
- Json is the JSON serialisation of networkx
- bcalm is a custom implementation of the bcalm format with extra metadata provided in the headers (genes and colors)

- For GraphViz format, if a non-dot extension is used, drawing to a file will be attempted.
Requires pygraphviz installed (non-default as it requires also graphviz binaries and dev
to be installed).
""",
)

parser.add_argument(
    "graph_name",
    help=f"A graph name. {graphs_list()}",
    metavar="graph",
    type=str,
    choices=graphs_list(),
)

parser.add_argument(
    "-o",
    "--output-file",
    help="File to store the result. Default is stdin.",
    type=Path,
    required=True,
)

parser.add_argument(
    "-f",
    "--export-format",
    help=f"The export format. One of {export_formats_str}. Default is nodelist",
    default="nodelist",
)

parser.add_argument(
    "-kf",
    "--kmer-files",
    help="Path toward files containing kmers (fasta format, possibly gzip compressed)",
    metavar="kmer_files",
    nargs="+",
    default=[],
    type=Path,
)

parser.add_argument(
    "-d",
    "--dna",
    help="Enumeration of DNA sequences",
    metavar="dna",
    nargs="+",
    default=[],
    type=str,
)

parser.add_argument(
    "-n",
    "--nodes-ids",
    help="Explicit list of node id",
    metavar="nodes",
    nargs="+",
    default=[],
    type=int,
)

parser.add_argument(
    "-nf",
    "--node-files",
    help="A path toward a file containing a list of node id (one per line)",
    metavar="nodes",
    default=[],
    nargs="+",
    type=Path,
)

parser.add_argument(
    "-g",
    "--genes",
    nargs="+",
    help="A list of gene annotations",
    type=str,
    default=[],
)


parser.set_defaults(func=main)
