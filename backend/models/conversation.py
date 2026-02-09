from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from pydantic import field_serializer
from typing import Union


class ConversationBase(SQLModel):
    user_id: int


class Conversation(ConversationBase, table=True):
    """
    Represents a chat session between a user and the AI assistant,
    containing metadata about the conversation.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the conversation started")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the conversation was last updated")


class ConversationPublic(ConversationBase):
    """Public representation of conversation without internal fields"""
    id: int
    created_at: Union[datetime, str]
    updated_at: Union[datetime, str]
    
    @field_serializer('created_at')
    def serialize_created_at(self, value: Union[datetime, str]):
        if isinstance(value, datetime):
            return value.isoformat()
        return value
    
    @field_serializer('updated_at')
    def serialize_updated_at(self, value: Union[datetime, str]):
        if isinstance(value, datetime):
            return value.isoformat()
        return value