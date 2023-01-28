import feedparser
import pprint
from datetime import datetime


def parse_source(source):
    """parse_source returns a feedparser dict of information from
    source. Source can be filename, feed url, or raw string.

    Args:
        source (string): string filename, url, or raw RSS/Atom

    Returns:
        _type_: feedparser dict
    """
    parsed = feedparser.parse(source)

    if parsed.get("bozo", True):
        raise ValueError("invalid feed read")

    # add feed_ids to channel
    feed_id = source
    parsed["feed"]["dl_feed_id"] = feed_id

    parsed["feed"]["dl_checked"] = datetime.now()

    # add feed_id and source to entries
    for entry in parsed.entries:
        entry["dl_feed_id"] = feed_id

        entry["dl_checked"] = datetime.now()

    return parsed


if __name__ == "__main__":
    pprint.pprint(parse_source("rss2sample.xml").get("status"))
    pprint.pprint(parse_source("http://www.example.com/").get("status"))
