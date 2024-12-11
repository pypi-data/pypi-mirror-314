import os
from pathlib import Path

from vizitig.generate_graph import generate_graph
from vizitig.genes import gene
from vizitig.info import graphs, graphs_path, graph_path_name
from vizitig.update import update_graph
from vizitig.index import build_kmer_index
from vizitig.info import get_graph
from vizitig.paths import index_path_name
from shutil import rmtree
from vizitig.errors import NoIndex, NoGraphException
from vizitig.index import load_kmer_index
from pytest import fixture
from subprocess import run


@fixture(scope="session")
def setup_mini_bcalm_for_tests():
    try:
        _ = get_graph(test_graph_name)
        _ = load_kmer_index(test_graph_name)
    except NoGraphException:
        run("make small_ex", shell=True)
        run("vizitig index build {}".format(test_graph_name), shell=True)
    except NoIndex:
        run("vizitig index build {}".format(test_graph_name), shell=True)
    yield


test_graph_name = "mini_bcalm"
heavy_graph_name = "TO DELETE"
heavy_graph_rna = "TO DELETE"
heavy_graph_annot = "TO DELETE"
heavy_graph_path = Path("to", "delete")

kmer_set_and_nodes = [
    ("ATCGTGAGTCGTAGCTGATGC", [1]),
    ("TTATTCGATTAGCAGTTAGCT", [2]),
    ("AGTCGGATCGATAGCTGATAG", [3]),
]

sequences_set = [
    ("ATCGTGAGTCGTAGCTGATGCTAGCTGATCGATCGGATGTCGTAGCATCGNATTCCAaaaC", [1]),
    ("AGTTATTCGATTAGCAGTTAGCT".lower, [2]),
    ("AGTCGGATCGATAGCTGATAGCTAGCT", [3]),
]


def create_heavy_graph():
    """Creates a heavy graph for testing in the graphs_path folder
    This function is used in a fixture of pytest to clean after a test on the graph was executed."""
    output = graph_path_name(heavy_graph_name)
    generate_graph(
        Path(heavy_graph_path, f"{heavy_graph_name}.fna"), output, heavy_graph_name
    )


def build_index_heavy_graph():
    """Builds the index for the heavy graph"""
    build_kmer_index(heavy_graph_name)


def gene_heavy_graph():
    """ """
    gene(
        heavy_graph_name,
        Path(heavy_graph_path, f"{heavy_graph_annot}"),
        Path(heavy_graph_path, f"{heavy_graph_rna}"),
    )


def delete_heavy_graph():
    """Deletes the heavy graph in the graphs_path folder that contain the test_graph_name.
    This function is used in a fixture of pytest to clean after a test on the graph was executed.
    """
    try:
        del graphs[heavy_graph_name]
    except KeyError:
        pass
    finally:
        for file in graphs_path.glob(f"*{heavy_graph_name}*"):
            os.remove(file)


def create_dummy_graph():
    """Creates a dummy graph for testing in the graphs_path folder.
    This function is used in a fixture of pytest to clean after a test on the graph was executed.
    """
    tmp_file = Path(graphs_path, f"{test_graph_name}.fa")
    tmp_color1 = Path(graphs_path, f"{test_graph_name}_color1.fa")
    tmp_color2 = Path(graphs_path, f"{test_graph_name}_color2.fa")
    tmp_annotations = Path(graphs_path, f"{test_graph_name}_annot.gtf")
    tmp_annot_seq = Path(graphs_path, f"{test_graph_name}_seq.fa")
    tmp_graph = Path(graphs_path, f"{test_graph_name}.db")

    if tmp_graph.exists():
        tmp_graph.unlink()

    with open(tmp_file, "w") as file:
        file.write(
            """>1 Testus_testosaurusTR1 L:+:2:+\nATCGTGAGTCGTAGCTGATGCTAGCTGATCGATCGGATGTCGTAGCATCG\n>2 Testus_testosaurusTR2 L:-:1:- L:+:3:+\nAGTTATTCGATTAGCAGTTAGCT\n>3 Testus_testosaurusTR3 L:-:2:-\nAGTCGGATCGATAGCTGATAGCTAGCT""",
        )

    with open(tmp_color1, "w") as file:
        file.write(
            """
            >blabla\n
            ATCGTGAGTCGGCTGATGCTAGCTGATCGATCGGATGTCGTATAGCATCG
            """,
        )

    with open(tmp_color2, "w") as file:
        file.write(
            """
            >blabla\n
            AGTTATTCGATTAGCAGTTAGAGTTATTCGATTAGCTGATGCTAGCTGATCGATCGGATGTCGTAGTTAGCT
            """,
        )

    with open(tmp_annotations, "w") as file:
        file.write(
            """chr_test\trefGene\ttranscript\t33\t60\t.\t+\t.\tgene_id "testid"; transcript_id "NM_test";  gene_name "TEST";\n
chr_test\trefGene\tgene\t10\t94\t.\t+\t.\tgene_id "super_gene"; gene_name "TEST";,
chr_test\trefGene\tfoo\t8\t130\t.\t+\t.\tgene_id "bar"; gene_name "barbar";""",
        )

    with open(tmp_annot_seq, "w") as file:
        file.write(""">NM_test
TAGCTGATCGATCGGATGTCGTAG
>Something 
TACCACACCCCCCCCCCA
TAGTCGGATCGATAGCTGATAGCTAGCT
AGTTATTCGATTAGCAGTTAGCT
>else
TAGTCGGATCGATAGCTGATAGCTAGCT
ATCGTGAGTCGTAGCTGATGCTAGCTGATCGATCGGATGTCGTAGCATCG
AGTCGGATCGATAGCTGATAGCTAGCT
TACCACACCCCCCCCCCC
>else
TACCACACCCCCCCCCCA
TAGTCGGATCGATAGCTGATAGCTAGCT
TACCACACCCCCCCCCCA
""")

    generate_graph(
        tmp_file,
        tmp_graph,
        test_graph_name,
        21,
        edge_annotation=True,
        directed_edges=True,
        kmer_ingestion=False,
    )

    build_kmer_index(test_graph_name)

    update_graph(test_graph_name, "color1", "color1", tmp_color1, 10**6)

    update_graph(test_graph_name, "color2", "color2", tmp_color2, 10**6)

    gene(test_graph_name, tmp_annotations, tmp_annot_seq)

    # annotate(test_graph_name, tmp_annotations, tmp_annot_seq)


def delete_dummy_graph():
    """Deletes all the files in the graphs_path folder that contain the test_graph_name.
    This function is used in a fixture of pytest to clean after a test on the graph was executed.
    """
    try:
        del graphs[test_graph_name]
    except KeyError:
        pass
    for file in graphs_path.glob(f"*{test_graph_name}*"):
        os.remove(file)


def delete_dummy_index() -> None:
    path: Path = index_path_name(test_graph_name)
    rmtree(path)
