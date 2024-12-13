# ECO Parser

[![Run tests](https://github.com/DemocracyClub/eco-parser/actions/workflows/test.yml/badge.svg)](https://github.com/DemocracyClub/eco-parser/actions/workflows/test.yml)
![PyPI Version](https://img.shields.io/pypi/v/eco-parser.svg)
![License](https://img.shields.io/pypi/l/eco-parser.svg)
![Python Support](https://img.shields.io/pypi/pyversions/eco-parser.svg)

Parse ward lists from Electoral Change Orders on http://www.legislation.gov.uk/

## What does this package do?

This package solves a very specific problem.

Local Government electoral divisions/wards in the UK are defined by a piece of legislation called an Electoral Change Order. An Electoral Change Order (ECO) always comes into force the day before the first election which is held using the boundaries it defines. Once this first election has happened, details of the new divisions are fairly easy to get hold of. They are published as machine-readable structured data by organisations like [Ordnance Survey](https://www.ordnancesurvey.co.uk/business-and-government/products/boundary-line.html) and the [Office for National Statistics](http://geoportal.statistics.gov.uk/). If you need information about divisions that have already been used for one or more elections, use one of these sources. In that situation, this tool is probably the least useful route to the information you want.

In the case where we need to talk about local electoral divisions which have been defined by an ECO but which have not yet been used in an election (i.e: the ECO has been made, but has not yet come into force), the only source for the division names is the ECO legislation itself.

This package provides some routines to help with parsing ward and division names from the [legislation.gov.uk](http://www.legislation.gov.uk/)'s [XML API](http://www.legislation.gov.uk/developer/contents) outputs (which are semi-structured). It is early days, so there are probably going to be some formats we don't support yet. If you find one in new or recent legislation, [raise an issue](https://github.com/DemocracyClub/eco-parser/issues).

### TL;DR

If you need the official names of electoral divisions that are already in use, get the data from [OS Boundary Line](https://www.ordnancesurvey.co.uk/business-and-government/products/boundary-line.html), [ONS Geography](http://geoportal.statistics.gov.uk/) or a web service like [mapit](https://mapit.mysociety.org/). This information is already published as convenient machine-readable structured data.

If you need the official names of electoral divisions that are not in use yet, this package can help you parse them from legislation.

## Installation

```bash
pip install eco-parser
```

## Usage

### On the console

```bash
eco_parser "http://www.legislation.gov.uk/uksi/2017/1067/schedule/1/made/data.xml" > out.csv
```

### As a library

```python
from eco_parser import EcoParser, ParseError

p = EcoParser("http://www.legislation.gov.uk/uksi/2017/1067/schedule/1/made/data.xml")

try:
    result = p.parse()
except ParseError:
    raise
```

## Licensing

The `eco-parser` software is made available under the MIT License.

Data Parsed from legislation.gov.uk is covered by the [Open Government Licence v3](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Your use of the data should comply with it.

## Development

Run the tests locally:

```bash
./run_tests.py
```
