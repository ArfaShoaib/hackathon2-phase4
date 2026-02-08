from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


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
    created_at: datetime
    updated_at: datetime