import json
import pickle
from pathlib import Path
from typing import Dict, Sized

import networkx as nx

from vizitig.errors import EmptyExportError, FileExists
from vizitig.info import get_graph
from vizitig.types import Kmer, Color
from vizitig.utils import vizitig_logger

export_format = dict(
    bcalm="fa",
    json="json",
    networkx_pickle="pickle",
    gml="gml",
    graphviz="dot",
    nodelist="list",
)


def export_bcalm_by_iterator(graph_name: str, outputfile: str, batch_size=100):
    G = get_graph(graph_name)
    it = G.nbunch_iter()

    somme = sum(1 for _ in it)
    print("Number of nodes: ", somme)

    it = G.nbunch_iter()

    with open(outputfile + ".bcalm", "w") as file:
        buffer = list()
        for i, node in enumerate(it):
            buffer.append(dump_one_node_bcalm_for_iterator(G, node) + "\n")

            if (i + 1) % batch_size == 0:
                print(i)
                file.writelines(buffer)
                del buffer
                buffer = list()
                file.flush()

            del node

        if buffer:
            file.writelines(buffer)
            file.flush()


def dump_one_node_bcalm_for_iterator(G, node) -> str:
    s = f">{node}"
    sequence = G.nodes[node]["sequence"]
    neighbors: Dict[int, str] = dict()
    for target, esign in G[node].items():
        if esign:
            neighbors[target] = esign["sign"].value
        else:
            neighbors[target] = (
                "++"  # compute_sign(sequence, G.nodes[target]["sequence"])
            )
    edges = (f"L:{sign[0]}:{target}:{sign[1]}" for target, sign in neighbors.items())
    s += f" {' '.join(edges)}"

    colors: list[str] = list()
    for item in G.nodes[node]:
        if isinstance(item, Color):
            colors.append(str(item.offset))
    colors.reverse()
    color_header = ":".join(colors)
    return f"{s} [{color_header}]\n{sequence}"


def dump_one_node_bcalm(G, node) -> str:
    s = f">{node}"
    sequence = G.nodes[node]["sequence"]
    neighbors: Dict[int, str] = dict()
    for target, esign in G[node].items():
        if esign:
            neighbors[target] = esign["sign"].value
        else:
            neighbors[target] = (
                "  "  # compute_sign(sequence, G.nodes[target]["sequence"])
            )
    edges = (f"L:{sign[0]}:{target}:{sign[1]}" for target, sign in neighbors.items())
    s += f" {' '.join(edges)}"
    return f"{s}\n{sequence}"


def dump_bcalm(graph: nx.Graph, output_file: Path):
    with open(output_file, "a") as f:
        f.write("\n".join(map(lambda node: dump_one_node_bcalm(graph, node), graph)))


def export_graph(
    graph_name: str, nodes: Sized, format: str, output: Path, bcalm_iterator=False
):
    # Get a clean path object
    output_file = Path(output)

    # Raise en error if the file already exists
    if output_file.exists():
        raise FileExists(output_file)

    # Get the graph

    Graph = get_graph(graph_name)

    # Create a subgraph with the nodes to store
    # The subgraph will be loaded in RAM by networkx
    SubGraph = Graph.subgraph(nodes, temporary_table=True).copy_to_networkx()
    SubGraph.metadata = Graph.metadata
    if len(SubGraph) < len(nodes):
        vizitig_logger.warning(
            f"Some nodes are not experted (nodes exported: {len(SubGraph)}/{len(nodes)})",
        )
    if len(SubGraph) == 0:
        raise EmptyExportError

    for node, data in SubGraph.nodes(data=True):
        for key in list(data):
            if isinstance(key, Kmer):
                del data[key]

    # TODO, would be better to have this operation in subgraph?

    format = format.lower()

    if format == "json":
        with open(output_file, "w") as f:
            json.dump(nx.node_link_data(SubGraph), f)
    elif format == "pickle":
        with open(output_file, "wb") as f:
            pickle.dump(SubGraph, f)
    elif format == "bcalm":
        dump_bcalm(SubGraph, output_file)
    elif format == "graphviz":
        graphviz_graph = nx.nx_agraph.to_agraph(SubGraph)
        if output_file.suffix == ".dot":
            graphviz_graph.write(output_file)
        else:
            graphviz_graph.draw(output_file)
    elif format == "gml":
        nx.write_gml(SubGraph, output_file, lambda e: "" if e is None else e)
    elif format == "nodelist":
        with open(output_file, "w") as f:
            f.write("\n".join(map(str, SubGraph)))
    else:
        raise NotImplementedError(format)
    return SubGraph.nodes
