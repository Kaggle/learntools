function renderer({
  parent,
  step,
  frame,
  environment,
  width = 400,
  height = 400,
}) {
  console.log(step, frame);
  // Canvas Setup.
  let canvas = parent.querySelector("canvas");
  if (!canvas) {
    canvas = document.createElement("canvas");
    parent.appendChild(canvas);

    canvas.addEventListener("click", () => {
      console.log("canvas click");
    });
  }

  // Common Dimensions.
  const canvasSize = Math.min(height, width);
  const unit = 8;
  const offset = canvasSize > 400 ? canvasSize * 0.1 : unit / 2;
  const cellSize = (canvasSize - offset * 2) / 3;

  // Canvas setup and reset.
  const c = canvas.getContext("2d");
  canvas.width = canvasSize;
  canvas.height = canvasSize;
  c.clearRect(0, 0, canvas.width, canvas.height);

  const drawStyle = ({
    lineWidth = 1,
    lineCap,
    strokeStyle = "#FFF",
    shadow,
  }) => {
    c.lineWidth = lineWidth;
    c.strokeStyle = strokeStyle;
    if (lineCap) c.lineCap = lineCap;
    if (shadow) {
      c.shadowOffsetX = shadow.offsetX || 0;
      c.shadowOffsetY = shadow.offsetY || 0;
      c.shadowColor = shadow.color || strokeStyle;
      c.shadowBlur = shadow.blur || 0;
    }
  };

  const drawLine = ({ x1, y1, x2, y2, style }) => {
    c.beginPath();
    drawStyle(style || {});
    c.moveTo((x1 || 0) + offset, (y1 || 0) + offset);
    c.lineTo((x2 || x1) + offset, (y2 || y1) + offset);
    c.stroke();
  };

  const drawArc = ({ x, y, radius, sAngle, eAngle, style }) => {
    drawStyle(style || {});
    c.beginPath();
    c.arc(x, y, radius, sAngle, eAngle);
    c.stroke();
  };

  // Draw the Grid.
  const gridFrame = step === 0 ? frame : 1;
  const drawGridLine = ({
    x1s = 0,
    y1s = 0,
    x2s,
    y2s,
    x1o = 0,
    x2o = 0,
    y1o = 0,
    y2o = 0,
  }) =>
    drawLine({
      x1: x1s * cellSize + x1o * unit,
      x2: (x2s || x1s) * cellSize + x2o * unit,
      y1: y1s * cellSize + y1o * unit,
      y2: (y2s || y1s) * cellSize + y2o * unit,
      style: { strokeStyle: "#046BBF" },
    });

  // Vertical.
  drawGridLine({ x1s: 1, y1s: 0, y2s: gridFrame, y2o: -1 });
  drawGridLine({ x1s: 2, y1s: 0, y2s: gridFrame, y2o: -1 });
  drawGridLine({ x1s: 1, y1s: 1, y2s: 1 + gridFrame, y1o: 1, y2o: -1 });
  drawGridLine({ x1s: 2, y1s: 1, y2s: 1 + gridFrame, y1o: 1, y2o: -1 });
  drawGridLine({ x1s: 1, y1s: 2, y2s: 2 + gridFrame, y1o: 1 });
  drawGridLine({ x1s: 2, y1s: 2, y2s: 2 + gridFrame, y1o: 1 });

  // Horizontal.
  drawGridLine({ x1s: 0, y1s: 1, x2s: gridFrame, x2o: -1 });
  drawGridLine({ x1s: 1, y1s: 1, x2s: 1 + gridFrame, x1o: 1, x2o: -1 });
  drawGridLine({ x1s: 2, y1s: 1, x2s: 2 + gridFrame, x1o: 1 });
  drawGridLine({ x1s: 0, y1s: 2, x2s: gridFrame, x2o: -1 });
  drawGridLine({ x1s: 1, y1s: 2, x2s: 1 + gridFrame, x1o: 1, x2o: -1 });
  drawGridLine({ x1s: 2, y1s: 2, x2s: 2 + gridFrame, x1o: 1 });

  // Draw the Pieces.
  const drawX = (cell, cellFrame) => {
    const part = cellSize / 4;
    const gap = Math.min(Math.sqrt((unit * unit) / 2), canvasSize / 50);
    const row = Math.floor(cell / 3);
    const col = cell % 3;

    const drawXLine = ({ x1, y1, x2, y2 }) =>
      drawLine({
        x1: col * cellSize + x1,
        y1: row * cellSize + y1,
        x2: col * cellSize + x2,
        y2: row * cellSize + y2,
        style: {
          strokeStyle: "#00FFFF",
          lineWidth: 2,
          lineCap: "round",
          shadow: { blur: 8 },
        },
      });

    drawXLine({
      x1: part,
      y1: part,
      x2: part + part * 2 * cellFrame,
      y2: part + part * 2 * cellFrame,
    });
    if (Math.round(cellFrame) === 1) {
      drawXLine({
        x1: part,
        y1: part * 3,
        x2: part * 2 - gap,
        y2: part * 2 + gap,
      });
      drawXLine({
        x1: part * 2 + gap,
        y1: part * 2 - gap,
        x2: part * 3,
        y2: part,
      });
    }
  };
  const drawO = (cell, cellFrame) => {
    const row = Math.floor(cell / 3);
    const col = cell % 3;
    const radius = cellSize / 4 + 1; // +1 is for optical illusion.
    const gap =
      (Math.acos((2 * (radius ^ 2) - (unit ^ 2)) / (2 * radius * radius)) /
        180) *
      Math.PI *
      unit;
    const x = cellSize * col + cellSize / 2 + offset;
    const y = cellSize * row + cellSize / 2 + offset;

    const drawOArc = (sAngle, eAngle) =>
      drawArc({
        x,
        y,
        radius,
        sAngle,
        eAngle,
        style: {
          lineWidth: 2,
          strokeStyle: "#FFF",
          shadow: { blur: 8 },
        },
      });

    drawOArc(
      -Math.PI / 2 + gap,
      -Math.PI / 2 + gap + (Math.PI - gap * 2) * cellFrame
    );
    drawOArc(
      Math.PI / 2 + gap,
      Math.PI / 2 + gap + (Math.PI - gap * 2) * cellFrame
    );
  };

  const board = environment.steps[step][0].observation.board;

  board.forEach((value, cell) => {
    const cellFrame =
      step <= 1 ||
      environment.steps[step - 1][0].observation.board[cell] !== value
        ? frame
        : 1;
    if (value === 1) drawX(cell, cellFrame);
    if (value === 2) drawO(cell, cellFrame);
  });

  // Draw the winning line.
  // [cell1, cell2, cell3, x1, y1, x2, y2]
  const checks = [
    [0, 1, 2, 1 / 19, 1 / 6, 18 / 19, 1 / 6],
    [3, 4, 5, 1 / 19, 1 / 2, 18 / 19, 1 / 2],
    [6, 7, 8, 1 / 19, 5 / 6, 18 / 19, 5 / 6],
    [0, 3, 6, 1 / 6, 1 / 19, 1 / 6, 18 / 19],
    [1, 4, 7, 1 / 2, 1 / 19, 1 / 2, 18 / 19],
    [2, 5, 8, 5 / 6, 1 / 19, 5 / 6, 18 / 19],
    [0, 4, 8, 1 / 19, 1 / 19, 18 / 19, 18 / 19],
    [2, 4, 6, 18 / 19, 1 / 19, 1 / 19, 18 / 19],
  ];
  for (const check of checks) {
    if (
      board[check[0]] !== 0 &&
      board[check[0]] === board[check[1]] &&
      board[check[0]] === board[check[2]]
    ) {
      const x1 = check[3] * (cellSize * 3);
      const y1 = check[4] * (cellSize * 3);
      const winFrame = frame < 0.5 ? 0 : (frame - 0.5) / 0.5;
      if (winFrame > 0) {
        drawLine({
          x1,
          y1,
          x2: x1 + (check[5] * (cellSize * 3) - x1) * winFrame,
          y2: y1 + (check[6] * (cellSize * 3) - y1) * winFrame,
          style: {
            strokeStyle: "#FFF",
            lineWidth: 3 * winFrame,
            shadow: { blur: 8 * winFrame },
          },
        });
      }
      break;
    }
  }
}
