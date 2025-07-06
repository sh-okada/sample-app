from datetime import date
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, Field, SecretStr


class SignUp(BaseModel):
    username: str = Field(..., min_length=2, max_length=8)
    password: SecretStr = Field(..., min_length=8, max_length=100)


class PostProfile(BaseModel):
    joining_date: date = Field(...)
    years: int = Field(...)
    department_id: str = Field(...)
    grade_id: str = Field(...)


class PostDoc(BaseModel):
    title: str = Field(...)
    text: str = Field(...)


class PostArticle(BaseModel):
    title: str = Field(...)
    text: str = Field(...)


class DocIdPathParam(BaseModel):
    doc_id: str = Field(..., min_length=1, max_length=100)


class DocFilterParams(BaseModel):
    page: int = Field(default=1, ge=1, le=1000)
    limit: int = Field(default=5, ge=5, le=100)


class ArticleIdPathParam(BaseModel):
    id: str = Field(..., min_length=1, max_length=100)


class ArticleFilterParams(BaseModel):
    page: int = Field(default=1, ge=1, le=10000)
    limit: int = Field(default=5, ge=5, le=100)


ArticleFilterQuery = Annotated[ArticleFilterParams, Query()]
DocFilterQuery = Annotated[DocFilterParams, Query()]
