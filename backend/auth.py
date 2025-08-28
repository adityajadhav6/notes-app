from datetime import datetime, timedelta
from jose import JWTError, jwt          # For encoding/decoding JWT tokens
from typing import Optional  
from passlib.context import CryptContext  # For password hashing
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer  # Handles token extraction
from sqlalchemy.orm import Session
from database import SessionLocal
import models

# Secret key & JWT settings
SECRET_KEY = "supersecretkey"  # ⚠️ should be hidden in environment variables in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Tells FastAPI where to expect login token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Database dependency - opens & closes a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hash a plain password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify user’s password during login
def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

# Create a JWT access token with expiry
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Extract current user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode JWT and extract username
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Find user in DB
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
