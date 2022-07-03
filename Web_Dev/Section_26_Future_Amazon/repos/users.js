const crypto = require("crypto");
const util = require("util");
const Repo = require("./repo");

// util allows to promisify a func which receives a callback, hence can use async-await
const scrypt = util.promisify(crypto.scrypt);

class UsersRepo extends Repo {
  async create(attrs) {
    attrs["id"] = this.randomId();

    const salt = crypto.randomBytes(8).toString("hex");
    const buffer = await scrypt(attrs.password, salt, 64);
    const records = await this.getAll();
    const record = {...attrs, password: `${buffer.toString("hex")}.${salt}`};
    records.push(record);
    await this.writeAll(records);
    return record;
  }

  async comparePasswords(saved, input) {
    const [hashed, salt] = saved.split(".");
    const hashedInput = await scrypt(input, salt, 64);
    return hashed === hashedInput.toString("hex");
  }
}

// // XXX exporting the class
// module.exports = UsersRepo
// // Exporting as such requires that in another file,
// const UsersRepo = require("./users")
// const repo = new UsersRepo("users.json")

// Hence, export simply an instance of the class
module.exports = new UsersRepo("users.json");
// // In another file,
// const repo = require("./users");

// // TO TEST
// const test = async () => {
//   const repo = new UsersRepo("users.json");
//   await repo.create({email: "", password: ""});
// };

// test();
