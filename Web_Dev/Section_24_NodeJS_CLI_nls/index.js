#!/usr/bin/env node

// Emulating the "ls" CLI command
// Executable bin "nls" is in %appdata%\npm. Refer to "Where_executable_bin_are"
// fs: Node File System, https://nodejs.org/api/fs.html
// Chalk: color terminal, https://www.npmjs.com/package/chalk, "npm i chalk"

const fs = require("fs");
const util = require("util");
const path = require("path");
const chalk = require("chalk");

// Method 2A
// const lstat = filename => {
//   return new Promise((resolve, reject) => {
//     fs.lstat(filename, (err, stats) => {
//       if (err) reject(err);
//       resolve(stats);
//     });
//   });
// };

// Method 2B (NodeJS' Promise interface instead of normal callbacks )
// const lstat = util.promisify(fs.lstat);

// Method 2C
const {lstat} = fs.promises;

const targetDir = process.argv[2] || process.cwd();

fs.readdir(targetDir, async (err, filenames) => {
  if (err) console.log(err);

  // Method 1 (Callback-based, but gets confusing quickly esp if adding more layers of complexity (unscalable))
  // const allStats = Array(filenames.length).fill(null)
  //
  // for (let filename of filenames) {
  //     const index = filenames.indexOf(filename)
  //     fs.lstat(filename, (err, stats) => {
  //         if (err) console.log(err)
  //
  //         allStats[index] = stats
  //         const ready = allStats.every((stats)=>stats)
  //         if (ready) {
  //             allStats.forEach((stats, index) => console.log(filesname[index], stats.isFile()))
  //         }
  //     })
  // }

  // Method 2 (Promise-based, Runs sequentially awaiting for each lstat, so quite slow)
  // for (let filename of filenames) {
  //   try {
  //     const stats = await lstat(filename)
  //     console.log(filename, stats.isFile())
  //   } catch(err) {
  //     console.log(err)
  //   }
  // }

  // Method 3 (Promise.all-based, Runs parallel, seems sychronous)
  const statPromises = filenames.map((filename) => {
    // joins into targetDir/filename
    return lstat(path.join(targetDir, filename));
  });
  const allStats = await Promise.all(statPromises);
  for (let stats of allStats) {
    const index = allStats.indexOf(stats);

    stats.isFile()
      ? console.log(filenames[index])
      : console.log(chalk.bold(chalk.blue(filenames[index])));
  }
});
