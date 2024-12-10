"""Callable module and console script for gda_importer."""

import argparse

"""Console script for gda_importer."""
parser = argparse.ArgumentParser()
parser.add_argument("_", nargs="*")
args = parser.parse_args()

print(
    "Arguments: " + str(args._),
    "\n",
    "Replace this message by putting your code into",
    " 'gda_importer.__main__'",
)
