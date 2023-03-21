import React, { useState } from "react"

function ToDoItem(props){
    const [striked, setStrike] = useState(false)
    function handleClick(){
        // Toggling Mechanism
        // setStrike((prevValue) => !prevValue)
        props["onChecked"](props["id"])
    }
    // return <li onClick={handleClick} style={{textDecoration: striked && "line-through"}} >{props["text"]}</li>
    return <li onClick={handleClick} >{props["text"]}</li>
}


export default ToDoItem