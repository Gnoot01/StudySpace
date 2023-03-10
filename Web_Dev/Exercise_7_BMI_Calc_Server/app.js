const express = require("express");
const app = express();
const port = 3000;

app.use(express.urlencoded({extended: true}));

app.get("/bmicalculator", function (req, res) {
    res.sendFile(`${__dirname}/bmiCalculator.html`);
});

app.post("/bmicalculator", function (req, res) {
    let weight = parseFloat(req["body"]["weight"]);
    let height = parseFloat(req["body"]["height"]);
    console.log(typeof weight);
    res.write(`Your BMI is ${Math.round(weight / Math.pow(height, 2))}`);
});

app.listen(port, function () {
    console.log(`Server running at http://localhost:${port}`);
});
