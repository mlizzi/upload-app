import os

import redis
from flask import Flask, request

app = Flask(__name__)

# Use env variable to find redis host, default to localhost
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
database = redis.Redis(
    host=REDIS_HOST, password=REDIS_PASSWORD, decode_responses=True
)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
