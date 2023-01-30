import pytest
import app.parsers.rss as rss


EXAMPLE_FEED = "rss2sample.xml"


def test_parse_source():
    """check that sample feed has four entries and title 'Liftoff News'"""

    result = rss.parse_source(EXAMPLE_FEED)
    assert result.feed.title == "Liftoff News"
    assert len(result.entries) == 4
    assert result.feed.dl_feed_id == rss.encode_id("rss2sample.xml")
    assert result.entries[0].get("dl_feed_id") == rss.encode_id("rss2sample.xml")


def test_bad_feed_raises_exception():
    """Raise exception if bad data passed to parser."""

    with pytest.raises(Exception) as e:
        result = rss.parse_source("bad dog, no biscuit")
