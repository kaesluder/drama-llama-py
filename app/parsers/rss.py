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
    # add feed_ids to channel
    feed_id = parsed["feed"].get("title") or parsed["feed"].get("link")
    parsed["feed"]["dl_feed_id"] = feed_id

    # add source to ['feed']
    parsed["feed"]["dl_sourced"] = source
    parsed["feed"]["dl_checked"] = datetime.now()

    # add feed_id and source to entries
    for entry in parsed.entries:
        entry["dl_feed_id"] = feed_id

        # add source to ['feed']
        entry["dl_sourced"] = source
        entry["dl_checked"] = datetime.now()

    return parsed


if __name__ == "__main__":
    pprint.pprint(parse_source("rss2sample.xml"))
