// ECommerce App
// Express: Creating a web server, https://expressjs.com/, "npm i express"
// Nodemon: Restart web server whenever change detected, https://www.npmjs.com/package/nodemon, "npm i nodemon"
// Cookie-Session: cookie-creator, https://www.npmjs.com/package/cookie-session, "npm i cookie-session"
// Express-Validator: validate form data without website redirection, https://express-validator.github.io, "npm i express-validator"
// Multer: middleware func for receiving files Eg. createNew.js <form enctype != urlencoded, so bodyParser.urlencoded won't work, https://www.npmjs.com/package/multer, "npm i multer"

const express = require("express");
const bodyParser = require("body-parser");
const cookieSession = require("cookie-session");
const authRouter = require("./routes/admin/auth");
const adminProductsRouter = require("./routes/admin/products");
const productsRouter = require("./routes/products");
const cartsRouter = require("./routes/carts");

const app = express();
// Auto uses this middleware func on every "POST" form req, preventing "app.post("/...", bodyParser.urlencoded({ extended:true}), ...)" everytime
app.use(express.static("public")); // look inside cwd, make "public" directory public (available to entire outside world) such that any Eg. in layout.js will search public/css/main.css first.
app.use(bodyParser.urlencoded({extended: true}));
app.use(
  cookieSession({
    // random encryption key
    keys: ["gn9nr9g934niff"],
  })
);
app.use(authRouter);
app.use(adminProductsRouter);
app.use(productsRouter);
app.use(cartsRouter);

// // Under-the-hood inferior implementation of body-parser library
// // Express Middleware function (helper func in middle, b4 route handler)
// // next: Express framework created before promises, async-await, etc so next() allows Express to continue.
//
// const bodyParser = (req, res, next) => {
//   if (req["method"] === "POST") {
//     req.on("data", (data) => {
//       // <Buffer 69 61 22 ...> -> email=abc&password=abc&... -> {email:"abc", password:"abc", ...}
//       const parsed = data.toString("utf8");
//       const formData = {};
//       for (let pair of parsed) {
//         const [k, v] = pair.split("=");
//         formData[k] = v;
//       }
//       req["body"] = formData;
//       next();
//     });
//   } else {
//     next();
//   }
// };

app.listen(3000, () => {
  // port number to listen for incoming network reqs
  // "localhost:3000" in browser to receive network res
  // default port for http: 80, https:443, hence don't need specify for Eg. google.com as https://google.com
  console.log("Listening");
});
