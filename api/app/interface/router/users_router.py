from fastapi import APIRouter

from app.interface import responses
from app.shared.oauth2 import CurrentUserDep

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/me", response_model=responses.User)
def read_users_me(
    current_user: CurrentUserDep,
):
    return current_user
