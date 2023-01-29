from tinydb import TinyDB, Query
from copy import deepcopy


class Dl_db:
    def __init__(self, path):
        self.db = TinyDB(path)

    def create_tables(self):
        self.feeds = self.db.table("Feeds")
        self.entries = self.db.table("Entries")
        self.filters = self.db.table("Filters")
        self.preferences = self.db.table("Preferences")
        return (self.feeds, self.entries, self.filters, self.preferences)

    def upsert_RSS(self, parsed_rss):

        q = Query()
        new_rss = deepcopy(parsed_rss)

        # separate feed and entries
        feed_info = new_rss.get("feed")
        entries = new_rss.get("entries")

        self.feeds.upsert(feed_info, q.dl_feed_id == feed_info.dl_feed_id)

        for entry in entries:
            self.entries.upsert(entry, q.id == entry.id)

    def get_entry_by_source(self, source):
        q = Query()
        return self.entries.search(q.dl_feed_id == source)


if __name__ == "__main__":
    db = Dl_db("/tmp/Dl_db.json")
    feeds, entries, filters, preferences = db.create_tables()
    q = Query()
    feeds.upsert({"name": "john", "logged-in": True}, q.name == "john")
