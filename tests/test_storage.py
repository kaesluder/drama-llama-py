import app.storage
from tinydb import TinyDB, Query
import app.parsers.rss as rss

EXAMPLE_FEED = "rss2sample.xml"


def test_db_upsert():
    db = app.storage.Dl_db("/tmp/foo.json")
    (feeds, entries, filters, preferences) = db.create_tables()
    q = Query()


def test_bulk_upsert():
    db = app.storage.Dl_db("/tmp/foo.json")
    (feeds, entries, filters, preferences) = db.create_tables()
    db.upsert_RSS(rss.parse_source(EXAMPLE_FEED))
    assert len(db.feeds) == 1
    assert len(db.entries) == 4


def test_get_entries_by_source():
    db = app.storage.Dl_db("/tmp/foo.json")
    db.create_tables()
    db.upsert_RSS(rss.parse_source(EXAMPLE_FEED))
    results = db.get_entry_by_source(EXAMPLE_FEED)
    assert len(results) == 4
