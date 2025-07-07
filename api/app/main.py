from contextlib import asynccontextmanager

import jwt
from fastapi import APIRouter, FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.infrastructure.db.postgres import create_db_and_tables
from app.interface.router.articles_router import articles_router
from app.interface.router.auth_router import auth_router
from app.interface.router.users_router import users_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(articles_router)

app.include_router(api_router)


@app.exception_handler(ValidationError)
def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=None)


@app.exception_handler(jwt.PyJWTError)
def py_jwt_error_handler(request: Request, exc: jwt.PyJWTError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=None)
