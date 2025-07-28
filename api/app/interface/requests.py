import re
from typing import Annotated

from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, SecretStr, field_validator


class SignUp(BaseModel):
    username: str = Field(..., min_length=2, max_length=8, pattern=r"^[a-zA-Z0-9._-]+$")
    password: SecretStr = Field(..., min_length=8, max_length=100)

    """
    passwordの正規表現をPydanticで処理しようとすると以下のエラーがでる。
    error: look-around, including look-ahead and look-behind, is not supported
    このエラーは、Pydanticのregex_engineがrust-regexによるものらしい。

    model_config = ConfigDic(regex_engine="python-re")とするとregex_engineをpython-reにできるが、以下のエラーがでる。
    pydantic_core._pydantic_core.SchemaError: Error building "chain" validator:

    なので、今回はカスタムバリデーターで対応することにした。
    """

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        password_str = v.get_secret_value()

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$", password_str):
            raise ValueError(
                "Password must contain at least one lowercase letter, one uppercase letter, and one digit"
            )
        return v


class PostArticle(BaseModel):
    title: str = Field(...)
    text: str = Field(...)


class ArticleIdPathParam(BaseModel):
    id: str = Field(..., min_length=2, max_length=100)


class ArticleFilterParams(BaseModel):
    page: int = Field(default=1, ge=1, le=10000)
    limit: int = Field(default=5, ge=5, le=100)


OAuth2PasswordRequest = Annotated[OAuth2PasswordRequestForm, Depends()]
ArticleFilterQuery = Annotated[ArticleFilterParams, Query()]
