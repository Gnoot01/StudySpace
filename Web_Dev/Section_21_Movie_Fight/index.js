// https://omdbapi.com/
const apiKey = "...";
const autoCompleteConfig = {
  renderOption(movie) {
    const imgSRC = movie["Poster"] === "N/A" ? "" : movie["Poster"];
    return `<img src="${imgSRC}"/>
           ${movie["Title"]} (${movie["Year"]})`;
  },
  inputValue(movie) {
    return movie["Title"];
  },
  async fetchData(value) {
    const res = await axios.get("http://www.omdbapi.com/", {
      params: {apikey: apiKey, s: value},
    });
    return res["data"];
  },
};

createAutoComplete({
  ...autoCompleteConfig,
  root: document.querySelector("#left-autocomplete"),
  onOptionSelect(movie) {
    document.querySelector(".tutorial").classList.add("is-hidden");
    onMovieSelect(movie, document.querySelector("#left-summary"), "left");
  },
});

createAutoComplete({
  ...autoCompleteConfig,
  root: document.querySelector("#right-autocomplete"),
  onOptionSelect(movie) {
    document.querySelector(".tutorial").classList.add("is-hidden");
    onMovieSelect(movie, document.querySelector("#right-summary"), "right");
  },
});

let leftMovie;
let rightMovie;
const onMovieSelect = async (movie, summaryElement, side) => {
  const res = await axios.get("http://www.omdbapi.com/", {
    params: {apikey: apiKey, i: movie["imdbID"]},
  });

  // Resetting for multiple searches
  summaryElement.innerHTML = "";

  summaryElement.insertAdjacentHTML("afterbegin", movieTemplate(res["data"]));
  if (side === "left") leftMovie = res["data"];
  else rightMovie = res["data"];

  if (leftMovie && rightMovie) compare();
};

const movieTemplate = (movieDetail) => {
  // Better to use data attributes in html to compare than loop thru each article element and compare, as they may not be in the same order OR if(leftStat.contains("Awards")) very ugly
  const dollars = parseInt(
    movieDetail.BoxOffice.replace(/\$/g, "").replace(/,/g, "")
  );
  const metascore = parseInt(movieDetail.Metascore);
  const imdbRating = parseFloat(movieDetail.imdbRating);
  const imdbVotes = parseInt(movieDetail.imdbVotes.replace(/,/g, ""));
  const awards = movieDetail.Awards.split(" ").reduce((prev, word) => {
    const value = parseInt(word);
    if (isNaN(value)) return prev;
    else return parseInt((prev += value));
  }, 0);

  return `
  <article class="media">
    <figure class="media-left">
      <p class="image">
        <img src="${movieDetail["Poster"]}">
      </p>
    </figure>
    <div class="media-content">
      <div class="content">
      <h1>${movieDetail["Title"]}</h1>
      <h4>${movieDetail["Genre"]}</h4>
      <p>${movieDetail["Plot"]}</p>
  </article>
  <article data-value=${awards} class="notification is-primary">
    <p class="title">${movieDetail.Awards}</p>
    <p class="subtitle">Awards</p>
  </article>
  <article data-value=${dollars} class="notification is-primary">
    <p class="title">${movieDetail.BoxOffice}</p>
    <p class="subtitle">Box Office</p>
  </article>
  <article data-value=${metascore} class="notification is-primary">
    <p class="title">${movieDetail.Metascore}</p>
    <p class="subtitle">Metascore</p>
  </article>
  <article data-value=${imdbRating} class="notification is-primary">
    <p class="title">${movieDetail.imdbRating}</p>
    <p class="subtitle">IMDB Rating</p>
  </article>
  <article data-value=${imdbVotes} class="notification is-primary">
    <p class="title">${movieDetail.imdbVotes}</p>
    <p class="subtitle">IMDB Votes</p>
  </article>
  `;
};

const compare = () => {
  const leftSideStats = document.querySelectorAll(
    "#left-summary .notification"
  );
  const rightSideStats = document.querySelectorAll(
    "#right-summary .notification"
  );

  leftSideStats.forEach((leftStat, index) => {
    const rightStat = rightSideStats[index];
    // data attribute: are HTML (hence can style via CSS), to store extra info that doesn't have any visual representation as STRING (data-xxxx is in .dataset.xxxx)
    const leftSideValue = parseFloat(leftStat.dataset.value);
    const rightSideValue = parseFloat(rightStat.dataset.value);
    console.log("leftSideValue:", leftSideValue);
    console.log("rightSideValue:", rightSideValue);
    if (leftSideValue > rightSideValue) {
      rightStat.classList.remove("is-primary");
      rightStat.classList.add("is-warning");
      leftStat.classList.add("is-primary");
      leftStat.classList.remove("is-warning");
    } else if (rightSideValue > leftSideValue) {
      leftStat.classList.remove("is-primary");
      leftStat.classList.add("is-warning");
      rightStat.classList.add("is-primary");
      rightStat.classList.remove("is-warning");
    } else {
      rightStat.classList.add("is-primary");
      rightStat.classList.remove("is-warning");
      leftStat.classList.add("is-primary");
      leftStat.classList.remove("is-warning");
    }
  });
};
