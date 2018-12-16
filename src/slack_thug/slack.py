import os
import tempfile

import requests
from slackclient import SlackClient


def _token():
    return os.environ["SLACK_TOKEN"]


def download_file(url):
    r = requests.get(
        url, headers={"Authorization": "Bearer {}".format(_token())}, stream=True
    )
    r.raise_for_status()

    content_type = r.headers["content-type"]
    if "image" not in content_type:
        raise ValueError("Received unknown content type: {}".format(content_type))

    ext = ".{}".format(content_type.split("/")[1])
    _, path = tempfile.mkstemp(suffix=ext)

    with open(path, "wb") as f:
        f.write(r.content)

    return path


def send_file(file_path, channel):
    sc = SlackClient(_token())
    _, ext = os.path.splitext(file_path)
    file_name = "thugged{}".format(ext)

    with open(file_path, "rb") as f:
        sc.api_call("files.upload", channels=channel, file=f, filename=file_name)


def send_msg(msg, channel, thread_ts=None):
    sc = SlackClient(_token())
    kwargs = dict(channel=channel, text=msg)
    if thread_ts:
        kwargs["thread_ts"] = thread_ts
    sc.api_call("chat.postMessage", **kwargs)
