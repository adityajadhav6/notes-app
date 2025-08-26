# React + FastAPI Notes App

## Project Description
A full-stack Notes application with user authentication. Users can register, login, create, update, view, and delete their notes. The backend is built using **FastAPI** and the frontend uses **React with Vite and Tailwind CSS**. JWT (JSON Web Tokens) is used to secure API endpoints.

---

## Features

### Backend
- User registration (`POST /auth/register`)
- User login (`POST /auth/login`) → returns JWT token
- Notes CRUD operations:
  - `GET /notes/` → Fetch all notes for the current user
  - `POST /notes/` → Create a new note
  - `PUT /notes/{id}` → Update a note
  - `DELETE /notes/{id}` → Delete a note
- Authentication using JWT
- In-memory or SQLite database

### Frontend
- Login and Register pages
- NotesList page to display all notes
- NoteForm for creating and editing notes
- Delete notes functionality
- JWT stored in `localStorage` and sent with `Authorization` header
- Fully responsive and simple UI using Tailwind CSS

---

## Project Structure

### Backend
backend/
├── main.py                  # FastAPI app entrypoint
├── database.py              # SQLAlchemy engine, session, Base
├── models.py                # SQLAlchemy models (User, Note)
├── auth.py                  # Password hashing, JWT creation, user auth
├── schemas.py               # Pydantic schemas for requests/responses
├── requirements.txt         # Python dependencies
└── notes.db                 # SQLite database (if used)

### Frontend
frontend/
├── package.json
├── vite.config.js
├── node_modules/            # Auto-generated, do not upload
├── public/                  # Optional static files
├── src/
│   ├── main.jsx             # App entrypoint
│   ├── App.jsx              # Routes & PrivateRoute component
│   ├── api/
│   │   └── axiosInstance.js # Axios instance with JWT interceptor
│   ├── pages/
│      ├── Login.jsx
│      ├── Register.jsx
│      └── NotesList.jsx
│   
└── tailwind.config.js
