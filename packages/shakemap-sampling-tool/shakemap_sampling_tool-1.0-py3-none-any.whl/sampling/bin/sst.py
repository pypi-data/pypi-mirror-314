#!/usr/bin/env python

# stdlib imports
import argparse
import sys

# local imports
from sampling.parsers import (
    CustomFormatter,
    add_get_stations_parser,
    add_locations_parser,
    add_sample_parser,
)


def is_empty(args):
    attrlist = dir(args)
    non_standard = [not attr.startswith("_") for attr in attrlist]
    if any(non_standard):
        return False
    return True


def main():
    desc = """Sample ShakeMap data, online or on local ShakeMap installation.

This program offers a number of sub-commands, listed below. To see the help
for any of these commands, type:

%(prog)s [SUB-COMMAND] --help
"""
    parser = argparse.ArgumentParser(description=desc, formatter_class=CustomFormatter)

    subparsers = parser.add_subparsers(title="Sub-commands", help="sub-command help")

    add_get_stations_parser(subparsers)
    add_locations_parser(subparsers)
    add_sample_parser(subparsers)

    args = parser.parse_args()

    if is_empty(args):
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()
