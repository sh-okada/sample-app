from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt

from app.shared import config

jwt_config = config.JWT()


@dataclass
class TokenData:
    sub: str
    exp: datetime


def create_access_token(id: str):
    exp = datetime.now(timezone.utc) + timedelta(minutes=jwt_config.jwt_expire_minutes)

    return jwt.encode(
        payload=TokenData(id, exp).__dict__,
        key=jwt_config.jwt_secret_key,
        algorithm=jwt_config.jwt_algorithm,
    )


def decode_access_token(token: str) -> TokenData:
    payload = jwt.decode(
        token,
        key=jwt_config.jwt_secret_key,
        algorithms=[jwt_config.jwt_algorithm],
    )
    return TokenData(**payload)
