// A pangram is a sentence that contains every letter of the alphabet, like: "The quick brown fox jumps over the lazy dog"
// Write a function called isPangram, which checks to see if a given sentence contains every letter of the alphabet.  Make sure you igore string casing!

// Don't know why I took this approach... LOL
// function isPangram(sentence) {
//   const allAlphabetCodes = [];
//   for (let i = 97; i < 123; i++) allAlphabetCodes.push(i);
//   for (let i = 0; i < sentence.trim().length; i++) {
//     charCode = sentence.trim().toLowerCase().charCodeAt(i);
//     for (alphabetCode of allAlphabetCodes) {
//       if (charCode === alphabetCode) {
//         allAlphabetCodes.splice(allAlphabetCodes.indexOf(charCode), 1);
//       }
//     }
//   }
//   return allAlphabetCodes.length === 0;
// }

function isPangram(sentence) {
  for (let char of "abcdefghijklmnopqrstuvwxyz") {
    if (!sentence.trim().toLowerCase().includes(char)) {
      return false;
    }
  }
  return true;
}

console.log(isPangram("The five boxing wizards jump quickly")); //true
console.log(isPangram("The five boxing wizards jump quick")); //false
