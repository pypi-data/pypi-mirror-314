from pathlib import Path
import click
from loki.io_options import Input, Output
import xml.etree.ElementTree as ET
import Levenshtein

xml_input = Input("input", "i", "Input XML Path")
xml_output = Output("output", "o", "Output XML Path")


@click.command("find")
@xml_input.option()
@xml_output.option()
@click.argument("query")
@click.option(
    "--fuzzy",
    "-f",
    help="Further filter results by edit distance on text content",
    default=None,
)
@click.option(
    "--fuzzy-cutoff",
    "-c",
    type=click.FloatRange(0, 1),
    help="The minimal edit distance ratio to consider",
    default=0,
)
def find(
    input: Path | None,
    output: Path | None,
    query: str,
    fuzzy: str | None,
    fuzzy_cutoff: float,
):
    """Run XPath query, outputs all elements matching the query."""
    with xml_input.open(input) as i:
        tree = ET.fromstring(i.read())
        with xml_output.open(output) as o:
            for element in tree.findall(query):
                if fuzzy is not None:
                    if (
                        element.text is not None
                        and Levenshtein.ratio(
                            element.text, fuzzy, score_cutoff=fuzzy_cutoff
                        )
                        > 0
                    ):
                        o.write(ET.tostring(element, encoding="unicode"))
                else:
                    o.write(ET.tostring(element, encoding="unicode"))
