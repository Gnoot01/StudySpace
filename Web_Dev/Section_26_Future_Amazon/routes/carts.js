// Assign cart to anonymous user, like Amazon, by storing in cookie (req["session"])
// Store products in carts by NOT assigning carts to products, NOT duplicating full product data into individual carts,
// but by storing metadata (impt data like id, quantity) in individual carts to then lookup individual products
const express = require("express");
const cartsRepo = require("../repos/carts");
const productsRepo = require("../repos/products");
const cartShowTemplate = require("../templates/carts/show");

const router = express.Router();

router.post("/cart/products", async (req, res) => {
  let cart;
  if (!req["session"]["cartId"]) {
    cart = await cartsRepo.create({items: []});
    req["session"]["cartId"] = cart["id"];
  } else {
    cart = await cartsRepo.getOne(req["session"]["cartId"]);
  }

  const existingItem = cart["items"].find(
    (item) => item["id"] === req["body"]["productId"]
  );
  if (existingItem) existingItem["quantity"]++;
  else cart["items"].push({id: req["body"]["productId"], quantity: 1});
  await cartsRepo.update(cart["id"], {items: cart["items"]});
  res.redirect("/");
});

router.get("/cart", async (req, res) => {
  if (!req["session"]["cartId"]) return res.redirect("/");

  const cart = await cartsRepo.getOne(req["session"]["cartId"]);
  for (let item of cart["items"]) {
    const product = await productsRepo.getOne(item["id"]);
    item["product"] = product;
  }
  res.send(cartShowTemplate({items: cart["items"]}));
});

router.post("/cart/products/delete", async (req, res) => {
  const {itemId} = req["body"];
  const cart = await cartsRepo.getOne(req["session"]["cartId"]);
  const items = cart["items"].filter((item) => item.id !== itemId);

  await cartsRepo.update(req["session"]["cartId"], {items});
  res.redirect("/");
});

module.exports = router;