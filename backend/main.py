from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import jwt

app = FastAPI()

# CORS settings for React frontend
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory "database"
users_db = {}
notes_db = {}

SECRET_KEY = "secret"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ----------------- Schemas -----------------
class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Note(BaseModel):
    id: int
    title: str
    content: str
    owner: str

class NoteCreate(BaseModel):
    title: str
    content: str

# ----------------- Auth Helpers -----------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ----------------- Auth Routes -----------------
@app.post("/auth/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = user.password
    return {"message": "User registered successfully"}

@app.post("/auth/login", response_model=Token)
def login(user: User):
    if users_db.get(user.username) != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# ----------------- Notes Routes -----------------
@app.post("/notes/", response_model=Note)
def create_note(note: NoteCreate, current_user: str = Depends(get_current_user)):
    note_id = len(notes_db) + 1
    new_note = Note(id=note_id, title=note.title, content=note.content, owner=current_user)
    notes_db[note_id] = new_note
    return new_note

@app.get("/notes/", response_model=List[Note])
def get_notes(current_user: str = Depends(get_current_user)):
    return [note for note in notes_db.values() if note.owner == current_user]

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note: NoteCreate, current_user: str = Depends(get_current_user)):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    existing_note = notes_db[note_id]
    if existing_note.owner != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to update this note")
    updated_note = Note(id=note_id, title=note.title, content=note.content, owner=current_user)
    notes_db[note_id] = updated_note
    return updated_note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, current_user: str = Depends(get_current_user)):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    existing_note = notes_db[note_id]
    if existing_note.owner != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    del notes_db[note_id]
    return {"message": "Note deleted successfully"}
