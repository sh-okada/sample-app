from fastapi import APIRouter, HTTPException, Response, status

from app.domain.exceptions import (
    ArticleAlreadyLikedError,
    ArticleAlreadyUnLikedError,
    MyPostArticleError,
)
from app.domain.repository.article_repository import ArticleRepositoryDep
from app.domain.repository.user_repository import UserRepositoryDep
from app.interface import requests, responses
from app.shared import pydantic_fields
from app.shared.oauth2 import CurrentUserDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=responses.User)
def read_users_me(
    current_user: CurrentUserDep,
) -> responses.User:
    return current_user


@router.post("/me/liked-articles", response_model=responses.Message)
def like_article(
    form_data: requests.LikeArticle,
    user_repository: UserRepositoryDep,
    article_repository: ArticleRepositoryDep,
    current_user: CurrentUserDep,
) -> Response:
    user = user_repository.find_by_id(current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    article = article_repository.find_by_id(form_data.article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found."
        )

    try:
        user.like(article)
    except MyPostArticleError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot like own article.",
        )
    except ArticleAlreadyLikedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already liked this article.",
        )

    user_repository.update(user)

    return responses.Message(detail="Article liked successfully.")


@router.delete("/me/liked-articles/{id}")
def unlike_article(
    id: pydantic_fields.ArticleId,
    user_repository: UserRepositoryDep,
    article_repository: ArticleRepositoryDep,
    current_user: CurrentUserDep,
):
    user = user_repository.find_by_id(current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    article = article_repository.find_by_id(id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found."
        )

    try:
        user.unlike(article)
    except ArticleAlreadyUnLikedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Have not liked this article.",
        )

    user_repository.update(user)

    return Response(status_code=status.HTTP_200_OK)
