import { useState, useEffect } from "react";
import API from "../api/axiosInstance";

export default function NoteForm({ note, onClose }) {
  const [title, setTitle] = useState(note?.title || "");
  const [content, setContent] = useState(note?.content || "");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (note) {
      await API.put(`/notes/${note.id}`, { title, content });
    } else {
      await API.post("/notes/", { title, content });
    }
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded shadow w-full max-w-md">
        <h2 className="text-2xl font-bold mb-4">{note ? "Edit Note" : "Add Note"}</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <input
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="border p-2 rounded"
            required
          />
          <textarea
            placeholder="Content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="border p-2 rounded"
            rows={4}
          />
          <div className="flex justify-end gap-2 mt-2">
            <button type="button" onClick={onClose} className="bg-gray-300 px-4 py-2 rounded hover:bg-gray-400">Cancel</button>
            <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">{note ? "Update" : "Add"}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
