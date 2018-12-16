from unittest.mock import MagicMock
import tempfile
import os

import pytest

from slack_thug.db import init_db
from slack_thug.app import app


@pytest.fixture
def test_db(monkeypatch):
    _, db_uri = tempfile.mkstemp()
    monkeypatch.setenv("THUG_SQLITE_URI", db_uri)
    init_db()
    yield
    os.remove(db_uri)


@pytest.fixture
def slack_client(monkeypatch):
    monkeypatch.setenv("SLACK_TOKEN", "foo")
    c = MagicMock()
    monkeypatch.setattr("slack_thug.slack.SlackClient", c)
    return c()


@pytest.fixture
def client():
    c = app.test_client()
    yield c
