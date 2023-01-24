let dicee = document.querySelectorAll(".dice img");
let title = document.querySelector(".container h1");
let randomNumber1 = Math.floor(Math.random() * 6) + 1;
let randomNumber2 = Math.floor(Math.random() * 6) + 1;

dicee[0].setAttribute("src", `images/dice${randomNumber1}.png`);
dicee[1].setAttribute("src", `images/dice${randomNumber2}.png`);

if (randomNumber1 > randomNumber2) {
    title.innerText = "🚩Player 1 Wins!";
} else if (randomNumber1 < randomNumber2) {
    title.innerText = "Player 2 Wins!🚩";
} else {
    title.innerText = "Draw!";
}
