from pydantic import BaseModel

# -------- User Schemas --------
class UserCreate(BaseModel):
    username: str
    password: str

# -------- Note Schemas --------
class NoteCreate(BaseModel):
    title: str
    content: str

class NoteOut(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True

# -------- Auth Schemas --------
class Token(BaseModel):
    access_token: str
    token_type: str

# -------- General Schemas --------
class Message(BaseModel):
    message: str
