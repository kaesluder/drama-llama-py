from tinydb import TinyDB, Query
from copy import deepcopy
import sqlite3
import json
from app.parsers.rss import parse_source


class Dl_db:
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row

        create_feeds_table = """create table if not exists feeds( 
            id text not null primary key,
            source text not null,
            title text not null,
            published_parsed integer,
            json_data text
            );
        """

        create_entries_table = """create table if not exists entries(
            id text not null primary key, 
            feed_id text references feeds(id) 
                ON DELETE CASCADE ON UPDATE NO ACTION,
            title text,
            dl_read BOOLEAN,
            summary text,
            published_parsed integer,
            json_data text
            );
            """
        cursor = self.connection.cursor()
        for statement in [create_feeds_table, create_entries_table]:
            cursor.execute(statement)

        self.connection.commit()

    def upsert_RSS(self, parsed_rss):

        cursor = self.connection.cursor()
        new_rss = deepcopy(parsed_rss)

        # separate feed and entries
        feed_info = new_rss.get("feed")
        entries = new_rss.get("entries")

        upsert_feed_sql = """insert or replace into feeds 
        (id, source, title, published_parsed, json_data)
        values(?,?,?,?,?);"""

        upsert_entry_sql = """insert or ignore into entries
        (id, feed_id, title, dl_read, summary, published_parsed, json_data)
        values(?,?,?,?,?,?,?);"""

        cursor.execute(
            upsert_feed_sql,
            [
                feed_info["dl_feed_id"],
                feed_info["source"],
                feed_info["title"],
                feed_info.get("published_parsed"),
                json.dumps(feed_info),
            ],
        )

        for entry in entries:
            cursor.execute(
                upsert_entry_sql,
                [
                    entry["id"],
                    entry["dl_feed_id"],
                    entry.get("title"),
                    entry.get("dl_read", 0),
                    entry.get("summary"),
                    entry.get("published_parsed"),
                    json.dumps(entry),
                ],
            )

        self.connection.commit()

    def feeds(self):
        cursor = self.connection.cursor()
        results = cursor.execute("select json_data from feeds;").fetchall()
        return [json.loads(row["json_data"]) for row in results]

    def get_entries_by_feed_id(self, source):
        cursor = self.connection.cursor()
        results = cursor.execute(
            "select json_data from entries where feed_id = ?", [source]
        )
        return [json.loads(row["json_data"]) for row in results]

        q = Query()
        return self.entries.search(q.dl_feed_id == source)

    def mark_feed_read(self, source):
        q = Query()
        return self.entries.update({"dl_read": True}, q.dl_feed_id == source)


if __name__ == "__main__":
    db = Dl_db("/tmp/Dl_db.json")
    cursor = db.connection.cursor()
    EXAMPLE_FEED = "rss2sample.xml"
    db.upsert_RSS(parse_source(EXAMPLE_FEED))
    result = cursor.execute("select * from feeds").fetchone()
    print(dict(result))
    result = cursor.execute("select * from entries").fetchall()
    print([row["id"] for row in result])
