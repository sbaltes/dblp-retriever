
class Paper(object):
    """ DBLP paper. """

    def __init__(self, venue, year, identifier, heading, title, authors, pages, electronic_edition):
        self.venue = venue
        self.year = year
        self.identifier = identifier
        self.heading = heading
        self.title = title
        self.authors = authors
        self.pages = pages
        self.length = 0
        self.electronic_edition = electronic_edition

        # determine paper length
        page_range = self.pages.split("-")
        if len(page_range) == 1:
            self.length = 1
        elif len(page_range) == 2:
            begin_page = page_range[0].split(":")
            end_page = page_range[1].split(":")

            if len(begin_page) == 1:
                self.length = int(end_page[0]) - int(begin_page[0]) + 1
            elif len(begin_page) == 2:
                self.length = int(end_page[1]) - int(begin_page[1]) + 1  # numbered articles, see, e.g., TOSEM

    @classmethod
    def get_column_names(cls):
        return ["venue", "year", "identifier", "heading", "title", "authors", "pages", "length", "electronic_edition"]

    def get_column_values(self):
        return [self.venue, self.year, self.identifier, self.heading, self.title, self.authors, self.pages, self.length, self.electronic_edition]