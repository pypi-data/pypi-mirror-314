import gzip
import logging
import re
from itertools import groupby
from pathlib import Path
from typing import (
    Callable,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    TextIO,
    Tuple,
    cast,
)

from vizitig.metadata import GraphMetadata
from vizitig.types import DNA, ESign, Kmer, SubseqData
from vizitig.utils import vizitig_logger
from vizitig.errors import FormatInputError


class NodeHeader(NamedTuple):
    node_id: int
    metadatas: List[SubseqData]
    sequence: DNA
    successors: tuple[tuple[int, ESign], ...]
    occurence: float | None = None


dna_parse = re.compile(r"(([ACGTacgt]+\n)*)", re.DOTALL)


def parse_fasta_dna(f: TextIO, k: int, buffer_size: int = 10**8) -> Iterator[DNA]:
    buffer = ""
    for line in f:
        if line[0] == ">":
            yield from DNA.from_str(buffer)
            buffer = ""
        else:
            buffer += line.strip().upper()
    yield from DNA.from_str(buffer)


def parse_fasta(f: TextIO, k: int, buffer_size: int = 10**6) -> Iterator[Kmer]:
    for dna in parse_fasta_dna(f, k, buffer_size=buffer_size):
        yield from dna.enum_canonical_kmer(k)


def parse_reference_sequences_dna(
    file_path: Path, GM: GraphMetadata, annotation_data: dict[str, SubseqData]
) -> Iterable[Tuple[SubseqData, DNA]]:
    for bulk in parse_transcript_ref(file_path):
        assert bulk[0] == ">"
        name, remain = bulk.split(maxsplit=1)
        parse_name = annotation_data.get(name[1:])
        if not parse_name:
            continue
        yield from (
            (parse_name, dna) for dna in DNA.from_str(remain.upper().replace("\n", ""))
        )


def parse_transcript_ref(file_path: Path) -> Iterator[str]:
    """
    Amazing and simple parser
    """
    with open(file_path) as file:
        buffer = ""
        for line in file:
            if line[0] == ">" and buffer:
                yield buffer
                buffer = line
            else:
                buffer += line
        yield buffer


def parse_reference_sequences(
    file_path: Path,
    GM: GraphMetadata,
    annotation_data: Iterable[SubseqData],
    log_name: str = "vizitig",
) -> Iterable[Tuple[SubseqData, Kmer]]:
    logger = logging.getLogger(f"{log_name}.refseq")
    openfile: Callable = open
    if file_path.suffix == ".gz":
        openfile = gzip.open

    def emit_data(
        metadata_id: str,
        sequence: str,
        metadata_list: List[SubseqData],
    ) -> Iterable[Tuple[SubseqData, Kmer]]:
        result_filter = list(filter(lambda m: m.id == metadata_id, metadata_list))
        if metadata_id and result_filter == list():
            logger.warning(
                f"{metadata_id} parsed in fasta but not found in annotation file.",
            )
        elif len(result_filter) > 1:
            logger.info(
                f"""Your transcript was found {len(result_filter)} times in the metadata. 
                Please make sure they are no duplicates in your gtf or gff file.
                Stopping process.""",
            )
            raise IndexError
        elif metadata_id != "":
            sequence = sequence.upper()  # This might be done before
            elem = result_filter[0]
            dnas = list(DNA.from_str(sequence))
            first = True
            kmer = None
            for dna in dnas:
                for kmer in dna.enum_canonical_kmer(GM.k):
                    if first:
                        elem = elem.add_first_kmer(kmer)
                    yield (elem, kmer)
                    if elem.gene is not None:
                        yield (
                            SubseqData(
                                type="gene",
                                id=elem.gene,
                                start=-1,
                                stop=-1,
                                list_attr=[],
                            ),
                            kmer,
                        )

            if kmer is not None:
                elem = elem.add_last_kmer(kmer)

    metadata_list = list(annotation_data)

    with openfile(file_path, "rt") as file:
        sequence, metadata_id = "", ""
        for line in file:
            if line and line[0] == ">":
                # BUG HERE, SEE INDEX TESTS
                yield from emit_data(metadata_id, sequence, metadata_list)
                metadata_id = line.strip()[1:].split(".")[0]
                sequence = ""
            else:
                sequence += line.strip().upper()
        if metadata_id:
            yield from emit_data(metadata_id, sequence, metadata_list)


def parse_genes(gene_desc: str) -> Iterator[SubseqData]:
    for gene in gene_desc.split(";"):
        gene_name, transcripts_desc = gene.split(":", maxsplit=1)
        transcripts = list(transcripts_desc.split(","))
        yield SubseqData(
            id=gene_name,
            type="Gene",
            list_attr=list(),
            start=-1,
            stop=-1,
        )  # We don't know yet start and stop. TODO
        for t in transcripts:
            yield SubseqData(
                id=t,
                type="Transcript",
                list_attr=list(),
                start=-1,
                stop=-1,
            )


find_succ = re.compile(r"L:([+-]):(\d+):([+-])")
find_annotation = re.compile(r"genes:\[(.*?)\]")
occurence_pattern = re.compile(r"(?<=km:f:)[+-]?\d+(?:\.\d+)?")


def parse_one(line: str, seq: str) -> NodeHeader:
    """Function parsing one line of BCALM file
    Its important to note that one line refers
    to the one line that was grouped by the previous
    function
    Hereby one line is the header of a bcalm graph
    plus its sequence
    """
    assert line[0] == ">"
    gene_annotations = find_annotation.findall(line)
    assert len(gene_annotations) <= 1
    if gene_annotations:
        parsed_gene_annotations = list(parse_genes(gene_annotations[0]))
    else:
        parsed_gene_annotations = []

    occurence_match = occurence_pattern.findall(line)
    occurence: float | None = None
    if occurence_match:
        assert len(occurence_match) == 1
        occurence = float(occurence_match[0])

    return NodeHeader(
        node_id=int(line.split(" ")[0][1:]),
        occurence=occurence,
        metadatas=parsed_gene_annotations,
        sequence=DNA(seq),
        successors=tuple(
            map(lambda e: (int(e[1]), ESign(e[0] + e[2])), find_succ.findall(line)),
        ),
    )


def parse_one_ggcat(spec, seq) -> Tuple[int, str]:
    """Function parsing one line of BCALM file"""
    node_id = int(spec.split(" ")[0])
    return (node_id, seq)


def _buffer_read_data(f, buffsize) -> Iterator[str]:
    remain = ""
    while True:
        read = f.read(buffsize).decode()
        if not read:
            if remain.strip():
                yield remain.strip()
            return
        x = remain + read
        if "\n" not in x:
            remain = x
            continue
        body, remain = x.rsplit("\n", maxsplit=1)
        yield from body.split("\n")


def get_data(filename: Path, buffsize=10**6) -> Iterator[str]:
    if filename.name.endswith(".gz"):
        with gzip.open(filename) as f:
            yield from _buffer_read_data(f, buffsize)
    else:
        with open(filename, "rb") as f:
            yield from _buffer_read_data(f, buffsize)


def stat_bcalm(filename: Path, buffsize=10**6) -> tuple[int, int, int]:
    """Read a BCALM format and return the node size, edge size and an estimate for k
    obtained by taking the minimum length of a unitig node
    """
    data = get_data(filename, buffsize=buffsize)
    node_size = 0
    edge_size = 0
    estimate_k = 2**63
    for line in data:
        if line[0] != ">":
            estimate_k = min(estimate_k, len(line.strip()))
            continue
        node_size += 1
        edge_size += line.count("L:")
    return node_size, edge_size, estimate_k


def parse(
    filename: Path,
    buffsize=10**6,
) -> Iterator[NodeHeader]:
    """Function parsing a BCALM file returning an iterator over the parsed value

    Assume the file fits in RAM. More work is needed if it isn't the case.
    """
    data = get_data(filename, buffsize=buffsize)
    values = groupby(enumerate(data), lambda e: e[0] // 2)
    yield from (parse_one(spec, seq) for i, ((_, spec), (_, seq)) in values)


def parse_annotations_for_genes(file_path: Path, k: int) -> Iterator[SubseqData]:
    if file_path.suffix == ".gff":
        with open(file_path) as file:
            for elem in _parse_gff(file, k):
                if elem.type.upper() == "TRANSCRIPT":
                    yield elem
    elif file_path.suffix == ".gtf":
        with open(file_path) as file:
            for elem in _parse_gtf(file, k):
                if elem.type.upper() == "TRANSCRIPT":
                    yield elem
    else:
        raise FormatInputError(
            f"Annotation format extension is: {file_path.suffix}. Should be .gff or .gtf."
        )


def parse_annotations(file_path: Path, k: int) -> Iterator[SubseqData]:
    if file_path.suffix == ".gff":
        with open(file_path) as file:
            yield from _parse_gff(file, k)
    elif file_path.suffix == ".gtf":
        with open(file_path) as file:
            yield from _parse_gff(file, k)
    else:
        raise FormatInputError(
            f"Annotation format extension is: {file_path.suffix}. Should be .gff or .gtf."
        )


gene_search = re.compile(r'gene_id "([^"]+)"')
transcript_search = re.compile(r'transcript_id "([^"]+)"')


def _parse_gtf(file, k: int) -> Iterator[SubseqData]:
    for line_counter, line in enumerate(file):
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split("\t")
        match = gene_search.search(line)
        gene_id = match.group(1) if match else None
        match = transcript_search.search(line)
        transcript_id = match.group(1) if match else None
        id_desc = transcript_id or gene_id
        if not id_desc:
            vizitig_logger.error(
                f"ID not found for line {line_counter} of {file}. Make sure your annotation data respect the correct format.",
            )
            continue

        _, _, feature_type, start, stop, _, _, _, bulk_attributes = fields
        attributes = re.sub(r";\s+", ";", re.sub(r";\n", "", bulk_attributes))
        list_attributes = list(filter(bool, map(str.strip, attributes.split(";"))))
        start, stop = int(start), int(stop)
        object_type = feature_type[0].upper() + feature_type[1:]
        if stop - start < k:
            stop = start + k
        yield SubseqData(
            id=id_desc,
            type=object_type,
            list_attr=list_attributes,
            start=start,
            stop=stop,
            gene=gene_id,
        )


id_parser = re.compile(r"ID=([^;]+)")
parent_parser = re.compile(r"Parent=([^;]+)")


def _parse_gff(file, k: int) -> Iterator[SubseqData]:
    for line_counter, line in enumerate(file):
        if not line or line.startswith("#"):
            continue
        id_parsed = id_parser.search(line)
        parent_parsed = parent_parser.search(line)
        id_desc: str | None = None
        if id_parsed is not None:
            id_desc = id_parsed.group(1)
        elif parent_parsed is not None:
            id_desc = parent_parsed.group(1)
        if id_desc is None:
            vizitig_logger.error(
                f"ID not found for line {line_counter} of {file}. Make sure your annotation data respect the correct format.",
            )
            continue

        line = line.strip()
        fields = line.split("\t")

        _, _, feature_type, start, stop, _, strand, _, _ = fields
        _, _, feature_type, start, stop, _, _, _, bulk_attributes = fields
        attributes = re.sub(r";\s+", ";", re.sub(r";\n", "", bulk_attributes))
        list_attributes = attributes.split(";")
        start, stop = int(start), int(stop)
        object_type = feature_type[0].upper() + feature_type[1:]
        if stop - start < k:
            stop = start + k

        yield SubseqData(
            id=id_desc,
            type=object_type,
            list_attr=list_attributes,
            start=start,
            stop=stop,
        )


def parse_reference_sequence_for_full_annotation(
    refseq: Path,
    metadatas: list[SubseqData],
    k: int,
    logger_name: str = "vizitig",
) -> Iterator[Tuple[SubseqData, Kmer]]:
    logger = logging.getLogger(f"{logger_name}.refparsing")
    logger.info("Sorting annotation data before tagging the nodes. ")
    all_metadata: list[SubseqData] = sorted(
        metadatas,
        key=lambda vizikey: vizikey.stop,
    )
    logger.info("Sorting of metadata is finished.")

    # We store in a string a view on the refseq.
    # The string accumulate on the right and each time
    # a metadata.end is reached, it emit all its kmer at once.
    #
    # Then, we can potentially forget part of the refseq to avoid
    # to saturate the RAM. We use for that the min of all start point
    # of all metadata.

    # If all start point are after some value, we will simply skip through it
    # not storing the refseq at all.

    with open(refseq) as file:
        seq_tank = ""
        length_read = 0
        forget = min(m.start for m in all_metadata)
        while all_metadata:
            if all_metadata[0].stop < length_read:
                metadata = all_metadata.pop(0)
                elem, start, stop = (
                    metadata,
                    metadata.start,
                    metadata.stop,
                )
                assert start is not None
                assert stop is not None

                elem = elem.add_first_kmer(
                    Kmer.from_dna(
                        DNA(seq_tank[start - forget : start + k - forget]),
                    ),
                )
                elem = elem.add_last_kmer(
                    Kmer.from_dna(DNA(seq_tank[stop - k - forget : stop - forget])),
                )

                yield (
                    cast(SubseqData, elem),
                    DNA(seq_tank[start - forget : stop - forget]),
                )
                if all_metadata:
                    min_range = min(m.start for m in all_metadata)
                    if min_range > forget:
                        seq_tank = seq_tank[min_range - forget :]
                        forget = min_range

            else:
                buff = file.readline()
                if buff.startswith("#") or buff.startswith(">"):
                    continue
                if buff == "":
                    logger.info(
                        "Reached the end of file without finding all annotation's sequences. Please check your annotation data correspond to your refseq.",
                    )
                    break
                else:
                    data = buff.strip()
                    length_read += len(data)
                    if length_read > forget:
                        seq_tank += data
    logger.info("finished")
