from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import jwt

# ----------------- App Setup -----------------
app = FastAPI()

# Allow frontend (React running on localhost:5173) to talk to backend
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # only allow this frontend
    allow_credentials=True,
    allow_methods=["*"],    # allow GET, POST, PUT, DELETE
    allow_headers=["*"],    # allow all headers
)

# ----------------- "Fake Database" -----------------
# These are just Python dictionaries (not a real DB)
# In real apps, you’d replace with SQL or MongoDB
users_db = {}   # store username: password
notes_db = {}   # store note_id: Note object

# ----------------- JWT Setup -----------------
SECRET_KEY = "secret"      # secret for signing tokens
ALGORITHM = "HS256"        # algorithm used for JWT

# OAuth2PasswordBearer expects the user to send token in "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ----------------- Schemas (Data Models) -----------------
# These make sure requests/responses have correct structure

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
    owner: str  # which user created this note

class NoteCreate(BaseModel):
    title: str
    content: str

# ----------------- Helper: Get Current User -----------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    This function runs whenever a route requires authentication.
    It:
      - Takes the JWT token from request header
      - Decodes it using SECRET_KEY
      - Returns the username inside the token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # subject = username
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ----------------- Auth Routes -----------------
@app.post("/auth/register")
def register(user: User):
    """
    Register new user.
    - If username already exists → error
    - Otherwise, save username & password to users_db
    """
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = user.password
    return {"message": "User registered successfully"}

@app.post("/auth/login", response_model=Token)
def login(user: User):
    """
    Login route.
    - Checks if username/password match
    - If correct → create JWT token and return to user
    """
    if users_db.get(user.username) != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# ----------------- Notes Routes -----------------
@app.post("/notes/", response_model=Note)
def create_note(note: NoteCreate, current_user: str = Depends(get_current_user)):
    """
    Create a new note for logged-in user.
    - Note gets unique ID
    - Owner = current_user
    - Saves note in notes_db
    """
    note_id = len(notes_db) + 1
    new_note = Note(id=note_id, title=note.title, content=note.content, owner=current_user)
    notes_db[note_id] = new_note
    return new_note

@app.get("/notes/", response_model=List[Note])
def get_notes(current_user: str = Depends(get_current_user)):
    """
    Get all notes of the logged-in user.
    - Filters notes_db so user only sees their own notes
    """
    return [note for note in notes_db.values() if note.owner == current_user]

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note: NoteCreate, current_user: str = Depends(get_current_user)):
    """
    Update a note.
    - Check if note exists
    - Check if current user is the owner
    - Replace old note with updated content
    """
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
    """
    Delete a note.
    - Check if note exists
    - Check if current user is the owner
    - Remove it from notes_db
    """
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    existing_note = notes_db[note_id]
    if existing_note.owner != current_user:
        raise HTTPException(status_code=403, detail="Not authorized to delete this note")
    del notes_db[note_id]
    return {"message": "Note deleted successfully"}
