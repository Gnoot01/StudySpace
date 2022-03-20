// Write a getCard() function which returns a random playing card object, like:
// 		{
// 			value: 'K'
// 			suit: 'clubs'
// 		}
//Pick a random value from:
//----A,2,3,4,5,6,7,8,9,10,J,Q,K
//Pick a random suit from:
//----clubs,spades, hearts, diamonds
//Return both in an object

function choose(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function getCard() {
  const values = [
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
  ];
  const suits = ["clubs", "hearts", "diamonds", "spades"];
  return {
    value: choose(values),
    suit: choose(suits),
  };
}

console.log(getCard());
