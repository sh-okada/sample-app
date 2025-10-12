import uuid
from datetime import datetime
from typing import List

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)

    articles: List["Article"] = Relationship(back_populates="user", cascade_delete=True)
    likes: List["Like"] = Relationship(back_populates="user", cascade_delete=True)


class Article(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(nullable=False)
    text: str = Field(nullable=False)
    published_at: datetime = Field(default_factory=datetime.now, nullable=False)
    user_id: uuid.UUID = Field(nullable=False, foreign_key="user.id")

    user: "User" = Relationship(back_populates="articles")
    likes: List["Like"] = Relationship(back_populates="article", cascade_delete=True)


class Like(SQLModel, table=True):
    user_id: uuid.UUID = Field(primary_key=True, foreign_key="user.id")
    article_id: uuid.UUID = Field(primary_key=True, foreign_key="article.id")

    user: "User" = Relationship(back_populates="likes")
    article: "Article" = Relationship(back_populates="likes")
