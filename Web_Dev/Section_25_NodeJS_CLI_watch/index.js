#!/usr/bin/env node

// Detect & execute asap whenever anything changes in a watched folder
// Lodash: Useful funcs, https://lodash.com/docs/, "npm i lodash.debounce"
// Chokidar: Detect file changes, https://www.npmjs.com/package/chokidar, "npm i chokidar"
// Caporal: Helpful documentation for the tool (Eg. "watch -h" for documentation info on "watch"), https://www.npmjs.com/package/caporal, "npm i caporal"
// Child_Process: run code from within a program, https://nodejs.org/api/child_process.html

const debounce = require("lodash.debounce");
const chokidar = require("chokidar");
const program = require("caporal");
const {spawn} = require("child_process");
const fs = require("fs");
const chalk = require("chalk");

program
  .version("1.0.1")
  // Name of file can be optional due to below checking if "index.js" exists in folder.
  .argument("[filename]", "Name of file to execute")
  .action(async ({filename}) => {
    const name = filename || "index.js";

    try {
      // Checking if file of "name" exists /+ if user has permissions to read/write to that file
      await fs.promises.access(name);
    } catch (err) {
      throw new Error(`Could not find the file ${name}`);
    }

    let proc;
    const start = debounce(() => {
      // To kill off prev process Eg. Timeout, such that multiple diff unrelated processes are not running at once.
      if (proc) proc.kill();

      console.log(chalk.bold(chalk.red(">>> Starting Process >>>")));
      // stdio, inherit: any logs/errors emitted by that spawned child process will be passed to the parent (any error by child process is parent's)
      proc = spawn("node", [name], {stdio: "inherit"});
    }, 100);

    chokidar
      .watch(".")
      // When chokidar starts up, it registers each file individually as a new file added and invokes the callback func. Hence, a rate-limiter (debounce) is required.
      .on("add", start)
      .on("change", start)
      .on("unlink", start);
  });

program.parse(process.argv);
