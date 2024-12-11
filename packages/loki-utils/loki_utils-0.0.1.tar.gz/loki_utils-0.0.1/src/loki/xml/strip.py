from pathlib import Path
import click
from loki.io_options import Input, Output
import xml.etree.ElementTree as ET
from loki.xml.utils import xml_dfs

xml_input = Input("input", "i", "Input XML Path")
xml_output = Output("output", "o", "Output XML Path")


@click.command("strip")
@xml_input.option()
@xml_output.option()
@click.option(
    "--attributes",
    "-a",
    multiple=True,
    help="Attributes to remove, can be specified multiple times or as a semicolon separated list ('-a id -a class' or '-a id:class')",
)
@click.option(
    "--tags",
    "-t",
    multiple=True,
    help="Tags to remove, can be specified multiple times or as a semicolon separated list ('-t row -t p' or '-a row:p')",
)
@click.option(
    "--discard-children",
    "-d",
    is_flag=True,
    help="Discard child elements of deselected elements",
    default=False,
)
def strip(
    input: Path | None,
    output: Path | None,
    attributes: tuple[str, ...],
    tags: tuple[str, ...],
    discard_children: bool,
):
    """Remove attributes and tags from XML. Child elements of removed elements are added to the removed elements parent."""

    split_attributes = []
    for attribute in attributes:
        if ":" in attribute:
            split_attributes += attribute.split(":")
        else:
            split_attributes.append(attribute)
    attributes = tuple(split_attributes)

    split_tags = []
    for tag in tags:
        if ":" in tag:
            split_tags += tag.split(":")
        else:
            split_tags.append(tag)
    tags = tuple(split_tags)

    with xml_input.open(input) as i:
        tree = ET.fromstring(i.read())

        for element in xml_dfs(tree):
            for i, child in enumerate(list(element)):
                if child.tag in tags:
                    element.remove(child)
                    if not discard_children:
                        for grandchild in child:
                            element.insert(i, grandchild)
                    if element.text and element.text.isspace() and len(element) == 0:
                        element.text = None
        for element in tree.iter():
            for attribute in attributes:
                if attribute in element.attrib:
                    del element.attrib[attribute]
        xml_str = ET.tostring(tree, encoding="unicode", short_empty_elements=False)

        with xml_output.open(output) as o:
            o.write(xml_str)
