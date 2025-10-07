from typing import List

from pydantic import BaseModel

from app.shared import pydantic_fields


class User(BaseModel):
    id: pydantic_fields.UserId
    name: pydantic_fields.UserName


class UserWithAccessToken(BaseModel):
    id: pydantic_fields.UserId
    username: pydantic_fields.UserName
    access_token: pydantic_fields.JWT


class Article(BaseModel):
    id: pydantic_fields.ArticleId
    title: pydantic_fields.ArticleTitle
    text: pydantic_fields.ArticleText
    user: User


class Articles(BaseModel):
    values: List[Article]
    count: pydantic_fields.ArticleCount


class ArticleCount(BaseModel):
    count: pydantic_fields.ArticleCount
