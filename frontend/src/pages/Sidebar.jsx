import React from "react";
import { useNavigate } from "react-router-dom";

export default function Sidebar({ username }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="w-64 bg-gray-800 text-white h-screen p-6 flex flex-col justify-between">
      <div>
        <h2 className="text-2xl font-bold mb-6">Notes App</h2>
        <p className="mb-4">Hello, <span className="font-semibold">{username}</span>!</p>
        <ul className="flex flex-col gap-2">
          <li>
            <button onClick={handleLogout} className="w-full text-left px-4 py-2 rounded hover:bg-gray-700 transition">
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  );
}
