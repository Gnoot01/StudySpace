// Write a isValidPassword function
// It accepts 2 arguments: password and username
// Password must:
//	- be at least 8 characters
//  - cannot contain spaces
//  - cannot contain the username
// If all requirements are met, return true.
//Otherwise: false

function isValidPassword(password, username){
    return !(password.length < 8 || password.includes(" ") || password.includes(username))
}

console.log(isValidPassword('89Fjj1nms', 'dogLuvr'))   //true
console.log(isValidPassword('dogLuvr123!', 'dogLuvr')) //false
console.log(isValidPassword('hello1', 'dogLuvr'))      //false