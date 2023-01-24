let btns = document.querySelectorAll(".btn");
const buttonColours = ["red", "blue", "green", "yellow"];
const gamePattern = [];
const userClickedPattern = [];
let gameStarted = false;
let level = 1;

function pressAnimate(btn) {
    btn.classList.add("pressed");
    setTimeout(function () {
        btn.classList.remove("pressed");
    }, 100);
}

function pressSound(color) {
    let sound = new Audio(`sounds/${color}.mp3`);
    sound.play();
}

function nextSequence() {
    // Emptying a const array, so cannot simply = []
    userClickedPattern.length = 0;
    level++;
    document.querySelector("#level-title").innerHTML = `Level ${level}`;

    let randomNumber = Math.floor(Math.random() * 4);
    randomChosenColour = buttonColours[randomNumber];
    gamePattern.push(randomChosenColour);

    let btn = document.querySelector(`#${randomChosenColour}`);
    pressAnimate(btn);
    pressSound(randomChosenColour);
}

function checkAnswer(currentLevel) {
    if (userClickedPattern[currentLevel] === gamePattern[currentLevel]) {
        if (userClickedPattern.length === gamePattern.length) {
            setTimeout(function () {
                nextSequence();
            }, 1000);
        }
    } else {
        pressSound("wrong");
        document.body.classList.add("game-over");
        setTimeout(function () {
            document.body.classList.remove("game-over");
        }, 200);
        document.querySelector("#level-title").innerHTML =
            "Game Over, Press Any Key to Restart";
        startOver();
    }
}

function startOver() {
    level = 0;
    gamePattern.length = 0;
    gameStarted = false;
}

for (btnColour of btns) {
    btnColour.addEventListener("click", function () {
        // NOT let userChosenColour = btnColour.getAttribute("id");
        // NOT let userChosenColour = this.btnColour.getAttribute("id");
        let userChosenColour = this.getAttribute("id");
        userClickedPattern.push(userChosenColour);
        pressAnimate(this);
        pressSound(userChosenColour);

        checkAnswer(userClickedPattern.length - 1);
    });
}

document.addEventListener("keypress", function () {
    // Ensure further keypresses after the first do not trigger nextSequence again
    if (!gameStarted) {
        gameStarted = true;
        nextSequence();
    }
});
