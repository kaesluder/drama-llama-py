from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from .input_pipeline import pipeline, add_source
import traceback
import json
import os


from .storage import Dl_db

app = Flask(__name__)
CORS(app)

DB_PATH = os.getenv("HOME") + "/test_db.db"


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


@app.route("/api/feeds/<feed_id>/predelete", methods=["GET"])
def pre_delete_warning(feed_id):
    """Returns the number of items that will be deleted along with a feed.

    Args:
        feed_id (str): text id of feed to delete

    Returns:
        JSON: json object with "feed_id" and "item_count" fields.
    """
    try:
        db = Dl_db(DB_PATH)
        result = db.pre_delete_feed(feed_id)
        return make_response({"feed_id": feed_id, "item_count": result})
    except Exception as e:
        traceback.print_exc()
        return make_response(
            {"message": "Something went wrong.", "exception": str(e)}, 404
        )


@app.route("/api/feeds/<feed_id>/delete", methods=["DELETE"])
def delete_feed(feed_id):
    """Delete a feed and associated items from the database.

    Args:
        feed_id (str): text id of feed to delete

    Returns:
        JSON: json object with updated feed list.
    """
    try:
        db = Dl_db(DB_PATH)
        db.delete_feed(feed_id)
        feed_list = db.feeds()
        return make_response(feed_list)
    except Exception as e:
        traceback.print_exc()
        return make_response(
            {"message": "Something went wrong.", "exception": str(e)}, 404
        )


@app.route("/api/filters/add", methods=["POST"])
def add_filter():
    try:
        db = Dl_db(DB_PATH)
        request_body = request.get_json()
        db.add_filter(request_body)
        filters = db.load_filters()
        return make_response([f.export_config() for f in filters.values()], 201)

    except Exception as e:
        return make_response(
            {"message": "Something went wrong.", "exception": str(e)}, 404
        )


@app.route("/api/filters", methods=["GET"])
def get_filters():
    try:
        db = Dl_db(DB_PATH)
        filters = db.load_filters()
        return make_response([f.export_config() for f in filters.values()], 200)

    except Exception as e:
        return make_response(
            {"message": "Something went wrong.", "exception": str(e)}, 404
        )


@app.route("/api/filters/<filter_id>/delete", methods=["DELETE"])
def delete_filter(filter_id):
    try:
        db = Dl_db(DB_PATH)
        db.delete_filter(filter_id)
        filters = db.load_filters()
        return make_response([f.export_config() for f in filters.values()], 200)

    except Exception as e:
        return make_response(
            {"message": "Something went wrong.", "exception": str(e)}, 404
        )
