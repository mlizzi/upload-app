import os
from typing import Tuple

import redis
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# REDIS_HOST env necessary when running app in docker.
# If running app + redis locally, default to localhost
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
database = redis.Redis(host=REDIS_HOST, decode_responses=True)


@app.route("/subscribe", methods=["POST"])
def subscribe() -> Tuple[Response, int]:
    """Save progress bar subscription to database."""
    user_id = request.form.to_dict()["user_id"]
    database.set(f"{user_id}:subscribed", 1)

    return jsonify({"text": "Subscribed!"}), 201


@app.route("/unsubscribe", methods=["POST"])
def unsubscribe() -> Tuple[Response, int]:
    """Save progress bar unsubscribe to database."""
    user_id = request.form.to_dict()["user_id"]
    database.set(f"{user_id}:subscribed", 0)

    return jsonify({"text": "Unsubscribed!"}), 201


@app.route("/subscribed", methods=["GET"])
def subscribed() -> Tuple[Response, int]:
    """Get subscription status of user."""
    key = f"{request.args.get('user_id')}:subscribed"
    val = database.get(key)

    # If no subscription status for a user, default to subscribed
    if val is None:
        val = "1"
        database.set(key, val)
    return jsonify({"data": val}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
