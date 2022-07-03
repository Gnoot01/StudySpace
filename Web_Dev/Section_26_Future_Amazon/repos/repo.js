const fs = require("fs");
const crypto = require("crypto");

module.exports = class Repo {
  constructor(filename) {
    if (!filename) throw new Error("Creating a repository requires a filename");
    this.filename = filename;
    // Funcs in constructors CANNOT be async in nature. HENCE use sync versions all sync versions inside / async funcs outside & invoke separately
    try {
      // if file exists
      fs.accessSync(this.filename);
    } catch {
      // else, create file & writes string of empty array
      fs.writeFileSync(this.filename, "[]");
    }
  }

  randomId() {
    // <Buffer ...> -> hex, >> Math.random()
    return crypto.randomBytes(4).toString("hex");
  }

  async create(attrs) {
    attrs["id"] = this.randomId();
    const records = await this.getAll();
    records.push(attrs);
    await this.writeAll(records);
    return attrs;
  }

  async getAll() {
    return JSON.parse(
      await fs.promises.readFile(this.filename, {encoding: "utf8"})
    );
  }

  async writeAll(records) {
    await fs.promises.writeFile(
      this.filename,
      // custom formatting, level of indentation (no. of spaces every level down)
      JSON.stringify(records, null, 2)
    );
  }

  async getOne(id) {
    const records = await this.getAll();
    return records.find((record) => record["id"] === id);
  }

  async getOneBy(filters) {
    const records = await this.getAll();
    for (let record of records) {
      let found = true;
      for (let key in filters) {
        if (record[key] !== filters[key]) {
          found = false;
          break;
        }
      }
      if (found) return record;
    }
  }

  async update(id, attrs) {
    const records = await this.getAll();
    const record = records.find((record) => record["id"] === id);
    // Why don't use this.getOne() instead? - update requires this.writeAll anyway, so no diff
    // Why throw an error here, but not in getOne? - getOne is simply retrieval, may or may not exist.
    //                                               Update requires definite existence, so debugging error is necessary
    if (!record) throw new Error(`Record with id ${id} not found`);

    // assign: k-v pairs of later (attrs) copies (if doesn't exist) & overwrites (if exists) earlier (record) objects
    Object.assign(record, attrs);
    await this.writeAll(records);
  }

  async delete(id) {
    const records = await this.getAll();
    const filteredRecords = records.filter((record) => record["id"] !== id);
    await this.writeAll(filteredRecords);
  }
};
