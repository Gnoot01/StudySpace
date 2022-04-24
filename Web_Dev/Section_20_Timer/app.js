// Unsure how to make timer circle continue from where it was paused, instead of resetting each time

const durationInput = document.querySelector("#duration");
const startButton = document.querySelector("#startBtn");
const pauseButton = document.querySelector("#pauseBtn");
const circle = document.querySelector("circle");

const perimeter = circle.getAttribute("r") * 2 * Math.PI;
circle.setAttribute("stroke-dasharray", perimeter);

let duration;
const timer = new Timer(durationInput, startButton, pauseButton, {
  onStart(totalDuration) {
    duration = totalDuration;
  },

  onTick(timeRemaining) {
    circle.setAttribute(
      "stroke-dashoffset",
      (perimeter * timeRemaining) / duration - perimeter
    );
  },

  onComplete() {
    // need to setTimeout as otherwise js waits for alert to be resolved before continuing.
    setTimeout(() => alert("Time's up!"), 10);
    new Audio("dandelions.mp3").play();
  },
});
