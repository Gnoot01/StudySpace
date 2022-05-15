// https://brm.io/matter-js/ : is a HTML element <canvas> API
// Terminology:
// World: Object containing everything
// Engine: Reads current state of the world from World Object (knows of every object's dimensions in time & space), like transitioning from 1 snapshot to another
// Runner: Tells Engine to process all data in World 60 times/sec
// Render: Display all ran data on screen
// Body: Any shape

// Demo
/*const {World, Engine, Runner, Render, Bodies, Mouse, MouseConstraint} = Matter;

const width = window.innerWidth;
const height = window.innerHeight;
const engine = Engine.create();
const {world} = engine;
const render = Render.create({
  // display all ran data inside document.body, adding NOT replacing current document.body html code
  element: document.body,
  engine: engine,
  // width and height of canvas to display data
  options: {
    // Solid colored shapes instead of just outline
    wireframes: false,
    width,
    height,
  },
});
Render.run(render);
Runner.run(Runner.create(), engine);

// (1st, 2nd): position in world from top left corner to centre of body, (3rd, 4th): (x/w, y/h), isStatic: disable gravity
// Walls
const walls = [
  Bodies.rectangle(width / 2, 0, width, 40, {
    isStatic: true,
  }),
  Bodies.rectangle(0, height / 2, 40, height, {
    isStatic: true,
  }),
  Bodies.rectangle(width, height / 2, 40, height, {isStatic: true}),
  Bodies.rectangle(width / 2, height, width, 40, {
    isStatic: true,
  }),
];

// Need to add into world to display
// console.log(world) sometimes to check its array elements
World.add(
  world,
  MouseConstraint.create(engine, {mouse: Mouse.create(render.canvas)})
);
World.add(world, walls);
// Random Shapes
for (let i = 0; i < 30; i++) {
  if (Math.random() < 0.5) {
    World.add(
      world,
      Bodies.rectangle(Math.random() * width, Math.random() * height, 50, 50)
    );
  } else {
    World.add(
      world,
      Bodies.circle(Math.random() * width, Math.random() * height, 30, {
        render: {fillstyle: "green"},
      })
    );
  }
}
*/
const playGame = () => {
  const cellsHorizontal = 4;
  const cellsVertical = 6;
  const width = window.innerWidth;
  const height = window.innerHeight;
  const unitWidth = width / cellsHorizontal;
  const unitHeight = height / cellsVertical;

  const {World, Engine, Runner, Render, Bodies, Body, Events} = Matter;
  const engine = Engine.create();
  engine.world.gravity.y = 0; // Disabling gravity
  const {world} = engine;
  const render = Render.create({
    element: document.body,
    engine: engine,
    options: {
      wireframes: false,
      width,
      height,
    },
  });
  const runner = Runner.create();
  Render.run(render);
  Runner.run(runner, engine);

  // Barriers (top, bottom, left, right)
  const barriers = [
    Bodies.rectangle(width / 2, 0, width, 10, {
      label: "barrier",
      isStatic: true,
    }),
    Bodies.rectangle(width / 2, height, width, 10, {
      label: "barrier",
      isStatic: true,
    }),
    Bodies.rectangle(0, height / 2, 10, height, {
      label: "barrier",
      isStatic: true,
    }),
    Bodies.rectangle(width, height / 2, 10, height, {
      label: "barrier",
      isStatic: true,
    }),
  ];

  World.add(world, barriers);

  // Maze Generation (true=visited/open)
  // Refer to Maze_Generation_Steps, Maze_Generation_Visualization_1, Maze_Generation_Visualization_2
  // |_|_|_|
  // |_|_|_|
  // |_|_|_|

  const shuffle = (arr) => {
    let counter = arr.length;

    while (counter > 0) {
      const i = Math.floor(Math.random() * counter);
      counter--;
      const temp = arr[counter];
      arr[counter] = arr[i];
      arr[i] = temp;

      return arr;
    }
  };

  const grid = Array(cellsVertical) // Rows
    .fill(null) // Cannot just do .fill([false, false, false]), as they are the exact same arrays in memory, hence Eg. grid[0].push(true) will edit all 3 arrays
    .map(() => Array(cellsHorizontal).fill(false)); // Columns

  const verticals = Array(cellsVertical)
    .fill(null)
    .map(() => Array(cellsHorizontal - 1).fill(false));

  const horizontals = Array(cellsVertical - 1)
    .fill(null)
    .map(() => Array(cellsHorizontal).fill(false));

  const startRow = Math.floor(Math.random() * cellsVertical);
  const startColumn = Math.floor(Math.random() * cellsHorizontal);

  const stepThruCell = (r, c) => {
    if (grid[r][c]) return;
    grid[r][c] = true;
    const neighbors = shuffle([
      // Starting position: mid
      [r - 1, c, "up"],
      [r + 1, c, "down"],
      [r, c - 1, "left"],
      [r, c + 1, "right"],
    ]);

    for (let neighbor of neighbors) {
      const [nextRow, nextColumn, direction] = neighbor;
      // If next move is out of bounds
      if (
        nextRow < 0 ||
        nextRow >= cellsVertical ||
        nextColumn < 0 ||
        nextColumn >= cellsHorizontal
      )
        continue;
      // If next neighbor has been visited
      if (grid[nextRow][nextColumn]) continue;

      // Refer to Maze_Move_U_D
      if (direction === "up") horizontals[r - 1][c] = true;
      else if (direction === "down") horizontals[r][c] = true;
      // Refer to Maze_Move_L_R
      else if (direction === "left") verticals[r][c - 1] = true;
      else if (direction === "right") verticals[r][c] = true;

      stepThruCell(nextRow, nextColumn);
    }
  };

  stepThruCell(startRow, startColumn);

  // Generating the path via walls
  horizontals.forEach((r, rIndex) => {
    r.forEach((open, cIndex) => {
      if (open) return;
      const wall = Bodies.rectangle(
        cIndex * unitWidth + unitWidth / 2,
        rIndex * unitHeight + unitHeight,
        unitWidth,
        10,
        {label: "wall", isStatic: true, render: {fillStyle: "red"}}
      );
      World.add(world, wall);
    });
  });

  verticals.forEach((r, rIndex) => {
    r.forEach((open, cIndex) => {
      if (open) return;
      const wall = Bodies.rectangle(
        cIndex * unitWidth + unitWidth,
        rIndex * unitHeight + unitHeight / 2,
        10,
        unitHeight,
        {label: "wall", isStatic: true, render: {fillStyle: "red"}}
      );
      World.add(world, wall);
    });
  });

  // Goal
  const goal = Bodies.rectangle(
    width - unitWidth / 4,
    height - unitHeight / 4,
    unitWidth * 0.4,
    unitHeight * 0.4,
    {label: "goal", isStatic: true, render: {fillStyle: "green"}}
  );
  World.add(world, goal);

  // Ball
  const ballRadius = Math.min(unitWidth, unitHeight) / 4;
  const ball = Bodies.circle(unitWidth / 2, unitHeight / 2, ballRadius, {
    label: "ball",
    render: {fillStyle: "white"},
  });
  World.add(world, ball);

  // Continous Collision Detection (CCD) not implemented in MatterJS yet (Eg. Object travelling at high enough speeds can clip through a thin-enough object)
  // Hence, thin -> thicker / limit max speed / smaller timestep and multiple updates per frame
  // Limiting Max Speed
  const limitMaxSpeed = () => {
    let maxSpeed = 15;
    if (ball.velocity.x > maxSpeed)
      Body.setVelocity(ball, {x: maxSpeed, y: ball.velocity.y});

    if (ball.velocity.x < -maxSpeed)
      Body.setVelocity(ball, {x: -maxSpeed, y: ball.velocity.y});

    if (ball.velocity.y > maxSpeed)
      Body.setVelocity(ball, {x: ball.velocity.x, y: maxSpeed});

    if (ball.velocity.y < -maxSpeed)
      Body.setVelocity(ball, {x: -ball.velocity.x, y: -maxSpeed});
  };
  Events.on(engine, "beforeUpdate", limitMaxSpeed);

  // Handling Keypresses
  document.addEventListener("keydown", (e) => {
    const {x, y} = ball.velocity;
    if (e.key === "w") Body.setVelocity(ball, {x, y: y - 5}); // W: Move up
    if (e.key === "s") Body.setVelocity(ball, {x, y: y + 5}); // S: Move down
    if (e.key === "a") Body.setVelocity(ball, {x: x - 5, y}); // A: Move left
    if (e.key === "d") Body.setVelocity(ball, {x: x + 5, y}); // D: Move right
  });

  // Listening for events inside world object allows to create Win Condition
  Events.on(engine, "collisionStart", (e) => {
    // Chrome reuses the e each time, overwriting all info of prev es, hence need to loop thru e.pairs array
    e.pairs.forEach((collision) => {
      // collision array: {id: '...', bodyA: {…}, bodyB: {…}, collision: {…}, ...}
      // Doing this is btr than checking if ["bodyA"]["label"] collides into ["bodyB"]["label"] or vice versa
      const labels = ["ball", "goal"];
      if (
        labels.includes(collision["bodyA"]["label"]) &&
        labels.includes(collision["bodyB"]["label"])
      ) {
        document.querySelector(".winner").classList.remove("hidden");
        world.gravity.y = 1;
        world.bodies.forEach((body) => {
          if (body["label"] === "wall") Body.setStatic(body, false);
        });
      }
    });
  });

  document.querySelector("#playAgain").addEventListener("click", () => {
    // clearing MatterJS-related
    World.clear(world);
    Engine.clear(engine);
    Render.stop(render);
    Runner.stop(runner);
    render.canvas.remove();
    render.canvas = null;
    render.context = null;
    render.textures = {};

    // clearing HTML
    document.body.innerHTML = `
    <div class="winner hidden">
        <h1>You Win!<br>
        <button id="playAgain">Play Again?</button>
        </h1>
    </div>
    <script src="index.js"></script>
`;
    document.querySelector(".winner").classList.add("hidden");
    playGame();
  });
};

playGame();
