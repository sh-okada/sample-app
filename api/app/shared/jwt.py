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
    exp = datetime.now(timezone.utc) + timedelta(minutes=jwt_config.JWT_EXPIRE_MINUTES)

    return jwt.encode(
        payload=TokenData(id, exp).__dict__,
        key=jwt_config.JWT_SECRET_KEY,
        algorithm=jwt_config.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> TokenData:
    payload = jwt.decode(
        token,
        key=jwt_config.JWT_SECRET_KEY,
        algorithms=[jwt_config.JWT_ALGORITHM],
    )
    return TokenData(**payload)
