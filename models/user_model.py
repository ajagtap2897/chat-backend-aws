from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: str
    password: str
    profile_pic: str

class ResponseUser(BaseModel):
    id: str
    name: str
    email: str
    profile_pic: str

class CreateUser(BaseModel):
    name: str
    email: str