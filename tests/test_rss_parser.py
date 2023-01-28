import pytest
import app.parsers.rss as rss

EXAMPLE_FEED = "rss2sample.xml"


def test_parse_source():
    """check that sample feed has four entries and title 'Liftoff News'"""

    result = rss.parse_source(EXAMPLE_FEED)
    assert result.feed.title == "Liftoff News"
    assert len(result.entries) == 4
    assert result.feed.dl_feed_id == "Liftoff News"
