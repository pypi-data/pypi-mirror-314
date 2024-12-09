#!/usr/bin/env python3
import click
import pathlib

from .util.types import JsonFSM
from .util.yaml import load_yaml, write_yaml
from .util.json import load_json, write_json
from .util.dot import write_png, write_svg, write_dot


@click.command()
@click.argument("infile", metavar="INPUT")
@click.argument("outfile", metavar="OUTPUT")
@click.option(
    "--input-format",
    "-i",
    type=click.Choice(["JSON", "YAML"], case_sensitive=False),
    #    default="JSON",
    #    show_default=True,
    help="force input file format",
)
@click.option(
    "--output-format",
    "-o",
    type=click.Choice(["PNG", "SVG", "DOT", "JSON", "YAML"], case_sensitive=False),
    #    default="PNG",
    #    show_default=True,
    help="force output file format",
)
@click.option("--overwrite", "-f", is_flag=True, help="overwrite existing output files")
@click.version_option(
    message="%(prog)s, version %(version)s - Home Assistant State Machine Tools"
)
def cli(infile, outfile, input_format, output_format, overwrite):
    """
    This utility lets you convert the json format used for defining the
    State Machine in Home Assistant into various output formats.
    Notably you can create a png or svg file visualizing the FSM.

    Internally this tool uses graphviz, you can also store the graph as dotfile.

    You can also convert between JSON and YAML - in both directions.

    In YAML the first state that is defined will become the initial state.

    """
    # click file feels too inflexible, e.g. our outfile is either text or binary
    infile = pathlib.Path(infile)
    outfile = pathlib.Path(outfile)

    if not infile.exists():
        raise click.ClickException(f"File not found: {infile}")

    if outfile.exists() and not overwrite:
        raise click.ClickException(f"Refusing to overwrite {outfile}")

    if input_format is None:
        ftype = infile.suffix.lower()
        if ftype in (".yaml", ".yml"):
            input_format = "YAML"
        elif ftype == ".json":
            input_format = "JSON"

    if output_format is None:
        ftype = outfile.suffix.lower()
        if ftype == ".png":
            output_format = "PNG"
        elif ftype == ".svg":
            output_format = "SVG"
        elif ftype == ".dot":
            output_format = "DOT"
        elif ftype == ".json":
            output_format = "JSON"
        elif ftype == ".yaml":
            output_format = "YAML"

    if input_format == "YAML":
        fsm: JsonFSM = load_yaml(infile)
    elif input_format == "JSON":
        fsm: JsonFSM = load_json(infile)
    else:
        raise click.ClickException(f"Unsupported input format {input_format}")

    if output_format == "PNG":
        write_png(fsm, outfile)
    elif output_format == "SVG":
        write_svg(fsm, outfile)
    elif output_format == "DOT":
        write_dot(fsm, outfile)
    elif output_format == "JSON":
        write_json(fsm, outfile)
    elif output_format == "YAML":
        write_yaml(fsm, outfile)
    else:
        raise click.ClickException(f"Unsupported output format {output_format}")


if __name__ == "__main__":
    cli()
