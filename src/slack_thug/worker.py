import os

from rq import Connection, Worker
from redis import Redis
from slack_thug.db import init_db

if __name__ == "__main__":
    init_db()
    REDIS_URL = os.environ.get("REDIS_URL")
    if REDIS_URL:
        redis = Redis.from_url(REDIS_URL)
    else:
        redis = Redis()

    with Connection(redis):
        worker = Worker(["default"])
        worker.work()
