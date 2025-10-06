import re
import uuid
from typing import Annotated

from pydantic import (
    UUID4,
    AfterValidator,
    Field,
    SecretStr,
)

JWT = Annotated[str, Field(..., min_length=1, max_length=500)]
ArticleId = Annotated[UUID4, Field(..., default_factory=uuid.uuid4)]
ArticleTitle = Annotated[str, Field(..., max_length=200)]
ArticleText = Annotated[str, Field(..., max_length=20000)]
UserId = Annotated[UUID4, Field(..., default_factory=uuid.uuid4)]
UserName = Annotated[
    str, Field(..., min_length=2, max_length=8, pattern=r"^[a-zA-Z0-9._-]+$")
]
ArticleCount = Annotated[int, Field(..., ge=0)]
Page = Annotated[int, Field(default=1, ge=1, le=10000)]
Limit = Annotated[int, Field(default=5, ge=5, le=100)]
Q = Annotated[str, Field(default="", max_length=100)]


"""
passwordの正規表現をPydanticで処理しようとすると以下のエラーがでる。
error: look-around, including look-ahead and look-behind, is not supported
このエラーは、Pydanticのregex_engineがrust-regexによるものらしい。

model_config = ConfigDic(regex_engine="python-re")とするとregex_engineをpython-reにできるが、以下のエラーがでる。
pydantic_core._pydantic_core.SchemaError: Error building "chain" validator:

なので、今回はカスタムバリデーターで対応することにした。
"""


def validate_password(v: SecretStr) -> SecretStr:
    password_str = v.get_secret_value()

    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$", password_str):
        raise ValueError(
            "Password must contain at least one lowercase letter, one uppercase letter, and one digit"
        )
    return v


Password = Annotated[
    SecretStr,
    Field(..., min_length=8, max_length=100),
    AfterValidator(validate_password),
]
