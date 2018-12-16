import json
from os import path as osp
from unittest.mock import patch, MagicMock

import pytest

from slack_thug.event import event_handler

from .payload import img_payload, thread_payload

IMG_PATH = osp.join(osp.dirname(__file__), "data", "img", "empty.png")


@pytest.fixture
def handle_events(monkeypatch):
    # Called as event_handler.delay so a little trick needed
    mock = MagicMock()
    monkeypatch.setattr("slack_thug.app.event_handler", mock)
    mock.delay = event_handler


@pytest.mark.usefixtures("test_db", "handle_events")
@patch("slack_thug.event.download_file")
@patch("slack_thug.event.create_thug_meme")
class TestUseCases:
    def test_uploading_image_and_thugging_it_after(
        self, create_thug, download_file, client, slack_client
    ):
        create_thug.return_value = IMG_PATH

        client.post(
            "/event", data=json.dumps(img_payload), content_type="application/json"
        )

        client.post(
            "/event", data=json.dumps(thread_payload), content_type="application/json"
        )

        download_file.assert_called_once_with("foo/img.jpg")
        args, kwargs = slack_client.api_call.call_args
        assert args[0] == "files.upload"
        assert kwargs["file"].name == IMG_PATH
