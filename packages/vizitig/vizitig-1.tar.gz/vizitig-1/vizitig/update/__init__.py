import gzip
from datetime import datetime
from pathlib import Path

from vizitig.cli import subparsers
from vizitig.info import get_graph, reload_graph
from vizitig.parsing import parse_fasta_dna
from vizitig.types import Color
from vizitig.update.bulk_update import tag_graph_from_dna
from vizitig.utils import SubLog
from vizitig.utils import vizitig_logger as logger

now = datetime.now


def main(args):
    with SubLog("update"):
        update_graph(
            args.graph_name,
            args.metadata_name,
            args.metadata_description,
            args.kmer_file,
            buffer_size=args.buffer_size,
        )


def update_graph(graph_name, m, d, kmer_file, buffer_size=10**6):
    G = get_graph(graph_name)
    GM = G.metadata
    k = GM.k
    color = GM.add_metadata(
        Color(id=m, description=d),
    )
    GM.set_all_offsets()
    GM.commit_to_graph(G)
    del G
    reload_graph(graph_name)

    kmer_files = set((kmer_file,) if kmer_file else ())
    while kmer_files:
        f = kmer_files.pop()
        if not f.exists():
            logger.warning(f"File `{f}` doesn't exists, skipping ...")
            continue
        logger.info(f"Starting with {f}")
        if f.suffix == ".fof":
            with open(f) as file:
                kmer_files.update(map(Path, map(str.strip, filter(bool, file))))
                continue

        def dna_generator():
            openfile = open
            if f.suffix == ".gz":
                openfile = gzip.open
            with openfile(f, "rt") as file:
                yield from filter(
                    lambda e: len(e) >= k, parse_fasta_dna(file, k, buffer_size)
                )

        with SubLog("tag_graph_from_dna"):
            tag_graph_from_dna(
                graph_name,
                dna_generator,
                color,
            )


parser = subparsers.add_parser(
    "update",
    help="update a graph",
)

parser.add_argument(
    "graph_name",
    help="A graph name. List possible graph with python3 -m vizitig info",
    metavar="graph",
    type=str,
)

parser.add_argument(
    "-m",
    "--metadata-name",
    help="A key to identify the metadata to add to the graph",
    metavar="name",
    required=True,
    type=str,
)

parser.add_argument(
    "-d",
    "--metadata-description",
    help="A description of the metadata",
    metavar="description",
    type=str,
    default="",
)

parser.add_argument(
    "-k",
    "--kmer-file",
    help="Path toward files containing DNA (fasta format) or a file of file",
    metavar="file",
    type=Path,
)

parser.add_argument(
    "-b",
    "--buffer-size",
    help="Maximum size of a buffer",
    metavar="buffer",
    type=int,
    default=10**6,
)

parser.add_argument(
    "-c",
    "--color",
    help="Default color to use in the vizualisation. Default is None",
    metavar="color",
    type=str,
)

parser.set_defaults(func=main)
