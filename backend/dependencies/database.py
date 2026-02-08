from typing import Generator
from dotenv import load_dotenv # type: ignore
import os
from sqlmodel import Session # type: ignore

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the database engine
# Handle different database types appropriately
def create_engine_func():
    from sqlmodel import create_engine
    
    if DATABASE_URL.startswith("postgresql://"):
        # For PostgreSQL, we need psycopg2
        try:
            return create_engine(DATABASE_URL, echo=False)
        except ImportError:
            print("PostgreSQL driver not found. Please install psycopg2-binary or switch to SQLite.")
            print("Falling back to SQLite database...")
            sqlite_url = "sqlite:///./todo_app.db"
            return create_engine(sqlite_url, echo=False)
    elif DATABASE_URL.startswith("sqlite://"):
        # For SQLite
        return create_engine(DATABASE_URL, echo=False)
    else:
        # Default to SQLite if URL format is unrecognized
        print(f"Unrecognized database URL format: {DATABASE_URL}. Using SQLite instead.")
        sqlite_url = "sqlite:///./todo_app.db"
        return create_engine(sqlite_url, echo=False)

engine = create_engine_func()


def get_session():
    """
    Dependency function to get a database session.
    """
    from sqlmodel import Session
    with Session(engine) as session:
        print(f"DEBUG: Database session created successfully for engine: {engine}")
        yield session


def get_session_context():
    """
    Context manager function to get a database session.
    """
    from sqlmodel import Session
    return Session(engine)


def create_db_and_tables():
    """
    Create database tables.
    """
    # Import models in the correct order to avoid circular dependencies
    from models.user import User
    from models.task import Task
    from models.conversation import Conversation
    from models.message import Message
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)