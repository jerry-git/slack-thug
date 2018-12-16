import os

from redis import Redis
from rq import Queue
from rq.decorators import job

from slack_thug.db import get_img_details, add_img_details
from slack_thug.slack import download_file, send_msg, send_file
from slack_thug.thugify import create_thug_meme, parse_msg

REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    redis = Redis.from_url(REDIS_URL)
else:
    redis = Redis()


queue = Queue(connection=redis)


@job(queue, result_ttl=0)
def event_handler(payload):
    e = payload.get("event", {})
    f = e.get("files", [None])[0]

    img_details = None
    thread_ts = e.get("thread_ts")

    if thread_ts:
        img_details = get_img_details(thread_ts)

    if e.get("subtype") == "file_share" and "image" in f.get("mimetype"):
        url = f["url_private_download"]
        if "thugged" in url:
            # This is uploaded by me
            return

        add_img_details(e["ts"], url, e["channel"])

    elif img_details:
        msg = e.get("text", "")
        if msg.lower().startswith("thug"):
            try:
                thug_msg = parse_msg(msg)
            except Exception:
                msg = "Sorry, can't parse the thug msg :hushed:"
                send_msg(msg, img_details.channel, thread_ts)
                raise
            try:
                orig_path = download_file(img_details.url)
            except Exception:
                msg = "Sorry, could not download the original img :pensive:"
                send_msg(msg, img_details.channel, thread_ts)
                raise
            try:
                res_path = create_thug_meme(orig_path, thug_msg)
            except Exception:
                msg = "Sorry, too hard to create thug meme for this one :disappointed:"
                send_msg(msg, img_details.channel, thread_ts)
                raise

            send_file(res_path, img_details.channel)
