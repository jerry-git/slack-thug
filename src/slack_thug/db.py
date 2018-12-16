from collections import namedtuple
import os
import sqlite3

ImgDetails = namedtuple("ImgDetails", ["url", "channel"])


def _db_uri():
    return os.environ.get("THUG_SQLITE_URI", "thug_base.db")


def init_db():
    _maybe_create_img_details_table()


def _maybe_create_img_details_table():
    conn = sqlite3.connect(_db_uri())
    c = conn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS img_details (ts text, url text, channel text)"
    c.execute(sql)
    conn.commit()
    c.close()


def add_img_details(ts, url, channel):
    conn = sqlite3.connect(_db_uri())
    c = conn.cursor()
    c.execute(
        "INSERT INTO img_details(ts, url, channel) VALUES (?,?,?)", (ts, url, channel)
    )
    conn.commit()
    conn.close()


def get_img_details(ts):
    conn = sqlite3.connect(_db_uri())
    c = conn.cursor()
    c.execute("SELECT * FROM img_details WHERE ts=?", (ts,))
    row = c.fetchone()
    conn.close()
    if row:
        return ImgDetails(row[1], row[2])
    return None
