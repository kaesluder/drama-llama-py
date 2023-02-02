import app.storage
import app.parsers.rss as rss
import json

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
