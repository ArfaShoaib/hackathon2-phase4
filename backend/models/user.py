from sqlmodel import SQLModel, Field # type: ignore
from datetime import datetime, timezone
from typing import Optional


class User(SQLModel, table=True):
    """
    User model representing registered application users.
    """
    __tablename__ = "user"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))