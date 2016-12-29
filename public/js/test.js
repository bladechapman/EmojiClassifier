"use strict";

document.addEventListener("DOMContentLoaded", () => {
  let canvas = new window.BresenhamCanvas(document.getElementById("input"), 50, 50, 5);

  for (var i in window.labels) {
    document.getElementById("title").innerHTML += " " + window.labels[i];
  }

  document.getElementById("reset").addEventListener("click", () => {
    canvas.reset();
    document.getElementById("guess").innerHTML = "";
  });

  document.getElementById("send").addEventListener("click", sendData);

  function sendData() {
    let param = JSON.stringify({
      "data": canvas.data
    });
    let evaluateReq = new XMLHttpRequest();
    evaluateReq.open("POST", "/evaluate");
    evaluateReq.setRequestHeader("Content-type", "application/json;charset=utf-8");
    evaluateReq.send(param);
    evaluateReq.responseType = "text"

    evaluateReq.onreadystatechange = () => {
      if (evaluateReq.readyState === XMLHttpRequest.DONE) {
        document.getElementById("guess").innerHTML = "";
        document.getElementById("guess").innerHTML = "Hmm... is it " + evaluateReq.response + " ?";
      }
    };
  }
});
