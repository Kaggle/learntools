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

  const size = Math.min(height, width);
  canvas.width = size;
  canvas.height = size;

  const c = canvas.getContext("2d");
  c.clearRect(0, 0, canvas.width, canvas.height);
}
