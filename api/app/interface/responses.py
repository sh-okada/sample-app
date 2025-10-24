from typing import List

from pydantic import BaseModel

from app.shared import pydantic_fields


class Tokens(BaseModel):
    access_token: pydantic_fields.JWT
    refresh_token: pydantic_fields.JWT


class User(BaseModel):
    id: pydantic_fields.UserId
    name: pydantic_fields.UserName


class UserWithToken(Tokens):
    id: pydantic_fields.UserId
    username: pydantic_fields.UserName


class Article(BaseModel):
    id: pydantic_fields.ArticleId
    title: pydantic_fields.ArticleTitle
    text: pydantic_fields.ArticleText
    published_at: pydantic_fields.PublishedAt
    user: User


class Articles(BaseModel):
    values: List[Article]
    count: pydantic_fields.ArticleCount
    total_pages: pydantic_fields.ArticleTotalPages


class Message(BaseModel):
    detail: str
