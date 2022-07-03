const express = require("express");
const {handleErrors} = require("./middlewares");
const usersRepo = require("../../repos/users");
const signupTemplate = require("../../templates/admin/auth/signup");
const signinTemplate = require("../../templates/admin/auth/signin");
const {
  requireEmail,
  requirePassword,
  requirePasswordConfirmation,
  requireEmailExists,
  requireValidPassword,
} = require("./validators");

// router = app in index.js, essentially keeping track of diff routes + allows linking back to app
const router = express.Router();

// Route handler func: signup route, "GET"
router.get("/signup", (req, res) => {
  // req is browser->server, res is server->browser
  res.send(signupTemplate({req}));
});

// signup route, "POST"
// Problem: Server immediately runs callback once seeing req with path and method (Doesn't wait until full thing can be accessed, sent over in chunks as Buffer object (array of raw info))
router.post(
  "/signup",
  // any no. of callbacks, processed sequentially
  [requireEmail, requirePassword, requirePasswordConfirmation],
  handleErrors(signupTemplate),
  async (req, res) => {
    const {email, password} = req.body;
    const user = await usersRepo.create({email, password});
    // req["session"] is Object {} created by cookieSession, to authenticate user via userId cookie
    req["session"]["userId"] = user["id"];
    res.redirect("/admin/products");
  }
);

router.get("/signin", (req, res) => {
  // pass in {} since signinTemplate takes & destructures {error}
  res.send(signinTemplate({}));
});

router.post(
  "/signin",
  [requireEmailExists, requireValidPassword],
  handleErrors(signinTemplate),
  async (req, res) => {
    const {email} = req.body;
    const user = await usersRepo.getOneBy({email});
    req["session"]["userId"] = user["id"];
    res.redirect("/admin/products");
  }
);

router.get("/signout", (req, res) => {
  req["session"] = null;
  res.send("Logged out!");
});

module.exports = router;
