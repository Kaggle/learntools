function renderer({
  parent,
  step,
  frame,
  environment,
  width = 400,
  height = 400,
}) {
  // Canvas Setup.
  let canvas = parent.querySelector("canvas");
  if (!canvas) {
    canvas = document.createElement("canvas");
    parent.appendChild(canvas);

    canvas.addEventListener("click", () => {
      console.log("canvas click");
    });
  }

  // Configuration.
  const { rows, columns, inarow } = environment.configuration;

  // Common Dimensions.
  const unit = 8;
  const minCanvasSize = Math.min(height, width);
  const minOffset = minCanvasSize > 400 ? 30 : unit / 2;
  const cellSize = Math.min(
    (width - minOffset * 2) / columns,
    (height - minOffset * 2) / rows
  );
  const cellInset = 0.8;
  const pieceScale = cellSize / 100;
  const xOffset = Math.max(0, (width - cellSize * columns) / 2);
  const yOffset = Math.max(0, (height - cellSize * rows) / 2);

  // Character Paths (based on 100x100 tiles).
  const kPath = new Path2D(
    `M78.3,96.5c-0.1,0.4-0.5,0.6-1.1,0.6H64.9c-0.7,0-1.4-0.3-1.9-1l-20.3-26L37,75.5v20.1 c0,0.9-0.5,1.4-1.4,1.4H26c-0.9,0-1.4-0.5-1.4-1.4V3.9c0-0.9,0.5-1.4,1.4-1.4h9.5C36.5,2.5,37,3,37,3.9v56.5l24.3-24.7 c0.6-0.6,1.3-1,1.9-1H76c0.6,0,0.9,0.2,1.1,0.7c0.2,0.6,0.1,1-0.1,1.2l-25.7,25L78,95.1C78.4,95.5,78.5,95.9,78.3,96.5z`
  );
  const goose1Path = new Path2D(
    `M8.8,92.7c-4-18.5,4.7-37.2,20.7-46.2c0,0,2.7-1.4,3.4-1.9c2.2-1.6,3-2.1,3-5c0-5-2.1-7.2-2.1-7.2 c-3.9-3.3-6.3-8.2-6.3-13.7c0-10,8.1-18.1,18.1-18.1s18.1,8.1,18.1,18.1c0,6-1.5,32.7-2.3,38.8l-0.1,1`
  );
  const goose2Path = new Path2D(
    `M27.4,19L8.2,27.6c0,0-7.3,2.9,2.6,5c6.1,1.3,24,5.9,24,5.9l1,0.3`
  );
  const goose3Path = new Path2D(
    `M63.7,99.6C52.3,99.6,43,90.3,43,78.9s9.3-20.7,20.7-20.7c10.6,0,34.4,0.1,35.8,9`
  );

  // Canvas setup and reset.
  const c = canvas.getContext("2d");
  canvas.width = width;
  canvas.height = height;
  c.fillStyle = "#000B2A";
  c.fillRect(0, 0, canvas.width, canvas.height);

  const getRowCol = cell => [Math.floor(cell / columns), cell % columns];

  const getColor = (mark, opacity = 1) => {
    if (mark === 1) return `rgba(0,255,255,${opacity})`;
    if (mark === 2) return `rgba(255,255,255,${opacity})`;
    return "#fff";
  };

  const drawCellCircle = (cell, xFrame = 1, yFrame = 1, radiusOffset = 0) => {
    const [row, col] = getRowCol(cell);
    c.arc(
      xOffset + xFrame * (col * cellSize + cellSize / 2),
      yOffset + yFrame * (row * cellSize + cellSize / 2),
      (cellInset * cellSize) / 2 - radiusOffset,
      2 * Math.PI,
      false
    );
  };

  // Render the pieces.
  const board = environment.steps[step][0].observation.board;

  const drawPiece = mark => {
    // Base Styles.
    const opacity = minCanvasSize < 300 ? 0.6 - minCanvasSize / 1000 : 0.1;
    c.fillStyle = getColor(mark, opacity);
    c.strokeStyle = getColor(mark);
    c.shadowColor = getColor(mark);
    c.shadowBlur = 8 / cellInset;
    c.lineWidth = 1 / cellInset;

    // Outer circle.
    c.save();
    c.beginPath();
    c.arc(50, 50, 50, 2 * Math.PI, false);
    c.closePath();
    c.lineWidth *= 4;
    c.stroke();
    c.fill();
    c.restore();

    // Inner circle.
    c.beginPath();
    c.arc(50, 50, 40, 2 * Math.PI, false);
    c.closePath();
    c.stroke();

    // Kaggle "K".
    if (mark === 1) {
      const scale = 0.54;
      c.save();
      c.translate(23, 23);
      c.scale(scale, scale);
      c.lineWidth /= scale;
      c.shadowBlur /= scale;
      c.stroke(kPath);
      c.restore();
    }

    // Kaggle "Goose".
    if (mark === 2) {
      const scale = 0.6;
      c.save();
      c.translate(24, 28);
      c.scale(scale, scale);
      c.lineWidth /= scale;
      c.shadowBlur /= scale;
      c.stroke(goose1Path);
      c.stroke(goose2Path);
      c.stroke(goose3Path);
      c.beginPath();
      c.arc(38.5, 18.6, 2.7, 0, Math.PI * 2, false);
      c.closePath();
      c.fill();
      c.restore();
    }
  };

  for (let i = 0; i < board.length; i++) {
    const [row, col] = getRowCol(i);
    if (board[i] === 0) continue;
    // Easing In.
    let yFrame = Math.min(
      (columns * Math.pow(frame, 3)) / Math.floor(i / columns),
      1
    );

    if (
      step > 1 &&
      environment.steps[step - 1][0].observation.board[i] === board[i]
    ) {
      yFrame = 1;
    }

    c.save();
    c.translate(
      xOffset + cellSize * col + (cellSize - cellSize * cellInset) / 2,
      yOffset +
        yFrame * (cellSize * row) +
        (cellSize - cellSize * cellInset) / 2
    );
    c.scale(pieceScale * cellInset, pieceScale * cellInset);
    drawPiece(board[i]);
    c.restore();
  }

  // Background Gradient.
  const bgRadius = (Math.min(rows, columns) * cellSize) / 2;
  const bgStyle = c.createRadialGradient(
    xOffset + (cellSize * columns) / 2,
    yOffset + (cellSize * rows) / 2,
    0,
    xOffset + (cellSize * columns) / 2,
    yOffset + (cellSize * rows) / 2,
    bgRadius
  );
  bgStyle.addColorStop(0, "#000B49");
  bgStyle.addColorStop(1, "#000B2A");

  // Render the board overlay.
  c.beginPath();
  c.rect(0, 0, canvas.width, canvas.height);
  c.closePath();
  c.shadowBlur = 0;
  for (let i = 0; i < board.length; i++) {
    drawCellCircle(i);
    c.closePath();
  }
  c.fillStyle = bgStyle;
  c.fill("evenodd");

  // Render the board overlay cell outlines.
  for (let i = 0; i < board.length; i++) {
    c.beginPath();
    drawCellCircle(i);
    c.strokeStyle = "#0361B2";
    c.lineWidth = 1;
    c.stroke();
    c.closePath();
  }

  const drawLine = (fromCell, toCell) => {
    if (frame < 0.5) return;
    const lineFrame = (frame - 0.5) / 0.5;
    const x1 = xOffset + (fromCell % columns) * cellSize + cellSize / 2;
    const x2 =
      x1 +
      lineFrame *
        (xOffset + ((toCell % columns) * cellSize + cellSize / 2) - x1);
    const y1 =
      yOffset + Math.floor(fromCell / columns) * cellSize + cellSize / 2;
    const y2 =
      y1 +
      lineFrame *
        (yOffset + Math.floor(toCell / columns) * cellSize + cellSize / 2 - y1);
    c.beginPath();
    c.lineCap = "round";
    c.lineWidth = 4;
    c.strokeStyle = getColor(board[fromCell]);
    c.shadowBlur = 8;
    c.shadowColor = getColor(board[fromCell]);
    c.moveTo(x1, y1);
    c.lineTo(x2, y2);
    c.stroke();
  };

  // Generate a graph of the board.
  const getCell = (cell, rowOffset, columnOffset) => {
    const row = Math.floor(cell / columns) + rowOffset;
    const col = (cell % columns) + columnOffset;
    if (row < 0 || row >= rows || col < 0 || col >= columns) return -1;
    return col + row * columns;
  };
  const makeNode = cell => {
    const node = { cell, directions: [], value: board[cell] };
    for (let r = -1; r <= 1; r++) {
      for (let c = -1; c <= 1; c++) {
        if (r === 0 && c === 0) continue;
        node.directions.push(getCell(cell, r, c));
      }
    }
    return node;
  };
  const graph = board.map((_, i) => makeNode(i));

  // Check for any wins!
  const getSequence = (node, direction) => {
    const sequence = [node.cell];
    while (sequence.length < inarow) {
      const next = graph[node.directions[direction]];
      if (!next || node.value !== next.value || next.value === 0) return;
      node = next;
      sequence.push(node.cell);
    }
    return sequence;
  };

  // Check all nodes.
  for (let i = 0; i < board.length; i++) {
    // Check all directions (not the most efficient).
    for (let d = 0; d < 8; d++) {
      const seq = getSequence(graph[i], d);
      if (seq) {
        drawLine(seq[0], seq[3]);
        i = board.length;
        break;
      }
    }
  }
}
