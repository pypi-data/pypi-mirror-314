# stdlib imports
import argparse
import textwrap

# local imports
from sampling.handlers import (
    get_locations_handler,
    get_sample_handler,
    get_stations_handler,
)


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def add_get_stations_parser(subparsers):
    desc = """Return a list of stations contained in the processed files."""
    # create the parser for the "stop_event" command
    parser = subparsers.add_parser(
        "get-stations",
        description=desc,
        formatter_class=CustomFormatter,
        help=(("Get list of stations " "included in ShakeMap")),
    )
    parser.add_argument("eventid", help="ComCat event ID.")
    parser.add_argument(
        "-l",
        "--local",
        action="store_true",
        default=False,
        help=("Search for ShakeMap information " "on local system."),
    )
    parser.add_argument(
        "-o", "--outfile", help="Output station information to Excel/CSV file."
    )
    parser.add_argument(
        "-m",
        "--max-horizontal",
        action="store_true",
        default=False,
        help="Only return rows with maximum horizontal value.",
    )
    parser.set_defaults(func=get_stations_handler)


def add_locations_parser(subparsers):
    # create the parser locations
    desc = (
        "Extract all array values for a LOCAL sampled (i.e., "
        "not grid-based) ShakeMap HDF file."
    )
    parser = subparsers.add_parser(
        "locations",
        description=desc,
        formatter_class=CustomFormatter,
        help=("Extract table of IMT values at all locations."),
    )
    parser.add_argument("eventid", help="ComCat event ID.")
    parser.add_argument(
        "-o", "--outfile", help="Output station information to Excel/CSV file."
    )
    parser.set_defaults(func=get_locations_handler)


def add_sample_parser(subparsers):
    desc = """Sample local data sets using one of a number of methods.
        Mutually exclusive sampling options include:
          - By a single set of coordinates: (-c, --coordinates)
          - By supplying station IDs found in ShakeMap: (-s, --stations)
          - Sample locations of every station found in ShakeMap: (-a, --all-stations)
          - By supplying an input file with IDs and coordinates: (-f, --file)"""

    # create the parser for the "stop_event" command
    parser = subparsers.add_parser(
        "sample",
        description=desc,
        formatter_class=CustomFormatter,
        help=("Sample online ShakeMap."),
    )
    parser.add_argument("eventid", help="ComCat event ID.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-c",
        "--coordinates",
        nargs=3,
        metavar=("ID", "LAT", "LON"),
        help=("Use an ID string and single set of coordinates " "to sample ShakeMap."),
    )
    group.add_argument(
        "-s",
        "--stations",
        nargs="+",
        help=(
            "Use station codes (NET.STA format) "
            "(found in ShakeMap) to sample ShakeMap."
        ),
    )
    group.add_argument(
        "-a",
        "--all-stations",
        action="store_true",
        default=False,
        help=("Output values at nearest point " "of all stations found in ShakeMap."),
    )
    fhelp = textwrap.fill(
        (
            "Use CSV/Excel file to sample ShakeMap. "
            "File must at least contain columns that "
            'start with "lat" or "lon" (case does not '
            "matter. Optionally, it may contain "
            'a column called "id" (again, case insensitive) '
            "which will be used to identify each point. In the "
            "absence of this column, each point will "
            "be assigned an oridinal ID number "
            '"Point1", "Point2", and so on.'
        )
    )

    group.add_argument("-f", "--file", help=fhelp)

    parser.add_argument(
        "-o", "--outfile", help="Output station information to Excel/CSV file."
    )
    parser.add_argument(
        "-l",
        "--local",
        action="store_true",
        default=False,
        help=(
            "Sample local HDF file (found by looking in "
            "configured ShakeMap data directory)."
        ),
    )

    parser.set_defaults(func=get_sample_handler)
