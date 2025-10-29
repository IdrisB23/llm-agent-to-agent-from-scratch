"""A message model for inter-agent communication."""


import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class MetaData(BaseModel):
    """Metadata for a message."""
    intent: Optional[int] = Field(None, description="Intent of the message.")
    conversation_id: Optional[list[str]] = Field(None, description="Conversation ID of the message.")


class Message(BaseModel):
    """A message exchanged between agents."""
    type: str = Field(..., description="The type of the message.")
    sender: str = Field(..., description="The identifier of the sender agent.")
    recipient: str = Field(..., description="The identifier of the recipient agent.")
    content: str = Field(..., description="The content of the message.")
    timestamp: Optional[datetime.datetime] = Field(None, description="The time the message was sent.")
    metadata: Optional[MetaData] = Field(None, description="Additional metadata for the message.")

    # content can be of arbitrary length
    # model_config = ConfigDict(str_max_length=10)