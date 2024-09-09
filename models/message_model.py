from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import date, datetime, time, timedelta

class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    sender: str
    receiver: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

class CreateMessageRequest(BaseModel):
    sender: str
    receiver: str
    content: str