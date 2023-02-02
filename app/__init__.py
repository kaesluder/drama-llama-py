from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from .input_pipeline import pipeline


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
    """Fetch a list of all feeds currently known by the backend.

    Returns:
    JSON: list of entry items in JSON format, or error message."""
    try:
        feed_list = feeds.all()
        return jsonify(feed_list)

    except:
        return make_response(
            {"message": "Invalid data. Please check input for card."}, 404
        )


@app.route("/api/<feed_id>/entries", methods=["GET"])
def list_all_entries_for_feed(feed_id):
    """Fetch all the downloaded entries for a single feed.

    Args:
        feed_id (str): Feed ID extracted from URL.

    Returns:
        JSON: list of entry items in JSON format, or error message.
    """
    try:
        entry_list = db.get_entry_by_source(feed_id)
        # print(entry_list)
        return jsonify(entry_list)

    except:
        return make_response({"message": "Invalid data. Please snabble for card."}, 404)


@app.route("/api/<feed_id>/read", methods=["PATCH"])
def mark_feed_read(feed_id):
    try:
        print("mark_feed_read")
        result = db.mark_feed_read(feed_id)
        return make_response({"message": f"Messages for {feed_id} marked read"}, 200)
    except Exception as e:
        return make_response({"message": str(e)})


@app.route("/api/refresh", methods=["GET"])
def request_refresh():

    try:
        pipeline()
        return make_response({"message": "Databse successfully refreshed."})

    except Exception as e:
        return make_response(
            {"message": "Something went wrong.", "exception": str(e)}, 404
        )
