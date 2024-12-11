from pathlib import Path
import click
from loki.io_options import Input, Output
import xml.etree.ElementTree as ET
from loki.xml.utils import xml_dfs

xml_input = Input("input", "i", "Input XML Path")
xml_output = Output("output", "o", "Output XML Path")


@click.command("cut")
@xml_input.option()
@xml_output.option()
@click.argument("query")
@click.option(
    "--discard-children",
    "-d",
    is_flag=True,
    help="Discard child elements of deselected elements",
    default=False,
)
def cut(input: Path | None, output: Path | None, query: str, discard_children: bool):
    """Run XPath query, outputs all elements NOT matching the query."""

    raw = ""
    with xml_input.open(input) as i:
        raw = i.read()

    xml_declaration = None
    if raw.startswith("<?xml"):
        i = raw.index("?>") + 2
        xml_declaration = raw[0:i]
        if raw[i] == "\n":
            xml_declaration += "\n"

    tree = ET.fromstring(raw)
    matches = tree.findall(query)

    for parent in xml_dfs(tree):
        for i, child in enumerate(list(parent)):
            if child in matches:
                matches.remove(child)
                parent.remove(child)
                if not discard_children:
                    for grandchild in child:
                        parent.insert(i, grandchild)

        if parent.text and parent.text.isspace() and len(parent) == 0:
            parent.text = None
    xml_str = ET.tostring(tree, encoding="unicode", short_empty_elements=False)

    with xml_output.open(output) as o:
        if xml_declaration is not None:
            o.write(xml_declaration)
        o.write(xml_str)
