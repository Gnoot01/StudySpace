const express = require("express");
const app = express();
const port = 3000;

app.use(express.urlencoded({extended: true}));
app.use(express.static("public"));
app.set("view engine", "ejs");

const items = ["Buy", "Cook", "Eat"];
const workItems = [];

app.get("/", function (req, res) {
    const today = new Date();
    const options = {
        weekday: "long",
        day: "numeric",
        month: "long",
    };
    const day = today.toLocaleDateString("en-US", options);

    res.render("list", {listTitle: day, items: items});
});

app.post("/", function (req, res) {
    const newListItem = req["body"]["newItem"];
    // usage of name="" + value="" in list.ejs to redirect to diff POST path
    if (req["body"]["list"] == "Work") {
        workItems.push(newListItem);
        res.redirect("/work");
    } else {
        items.push(newListItem);
        res.redirect("/");
    }
});

app.get("/work", function (req, res) {
    res.render("list", {listTitle: "Work List", items: workItems});
});

app.get("/about", function (req, res) {
    res.render("about");
});

app.listen(port, function () {
    console.log(`Server running at http://localhost:${port}`);
});
