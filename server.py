from flask import Flask, url_for, redirect, request
from learning import learning_utils
import json

app = Flask(__name__, static_path="", static_folder='public')

@app.route("/collect")
def redirect_to_collect_page():
    return redirect(url_for("static", filename="collect.html"), code=302)

@app.route("/data", methods=["POST"])
def record_data():
    learning_utils.save_sample(request.data.decode("utf-8"))
    return "received"

@app.route("/test")
def redirect_to_test_page():
    return redirect(url_for("static", filename="test.html"), code=302)

if __name__ == "__main__":
    app.run("0.0.0.0")
