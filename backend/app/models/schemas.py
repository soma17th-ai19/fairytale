from __future__ import annotations

from datetime import date
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class PersonKind(str, Enum):
    family = "가족"
    friend = "친구"
    teacher = "선생님"
    neighbor = "이웃"
    other = "기타"


class Person(BaseModel):
    name: str = Field(..., description="인물 이름")
    relation: str = Field(..., description="아이와의 관계 (예: 엄마, 짝꿍, 담임선생님)")
    kind: PersonKind = Field(PersonKind.other, description="관계 분류")
    closeness: Optional[int] = Field(
        None, ge=1, le=5,
        description="아이가 느끼는 친밀도 (1=어색함, 5=아주 가까움)",
    )
    role_today: Optional[str] = Field(None, description="오늘 일기 속에서의 역할 (예: 함께 놀았음, 갈등 상대, 도와줌)")
    traits: list[str] = Field(default_factory=list, description="특징/성격 키워드")
    note: Optional[str] = Field(None, description="추가 설명")


class StoryRequest(BaseModel):
    diary_date: date = Field(..., description="일기 날짜")
    diary: str = Field(..., description="해당 날짜의 일기 본문")
    people: list[Person] = Field(default_factory=list, description="주변 인물 관계")


class Story(BaseModel):
    title: str
    body: str


class StoryResponse(BaseModel):
    story: Story
