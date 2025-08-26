import { useState, useEffect } from "react";
import API from "../api/axiosInstance";
import NoteForm from "./NoteForm";
import Sidebar from "./Sidebar";

export default function NotesList() {
  const [notes, setNotes] = useState([]);
  const [editingNote, setEditingNote] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [username, setUsername] = useState("");

  const fetchNotes = async () => {
    try {
      const res = await API.get("/notes/");
      setNotes(res.data);

      // Decode username from token for display
      const token = localStorage.getItem("token");
      if (token) {
        const payload = JSON.parse(atob(token.split(".")[1]));
        setUsername(payload.sub);
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => { fetchNotes(); }, []);

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this note?")) {
      await API.delete(`/notes/${id}`);
      fetchNotes();
    }
  };

  const handleEdit = (note) => {
    setEditingNote(note);
    setShowForm(true);
  };

  const handleFormClose = () => {
    setEditingNote(null);
    setShowForm(false);
    fetchNotes();
  };

  return (
    <div className="flex">
      <Sidebar username={username} />

      <div className="flex-1 p-6 bg-gray-100 min-h-screen">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">My Notes</h1>
          <button onClick={() => setShowForm(true)} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition">
            Add Note
          </button>
        </div>

        {showForm && <NoteForm note={editingNote} onClose={handleFormClose} />}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {notes.map(note => (
            <div key={note.id} className="bg-white p-4 rounded shadow relative">
              <h2 className="text-xl font-semibold mb-2">{note.title}</h2>
              <p className="text-gray-700 mb-4">{note.content}</p>
              <div className="absolute top-2 right-2 flex gap-2">
                <button onClick={() => handleEdit(note)} className="text-blue-500 hover:underline">Edit</button>
                <button onClick={() => handleDelete(note.id)} className="text-red-500 hover:underline">Delete</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
