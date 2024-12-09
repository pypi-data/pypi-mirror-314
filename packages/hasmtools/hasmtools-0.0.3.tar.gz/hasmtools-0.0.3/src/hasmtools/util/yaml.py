#!/usr/bin/env python3
import pathlib
import yaml

from .types import YamlFSM, JsonFSM


def yaml2json(fsm_yaml: YamlFSM) -> JsonFSM:
    first = True
    ret = {"transitions": {}}
    for state, edges in fsm_yaml.items():
        if first:
            first = False
            ret["state"] = {"status": state}
        ret["transitions"][state] = edges
    return ret


def json2yaml(fsm: JsonFSM) -> YamlFSM:
    ret = {}

    initial = fsm["state"].get("status")
    if not initial:
        raise ValueError("No initial state found")

    # we need to write out the initial state first:
    ret[initial] = fsm["transitions"][initial]

    # now all the others:
    for state, edges in fsm["transitions"].items():
        if state == initial:
            continue
        else:
            ret[state] = edges
    return ret


def load_yaml(infile: pathlib.Path) -> JsonFSM:
    with open(infile) as stream:
        try:
            fsm = yaml.safe_load(stream)
        except yaml.YAMLError as ex:
            raise ValueError(f"Error reading yaml from {infile}:\n{ex}")
    return yaml2json(fsm)


def write_yaml(fsm: JsonFSM, outfile: pathlib.Path):
    fsm_y = json2yaml(fsm)
    with open(outfile, "w") as f:
        yaml.dump(fsm_y, f, sort_keys=False)
