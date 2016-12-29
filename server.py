from flask import Flask, url_for, redirect, request
from learning import learning_utils, naive_bayes
import json

app = Flask(__name__, static_path="", static_folder='public')
data = learning_utils.read_samples()
training_data = naive_bayes.train(data)

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

@app.route("/evaluate", methods=["POST"])
def evaluate_sample():
    global training_data
    req_data = json.loads(request.data.decode("utf-8"))
    sample = req_data["data"]
    return naive_bayes.test(sample, training_data)

if __name__ == "__main__":
    app.run("0.0.0.0")
