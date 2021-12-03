import logging
import re

import requests

from lxml import html
from dblp.paper import Paper

logger = logging.getLogger("dblp-retriever_logger")


class Venue(object):
    """ A venue on DBLP. """

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
                logger.info("Successfully retrieved TOC of venue: " + str(self))

                tree = html.fromstring(response.content)
                items = tree.xpath('//header[not(@class)]/h2 | //header[not(@class)]/h3 | //ul[@class="publ-list"]/li')

                current_heading = ""

                for item in items:
                    if item.tag == "h2" or item.tag == "h3":
                        heading = item.xpath("descendant-or-self::*/text()")
                        if len(heading) > 0:
                            current_heading = re.sub(r'\s+', ' ',  # unify whitespaces/ remove newlines
                                                     str(" ".join(str(element).strip() for element in heading)))
                        else:
                            current_heading = ""
                    elif item.tag == "li":
                        if current_heading == "":
                            # the following only works for conferences, not for journals
                            # year = item.xpath('div[contains(@class, "data")]/span[@itemprop="datePublished"]/text()')
                            # if len(year) > 0:
                            #     year = str(year[0])
                            # else:
                            #     year = ""
                            continue

                        title = item.xpath('cite[contains(@class, "data")]/span[@itemprop="name"]'
                                           '/descendant-or-self::*/text()')
                        if len(title) > 0:
                            title = str(" ".join(str(element).strip() for element in title))
                        else:
                            title = ""

                        pages = item.xpath('cite[contains(@class, "data")]/span[@itemprop="pagination"]/text()')
                        if len(pages) > 0:
                            pages = str(pages[0])
                        else:
                            pages = ""

                        ee = item.xpath('nav[@class="publ"]/ul/li[@class="drop-down"]/div[@class="head"]/a/@href')
                        if len(ee) > 0:
                            # select DOI link if available, first link otherwise
                            doi_link = [link for link in ee if "doi.org" in link]
                            if len(doi_link) > 0:
                                ee = str(doi_link[0])
                            else:
                                ee = str(ee[0])

                        else:
                            ee = ""

                        authors = item.xpath('cite[contains(@class, "data")]/span[@itemprop="author"]/a'
                                             '/span[@itemprop="name"]/text()')
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

                logger.info("Successfully parsed TOC of venue: " + str(self))
            else:
                logger.error("An error occurred while retrieving TOC of venue: " + str(self))

        except ConnectionError:
            logger.error("An error occurred while retrieving TOC of venue: " + str(self))

    def validate_page_ranges(self):
        logger.info("Sorting papers of venue: " + str(self))

        self.papers.sort(key=lambda p: p.first_page)

        logger.info("Validating page ranges of venue: " + str(self))

        if len(self.papers) < 2:
            return

        previous_paper = self.papers[0]
        for i in range(1, len(self.papers)):
            current_paper = self.papers[i]

            if current_paper.page_range == "" or previous_paper.page_range == "":
                previous_paper = self.papers[i]
                continue

            if current_paper.regular_page_range and current_paper.first_page != previous_paper.last_page + 1:
                current_paper.append_comment("issue_first_page")
                previous_paper.append_comment("issue_last_page")
                logger.warning("First page of paper " + str(current_paper) + " does not match previous paper "
                               + str(previous_paper))

            elif current_paper.numbered_page_range and current_paper.article_number != previous_paper.article_number + 1:
                current_paper.append_comment("issue_article_number")
                previous_paper.append_comment("issue_article_number")
                logger.warning("Article number of paper " + str(current_paper) + " does not match previous paper "
                               + str(previous_paper))

            previous_paper = self.papers[i]

    def get_rows(self):
        rows = []
        for paper in self.papers:
            rows.append(paper.get_column_values())
        return rows

    def __str__(self):
        return str(self.identifier)
