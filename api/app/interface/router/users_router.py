from fastapi import APIRouter

from app.interface import responses
from app.shared.oauth2 import CurrentUserDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=responses.User)
def read_users_me(
    current_user: CurrentUserDep,
):
    return current_user
