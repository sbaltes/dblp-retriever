import argparse
import logging

# get global logger
from dblp.venue import Venue
from dblp.venue_list import VenueList

logger = logging.getLogger('dblp-retriever_logger')


def get_argument_parser():
    arg_parser = argparse.ArgumentParser(
        description='Retrieve paper metadata from DBLP,'
    )
    arg_parser.add_argument(
        '-i', '--input-file',
        required=True,
        help='CSV file with venue identifiers.',
        dest='input_file'
    )
    arg_parser.add_argument(
        '-o', '--output-dir',
        required=True,
        help='Path to output directory',
        dest='output_dir'
    )
    arg_parser.add_argument(
        '-d', '--delimiter',
        required=False,
        default=',',
        help='delimiter for CSV files (default: \',\')',
        dest='delimiter'
    )
    return arg_parser


def main():
    # parse command line arguments
    parser = get_argument_parser()
    args = parser.parse_args()

    # read venue identifiers from CSV
    venue_list = VenueList()
    venue_list.read_from_csv(args.input_file, args.delimiter)

    # retrieve papers
    venue_list.retrieve_papers()

    # write entities to CSV file
    venue_list.write_to_csv(args.output_dir, args.delimiter)


if __name__ == '__main__':
    main()
