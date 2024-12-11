from pathlib import Path
from typing import Tuple, Iterator

from vizitig.cli import subparsers
from vizitig.info import get_graph, reload_graph
from vizitig.parsing import (
    parse_annotations,
    parse_reference_sequence_for_full_annotation,
)
from vizitig.types import DNA, SubseqData
from vizitig.update.bulk_update import bulk_annotate_graph
from vizitig.utils import SubLog


def annotate(graph_name: str, metadata: Path, ref_seq: Path):
    with SubLog("annotate"):
        Graph = get_graph(graph_name)
        k = Graph.metadata.k
        annotation_data: list[SubseqData] = list(parse_annotations(metadata, k))

        kmer_annotation: Iterator[Tuple[SubseqData, DNA]] = (
            parse_reference_sequence_for_full_annotation(
                ref_seq,
                annotation_data,
                k,
            )
        )

        metadatas = [Graph.metadata.add_metadata(meta) for meta, _ in kmer_annotation]

        def generator() -> Iterator[Tuple[DNA, int]]:
            it = parse_reference_sequence_for_full_annotation(
                ref_seq,
                metadatas,
                k,
            )
            for meta, dna in it:
                yield dna, Graph.metadata.encode(meta)

        bulk_annotate_graph(graph_name, generator)

        Graph.metadata.commit_to_graph(Graph)
        reload_graph(graph_name)


def main(args) -> None:
    annotate(args.graph_name, Path(args.metadata), Path(args.ref_seq))


parser = subparsers.add_parser(
    "annotate",
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

parser.set_defaults(func=main)
