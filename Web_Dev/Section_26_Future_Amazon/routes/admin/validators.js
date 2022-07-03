const {check, validationResult} = require("express-validator");
const usersRepo = require("../../repos/users");

module.exports = {
  requireEmail: check("email")
    .trim()
    .normalizeEmail()
    .isEmail()
    // Custom msg for default validators
    .withMessage("Must be a valid email")
    // Custom msg in form of error for custom validator
    .custom(async (email) => {
      const existingUser = await usersRepo.getOneBy({email});
      if (existingUser) throw new Error("Email in use");
    }),

  requirePassword: check("password")
    .trim()
    .isLength({min: 4, max: 20})
    .withMessage("Must be between 4 and 20 characters"),

  // If want to compare against another field's value, need {req} as argument
  requirePasswordConfirmation: check("passwordConfirmation")
    .trim()
    .isLength({min: 4, max: 20})
    .withMessage("Must be between 4 and 20 characters")
    .custom((passwordConfirmation, {req}) => {
      if (passwordConfirmation !== req["body"]["password"])
        throw new Error("Passwords must match");
      // NEEDED as some issue with express-validator custom, else throws generic "Invalid Value" error
      else return true;
    }),

  requireEmailExists: check("email")
    .trim()
    .normalizeEmail()
    .isEmail()
    .withMessage("Must be a valid email")
    .custom(async (email) => {
      const existingUser = await usersRepo.getOneBy({email});
      if (!existingUser) throw new Error("Email not found");
    }),

  requireValidPassword: check("password")
    .trim()
    .custom(async (password, {req}) => {
      const existingUser = await usersRepo.getOneBy({
        email: req["body"]["email"],
      });
      if (!existingUser) throw new Error("Wrong password");

      const validPassword = await usersRepo.comparePasswords(
        existingUser["password"],
        password
      );
      if (!validPassword) throw new Error("Wrong password");
    }),

  requireTitle: check("title")
    .trim()
    .isLength({min: 5, max: 40})
    .withMessage("Must be between 5 and 40 characters"),

  // field is entered as string, so need to convert to float and ensure it was converted to float >= 1
  requirePrice: check("price")
    .trim()
    .toFloat()
    .isFloat({min: 1})
    .withMessage("Must be number greater than 1"),
};
