from pathlib import Path
from typing import Iterator, Tuple

from vizitig.cli import subparsers
from vizitig.info import get_graph, reload_graph, GraphLogger
from vizitig.parsing import parse_annotations_for_genes, parse_reference_sequences_dna
from vizitig.types import DNA, SubseqData
from vizitig.utils import vizitig_logger as logger
from vizitig.update.bulk_update import bulk_annotate_graph


def main(args):
    with GraphLogger(args.graph_name, "gene"):
        gene(args.graph_name, args.metadata, args.ref_seq, args.parse_only)


def gene(
    graph_name: str, metadata_file: Path, ref_seq_file: Path, parse_only: bool = False
) -> None:
    Graph = get_graph(graph_name)
    k = Graph.metadata.k
    annotation_data: dict[str, SubseqData] = {
        s.id: s for s in parse_annotations_for_genes(metadata_file, k)
    }
    for subseq, _ in parse_reference_sequences_dna(
        ref_seq_file, Graph.metadata, annotation_data
    ):
        Graph.metadata.add_metadata(subseq)

    def generator() -> Iterator[Tuple[DNA, int]]:
        for subseq, dna in parse_reference_sequences_dna(
            ref_seq_file, Graph.metadata, annotation_data
        ):
            yield (dna, Graph.metadata.encoder(subseq))

    if parse_only:
        it_dna = generator()
        it_kmer = (
            (kmer, meta) for dna, meta in it_dna for kmer in dna.enum_canonical_kmer(k)
        )
        logger.info("parsing only")
        logger.info(f"count {sum(1 for _ in it_kmer)}")
        return

    bulk_annotate_graph(graph_name, generator)
    Graph.metadata.commit_to_graph(Graph)
    reload_graph(graph_name)


parser = subparsers.add_parser(
    "genes",
    help="Add gene annotation to a given graph",
)

parser.add_argument(
    "graph_name",
    help="A graph name. List possible graph with python3 -m vizitig info",
    metavar="graph",
    type=str,
)

parser.add_argument(
    "-r",
    "--ref-seq",
    help="Path toward a (possibly compressed) fasta files containing reference sequences",
    metavar="refseq",
    type=Path,
    required=True,
)

parser.add_argument(
    "-m",
    "--metadata",
    help="Path towards a (possibly compressed) gtf files containing metadata of reference sequences",
    metavar="gtf",
    type=Path,
    required=True,
)

parser.add_argument(
    "-p",
    "--parse-only",
    help="Go through the data without ingesting. Provides the number of line to ingest",
    action="store_true",
)

parser.set_defaults(func=main)
