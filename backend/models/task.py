from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from pydantic import field_serializer
from typing import Union


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
    
    @field_serializer('created_at')
    def serialize_created_at(self, value: Union[datetime, str]):
        if isinstance(value, datetime):
            return value.isoformat()
        return value
    
    @field_serializer('updated_at')
    def serialize_updated_at(self, value: Union[datetime, str, None]):
        if isinstance(value, datetime):
            return value.isoformat()
        return value