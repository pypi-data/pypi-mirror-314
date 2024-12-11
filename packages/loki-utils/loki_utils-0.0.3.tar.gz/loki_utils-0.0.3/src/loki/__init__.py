import click
from loki.xml import xml


@click.group("loki")
def main():
    pass


main.add_command(xml)
