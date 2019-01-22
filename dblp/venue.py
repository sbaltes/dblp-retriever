import logging

# get root logger
import requests
from lxml import html

from dblp.paper import Paper

logger = logging.getLogger("dblp-retriever_logger")


class Venue(object):
    """ DBLP venue. """

    def __init__(self, name, year, identifier):
        self.name = str(name)
        self.year = str(year)
        self.identifier = str(identifier)
        self.uri = "https://dblp.org/db/" + self.identifier + ".html"

        self.papers = []

        # session for data retrieval
        self.session = requests.Session()

    def retrieve_papers(self):
        try:
            # retrieve data
            response = self.session.get(self.uri)

            if response.ok:
                logger.info("Successfully retrieved TOC of venue: " + self.identifier)

                tree = html.fromstring(response.content)
                items = tree.xpath('//header[not(@class)]/h2 | //header[not(@class)]/h3 | //ul[@class="publ-list"]/li')

                current_heading = ""
                year = ""

                for item in items:
                    if item.tag == "h2" or item.tag == "h3":
                        current_heading = item.text
                    elif item.tag == "li":
                        if current_heading == "":
                            # the following only works for conferences, not for journals
                            # year = item.xpath('div[@class="data"]/span[@itemprop="datePublished"]/text()')
                            # if len(year) > 0:
                            #     year = str(year[0])
                            # else:
                            #     year = ""
                            continue

                        title = item.xpath('div[@class="data"]/span[@itemprop="name"]/text()')
                        if len(title) > 0:
                            title = str(title[0])
                        else:
                            title = ""

                        pages = item.xpath('div[@class="data"]/span[@itemprop="pagination"]/text()')
                        if len(pages) > 0:
                            pages = str(pages[0])
                        else:
                            pages = ""

                        ee = item.xpath('nav[@class="publ"]/ul/li[@class="drop-down"]/div[@class="head"]/a/@href')
                        if len(ee) > 0:
                            ee = str(ee[0])
                        else:
                            ee = ""

                        authors = item.xpath('div[@class="data"]/span[@itemprop="author"]/a/span[@itemprop="name"]/text()')
                        if len(authors) == 1:
                            authors = str(authors[0])
                        else:
                            authors = "; ".join(authors)

                        self.papers.append(Paper(
                            self.name,
                            self.year,
                            self.identifier,
                            current_heading,
                            title,
                            authors,
                            pages,
                            ee
                        ))

                logger.info("Successfully parsed TOC of venue: " + self.identifier)
            else:
                logger.error("An error occurred while retrieving TOC of venue: " + self.identifier)

        except ConnectionError:
            logger.error("An error occurred while retrieving TOC of venue: " + self.identifier)

    def get_rows(self):
        rows = []
        for paper in self.papers:
            rows.append(paper.get_column_values())
        return rows
