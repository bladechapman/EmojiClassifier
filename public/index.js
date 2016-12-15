"use strict";

document.addEventListener("DOMContentLoaded", () => {
  initializeCanvas(document.getElementById("input"), 50, 50);
});

const pixel_width = 5;
const pixel_height = 5;
function initializeCanvas(canvas, width, height) {
  let ctx = canvas.getContext("2d");
  let data = new Array(pixel_width * pixel_height).fill(false);

  canvas.setAttribute("width", width * pixel_width);
  canvas.setAttribute("height", height * pixel_height);

  let end_coord = null;
  let start_coord = null;

  canvas.addEventListener("mousedown", (event) => {
    let x = parseInt(event.offsetX / pixel_width);
    let y = parseInt(event.offsetY / pixel_height);
    fillPixelFromCoordinates(ctx, x, y);
    start_coord = [x, y];
    end_coord = [x, y];

    canvas.addEventListener("mousemove", drawLineFromMouseEvent);
  });
  canvas.addEventListener("mouseup", (event) => {
    canvas.removeEventListener("mousemove", drawLineFromMouseEvent);
    fillPixelFromCoordinates(ctx, end_coord[0], end_coord[1]);
  });
  canvas.addEventListener("mouseout", (event) => {
    canvas.removeEventListener("mousemove", drawLineFromMouseEvent);
    fillPixelFromCoordinates(ctx, end_coord[0], end_coord[1]);
  });

  canvas.addEventListener("touchstart", (event) => {
    let touch = event.touches[0];
    let x = parseInt((touch.pageX - touch.target.offsetLeft) / pixel_width);
    let y = parseInt((touch.pageY - touch.target.offsetTop) / pixel_height);
    fillPixelFromCoordinates(ctx, x, y);
    start_coord = [x, y];
    event.preventDefault();
  });
  canvas.addEventListener("touchmove", drawLineFromTouchEvent);

  function drawLineFromTouchEvent(event) {
    let touch = event.touches[0];
    let x = parseInt((touch.pageX - touch.target.offsetLeft) / pixel_width);
    let y = parseInt((touch.pageY - touch.target.offsetTop) / pixel_height);

    end_coord = [x, y];
    bresenhamPlot(ctx, start_coord, end_coord);
    start_coord = end_coord;
    event.preventDefault();
  }

  function drawLineFromMouseEvent(event) {
    let x = parseInt(event.offsetX / pixel_width);
    let y = parseInt(event.offsetY / pixel_height);

    end_coord = [x, y];
    bresenhamPlot(ctx, start_coord, end_coord);
    start_coord = end_coord;
    event.preventDefault();
  }
}


function bresenhamPlot(ctx, start_coord, end_coord) {
  let x0 = 0;
  let y0 = 0;
  let x1 = Math.abs(end_coord[0] - start_coord[0]);
  let y1 = Math.abs(end_coord[1] - start_coord[1]);

  if (x1 - x0 > y1 - y0) {
    for (let x = 0, l = x1 - x0; x < l; x++) {
      let y = parseInt((y1 - y0) / (x1 - x0) * (x - x0) + y0);
      let plot_x = 0;
      let plot_y = 0;
      switch (determineOctant(start_coord, end_coord)) {
        case 0:
          plot_x = x;
          plot_y = y;
          break;
        case 3:
          plot_x = -x;
          plot_y = y;
          break;
        case 4:
          plot_x = -x;
          plot_y = -y;
          break;
        case 7:
          plot_x = x;
          plot_y = -y;
          break;
      }
      fillPixelFromCoordinates(ctx, plot_x + start_coord[0], plot_y + start_coord[1])
    }
  } else {
    for (let y = 0, l = y1 - y0; y < l; y++) {
      let x = parseInt((y - y0) / (y1 - y0) * (x1 - x0) + x0);

      let plot_x = 0;
      let plot_y = 0;
      switch (determineOctant(start_coord, end_coord)) {
        case 1:
          plot_x = x;
          plot_y = y;
          break;
        case 2:
          plot_x = -x;
          plot_y = y;
          break;
        case 5:
          plot_x = -x;
          plot_y = -y;
          break;
        case 6:
          plot_x = x;
          plot_y = -y;
          break;
      }
      fillPixelFromCoordinates(ctx, plot_x + start_coord[0], plot_y + start_coord[1])
    }
  }
}

function determineOctant(start_coord, end_coord) {
  let x_range = end_coord[0] - start_coord[0];
  let y_range = end_coord[1] - start_coord[1];
  let x_dist = Math.abs(x_range);
  let y_dist = Math.abs(y_range);

  if (x_dist > y_dist) {
    if (y_range > 0 && x_range > 0 || y_range == 0 && x_range > 0) {
      return 0;
    } else if (y_range > 0 && x_range < 0 || y_range == 0 && x_range < 0) {
      return 3;
    } else if (y_range < 0 && x_range < 0) {
      return 4;
    } else {
      return 7;
    }
  } else {
    if (y_range > 0 && x_range > 0 || y_range > 0 && x_range == 0) {
      return 1;
    } else if (y_range > 0 && x_range < 0) {
      return 2;
    } else if (y_range < 0 && x_range < 0 || y_range < 0 && x_range == 0) {
      return 5;
    } else {
      return 6;
    }
  }
}

function fillPixelFromCoordinates(ctx, x_coord, y_coord) {
  let x = x_coord * pixel_width;
  let y = y_coord * pixel_height;

  ctx.beginPath();
  ctx.rect(x, y, pixel_width, pixel_height);
  ctx.fillStyle = "black";
  ctx.fill();
}
