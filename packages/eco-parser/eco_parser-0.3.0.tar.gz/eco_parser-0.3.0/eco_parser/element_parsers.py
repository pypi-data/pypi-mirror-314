import abc

from eco_parser.core import (
    NAMESPACES,
    ParseError,
    get_child_text,
    get_single_element,
)


class ElementParser(metaclass=abc.ABCMeta):
    def __init__(self, element):
        self.element = element

    @abc.abstractmethod
    def parse(self):
        pass


class TableParser(ElementParser):
    FORMAT_UNKNOWN = 0
    FORMAT_STANDARD_TABLE = 1
    FORMAT_ONE_ROW_PARA = 2

    def parse_head(self):
        thead = get_single_element(self.element, "html:thead")
        return tuple(get_child_text(th) for th in thead[0])

    def is_header(self, row):
        if len(row.xpath("./html:th", namespaces=NAMESPACES)) > 0:
            return True
        return False

    def get_table_format(self, tbody):
        if len(tbody) == 1:
            para_tags = tbody.xpath("//l:Para", namespaces=NAMESPACES)
            if len(para_tags) > 0:
                return self.FORMAT_ONE_ROW_PARA
        elif len(tbody) > 1:
            return self.FORMAT_STANDARD_TABLE
        return self.FORMAT_UNKNOWN

    def parse_standard_table(self, tbody):
        data = []
        for row in tbody:
            if not self.is_header(row):
                data.append(tuple(get_child_text(col) for col in row))
        return data

    def parse_one_row_table(self, tbody):
        data = []
        tr = tbody[0]

        i = 0
        for td in tr:
            data.append([])
            for line in td:
                text = get_single_element(line, "l:Text")
                data[i].append(get_child_text(text))
            i = i + 1

        # check all the lists we've found are the same length
        # if not, throw an error
        expected_length = len(data[0])
        for j in range(0, i):
            if len(data[j]) != expected_length:
                raise ParseError(
                    "Expected %i elements, found %i"
                    % (expected_length, len(data[j])),
                    0,
                )

        # transpose rows and columns
        return list(map(tuple, zip(*data)))

    def parse_body(self):
        tbody = get_single_element(self.element, "html:tbody")
        table_format = self.get_table_format(tbody)
        if table_format == self.FORMAT_ONE_ROW_PARA:
            return self.parse_one_row_table(tbody)
        if table_format == self.FORMAT_STANDARD_TABLE:
            return self.parse_standard_table(tbody)
        raise ParseError("Could not detect table format", 0)

    def parse(self):
        try:
            header = [self.parse_head()]
        except ParseError:
            header = []
        return header + self.parse_body()


class BodyParser(ElementParser):
    def parse(self):
        elements = self.element.xpath("//l:Text", namespaces=NAMESPACES)
        return [(get_child_text(el).strip().rstrip(",.;"),) for el in elements]


class ElementParserFactory:
    @staticmethod
    def create(element):
        try:
            tabular = get_single_element(element, "l:Tabular")
            table = get_single_element(tabular, "html:table")
            return TableParser(table)
        except ParseError as e:
            if e.matches == 0:
                return BodyParser(element)
            raise e
