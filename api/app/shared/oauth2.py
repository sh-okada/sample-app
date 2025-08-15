from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep
from app.interface import responses
from app.shared import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(token: TokenDep, session: SessionDep):
    token_data = jwt.decode_access_token(token)
    user = session.get(db_models.User, token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return responses.User(
        id=user.id,
        name=user.name,
    )


CurrentUserDep = Annotated[responses.User, Depends(get_current_user)]
