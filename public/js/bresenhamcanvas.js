"use strict";

class BresenhamCanvas {
  constructor(elem, width, height, pixel_size) {
    this.ctx = elem.getContext("2d");
    this.data = new Array(width * height).fill(false);

    this.elem = elem;
    this.pixel_size = pixel_size;
    this.start_coord = null;
    this.end_coord = null;
    this.width = width;
    this.height = height;

    elem.setAttribute("width", width * pixel_size);
    elem.setAttribute("height", height * pixel_size);

    this._boundDrawLineFromMouseEvent = this._drawLineFromMouseEvent.bind(this);
    this.elem.addEventListener("mousedown", (event) => {
      let x = parseInt(event.offsetX / pixel_size);
      let y = parseInt(event.offsetY / pixel_size);
      this.fillPixelFromCoordinates(x, y);
      this.start_coord = [x, y];
      this.elem.addEventListener("mousemove", this._boundDrawLineFromMouseEvent);
    });
    this.elem.addEventListener("mouseup", () => {
      this.elem.removeEventListener("mousemove", this._boundDrawLineFromMouseEvent);
      if (this.end_coord !== null) {
        this.fillPixelFromCoordinates(this.end_coord[0], this.end_coord[1]);
      }
    });
    this.elem.addEventListener("mouseout", () => {
      this.elem.removeEventListener("mousemove", this._boundDrawLineFromMouseEvent);
      if (this.end_coord !== null) {
        this.fillPixelFromCoordinates(this.end_coord[0], this.end_coord[1]);
      }
    });

    elem.addEventListener("touchstart", (event) => {
      let touch = event.touches[0];
      let x = parseInt((touch.pageX - touch.target.offsetLeft) / pixel_size);
      let y = parseInt((touch.pageY - touch.target.offsetTop) / pixel_size);
      this.fillPixelFromCoordinates(x, y);
      this.start_coord = [x, y];
      event.preventDefault();
    });
    elem.addEventListener("touchmove", this._drawLineFromTouchEvent.bind(this));
  }

  _drawLineFromTouchEvent(event) {
    let touch = event.touches[0];
    let x = parseInt((touch.pageX - touch.target.offsetLeft) / this.pixel_size);
    let y = parseInt((touch.pageY - touch.target.offsetTop) / this.pixel_size);

    this.end_coord = [x, y];
    this.bresenhamPlot(this.start_coord, this.end_coord);
    this.start_coord = this.end_coord;
    event.preventDefault();
  }

  _drawLineFromMouseEvent(event) {
    let x = parseInt(event.offsetX / this.pixel_size);
    let y = parseInt(event.offsetY / this.pixel_size);

    this.end_coord = [x, y];
    this.bresenhamPlot(this.start_coord, this.end_coord);
    this.start_coord = this.end_coord;
    event.preventDefault();
  }

  bresenhamPlot(start_coord, end_coord) {
    let x0 = 0;
    let y0 = 0;
    let x1 = Math.abs(end_coord[0] - start_coord[0]);
    let y1 = Math.abs(end_coord[1] - start_coord[1]);

    if (x1 - x0 > y1 - y0) {
      for (let x = 0, l = x1 - x0; x < l; x++) {
        let y = parseInt((y1 - y0) / (x1 - x0) * (x - x0) + y0);
        let plot_x = 0;
        let plot_y = 0;
        switch (this.determineOctant(start_coord, end_coord)) {
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
        this.fillPixelFromCoordinates(plot_x + start_coord[0], plot_y + start_coord[1])
      }
    }
    else {
      for (let y = 0, l = y1 - y0; y < l; y++) {
        let x = parseInt((y - y0) / (y1 - y0) * (x1 - x0) + x0);
        let plot_x = 0;
        let plot_y = 0;
        switch (this.determineOctant(start_coord, end_coord)) {
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
        this.fillPixelFromCoordinates(plot_x + start_coord[0], plot_y + start_coord[1])
      }
    }
  }

  fillPixelFromCoordinates(x_coord, y_coord) {
    this.data[this.width * y_coord + x_coord] = true;

    let x = x_coord * this.pixel_size;
    let y = y_coord * this.pixel_size;

    this.ctx.beginPath();
    this.ctx.rect(x, y, this.pixel_size, this.pixel_size);
    this.ctx.fillStyle = "black";
    this.ctx.fill();
  }

  determineOctant(start_coord, end_coord) {
    let x_range = end_coord[0] - start_coord[0];
    let y_range = end_coord[1] - start_coord[1];
    let x_dist = Math.abs(x_range);
    let y_dist = Math.abs(y_range);

    if (x_dist > y_dist) {
      if (y_range > 0 && x_range > 0 || y_range === 0 && x_range > 0) {
        return 0;
      } else if (y_range > 0 && x_range < 0 || y_range === 0 && x_range < 0) {
        return 3;
      } else if (y_range < 0 && x_range < 0) {
        return 4;
      } else {
        return 7;
      }
    }
    else {
      if (y_range > 0 && x_range > 0 || y_range > 0 && x_range === 0) {
        return 1;
      } else if (y_range > 0 && x_range < 0) {
        return 2;
      } else if (y_range < 0 && x_range < 0 || y_range < 0 && x_range === 0) {
        return 5;
      } else {
        return 6;
      }
    }
  }

  reset() {
    this.start_coord = null;
    this.end_coord = null;
    this.ctx.clearRect(0, 0, this.elem.width, this.elem.height);
    this.data = new Array(this.width * this.height).fill(false);
    this.elem.removeEventListener("mousemove", this._boundDrawLineFromMouseEvent);
  }
}

window.BresenhamCanvas = BresenhamCanvas;
