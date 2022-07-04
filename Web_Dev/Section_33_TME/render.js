const path = require("path");
const jsdom = require("jsdom");
const {JSDOM} = jsdom;

const render = async (filename) => {
  const filePath = path.join(process.cwd(), filename);
  const dom = await JSDOM.fromFile(filePath, {
    // NodeJS environment is terminal, which has full access to local computer. So can be dangerous executing random JS code
    // But this will always run code we trust
    runScripts: "dangerously",
    resources: "usable",
  });

  // Issue was test.js not waiting for all js files to be loaded first before running, hence wrong results.
  return new Promise((resolve, reject) => {
    dom.window.document.addEventListener("DOMContentLoaded", () =>
      resolve(dom)
    );
  });
};

module.exports = render;
