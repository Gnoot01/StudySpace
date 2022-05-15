// "npx now" in console with NodeJS installed to deploy live.

const {hash} = window.location;
const msg = atob(hash.replace("#", ""));

if (msg) {
  document.querySelector("#msg-form").classList.add("hide");
  document.querySelector("#msg-show").classList.remove("hide");

  document.querySelector("h1").innerHTML = msg;
}

document.querySelector("form").addEventListener("submit", (e) => {
  // default browser behavior is to submit info in form to a backend server (appears as if refreshing)
  e.preventDefault();

  document.querySelector("#msg-form").classList.add("hide");
  document.querySelector("#link-form").classList.remove("hide");

  const msgInput = document.querySelector("#msg-input");
  // Encoding is basically combining all bits then splitting from ASCII (8) to base64 (6) (btoa(...))
  const encrypted = btoa(msgInput.value);

  const linkInput = document.querySelector("#link-input");
  linkInput.value = `${window.location}#${encrypted}`;
  linkInput.select();
});
