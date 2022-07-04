const fs = require("fs");
const path = require("path");
const chalk = require("chalk");
const render = require("./render");

// Don't want to run .test.js files inside these dirs
const forbiddenDirs = ["node_modules"];

class Runner {
  constructor() {
    this.testFiles = [];
  }

  async collectFiles(targetPath) {
    const files = await fs.promises.readdir(targetPath);
    for (let file of files) {
      const filepath = path.join(targetPath, file);
      const stats = await fs.promises.lstat(filepath);

      if (stats.isFile() && file.includes(".test.js")) {
        // name is absolute path, shortName is relative path to cwd
        this.testFiles.push({name: filepath, shortName: file});
      } else if (stats.isDirectory() && !forbiddenDirs.includes(file)) {
        const childFiles = await fs.promises.readdir(filepath);
        // Need ...childFiles to ensure pushing childFiles and not an array of childFiles
        // Need .map to join previous file (if folder) path to childFile f
        files.push(...childFiles.map((f) => path.join(file, f)));
      }
    }
  }

  async runTests() {
    for (let file of this.testFiles) {
      console.log(chalk.gray(`---- ${file.shortName}`));
      // Node will first find if "it" was defined anywhere in current file.
      // If not, will find in global variables which are shared between all diff files
      const beforeEaches = [];
      global.render = render;

      global.beforeEach = (fn) => {
        beforeEaches.push(fn);
      };

      global.it = async (desc, fn) => {
        beforeEaches.forEach((func) => func());
        try {
          await fn();
          console.log(chalk.green(`\tOK - ${desc}`));
        } catch (err) {
          // Replace every newline char inside errMsg with a newline+2 tabs
          const errMsg = err.message.replace(/\n/g, "\n\t\t");
          console.log(chalk.red(`\tX - ${desc}`));
          // to condense down err without stacktrace
          console.log(chalk.red("\t", errMsg));
        }
      };

      try {
        require(file.name);
      } catch (err) {
        console.log(chalk.red(err));
      }
    }
  }
}

module.exports = Runner;
