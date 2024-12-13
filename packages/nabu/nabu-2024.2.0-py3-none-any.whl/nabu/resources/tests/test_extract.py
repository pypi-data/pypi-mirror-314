import pytest
from nabu.utils import list_match_queries


def test_list_match_queries():

    # entry0000 .... entry0099
    avail = ["entry%04d" % i for i in range(100)]
    query = "entry0000"
    list_match_queries()
