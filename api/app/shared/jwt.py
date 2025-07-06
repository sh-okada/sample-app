from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt

from app.shared import env


@dataclass
class TokenData:
    sub: str
    exp: datetime


def create_access_token(id: str):
    exp = datetime.now(timezone.utc) + timedelta(minutes=env.JWT.EXPIRE_MINUTES)

    return jwt.encode(
        payload=TokenData(id, exp).__dict__,
        key=env.JWT.SECRET_KEY,
        algorithm=env.JWT.ALGORITHM,
    )


def decode_access_token(token: str) -> TokenData:
    payload = jwt.decode(
        token,
        key=env.JWT.SECRET_KEY,
        algorithms=[env.JWT.ALGORITHM],
    )
    return TokenData(**payload)
