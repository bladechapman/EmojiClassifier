from flask import Flask, url_for, redirect, request
from learning import learning_utils, naive_bayes, sample
import json

app = Flask(__name__, static_path="", static_folder='public')
samples = learning_utils.read_samples()
nb_model = naive_bayes.NaiveBayes()
nb_model.train(samples)

@app.route("/collect")
def redirect_to_collect_page():
    return redirect(url_for("static", filename="collect.html"), code=302)

@app.route("/data", methods=["POST"])
def record_data():
    s = sample.Sample(json_str=request.data.decode("utf-8"))
    s.normalize()
    s.save()
    return "received"

@app.route("/test")
def redirect_to_test_page():
    return redirect(url_for("static", filename="test.html"), code=302)

@app.route("/evaluate", methods=["POST"])
def evaluate_sample():
    req_data = json.loads(request.data.decode("utf-8"))
    s = sample.Sample(data=req_data["data"], label="_")
    s.normalize()
    return nb_model.test(s.data)

if __name__ == "__main__":
    app.run("0.0.0.0")
