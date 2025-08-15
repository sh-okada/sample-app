import uuid
from typing import List

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)

    articles: List["Article"] = Relationship(back_populates="user")


class Article(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(nullable=False)
    text: str = Field(nullable=False)
    user_id: uuid.UUID = Field(nullable=False, foreign_key="user.id")

    user: "User" = Relationship(back_populates="articles")
