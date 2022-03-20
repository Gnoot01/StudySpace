// Write a function to find the average value in an array of numbers

function getAvg(array) {
  let total = 0;
  for (num of array) total += num;
  return total / array.length;
}

console.log(getAvg([0, 50])); //25
console.log(getAvg([75, 76, 80, 95, 100])); //85.2
