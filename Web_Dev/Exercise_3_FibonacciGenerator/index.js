function fibonacciGenerator(n) {
    const seq = [];
    if (n === 1) {
        seq.push(0);
    } else if (n === 2) {
        seq.push(0, 1);
    } else {
        seq.push(0, 1);
        for (let i = 2; i < n; i++) {
            let seqLength = seq.length;
            seq.push(seq[seqLength - 1] + seq[seqLength - 2]);
        }
    }
    return seq;
}

console.log(fibonacciGenerator(10));
