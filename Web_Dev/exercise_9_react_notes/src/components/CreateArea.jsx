import React, { useState } from "react";
import {AddIcon} from "@material-ui/icons"
import {Fab, Zoom} from "@material-ui/core"

function CreateArea(props) {
    // For Note expansion upon click
    const [isExpanded, setExpanded] = useState(false)

    const [note, setNote] = useState({title: "", content:""})
    function handleChange(e){
        const {name, value} = e.target
        setNote(prevNote => {return {...prevNote, [name]: value}})
    }

  return (
    <div>
      <form className="create-note" onSubmit={(e) => {
        props.onAdd(note)
        setNote({title: "", content:""})
        e.preventDefault()
            }
        }>
        {isExpanded && <input onChange={handleChange} value={note["title"]} name="title" placeholder="Title" />}
        <textarea onClick={() => setExpanded=true} onChange={handleChange} value={note["content"]} name="content" placeholder="Take a note..." rows={isExpanded ? "1" : "3"} />
        <Zoom in={isExpanded}>
          {/* Floating Action Button from Material-UI works exactly the same as normal <button> */}
          <Fab><AddIcon /></Fab>
        </Zoom>  
      </form>
    </div>
  );
}

export default CreateArea;
