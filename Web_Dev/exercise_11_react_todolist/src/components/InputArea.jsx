import React, {useState} from "react"

function InputArea(props){
    const [inputField, setInputField] = useState("")

    function handleChange(e){
        setInputField(e.target.value)
    }
    
    return (<div className="form">
    <input onChange={handleChange} value={inputField} type="text" />
    <button onClick={() => {
        props["handleClick"](inputField)
        setInputField("")
        }}>
      <span>Add</span>
    </button>
  </div>)
}

export default InputArea