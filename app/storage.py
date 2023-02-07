from copy import deepcopy
import sqlite3
import json
from app.parsers.rss import parse_source


class Dl_db:
    """Interface object representing a database opened at `path`.

    Will create tables when object is created if none currently exist."""

    def __init__(self, path):
        """Args:
            path (str): string identifying path to sqlite3 database

        Returns:
            (Dl_db): Class database instance."""
        self.path = path
        self.connection = sqlite3.connect(path)
        # return dicts mapping column name to column value
        self.connection.row_factory = sqlite3.Row

        # this seems to be incompatible with INSERT OR IGNORE
        # self.connection.execute("PRAGMA foreign_keys = ON;")

        # setting this explicitly is recommended by sqlite docs
        self.connection.execute("PRAGMA foreign_keys = OFF;")

        create_feeds_table = """
        create table if not exists feeds( 
            id text not null primary key,
            source text not null,
            title text not null,
            published_parsed integer,
            json_data text
            );
        """

        create_entries_table = """create table if not exists entries(
            id text not null primary key, 
            feed_id text references feeds(id),
            title text,
            dl_read BOOLEAN,
            summary text,
            published_parsed integer,
            json_data text, 
            CONSTRAINT fk_feeds
            FOREIGN KEY (feed_id)
            REFERENCES feeds(id)
            ON DELETE CASCADE
            );
            """
        cursor = self.connection.cursor()
        for statement in [create_feeds_table, create_entries_table]:
            cursor.execute(statement)

        self.connection.commit()

    def upsert_RSS(self, parsed_rss):
        """Updated database with information from a parsed RSS object.
        Changes to the feed metadata will be upserted.
        Entries with a duplicate id in the database will be ignored.

        Args:
            parsed_rss (dict): parsed RSS objects including a `feed` and `entries` dicts.
        """

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

        cursor.connection.commit()

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
        """Generate a list of all feeds in the database.

        Returns:
            [dict]: list of dict objects containing feed data
        """

        cursor = self.connection.cursor()
        results = cursor.execute("select json_data from feeds;").fetchall()
        return [json.loads(row["json_data"]) for row in results]

    def get_entries_by_feed_id(self, feed_id):
        """Generate a list of entries posted to feed with feed_id.

        Args:
            feed_id (str): string feed identifier

        Returns:
            [dict]: list of dict objects containing entry data
        """
        cursor = self.connection.cursor()
        results = cursor.execute(
            "select json_data from entries where feed_id = ?", [feed_id]
        )
        return [json.loads(row["json_data"]) for row in results]

    def mark_feed_read(self, feed_id):
        """Mark all items in a feed as read by feed_id

        Args:
            feed_id (string): feed id
        """
        cursor = self.connection.cursor()

        update_sql = """update entries
        set json_data = json_set(json_data, '$.dl_read', True), 
        dl_read = 1
        where feed_id = (?)"""

        cursor.execute(update_sql, [feed_id])
        self.connection.commit()
        cursor.close()

    def pre_delete_feed(self, feed_id):
        """Returns the number of entries that
        will be deleted if the feed is deleted.

        Args:
            feed_id (str): unique feed identifier

        Returns:
            (int): number of entry records that will be affected.
        """
        cursor = self.connection.cursor()

        pre_delete_sql = """select count(*) 
        from entries 
        where feed_id = (?)"""

        results = cursor.execute(pre_delete_sql, [feed_id]).fetchone()
        cursor.close()
        return results["count(*)"]

    def delete_feed(self, feed_id):
        """Delete a feed along with attached entry records.

        Args:
            feed_id (str): String feed id.
        """
        cursor = self.connection.cursor()

        delete_sql = """delete 
        from feeds 
        where id = (?);"""

        # setting foreign_keys = OFF requires clearing
        # feeds and entries separately.
        delete_entries_sql = """delete
        from entries
        where feed_id = (?);"""

        results = cursor.execute(delete_sql, [feed_id]).fetchone()
        results2 = cursor.execute(delete_entries_sql, [feed_id]).fetchone()
        self.connection.commit()
        cursor.close()
        return results


if __name__ == "__main__":
    db = Dl_db("/tmp/Dl_db.json")
    cursor = db.connection.cursor()
    EXAMPLE_FEED = "rss2sample.xml"
    db.upsert_RSS(parse_source(EXAMPLE_FEED))
    result = cursor.execute("select * from feeds").fetchone()
    print(dict(result))
    result = cursor.execute("select * from entries").fetchall()
    print([row["id"] for row in result])
