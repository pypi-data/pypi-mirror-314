import os

from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def _get_description():
    try:
        path = os.path.join(os.path.dirname(__file__), "README.md")
        with open(path, encoding="utf-8") as f:
            return f.read()
    except IOError:
        return ""


setup(
    name="eco_parser",
    version="0.3.0",
    author="chris48s",
    license="MIT",
    url="https://github.com/DemocracyClub/eco-parser/",
    packages=["eco_parser"],
    description="Parse ward lists from Electoral Change Orders on http://www.legislation.gov.uk/",
    long_description=_get_description(),
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["eco_parser = eco_parser.__main__:main"]},
    install_requires=["lxml", "requests"],
    extras_require={
        "testing": ["coveralls"],
        "development": ["ruff==0.3.7"],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
