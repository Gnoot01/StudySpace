function makeSound(key) {
    switch (key) {
        case "s":
            let c = new Audio("sounds/c.mp3");
            c.play();
            break;
        case "d":
            let d = new Audio("sounds/d.mp3");
            d.play();
            break;
        case "f":
            let e = new Audio("sounds/e.mp3");
            e.play();
            break;
        case "g":
            let f = new Audio("sounds/f.mp3");
            f.play();
            break;
        case "h":
            let g = new Audio("sounds/g.mp3");
            g.play();
            break;
        case "j":
            let a = new Audio("sounds/a.mp3");
            a.play();
            break;
        case "k":
            let b = new Audio("sounds/b.mp3");
            b.play();
            break;
        case "e":
            let cSharp = new Audio("sounds/cSharp.mp3");
            cSharp.play();
            break;
        case "r":
            let dSharp = new Audio("sounds/dSharp.mp3");
            dSharp.play();
            break;
        case "y":
            let fSharp = new Audio("sounds/fSharp.mp3");
            fSharp.play();
            break;
        case "u":
            let gSharp = new Audio("sounds/gSharp.mp3");
            gSharp.play();
            break;
        case "i":
            let aSharp = new Audio("sounds/aSharp.mp3");
            aSharp.play();
            break;
        default:
            console.log(buttonInnerHTML);
            break;
    }
}

function buttonAnimation(key) {
    let activeButton = document.querySelector(`.${key}`);
    activeButton.classList.add("pressed");
    setTimeout(function () {
        activeButton.classList.remove("pressed");
    }, 100);
}

// Click
let instruments = document.querySelectorAll(".key");
for (instrument of instruments) {
    instrument.addEventListener("click", function () {
        let buttonInnerHTML = this.innerHTML;
        makeSound(buttonInnerHTML);
        buttonAnimation(buttonInnerHTML);
    });
}

// Keyboard
document.addEventListener("keydown", function (e) {
    makeSound(e.key);
    buttonAnimation(e.key);
});
