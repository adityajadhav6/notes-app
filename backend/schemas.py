from pydantic import BaseModel

# For user signup
class UserCreate(BaseModel):
    username: str
    password: str

# For creating a note
class NoteCreate(BaseModel):
    title: str
    content: str

# For showing a note in response
class NoteOut(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True  # allows conversion from ORM model

# For JWT tokens
class Token(BaseModel):
    access_token: str
    token_type: str

# For simple responses like {"message": "Success"}
class Message(BaseModel):
    message: str
