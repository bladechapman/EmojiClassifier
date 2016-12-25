"use strict";

document.addEventListener("DOMContentLoaded", () => {
  let canvas = new window.BresenhamCanvas(document.getElementById("input"), 50, 50, 5);
  let label = beginNewSampling(canvas);

  document.addEventListener("keyup", (event) => {
    if (event.keyCode === 13) {
      sendData();
    }
    else if (event.keyCode === 27) {
      canvas.reset();
    }
  });

  document.getElementById("send").addEventListener("click", sendData);
  document.getElementById("reset").addEventListener("click", () => {
    canvas.reset();
  });

  function sendData() {
    let param = JSON.stringify({
      "label": label,
      "data": canvas.data
    });

    let dataReq = new XMLHttpRequest();
    dataReq.open("POST", "/data");
    dataReq.setRequestHeader("Content-type", "application/json;charset=utf-8");
    dataReq.send(param);
    label = beginNewSampling(canvas);
  }

  function beginNewSampling(canvas) {
    let label = window.labels[parseInt(Math.random() * window.labels.length)];
    document.getElementById("target").innerHTML = label;
    canvas.reset();
    return label;
  }
});
