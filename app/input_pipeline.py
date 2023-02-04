from .filters import BaseFilter
from .storage import Dl_db
from .parsers import rss


filter_map = {"BaseFilter": BaseFilter.BaseFilter}

test_filter = BaseFilter.BaseFilter("hello", "yes")


filter_list = [test_filter]


sources = [
    "https://rsshub.app/apnews/topics/apf-topnews",
    "https://www.them.us/feed/rss",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCoxcjq-8xIDTYp3uz647V5A",
    "https://killsixbilliondemons.com/feed/",
]

DB_PATH = "/tmp/test_db.db"


def pipeline():
    db = Dl_db(DB_PATH)
    for source in sources:
        data = rss.parse_source(source)
        for filter in filter_list:
            for item in data["entries"]:
                item = filter.analyze(item)
        db.upsert_RSS(data)
    db.connection.close()


def add_source(source):
    db = Dl_db(DB_PATH)

    data = rss.parse_source(source)
    for filter in filter_list:
        for item in data["entries"]:
            item = filter.analyze(item)
    db.upsert_RSS(data)
    return True


if __name__ == "__main__":
    pipeline()
