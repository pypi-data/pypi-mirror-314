from pytest import fixture, mark
from vizibridge import DNA, Kmer

from vizitig.info import get_graph
from vizitig.tests.utils import (
    create_dummy_graph,
    delete_dummy_graph,
    delete_dummy_index,
    test_graph_name,
)
from vizitig.types import DNAPython, KmerPython

mixed_types_kmers = [KmerPython, Kmer]
mixed_types_dna = [DNAPython, DNA]

sequences = [
    "TGCTATCGATTCGATATCAGATTCGATCGG",
    "ATGCTAGTCTGATCGATTAGCTTAGCTTAGTCTAGTAGCTAGGCTAGATCGATCGTAGCTGAT",
]


class TestVizibridge:
    @mark.usefixtures("Setup_and_cleaning_fixture_for_vizitig_graph_testing")
    @mark.parametrize("seq", sequences)
    def test_vizibridge_kmers(self, seq: str):
        G = get_graph(test_graph_name)
        k = G.metadata.k
        l1 = list(next(DNA.from_str(seq)).enum_canonical_kmer(k))
        l2 = list(next(DNAPython.from_str(seq)).enum_canonical_kmer(k))
        assert len(l1) == len(l2)
        for i in range(len(l1)):
            assert l1[i].data == l2[i].data

    @mark.usefixtures("Setup_and_cleaning_fixture_for_vizitig_graph_testing")
    @mark.parametrize("seq", sequences)
    def test_vizibridge_kmers_enumeration(self, seq: str):
        G = get_graph(test_graph_name)
        k = G.metadata.k
        l1 = list(next(DNA.from_str(seq)).enum_kmer(k))
        l2 = list(next(DNAPython.from_str(seq)).enum_kmer(k))
        assert len(l1) == len(l2)
        for i in range(len(l1)):
            assert l1[i].data == l2[i].data

    # @mark.usefixtures("Setup_and_cleaning_fixture_for_vizitig_graph_testing") -> !! Need to redo this test using queries
    # @mark.parametrize("kmer_seq, result", kmer_set_and_nodes)
    # @mark.parametrize("DNAType", mixed_types_dna)
    # def test_vizibridge_kmer_coherence(
    #     self,
    #     kmer_seq: str,
    #     result: List[int],
    #     DNAType: Type,
    # ):
    #     G = get_graph(test_graph_name)
    #     K1 = Kmer.from_dna(next(DNAType.from_str(kmer_seq))).canonical()
    #     K2 = KmerPython.from_dna(next(DNAType.from_str(kmer_seq))).canonical()
    #     breakpoint()
    #     assert list(G.find_all_nodes(K1)) == result
    #     assert list(G.find_all_nodes(K2)) == result

    # The idea of this test is to make sure we get the same result by using
    # DNA in Python or Rust, but fails because we should not use DNA
    # classes to query graphs. The tests will be commented for the sake of
    # remembering to test the query of sequences, but cannot remain as it is
    # @mark.usefixtures("Setup_and_cleaning_fixture_for_vizitig_graph_testing")
    # @mark.parametrize("sequence, result", sequences_set)
    # def test_vizibridge_dna_coherence(self, sequence: str, result: List[int]):
    #     G = get_graph(test_graph_name)
    #     D1 = next(DNA.from_str(sequence))
    #     D2 = next(DNAPython.from_str(sequence))
    #     assert list(G.find_all_nodes(D1)) == result
    #     assert list(G.find_all_nodes(D2)) == result


@fixture(scope="function")
def Setup_and_cleaning_fixture_for_vizitig_graph_testing():
    """This fixture is used to setup and clean before and after a test.
    First it calls create_dummy_grah that creates a dummy graph and will be
    used for testing, then it deletes all the files that contain the
    test_graph_name wth delete_dummy_graph, to remove the .db and .fa
    files that were created for the test.
    In between, it runs the test.
    """
    delete_dummy_graph()
    delete_dummy_index()
    create_dummy_graph()
    yield
    delete_dummy_graph()
    delete_dummy_index()
