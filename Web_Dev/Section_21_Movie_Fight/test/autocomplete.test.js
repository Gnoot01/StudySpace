// mocha: Testing Library Framework, https://mochajs.org/, "npm i --global mocha"

const waitFor = (selector) => {
  return new Promise((resolve, reject) => {
    const interval = setInterval(() => {
      if (document.querySelector(selector)) {
        clearInterval(interval);
        clearTimeout(timeout);
        resolve();
      }
    }, 30);

    const timeout = setTimeout(() => {
      clearInterval(interval);
      reject();
    }, 2000);
  });
};

// Sets up a clean testing environment before each test
beforeEach(() => {
  document.querySelector("#target").innerHTML = "";
  createAutoComplete({
    root: document.querySelector("#target"),
    renderOption(movie) {
      return movie["Title"];
    },
    // dummy data instead of actually calling API
    fetchData() {
      return [
        {Title: "Avengers"},
        {Title: "Not Avengers"},
        {Title: "Some movie"},
      ];
    },
  });
});

it("Dropdown starting closed", () => {
  const dropdown = document.querySelector(".dropdown");
  chai.assert.notInclude(dropdown.className, "is-active");
});

it("After searching, dropdown opens up", async () => {
  const input = document.querySelector("input");
  // manually setting input value doesn't trigger same event as typing
  input.value = "avengers";
  // Hence, need to manually trigger event
  input.dispatchEvent(new Event("input"));

  // timer to prevent test failing before dropdown even opens up, as the debounce func takes 500ms
  await waitFor(".dropdown-item");

  const dropdown = document.querySelector(".dropdown");
  chai.assert.include(dropdown.className, "is-active");
});

it("After searching, displays some results", async () => {
  const input = document.querySelector("input");
  input.value = "avengers";
  input.dispatchEvent(new Event("input"));

  await waitFor(".dropdown-item");

  const items = document.querySelectorAll(".dropdown-item");
  assert.strictEqual(items.length, 3);
});
