from datetime import datetime, timedelta, timezone

import jwt
from pydantic import BaseModel

from app.shared import config, pydantic_fields

jwt_config = config.JWT()


class TokenData(BaseModel):
    sub: pydantic_fields.UserId
    exp: int


def create_access_token(id: pydantic_fields.UserId) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=jwt_config.jwt_expire_minutes)

    return jwt.encode(
        payload={"sub": str(id), "exp": exp},
        key=jwt_config.jwt_secret_key,
        algorithm=jwt_config.jwt_algorithm,
    )


def create_refresh_token(id: pydantic_fields.UserId) -> str:
    exp = datetime.now(timezone.utc) + timedelta(
        days=jwt_config.refresh_jwt_expire_days
    )

    return jwt.encode(
        payload={"sub": str(id), "exp": exp},
        key=jwt_config.refresh_jwt_secret_key,
        algorithm=jwt_config.refresh_jwt_algorithm,
    )


def decode_access_token(token: str) -> TokenData:
    payload = jwt.decode(
        token,
        key=jwt_config.jwt_secret_key,
        algorithms=[jwt_config.jwt_algorithm],
    )
    return TokenData(**payload)


def decode_refresh_token(token: str) -> TokenData:
    payload = jwt.decode(
        token,
        key=jwt_config.refresh_jwt_secret_key,
        algorithms=[jwt_config.refresh_jwt_algorithm],
    )

    return TokenData(**payload)
