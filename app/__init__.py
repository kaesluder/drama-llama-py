from flask import Flask, request, jsonify, make_response
from flask_cors import CORS


from .storage import Dl_db

app = Flask(__name__)
CORS(app)

db = Dl_db("/tmp/test_db.json")
feeds, entries, filters, preferences = db.create_tables()


@app.route("/")
def hello():
    return "<h1>Hello, World!</h1>"


@app.route("/api/feeds", methods=["GET"])
def list_all_feeds():
    try:
        feed_list = feeds.all()
        return jsonify(feed_list)

    except:
        return make_response(
            {"message": "Invalid data. Please check input for card."}, 404
        )


@app.route("/api/entries", methods=["GET"])
def list_all_entries_for_feed():
    try:
        # request_body = request.get_json()
        feed_id = request.args["feed_id"]

        test_source = "https%3A//rsshub.app/apnews/topics/apf-topnews"
        entry_list = db.get_entry_by_source(feed_id)
        # print(entry_list)
        return jsonify(entry_list)

    except:
        return make_response({"message": "Invalid data. Please snabble for card."}, 404)
