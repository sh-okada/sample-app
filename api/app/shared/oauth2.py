from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, PyJWTError

from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep
from app.interface import responses
from app.shared import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(token: TokenDep, session: SessionDep) -> responses.User:
    try:
        token_data = jwt.decode_access_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.get(db_models.User, token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return responses.User(
        id=user.id,
        name=user.name,
    )


CurrentUserDep = Annotated[responses.User, Depends(get_current_user)]
