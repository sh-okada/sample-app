import uuid
from typing import List

from sqlmodel import Field, Relationship, SQLModel


def generate_uuid4() -> str:
    return str(uuid.uuid4())


class User(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid4, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)

    articles: List["Article"] = Relationship(back_populates="user")


class Article(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid4, primary_key=True)
    title: str = Field(nullable=False)
    text: str = Field(nullable=False)
    user_id: str = Field(nullable=False, foreign_key="user.id")

    user: "User" = Relationship(back_populates="articles")
