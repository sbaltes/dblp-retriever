import logging

from util.regex import REGULAR_PAGE_RANGE_REGEX, NUMBERED_PAGE_RANGE_REGEX

logger = logging.getLogger("dblp-retriever_logger")


class Paper(object):
    """ Paper metadata from DBLP. """

    def __init__(self, venue, year, identifier, heading, title, authors, page_range, electronic_edition):
        self.venue = venue
        self.year = year
        self.identifier = identifier
        self.heading = heading
        self.title = title
        self.authors = authors
        self.page_range = page_range
        self.article_number = -1
        self.first_page = -1
        self.last_page = -1
        self.length = -1
        self.electronic_edition = electronic_edition
        self.comment = ""
        self.regular_page_range = REGULAR_PAGE_RANGE_REGEX.fullmatch(page_range)
        self.numbered_page_range = NUMBERED_PAGE_RANGE_REGEX.fullmatch(page_range)

        # determine paper length
        if page_range == "":
            # empty page range
            self.first_page = -1
            self.last_page = -1
            self.length = 0
            self.append_comment("empty_page_range")
            logger.warning("Empty page range for paper " + str(self))
        elif self.regular_page_range:
            page_range = Paper.split_page_range(self.page_range)
            if len(page_range) == 1:
                # only one page, e.g. "5"
                self.first_page = int(page_range[0])
                self.last_page = int(page_range[0])
                self.length = 1
            elif len(page_range) == 2:
                # regular page range, e.g. "60-71"
                self.first_page = int(page_range[0])
                self.last_page = int(page_range[1])
                self.length = self.last_page - self.first_page + 1

        elif self.numbered_page_range:
            page_range = Paper.split_numbered_page_range(self.page_range)
            if len(page_range) == 2:
                # only one page, e.g. "27:1"
                self.article_number = int(page_range[0])
                self.first_page = int(page_range[1])
                self.last_page = int(page_range[1])
                self.length = 1
            elif len(page_range) == 4:
                # numbered article page range, e.g., "18:1-18:33"
                self.article_number = int(page_range[0])
                self.first_page = int(page_range[1])
                self.last_page = int(page_range[3])
                self.length = self.last_page - self.first_page + 1

    def append_comment(self, comment):
        if self.comment == "":
            self.comment = comment
        else:
            self.comment = self.comment + ";" + comment

    def __str__(self):
        return str(self.electronic_edition)

    def get_column_values(self):
        return [self.venue, self.year, self.identifier, self.heading, self.title, self.authors, self.page_range,
                self.length, self.electronic_edition, self.comment]

    @classmethod
    def get_column_names(cls):
        return ["venue", "year", "identifier", "heading", "title", "authors", "page_range", "length",
                "electronic_edition", "comment"]

    @classmethod
    def split_page_range(cls, page_range):
        return str(page_range).split("-")

    @classmethod
    def split_numbered_page_range(cls, numbered_page_range):
        page_range = Paper.split_page_range(numbered_page_range)
        fragments = []
        for page in page_range:
            fragments = fragments + str(page).split(":")
        return fragments
