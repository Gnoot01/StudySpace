import React, { useState } from "react";
import Header from "./Header";
import Footer from "./Footer";
import Note from "./Note";
import CreateArea from "./CreateArea";

function App() {
    const [notes, setNotes] = useState([])
    
    function addNote(note){
        setNotes(prevNotes => [...prevNotes, note])
    }

    // IMPT 
    function deleteNote(id){
        setNotes((prevNotes) => {
            return prevNotes.filter((note, index) => index !== id)
        })
    }
    return (
        <div>
        <Header />
        <CreateArea onAdd={addNote}/>
        {/* IMPT Adding id to note */}
        {notes.map((note, index) => <Note onDelete={deleteNote} key={index} id={index} title={note["title"]} content={note["content"]} />)}
        <Footer />
        </div>
    );
}

export default App;
