from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError, PyJWTError
from sqlmodel import select

from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep
from app.interface import requests, responses
from app.shared import jwt, password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=responses.UserWithToken)
def login(
    form_data: requests.OAuth2PasswordRequest, session: SessionDep
) -> responses.UserWithToken:
    statement = select(db_models.User).where(
        db_models.User.name == form_data.username,
    )
    user = session.exec(statement).one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password.",
        )

    if not password.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password.",
        )

    access_token = jwt.create_access_token(user.id)
    refresh_token = jwt.create_refresh_token(user.id)

    return responses.UserWithToken(
        id=user.id,
        username=user.name,
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/signup", response_model=responses.Message)
def signUp(form_data: requests.SignUp, session: SessionDep) -> JSONResponse:
    statement = select(db_models.User).where(
        db_models.User.name == form_data.username,
    )
    user = session.exec(statement).one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already in use.",
        )

    user = db_models.User(
        name=form_data.username,
        password=password.get_password_hash(form_data.password.get_secret_value()),
    )

    session.add(user)
    session.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(
            responses.Message(detail="User created successfully.")
        ),
    )


@router.post("/tokens/refresh", response_model=responses.Tokens)
def refresh_tokens(
    form_data: requests.RefreshToken, session: SessionDep
) -> responses.Tokens:
    try:
        token_data = jwt.decode_refresh_token(form_data.refresh_token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired.",
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token.",
        )

    user = session.get(db_models.User, token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    access_token = jwt.create_access_token(user.id)
    refresh_token = jwt.create_refresh_token(user.id)

    return responses.Tokens(
        access_token=access_token,
        refresh_token=refresh_token,
    )
