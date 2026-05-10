from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field
from pydantic import ConfigDict, EmailStr


class MessageResponse(BaseModel):
    message: str = "Endpoint is not implemented yet."


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class TokenPayload(BaseModel):
    sub: str
    email: EmailStr
    type: str
    exp: int
    iat: int


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


class StoryGenerateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    body: str
    lesson: str
    image_url: str | None = None
    audio_url: str | None = None
    created_at: datetime
