from pydantic import BaseModel

from app.shared import pydantic_fields


class User(BaseModel):
    id: pydantic_fields.UserId
    name: str


class UserWithAccessToken(BaseModel):
    id: pydantic_fields.UserId
    username: pydantic_fields.UserName
    access_token: str


class Article(BaseModel):
    id: pydantic_fields.ArticleId
    title: pydantic_fields.ArticleTitle
    text: pydantic_fields.ArticleText
    user: User


class ArticleCount(BaseModel):
    count: int
