module.exports = {
  getError(errors, property) {
    // try-catch for if no errors/property (undefined)
    try {
      // []->{property: {msg: "..."}}
      return errors.mapped()[property].msg;
    } catch (err) {
      return "";
    }
  },
};
