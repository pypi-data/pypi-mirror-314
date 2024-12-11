import random
from pathlib import Path

from pytest import fixture, mark, raises

from vizitig.errors import EmptyExportError
from vizitig.export import export_graph
from vizitig.tests.utils import (
    create_dummy_graph,
    delete_dummy_graph,
    test_graph_name,
    delete_dummy_index,
)


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


@mark.usefixtures("Setup_and_cleaning_fixture_for_vizitig_graph_testing")
def test_export_graph_bcalm_in_normal_conditions(tmp_path: Path):
    test_file = tmp_path / "file"
    export_graph(test_graph_name, list(range(32)), "bcalm", test_file)
    assert test_file.exists()
    test_file.unlink()


@mark.usefixtures("Setup_and_cleaning_fixture_for_vizitig_graph_testing")
def test_export_graph_bcalm_subgraph(tmp_path: Path):
    test_file = tmp_path / "file"
    sample_nodes = random.sample(list(range(32)), 16) + [
        1,
    ]  # We want to extract at least the first node.
    # With small example graphs, it can happen that no nodes are picked in the sample so we add
    # at least the first node to avoid the EmptyExportError
    export_graph(test_graph_name, sample_nodes, "bcalm", test_file)
    assert test_file.exists()
    test_file.unlink()


@mark.usefixtures("Setup_and_cleaning_fixture_for_vizitig_graph_testing")
def test_export_graph_bcalm_crashes_with_bad_nodes_id(tmp_path: Path):
    test_file = tmp_path / "file"
    with raises(EmptyExportError):
        export_graph(test_graph_name, list([-1]), "bcalm", test_file)
    assert not test_file.exists()
