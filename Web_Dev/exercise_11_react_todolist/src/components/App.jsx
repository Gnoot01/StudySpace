import React, {useState} from "react";
import ToDoItem from "./ToDoItem"
import InputArea from "./InputArea"

function App() {
  const [listOfItems, setListOfItems] = useState([])
  
  function addItem(inputField){
    setListOfItems((prevValue)=>[...prevValue, inputField])
  }

  // Optional deleting on click instead of just striking-through
  function deleteItem(id) {
    setListOfItems(prevItems => {
      return prevItems.filter((item, index) => {
        return index !== id
      })
    })
  }
  return (
    <div className="container">
      <div className="heading">
        <h1>To-Do List</h1>
      </div>
      <InputArea handleClick={addItem}/>
      <div>
        <ul>
          {listOfItems.map((item, index)=><ToDoItem key={index} id={index} text={item} onChecked={deleteItem}/>)}
        </ul>
      </div>
    </div>
  );
}

export default App;
