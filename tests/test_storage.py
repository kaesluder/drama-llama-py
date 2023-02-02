import app.storage

# from tinydb import TinyDB, Query
import app.parsers.rss as rss

EXAMPLE_FEED = "rss2sample.xml"

DB = "/tmp/test.db"


def test_db_connection():
    db = app.storage.Dl_db(TEST_DB)


def test_bulk_upsert():
    db = app.storage.Dl_db(TEST_DB)
    db.upsert_RSS(rss.parse_source(EXAMPLE_FEED))
    assert len(db.feeds) == 1
    assert len(db.entries) == 4


def test_get_entries_by_source():
    db = app.storage.Dl_db("/tmp/foo.json")
    db.upsert_RSS(rss.parse_source(EXAMPLE_FEED))
    results = db.get_entry_by_source(rss.encode_id(EXAMPLE_FEED))
    assert len(results) == 4
