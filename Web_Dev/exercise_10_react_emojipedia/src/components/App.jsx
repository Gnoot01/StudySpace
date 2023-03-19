import React from "react";
import Card from "./Card"
import emojipedia from "../emojipedia";

function App() {
  return (
    <div>
      <h1>
        <span>Emojipedia</span>
      </h1>
      <dl className="dictionary">
      {emojipedia.map(emoji => <Card key={emoji["id"]} emoji={emoji["emoji"]} name={emoji["name"]} meaning={emoji["meaning"]}/>)}
      </dl>
      <footer>From https://www.emojimeanings.net/list-smileys-people-whatsapp</footer>
    </div>
  );
}

export default App;
