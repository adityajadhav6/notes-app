from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define where our database is located (SQLite in this case)
DATABASE_URL = "sqlite:///./notes.db"

# Create a connection engine to interact with the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal is what we’ll use to talk to the database in our code
# autocommit=False -> we control when to commit changes
# autoflush=False -> prevents automatic DB flushes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all our models (tables) will inherit from
Base = declarative_base()
