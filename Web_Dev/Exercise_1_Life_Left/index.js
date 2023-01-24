function lifeLeft(age) {
    // Assuming 365 days, 52 weeks and 12 months in a year
    let yearsRemaining = 90 - age;
    let daysLeft = yearsRemaining * 365;
    let weeksLeft = yearsRemaining * 52;
    let monthsLeft = yearsRemaining * 12;
    console.log(
        `You have ${daysLeft} days, ${weeksLeft} weeks, and ${monthsLeft} months left.`
    );
}

lifeLeft(21);
