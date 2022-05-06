const createAutoComplete = ({
  root,
  renderOption,
  onOptionSelect,
  inputValue,
  fetchData,
}) => {
  root.insertAdjacentHTML(
    "afterbegin",
    `
    <label><strong>Search For An Item</strong></label>
    <input class="input"/>
    <div class="dropdown">
    <div class="dropdown-menu">
    <div class="dropdown-content results"></div>
    </div>
    </div>
    `
  );
  const input = root.querySelector("input");
  const dropdown = root.querySelector(".dropdown");
  const resultsWrapper = root.querySelector(".results");

  input.addEventListener(
    "input",
    debounce(async (e) => {
      const res = await fetchData(e.target.value);

      resultsWrapper.innerHTML = "";
      dropdown.classList.remove("is-active");

      if (!res["Error"]) {
        dropdown.classList.add("is-active");
        res["Search"].forEach((item) => {
          const option = document.createElement("a");
          option.classList.add("dropdown-item");
          option.insertAdjacentHTML("afterbegin", renderOption(item));

          option.addEventListener("click", (e) => {
            input.value = inputValue(item);
            dropdown.classList.remove("is-active");
            onOptionSelect(item);
          });

          resultsWrapper.appendChild(option);
        });
      }
    }, 1000)
  );

  // e.target reveals the element clicked on, anywhere in the document.
  document.addEventListener("click", (e) => {
    // If any element in the root is clicked, dropdown will remain open. Otherwise, will close.
    if (!root.contains(e.target)) dropdown.classList.remove("is-active");
  });
};
