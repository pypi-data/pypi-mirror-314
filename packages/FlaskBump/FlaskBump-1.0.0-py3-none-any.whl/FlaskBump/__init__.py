"""Flask Bump"""

__version__ = "1.0.0"

import os
import json
from pathlib import Path

from .flocked import open_lockfile, flocked

from flask import Flask

app = Flask(__name__)

# keeping a separate lock file prevents headaches
# from locking real files of interest
LOCK_FILEPATH = Path(os.environ.get(
    "FLASKBUMP_LOCK_FILEPATH",
    ".lock"
))

# open lockfile for duration of app process
LOCKFILE = open_lockfile(LOCK_FILEPATH)

STATE_FILEPATH = Path(os.environ.get(
    "FLASKBUMP_STATE_FILEPATH",
    "state.json"
))

def read_state():
    return json.loads(STATE_FILEPATH.read_text())

def write_state(j):
    STATE_FILEPATH.write_text(json.dumps(j) + "\n")

@app.route("/")
def index():
    with flocked(LOCKFILE):
        j = read_state()
        count = j["count"]
        j["count"] += 1
        write_state(j)
    return f"{count}\n"
