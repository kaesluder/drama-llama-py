from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from .input_pipeline import pipeline, add_source
import traceback


from .storage import Dl_db

app = Flask(__name__)
CORS(app)

DB_PATH = "/tmp/test_db.db"


@app.route("/")
def hello():
    return "<h1>Hello, World!</h1>"


@app.route("/api/feeds", methods=["GET"])
def list_all_feeds():
    """Fetch a list of all feeds currently known by the backend.

    Returns:
    JSON: list of entry items in JSON format, or error message."""
    try:
        db = Dl_db(DB_PATH)
        feed_list = db.feeds()
        db.connection.close()
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
        db = Dl_db(DB_PATH)
        entry_list = db.get_entries_by_feed_id(feed_id)
        db.connection.close()
        return jsonify(entry_list)

    except:
        return make_response({"message": "Invalid data. Please snabble for card."}, 404)


@app.route("/api/<feed_id>/read", methods=["PATCH"])
def mark_feed_read(feed_id):
    try:
        db = Dl_db(DB_PATH)

        print(f"mark_feed_read: {feed_id}")
        db.mark_feed_read(feed_id)
        db.connection.commit()
        entry_list = db.get_entries_by_feed_id(feed_id)
        return jsonify(entry_list)
    except Exception as e:
        return make_response({"message": str(e)})


@app.route("/api/refresh", methods=["GET"])
def request_refresh():

    try:
        pipeline()
        return make_response({"message": "Database successfully refreshed."})

    except Exception as e:
        traceback.print_exc()
        return make_response(
            {"message": "Something went wrong.", "exception": str(e)}, 404
        )


@app.route("/api/feeds/add", methods=["POST"])
def add_new_feed():
    try:
        request_body = request.get_json()
        add_source(request_body["feed_source"])
        return list_all_feeds()

    except Exception as e:
        return make_response(
            {"message": "Something went wrong.", "exception": str(e)}, 404
        )
