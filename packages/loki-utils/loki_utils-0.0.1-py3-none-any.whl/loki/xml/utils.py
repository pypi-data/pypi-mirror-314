from typing import Generator
import xml.etree.ElementTree as ET


def xml_dfs(element: ET.Element) -> Generator[ET.Element, None, None]:
    """Iterate through this element and all children depth-first.

    :param element: root element
    :type element: ET.Element
    :yield: all sub elements
    :rtype: Generator[ET.Element, None, None]
    """
    for child in element:
        yield from xml_dfs(child)
    yield element
