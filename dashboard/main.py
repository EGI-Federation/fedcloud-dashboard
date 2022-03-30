import os
import sys

from flask import Flask, render_template

script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, script_dir)
from update_endpoints import read_endpoints

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("dashboard.html", endpoints=read_endpoints())


if __name__ == "__main__":
    ain()
