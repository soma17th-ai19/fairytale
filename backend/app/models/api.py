from __future__ import annotations

from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    message: str = "Endpoint is not implemented yet."


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)


class ChildCreateRequest(BaseModel):
    name: str
    age: int = Field(ge=0, le=18)
    personality: str
    favorite_character: str


class StoryGenerateRequest(BaseModel):
    child_id: str
    situation: str
    lesson: str
    mood: str
    category: str
