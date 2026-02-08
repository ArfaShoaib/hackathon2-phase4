from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """
    Task model representing individual todo items with ownership relationships.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1024)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)