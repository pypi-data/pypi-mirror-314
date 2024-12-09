import pathlib
import json

from .types import JsonFSM

def load_json(infile: pathlib.Path) -> JsonFSM:
    # internally we also use the original json format,
    # so not much to do here
    try:
        fsm = json.load(open(infile))
    except json.JSONDecodeError as ex:
        raise ValueError(f"Error reading json from {infile}:\n{ex}")
    return fsm


def write_json(fsm: JsonFSM, outfile: pathlib.Path):
    with open(outfile, "w") as f:
        f.write(json.dumps(fsm, sort_keys=True, indent=4))
