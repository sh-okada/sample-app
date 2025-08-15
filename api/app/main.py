from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from app.infrastructure.db.postgres import create_db_and_tables
from app.interface.router import articles_router, auth_router, users_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router.router)
api_router.include_router(users_router.router)
api_router.include_router(articles_router.router)

app.include_router(api_router)


# @app.exception_handler(jwt.PyJWTError)
# def py_jwt_error_handler(request: Request, exc: jwt.PyJWTError):
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
