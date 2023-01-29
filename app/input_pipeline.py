from filters import BaseFilter
from storage import Dl_db
from parsers import rss

filter_map = {"BaseFilter": BaseFilter.BaseFilter}

test_filter = BaseFilter.BaseFilter("hello", "yes")


filter_list = [test_filter]

db = Dl_db("/tmp/test_db.json")
feeds, entries, filters, preferences = db.create_tables()

sources = [
    "https://rsshub.app/apnews/topics/apf-topnews",
    "https://www.them.us/feed/rss",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCoxcjq-8xIDTYp3uz647V5A",
    "https://killsixbilliondemons.com/feed/",
]


def pipeline():
    for source in sources:
        data = rss.parse_source(source)
        for filter in filter_list:
            data = filter.analyze(data)
        db.upsert_RSS(data)


if __name__ == "__main__":
    # pipeline()
    print(len(entries))
    print(
        len(
            db.get_entry_by_source(
                "https://www.youtube.com/feeds/videos.xml?channel_id=UCoxcjq-8xIDTYp3uz647V5A"
            )
        )
    )
    print(len(feeds))
