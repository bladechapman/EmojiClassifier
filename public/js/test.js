"use strict";

document.addEventListener("DOMContentLoaded", () => {
  let canvas = new window.BresenhamCanvas(document.getElementById("input"), 50, 50, 5);

  document.getElementById("reset").addEventListener("click", () => {
    canvas.reset();
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
    evaluateReq.responseType = "json"

    evaluateReq.onreadystatechange = () => {
      if (evaluateReq.readyState === XMLHttpRequest.DONE) {
        document.getElementById("guess").innerHTML = "";
        for (var key in evaluateReq.response) {
          document.getElementById("guess").innerHTML += key + " " + (evaluateReq.response[key] * 100).toFixed(2) + "%<br>"
        }
      }
    };
  }

});
