from collections import namedtuple
from contextlib import closing
import os
import sqlite3

ImgDetails = namedtuple("ImgDetails", ["url", "channel"])


def _db_uri():
    return os.environ.get("THUG_SQLITE_URI", "thug_base.db")


def init_db():
    _maybe_create_img_details_table()


def _maybe_create_img_details_table():
    with sqlite3.connect(_db_uri()) as conn:
        with closing(conn.cursor()) as c:
            sql = "CREATE TABLE IF NOT EXISTS img_details (ts text, url text, channel text)"
            c.execute(sql)


def add_img_details(ts, url, channel):
    with sqlite3.connect(_db_uri()) as conn:
        with closing(conn.cursor()) as c:
            c.execute(
                "INSERT INTO img_details(ts, url, channel) VALUES (?,?,?)",
                (ts, url, channel),
            )


def get_img_details(ts):
    with sqlite3.connect(_db_uri()) as conn:
        with closing(conn.cursor()) as c:
            c.execute("SELECT * FROM img_details WHERE ts=?", (ts,))
            row = c.fetchone()
            if row:
                return ImgDetails(row[1], row[2])
            return None
