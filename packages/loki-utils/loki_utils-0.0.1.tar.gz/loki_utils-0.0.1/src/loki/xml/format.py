import ast
from pathlib import Path
from xml.dom import minidom
import click
from loki.io_options import Input, Output
import shlex
import xml.etree.ElementTree as ET


xml_input = Input("input", "i", "Input XML Path")
xml_output = Output("output", "o", "Output XML Path")


@click.command("format")
@xml_input.option()
@xml_output.option()
@click.option(
    "--indent",
    "-d",
    default="  ",
    help="Indentation string (i.e: '\\t'), defaults to 2 spaces",
)
def format(input: Path | None, output: Path | None, indent: str):
    """Format XML."""

    raw = ""
    with xml_input.open(input) as i:
        raw = i.read()

    skip_xml_declaration = True
    if raw.startswith("<?xml"):
        skip_xml_declaration = False

    tree = ET.fromstring(raw)
    for element in tree.iter():
        if element.text and element.text.isspace():
            element.text = None
        if element.tail and element.tail.isspace():
            element.tail = None
    xml_str = ET.tostring(tree, encoding="unicode", short_empty_elements=False)
    pretty_xml = minidom.parseString(xml_str).toprettyxml(
        newl="\n", indent=ast.literal_eval(shlex.quote(indent))
    )

    lines = pretty_xml.split("\n")
    last = lines.pop()
    lines = iter(lines)
    if skip_xml_declaration:
        next(lines)
    with xml_output.open(output) as o:
        for line in lines:
            o.write(line)
            o.write("\n")
        o.write(last)
