from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class MessageBase(SQLModel):
    user_id: int
    conversation_id: int  # Changed from str to int to match Conversation model
    role: str  # "user" or "assistant"
    content: str


class Message(MessageBase, table=True):
    """
    Represents individual messages within a conversation, storing both user inputs
    and AI responses.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(description="Links message to the owning user")
    conversation_id: int = Field(description="Links message to its parent conversation")  # Changed from str to int
    role: str = Field(description="Indicates whether message is from user or AI")
    content: str = Field(description="The actual message content")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the message was created")


class MessagePublic(MessageBase):
    """Public representation of message without internal fields"""
    id: int
    created_at: datetime