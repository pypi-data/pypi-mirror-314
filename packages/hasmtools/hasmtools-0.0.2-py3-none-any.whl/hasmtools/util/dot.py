import pathlib
import pydot

from .types import JsonFSM


def json2graph(fsm: JsonFSM) -> pydot.Dot:
    graph = pydot.Dot("HA-FSM", graph_type="graph", rankdir="LR")

    initial = fsm["state"].get("status")
    if not initial:
        raise ValueError("No initial state found.")

    for state, edges in fsm["transitions"].items():
        if state == initial:
            graph.add_node(pydot.Node(state, label=state, shape="doublecircle"))
        else:
            graph.add_node(pydot.Node(state, label=state, shape="circle"))

        for label, dest in edges.items():
            graph.add_edge(
                pydot.Edge(state, dest, label=label, dir="forward", len=5.00)
            )

    return graph


def write_png(fsm: JsonFSM, outfile: pathlib.Path):
    graph = json2graph(fsm)
    graph.write_png(outfile)


def write_svg(fsm: JsonFSM, outfile: pathlib.Path):
    graph = json2graph(fsm)
    graph.write_svg(outfile)


def write_dot(fsm: JsonFSM, outfile: pathlib.Path):
    graph = json2graph(fsm)
    graph.write_dot(outfile)
