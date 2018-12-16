from collections import namedtuple
import os
import re
import tempfile

from thug.cli import _load_configuration as load_thug_conf
from thug.detect.dlib import DlibDetector
from thug.meme.thug import ThugMeme

ParsedThugMsg = namedtuple("ParsedThugMsg", ["txt1", "txt2", "overrides"])


def create_thug_meme(path, thug_msg):
    conf = load_thug_conf(override=thug_msg.overrides, show_and_exit=False)

    _, ext = os.path.splitext(path)
    _, res_path = tempfile.mkstemp(suffix=ext)

    thugs = DlibDetector(conf["detect"]).find_thug_landmarks(path)
    if not thugs:
        raise ValueError("Detection failed captain")
    meme = ThugMeme(
        config=conf["meme"],
        thug_landmarks=thugs,
        img_path=path,
        txt1=thug_msg.txt1,
        txt2=thug_msg.txt2,
    )
    meme.create(res_path, show=False)

    return res_path


def parse_msg(msg):
    txt1 = txt2 = ""
    overrides = None

    msg = msg.strip()
    match = re.search("[Tt]hug (.*$)", msg)
    if match:
        msg = match.group(1).strip()
        match = re.search('["“](.*?)["”] ["“](.*?)["”](.*$)', msg)  # noqa
        if match:
            groups = match.groups()
            txt1, txt2 = groups[0], groups[1]
            overrides = groups[2].strip()
            if overrides.startswith("-o"):
                overrides = [o.strip() for o in overrides.split("-o") if o.strip()]
                overrides = [o.split() for o in overrides if len(o.split()) == 2]
        else:
            txt1 = msg

    return ParsedThugMsg(txt1, txt2, overrides)
