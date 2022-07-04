#!/usr/bin/env node

// All-in-1 testing framework, can test
// 1. terminal+browser
// 2. has a "watch" mode to prevent the need to restart
// 3. can auto find and run all files in a project with extension "test.js"
// 4. requires very little setup and tests entire application not just a small part

// jsdom: stimulates a browser loaded with .html & .js code, so can access browser from terminal (NodeJS environment), https://www.npmjs.com/package/jsdom

const Runner = require("./runner");
const path = require("path");
const runner = new Runner();

const run = async () => {
  await runner.collectFiles(process.cwd());
  runner.runTests();
};

run();
