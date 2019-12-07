function renderer({
  parent,
  step,
  frame,
  environment,
  width = 400,
  height = 400,
}) {
  console.log("render");
  // Configuration.
  const { size } = environment.configuration;

  const colors = {
    bg: "#000B49",
    bgGradient: "#000B2A",
    shipyards: [
      ["#00A3DE", "#00BFFF", "#80DFFF"],
      ["#C2AF00", "#E4CE00", "#F2E780"],
    ],
    ships: [
      [
        "#2FDEFF",
        "#20BDFF",
        "#1AA1D9",
        "#168EBE",
        "#105F80",
        "#0F516D",
        "#161616",
      ],
      [
        "#F1E61D",
        "#E2CD13",
        "#C0AE10",
        "#AA990E",
        "#716609",
        "#605708",
        "#161616",
      ],
    ],
    flames: ["#FF972E", "#FEF545", "#FFF5FF"],
    halite: ["#008DFF", "#00C9FF", "#0FF", "#FFF"],
  };

  // Rectangle coordinates on a 20x20 grid.
  const rects = {
    ship: [
      "9.5,0;9,1;8,3,1,2;7,5,1,2;6,7,1,2;7,10,2;9,9",
      "9,2,2,7;8,5,4,2;7,7,6,2;6,9,1,3;13,9,1,3;10,9;9,10,4,3;7,11,2,2;9,13,2",
      "10,1;11,3,1,2;12,5,1,2;13,7,1,2;8,13;11,13;9,14,2;9.5,15",
      "5,9;4,10;3,11;2,12;1,13",
      "5,10;4,11,2;3,12,3;14,10;14,11,2;14,12,3",
      "2,13,3;14,9;15,10;16,11;17,12;15,13,4",
      "9.5,6;9,7,2;8,8,4;7,9,2;11,9,2;6,12;5,13,3;4,14,5;13,12;12,13,3;11,14,5",
    ],
    shipFlames: [
      "5,15,3,1,4;6,16,1,1,4;4.5,15,4,1,4,0.33;5,16,3,1,4,0.33;6,17,1,1,4,0.33;4,15,5,2,4,0.66;5,17,3,1,4,0.66;6,18,1,1,4,0.66",
      "6,15,1,1,4;5.5,15,2,1,4,0.33;6,16,1,1,4,0.33;5,15,3,1,4,0.66;5.5,16,2,1,4,0.66;6,17,1,1,4,0.66",
      "6,15,1,1,4,0.66",
    ],
    shipyard: [
      "9,9,2,2;2,4,5,1,15;3,5,5,1,15;4,6,5,1,15",
      "9,9,2,2,0,0.2;2,2,2,2,14;2,3,3,1,15;3,4,3,1,15;4,5,3,1,15;5,6,3,1,15;",
      "9,9,2,2,0,0.4;6,6,1,1,14,0.6;5,5,1,1,14,0.7;4,4,1,1,14,0.8;3,3,1,1,14,0.9;2,2,1,1,14,1",
    ],
    largeHalite: [
      "2,2;17,6;2,13;17,17;9,1,2,18,1;5,7,10,6,1",
      "9,3,2,14;3,9,14,2",
      "6,2;17,2;2,17;13,17;4,9,12,2,1;7,7,6,6",
      "13,2;17,13;2,6;6,17;6,9,8,2,1",
    ],
    mediumHalite: [
      "6,4;16,7;16,12;6,15;4,9,12,2,1;6,8,8,4,1",
      "9,5,2,10,1;",
      "13,4;3,7;3,12;13,15;9,6,2,8,1;8,8,4,4",
      "9,7,2,6,1",
    ],
    smallHalite: [
      "13.5,6.5;13.5,12.5;9.5,5.5,1,9,1;8.5,6.5,3,7,1",
      "9.5,6.5,1,7,1",
      "5.5,6.5;5.5,12.5;9.5,7.5,1,5,1;8.5,8.5,3,3",
      "9.5,8.5,1,3,1",
    ],
  };

  // Helper Functions.
  const getById = id => parent.querySelector(`#${id}`);
  const createElement = (type, id) => {
    const el = document.createElement(type);
    el.id = id;
    parent.appendChild(el);
    return el;
  };

  const createCanvas = id => {
    const canvas = createElement("canvas", id);
    canvas.width = width;
    canvas.height = height;
    return canvas;
  };

  const getCanvas = (id, { clear, alpha } = { clear: false, alpha: false }) => {
    const canvas = getById(id);
    const ctx = canvas.getContext("2d", { alpha });
    if (clear) ctx.clearRect(0, 0, canvas.width, canvas.height);
    return [canvas, ctx];
  };

  const store = (o = {}) => {
    const ta = parent.querySelector("#storage");
    const orig = JSON.parse(ta.value || "{}");
    o = { ...orig, ...o };
    ta.value = JSON.stringify(o);
    return o;
  };

  const data = function(el, key, value) {
    if (arguments.length === 3) {
      el.setAttribute(`data-${key}`, JSON.stringify(value));
      return value;
    }
    if (el.hasAttribute(`data-${key}`)) {
      return JSON.parse(el.getAttribute(`data-${key}`));
    }
    return null;
  };

  const rotateCenter = (ctx, centerX, centerY, pct, fn) => {
    ctx.save();
    ctx.translate(centerX, centerY);
    ctx.rotate(Math.PI * 2 * pct);
    ctx.translate(-centerX, -centerY);
    fn();
    ctx.restore();
  };

  const drawRects = (ctx, rects, color = "#000", scale = 1, gridSize = 20) => {
    // rects="x,y,w,h,specials,minFrame,maxFrame;..."
    ctx.save();
    ctx.fillStyle = color;
    ctx.beginPath();
    const drawSpecials = (x, y, w, h, special) => {
      const size = gridSize * scale;
      if ((special & 1) === 1) ctx.rect(y, x, h, w); // swap x/y and w/h
      if ((special & 2) === 2) ctx.rect(x, size - y - h, w, h); // Mirror over X Axis
      if ((special & 4) === 4) ctx.rect(size - x - w, y, w, h); // Mirror over Y Axis
      if ((special & 8) === 8) ctx.rect(size - x - w, size - y - h, w, h); // Mirror over X & Y Axis
      // Repeat mirroring if a swap occurred.
      if ((special & 1) === 1) drawSpecials(y, x, h, w, special - 1);
    };
    rects
      .replace(/\s/g, "")
      .split(";")
      .forEach(coords => {
        const defaultCoords = ["0", "0", "1", "1", "0", "0", "1"];
        coords = coords.split(",");
        let [x, y, w, h, special, minFrame, maxFrame] = defaultCoords.map(
          (v, i) =>
            parseFloat(coords.length > i ? coords[i] : v) * (i < 4 ? scale : 1)
        );
        if (minFrame > frame || maxFrame < frame) return;
        ctx.rect(x, y, w, h);
        drawSpecials(x, y, w, h, special);
      });
    ctx.fill();
    ctx.closePath();
    ctx.restore();
  };

  const getShipDirection = (player, pos) => {
    //NORTH, SOUTH, EAST, WEST, undefined
    const col = pos % size;
    const row = Math.floor(pos / size);
    const directions = [
      [row === size - 1 ? col : pos + size, "NORTH"],
      [row === 0 ? size * (size - 1) + col : pos - size, "SOUTH"],
      [col === size - 1 ? row * size : pos + 1, "WEST"],
      [col === 0 ? (row + 1) * size - 1 : pos - 1, "EAST"],
    ];
    for (let s = step; s >= 0; s--) {
      for (let a of environment.steps[s][player].action) {
        for (let d of directions) {
          if (a[0] === d[0] && a[1] === d[1]) return d[1];
        }
      }
    }
  };

  // First time setup.
  if (!parent.querySelector("#storage")) {
    console.log("setup");
    createElement("textarea", "storage").style.display = "none";
    createCanvas("bg");
    createCanvas("fg");

    const cellInset = 0.8;
    const fixedCellSize = 100;
    const minOffset = Math.min(height, width) > 400 ? 30 : 4;
    const cellSize = Math.min(
      (width - minOffset * 2) / size,
      (height - minOffset * 2) / size
    );

    const preCanvas = createCanvas("pre");
    preCanvas.width = fixedCellSize;
    preCanvas.height = 0;
    preCanvas.style.display = "none";

    store({
      cellInset,
      cellScale: cellSize / fixedCellSize,
      cellSize,
      fixedCellSize,
      maxCellHalite: Math.max.apply(
        null,
        environment.steps.reduce(
          (arr, step) =>
            arr.concat(step[0].observation.board.map(cell => cell[0])),
          []
        )
      ),
      xOffset: Math.max(0, (width - cellSize * size) / 2),
      yOffset: Math.max(0, (height - cellSize * size) / 2),
    });
  }

  // Expand storage.
  const {
    cellInset,
    cellScale,
    cellSize,
    fixedCellSize,
    maxCellHalite,
    xOffset,
    yOffset,
  } = store();

  // Restore Canvases.
  const [preCanvas, preCtx] = getCanvas("pre", { alpha: true });
  const [bgCanvas, bgCtx] = getCanvas("bg");
  const [fgCanvas, fgCtx] = getCanvas("fg", { clear: true, alpha: true });

  // Cache common drawings.
  const preDrawImage = (ctx, key, drawFn) => {
    let y = data(preCanvas, key);
    if (y === null) {
      y = preCanvas.height || 0;
      preCanvas.height = y + fixedCellSize;
      data(preCanvas, key, y);
      preCtx.save();
      preCtx.translate(0, y);
      drawFn(preCtx);
      preCtx.restore();
    }
    console.log("preDrawImage", key);
    ctx.drawImage(
      preCanvas,
      0,
      y,
      fixedCellSize,
      fixedCellSize,
      10,
      10,
      fixedCellSize,
      fixedCellSize
    );
    // return new Promise(resolve => {
    //   if (preImage.complete) {
    //     render();
    //     resolve();
    //   } else {
    //     preImage.addEventListener(
    //       "load",
    //       () => {
    //         render();
    //         resolve();
    //       },
    //       false
    //     );
    //   }
    // });
  };

  // Render Background once per step (Gradient + Halite)
  if (data(bgCanvas, "step") !== step) {
    data(bgCanvas, "step", step);
    bgCtx.fillStyle = colors.bg;
    bgCtx.fillRect(0, 0, bgCanvas.width, bgCanvas.height);

    const r = Math.min(height, width) / 2;
    const bgStyle = bgCtx.createRadialGradient(r, r, 0, r, r, r);
    bgStyle.addColorStop(0, colors.bg);
    bgStyle.addColorStop(1, colors.bgGradient);
    bgCtx.fillStyle = bgStyle;
    bgCtx.fillRect(0, 0, bgCanvas.width, bgCanvas.height);

    // Render the halite.
    environment.steps[step][0].observation.board.forEach((cell, pos) => {
      const col = pos % size;
      const row = Math.floor(pos / size);
      const [cellHalite, shipyard, dropoff] = cell;
      if (!cellHalite || shipyard > -1 || dropoff > -1) return;

      console.log("render halite", col, row, pos);

      // Position the Cell.
      bgCtx.save();
      bgCtx.translate(
        xOffset + cellSize * col + (cellSize - cellSize * cellInset) / 2,
        yOffset + cellSize * row + (cellSize - cellSize * cellInset) / 2
      );
      bgCtx.scale(cellScale * cellInset, cellScale * cellInset);

      const pct = cellHalite / maxCellHalite;
      let scale = 1;
      let haliteRect;

      if (pct > 0.7) {
        haliteRect = "largeHalite";
        scale = pct;
      } else if (pct < 0.3) {
        haliteRect = "smallHalite";
        scale = pct / 0.3;
      } else {
        haliteRect = "mediumHalite";
        scale = pct + 0.3;
      }
      rects[haliteRect].forEach((v, i) =>
        drawRects(bgCtx, v, colors.halite[i], 5)
      );
      // preDrawImage(bgCtx, haliteRect, ctx => {
      //   rects[haliteRect].forEach((v, i) =>
      //     drawRects(ctx, v, colors.ships[1][i], 5)
      //   );
      // });

      // rotateCenter(bgCtx, fixedCellSize / 2, fixedCellSize / 2, 1, () => {
      //   bgCtx.save();
      //   bgCtx.translate(
      //     ...Array(2).fill((fixedCellSize - fixedCellSize * scale) / 2)
      //   );
      //   bgCtx.scale(scale, scale);
      //   preDrawImage(bgCtx, haliteRect, ctx => {
      //     rects[haliteRect].forEach((v, i) =>
      //       drawRects(ctx, v, colors.halite[i], 5)
      //     );
      //   });
      //   bgCtx.restore();
      // });

      bgCtx.restore();
    });
  }

  // Draw the foreground (every frame).
  environment.steps[step][0].observation.board.forEach((cell, pos) => {
    const col = pos % size;
    const row = Math.floor(pos / size);
    const [_, shipyard, dropoff, ship, shipHalite] = cell;

    // Position the Cell.
    fgCtx.save();
    fgCtx.translate(
      xOffset + cellSize * col + (cellSize - cellSize * cellInset) / 2,
      yOffset + cellSize * row + (cellSize - cellSize * cellInset) / 2
    );
    fgCtx.scale(cellScale * cellInset, cellScale * cellInset);

    // Draw either: A shipyard, a dropoff, or Halite.
    if (shipyard > -1) {
      rects.shipyard.forEach((v, i) =>
        drawRects(fgCtx, v, colors.shipyards[shipyard][i], 5)
      );
    } else if (dropoff > -1) {
    }

    // Draw the Ship.
    if (ship > -1) {
      const direction = getShipDirection(ship, pos) || "NORTH";
      const rotations = { NORTH: 0, EAST: 0.25, SOUTH: 0.5, WEST: 0.75 };
      rotateCenter(
        fgCtx,
        fixedCellSize / 2,
        fixedCellSize / 2,
        rotations[direction],
        () => {
          rects.ship.forEach((v, i) =>
            drawRects(fgCtx, v, colors.ships[ship][i], 5)
          );
          rects.shipFlames.forEach((v, i) =>
            drawRects(fgCtx, v, colors.flames[i], 5)
          );
        }
      );
    }

    fgCtx.restore();
  });
}
