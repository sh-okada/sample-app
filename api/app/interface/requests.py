from typing import Annotated

from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.shared import pydantic_fields


class SignUp(BaseModel):
    username: pydantic_fields.UserName
    password: pydantic_fields.Password


class PostArticle(BaseModel):
    title: pydantic_fields.ArticleTitle
    text: pydantic_fields.ArticleText


class ArticleFilterParams(BaseModel):
    page: pydantic_fields.Page
    limit: pydantic_fields.Limit


OAuth2PasswordRequest = Annotated[OAuth2PasswordRequestForm, Depends()]
ArticleFilterQuery = Annotated[ArticleFilterParams, Query()]
