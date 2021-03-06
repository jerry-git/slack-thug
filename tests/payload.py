img_payload = {
    "api_app_id": "foo",
    "authed_users": ["foo"],
    "event": {
        "channel": "channel1",
        "channel_type": "channel",
        "display_as_bot": False,
        "event_ts": "1000.00",
        "files": [
            {
                "created": 100,
                "display_as_bot": False,
                "editable": False,
                "external_type": "",
                "filetype": "jpg",
                "id": "foo",
                "image_exif_rotation": 1,
                "is_external": False,
                "is_public": True,
                "mimetype": "image/jpeg",
                "mode": "hosted",
                "name": "foo.jpg",
                "original_h": 400,
                "original_w": 600,
                "permalink": "foo",
                "permalink_public": "foo",
                "pretty_type": "JPEG",
                "public_url_shared": False,
                "size": 79411,
                "thumb_160": "foo",
                "thumb_360": "foo",
                "thumb_360_h": 240,
                "thumb_360_w": 360,
                "thumb_480": "foo",
                "thumb_480_h": 320,
                "thumb_480_w": 480,
                "thumb_64": "foo",
                "thumb_80": "foo",
                "timestamp": 100,
                "title": "foo",
                "url_private": "foo",
                "url_private_download": "foo/img.jpg",
                "user": "foo",
                "username": "foo",
            }
        ],
        "subtype": "file_share",
        "text": "foo",
        "ts": "10000.0",
        "type": "message",
        "upload": True,
        "user": "foo",
    },
    "event_id": "foo",
    "event_time": 1544304512,
    "team_id": "foo",
    "token": "foo",
    "type": "event_callback",
}


thread_payload = {
    "api_app_id": "foo",
    "authed_users": ["foo"],
    "event": {
        "channel": "channel1",
        "channel_type": "channel",
        "client_msg_id": "foo",
        "event_ts": "10001.0",
        "parent_user_id": "foo",
        "text": "thug",
        "thread_ts": "10000.0",  # this has to match with ts of img
        "ts": "10001.0",
        "type": "message",
        "user": "foo",
    },
    "event_id": "foo",
    "event_time": 100,
    "team_id": "foo",
    "token": "foo",
    "type": "event_callback",
}
