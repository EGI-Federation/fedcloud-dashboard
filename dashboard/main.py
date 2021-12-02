from flask import Flask, render_template
from update_endpoints import read_endpoints

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("dashboard.html", endpoints=read_endpoints())


if __name__ == "__main__":
    main()
