import re

NAMESPACES = {
    "l": "http://www.legislation.gov.uk/namespaces/legislation",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "dct": "http://purl.org/dc/terms/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "html": "http://www.w3.org/1999/xhtml",
    "atom": "http://www.w3.org/2005/Atom",
    "ukm": "http://www.legislation.gov.uk/namespaces/metadata",
}


class ParseError(Exception):
    def __init__(self, message, matches):
        super().__init__(message)
        self.matches = matches


def get_single_element(parent, tag):
    elements = parent.findall(tag, namespaces=NAMESPACES)
    if len(elements) != 1:
        raise ParseError(
            "Expected one match for tag '%s', found %i" % (tag, len(elements)),
            len(elements),
        )
    return elements[0]


def get_child_text(parent):
    text = "".join(parent.itertext())
    return re.sub("\s+", " ", text).strip()
