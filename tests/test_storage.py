import app.storage
import app.parsers.rss as rss
import json
import pprint

EXAMPLE_FEED = "rss2sample.xml"

TEST_DB = ":memory:"


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
