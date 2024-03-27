import os

import redis
from flask import Flask, request

app = Flask(__name__)

# REDIS_HOST used in docker-compose to reference docker redis instance.
# If running outside of docker, default to redis hosted at localhost.
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
database = redis.Redis(host=REDIS_HOST, decode_responses=True)


@app.route("/subscribe", methods=["POST"])
def subscribe() -> str:
    """Subscribe to getting progress bar updates on Slack."""
    user_id = request.form.to_dict()["user_id"]
    database.set(f"{user_id}:subscribed", 1)
    return "Subscribed to messages!"


@app.route("/unsubscribe", methods=["POST"])
def unsubscribe() -> str:
    """Unsubscribe to getting progress bar updates on Slack."""
    user_id = request.form.to_dict()["user_id"]
    database.set(f"{user_id}:subscribed", 0)
    return "Unsubscribed from messages!"


@app.route("/subscribed", methods=["GET"])
def subscribed() -> str:
    """Unsubscribe to getting progress bar updates on Slack."""
    key = f"{request.args.get('user_id')}:subscribed"

    if key not in database:
        database.set(key, 1)

    return database.get(key)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
