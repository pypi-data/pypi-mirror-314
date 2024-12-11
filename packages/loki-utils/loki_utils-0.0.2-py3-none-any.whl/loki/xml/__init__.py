import click
from loki.xml.find import find
from loki.xml.cut import cut
from loki.xml.format import format
from loki.xml.strip import strip


@click.group("xml")
def xml():
    pass


xml.add_command(find)
xml.add_command(cut)
xml.add_command(format)
xml.add_command(strip)
