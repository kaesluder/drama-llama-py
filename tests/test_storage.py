import app.storage
import app.parsers.rss as rss
import json
import pprint
import re
from app.filters.BaseFilter import BaseFilter
from app.filters.RegexFilter import RegexFilter


EXAMPLE_FEED = "rss2sample.xml"

TEST_DB = ":memory:"

example_item = rss.parse_source(EXAMPLE_FEED)["entries"][0]
base_test_filter = app.filters.BaseFilter.BaseFilter("hello world", "Yes!!")
regex_test_filter = app.filters.RegexFilter.RegexFilter(
    "hello regex",
    "regexMatch",
    "regexMatch",
    "a test of regex filter",
    None,
    "regex",
    test_extra="foo",
)


def test_db_connection():
    db = app.storage.Dl_db(TEST_DB)
    cursor = db.connection.cursor()
    result = cursor.execute("select 1;").fetchone()
    assert result[0] == 1


def test_bulk_upsert():
    db = app.storage.Dl_db(TEST_DB)
    db.upsert_RSS(rss.parse_source(EXAMPLE_FEED))
    cursor = db.connection.cursor()
    feeds = cursor.execute("select * from feeds").fetchall()
    entries = cursor.execute("select * from entries").fetchall()
    assert len(feeds) == 1
    assert len(entries) == 4


def test_feeds():
    db = app.storage.Dl_db(TEST_DB)
    db.upsert_RSS(rss.parse_source(EXAMPLE_FEED))
    feeds = db.feeds()
    assert feeds[0]["title"] == "Liftoff News"


def test_get_entries_by_feed_id():
    db = app.storage.Dl_db(TEST_DB)
    db.upsert_RSS(rss.parse_source(EXAMPLE_FEED))
    results = db.get_entries_by_feed_id(rss.encode_id(EXAMPLE_FEED))
    assert len(results) == 4


def test_mark_read():
    db = app.storage.Dl_db(TEST_DB)
    db.upsert_RSS(rss.parse_source(EXAMPLE_FEED))
    db.mark_feed_read(rss.encode_id(EXAMPLE_FEED))
    results = db.get_entries_by_feed_id(rss.encode_id(EXAMPLE_FEED))
    assert results[0]["dl_read"] == 1


def test_pre_delete():
    db = app.storage.Dl_db(TEST_DB)
    db.upsert_RSS(rss.parse_source(EXAMPLE_FEED))
    results = db.pre_delete_feed(rss.encode_id(EXAMPLE_FEED))
    assert results == 4


def test_pre_delete_returns_zero_for_bad_feedid():
    db = app.storage.Dl_db(TEST_DB)
    db.upsert_RSS(rss.parse_source(EXAMPLE_FEED))

    results = db.pre_delete_feed("foo")
    assert results == 0


def test_delete_feed():
    db = app.storage.Dl_db(TEST_DB)
    parsed = rss.parse_source(EXAMPLE_FEED)
    feed_id = parsed["feed"]["dl_feed_id"]
    db.upsert_RSS(parsed)
    db.delete_feed(feed_id)
    results = db.get_entries_by_feed_id(feed_id)
    assert len(results) == 0
    assert len(db.feeds()) == 0


def test_add_filter():
    db = app.storage.Dl_db(TEST_DB)
    db.upsert_filter(base_test_filter)
    db.upsert_filter(regex_test_filter)
    cursor = db.connection.cursor()
    filters = cursor.execute("select * from filters").fetchall()
    assert len(filters) == 2

    # check for expected fields
    assert "id" in dict(filters[0])
    assert "json_data" in dict(filters[0])


def test_load_filters():
    db = app.storage.Dl_db(TEST_DB)
    db.upsert_filter(base_test_filter)
    db.upsert_filter(regex_test_filter)
    filter_objs = db.load_filters()
    assert len(filter_objs) == 2
    assert "hello world" in filter_objs
    assert "hello regex" in filter_objs

    # check for correct type field
    assert filter_objs["hello world"].type == "BaseFilter"
    assert filter_objs["hello regex"].type == "RegexFilter"

    # check for correct python type
    assert isinstance(filter_objs["hello world"], BaseFilter)
    # check that the BaseFilter instance isn't a subclass
    assert not isinstance(filter_objs["hello world"], RegexFilter)

    # check for correct type on a RegexFilter
    assert isinstance(filter_objs["hello regex"], RegexFilter)


def test_delete_filter():
    db = app.storage.Dl_db(TEST_DB)
    db.upsert_filter(base_test_filter)
    db.upsert_filter(regex_test_filter)

    db.delete_filter("hello world")
    filter_objs = db.load_filters()

    assert len(filter_objs) == 1
    assert "hello world" not in filter_objs
    assert "hello regex" in filter_objs
