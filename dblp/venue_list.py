import codecs
import csv
import logging
import os

from dblp.paper import Paper
from dblp.venue import Venue
from util.exceptions import IllegalArgumentError

logger = logging.getLogger("dblp-retriever_logger")


class VenueList(object):
    """ List of DBLP venues. """

    def __init__(self):
        self.filename = ""
        self.venues = []

    def read_from_csv(self, input_file, delimiter):
        """
        Read venues from a CSV file (header required).
        :param input_file: Path to the CSV file.
        :param delimiter: Column delimiter in CSV file (typically ',').
        """

        # read CSV as UTF-8 encoded file (see also http://stackoverflow.com/a/844443)
        with codecs.open(input_file, encoding='utf8') as fp:
            logger.info("Reading venues from " + input_file + "...")

            reader = csv.reader(fp, delimiter=delimiter)

            # read header
            header = next(reader, None)
            if not header:
                raise IllegalArgumentError("Missing header in CSV file.")

            venue_index = header.index("venue")
            year_index = header.index("year")
            identifier_index = header.index("identifier")

            # read CSV file
            for row in reader:
                if row:
                    self.venues.append(
                        Venue(row[venue_index], row[year_index], row[identifier_index])
                    )
                else:
                    raise IllegalArgumentError("Wrong CSV format.")

        self.filename = os.path.basename(input_file)
        logger.info(str(len(self.venues)) + " venues have been imported.")

    def retrieve_papers(self):
        for venue in self.venues:
            venue.retrieve_papers()

    def validate_page_ranges(self):
        for venue in self.venues:
            venue.validate_page_ranges()

    def write_to_csv(self, output_dir, delimiter):
        """
        Export papers retrieved from venues to a CSV file.
        :param output_dir: Target directory for generated CSV file.
        :param delimiter: Column delimiter in CSV file (typically ',').
        """

        if len(self.venues) == 0:
            logger.info("Nothing to export.")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(output_dir, self.filename)

        # write paper list to UTF8-encoded CSV file (see also http://stackoverflow.com/a/844443)
        with codecs.open(file_path, 'w', encoding='utf8') as fp:
            logger.info('Exporting papers to ' + file_path + '...')
            writer = csv.writer(fp, delimiter=delimiter)

            column_names = Paper.get_column_names()

            # write header of CSV file
            writer.writerow(column_names)

            count = 0
            for venue in self.venues:
                try:
                    for row in venue.get_rows():
                        if len(row) == len(column_names):
                            writer.writerow(row)
                            count = count + 1
                        else:
                            raise IllegalArgumentError(
                                str(len(column_names) - len(row)) + " parameter(s) is/are missing for venue "
                                + venue.identifier)

                except UnicodeEncodeError:
                    logger.error("Encoding error while writing data for venue: " + venue.identifier)

            logger.info(str(count) + ' papers have been exported.')
