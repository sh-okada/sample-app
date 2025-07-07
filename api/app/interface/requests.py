from typing import Annotated

from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, SecretStr


class SignUp(BaseModel):
    username: str = Field(..., min_length=2, max_length=8)
    password: SecretStr = Field(..., min_length=8, max_length=100)


class PostArticle(BaseModel):
    title: str = Field(...)
    text: str = Field(...)


class ArticleIdPathParam(BaseModel):
    id: str = Field(..., min_length=1, max_length=100)


class ArticleFilterParams(BaseModel):
    page: int = Field(default=1, ge=1, le=10000)
    limit: int = Field(default=5, ge=5, le=100)


OAuth2PasswordRequest = Annotated[OAuth2PasswordRequestForm, Depends()]
ArticleFilterQuery = Annotated[ArticleFilterParams, Query()]
