import argparse
import csv
import sys

from eco_parser.parser import EcoParser


def main():
    arg_parser = argparse.ArgumentParser(
        description="Parse ward lists from Electoral Change Orders on legislation.gov.uk"
    )
    arg_parser.add_argument(
        "url",
        help="URL to grab XML from e.g: http://www.legislation.gov.uk/uksi/2017/1067/schedule/1/made/data.xml",
    )
    args = arg_parser.parse_args()

    p = EcoParser(args.url)
    data = p.parse()
    writer = csv.writer(sys.stdout)
    for row in data:
        writer.writerow(row)
