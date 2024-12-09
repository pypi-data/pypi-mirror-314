import os

import pytest
from lxml.html import fromstring

from pyawful.parse.forum_parser import parse_forum_page


@pytest.fixture()
def example_html():
    fixture_file = os.path.join(
        os.path.dirname(__file__),
        "fixtures/forumdisplay.html",
    )

    with open(fixture_file) as f:
        yield f.read()


def test_parse_gets_page_location(example_html: str):
    response = parse_forum_page(fromstring(example_html))

    assert response.current_page == 1
    assert response.last_page == 651


def test_parse_gets_forum_name(example_html: str):
    response = parse_forum_page(fromstring(example_html))

    assert response.forum.id == 273
    assert response.forum.name == "General Bullshit"
