""" Collection of regular expressions. """

import re

# regular expressions for page ranges
REGULAR_PAGE_RANGE_REGEX = re.compile(r'\d+(-\d+)?')
NUMBERED_PAGE_RANGE_REGEX = re.compile(r'\d+:\d+(-\d+:\d+)?')
