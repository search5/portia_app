from flask import render_template
from portia.factory import create_app
import os

app = create_app(os.getenv("PORTIA_CONFIG", "../config.json"))


@app.route("/", defaults={'path': ''})
@app.route('/<path:path>')
def main_page(path):
    return render_template("index.html")


@app.route("/short")
def short():
    return "short!"
