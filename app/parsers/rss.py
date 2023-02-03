import feedparser
import pprint
from datetime import datetime
from time import mktime, gmtime
import re


def encode_id(id_string):
    return re.sub(r"\W", "", id_string)


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

    parsed["feed"]["source"] = source

    # add feed_ids to channel
    feed_id = encode_id(source)
    parsed["feed"]["dl_feed_id"] = feed_id

    parsed["feed"]["dl_checked"] = mktime(gmtime())

    # convert dates
    if "published_parsed" in parsed["feed"]:
        parsed["feed"]["published_parsed"] = mktime(parsed["feed"]["published_parsed"])

    if "updated_parsed" in parsed["feed"]:
        parsed["feed"]["updated_parsed"] = mktime(parsed["feed"]["updated_parsed"])

    # add feed_id and source to entries
    for entry in parsed.entries:
        entry["dl_feed_id"] = feed_id

        entry["dl_checked"] = mktime(gmtime())
        entry["dl_read"] = False
        entry["dl_keep"] = False
        # convert dates
        if "published_parsed" in entry:
            entry["published_parsed"] = mktime(entry["published_parsed"])

        if "updated_parsed" in entry:
            entry["updated_parsed"] = mktime(entry["updated_parsed"])

    return parsed


if __name__ == "__main__":
    pprint.pprint(parse_source("rss2sample.xml").get("entries"))
