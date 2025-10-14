from fastapi import APIRouter, HTTPException, status
from sqlmodel import and_, select

from app.domain.exceptions import (
    ArticleAlreadyLikedError,
    ArticleAlreadyUnLikedError,
    MyPostArticleError,
)
from app.domain.repository.article_repository import ArticleRepositoryDep
from app.domain.repository.user_repository import UserRepositoryDep
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep
from app.interface import requests, responses
from app.shared import pydantic_fields
from app.shared.oauth2 import CurrentUserDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=responses.User)
def read_users_me(
    current_user: CurrentUserDep,
) -> responses.User:
    return current_user


@router.get("/me/liked-articles/{id}", response_model=responses.Article)
def get_liked_article(
    id: pydantic_fields.ArticleId,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> responses.Article:
    statement = select(db_models.Like).where(
        and_(
            db_models.Like.user_id == current_user.id,
            db_models.Like.article_id == id,
        )
    )
    liked_article = session.exec(statement).one_or_none()
    if not liked_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Liked article not found."
        )

    return responses.Article(
        id=liked_article.article.id,
        title=liked_article.article.title,
        text=liked_article.article.text,
        published_at=liked_article.article.published_at,
        user=responses.User(
            id=liked_article.article.user.id, name=liked_article.article.user.name
        ),
    )


@router.post("/me/liked-articles", response_model=responses.Message)
def like_article(
    form_data: requests.LikeArticle,
    user_repository: UserRepositoryDep,
    article_repository: ArticleRepositoryDep,
    current_user: CurrentUserDep,
) -> responses.Message:
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


@router.delete("/me/liked-articles/{id}", response_model=responses.Message)
def unlike_article(
    id: pydantic_fields.ArticleId,
    user_repository: UserRepositoryDep,
    article_repository: ArticleRepositoryDep,
    current_user: CurrentUserDep,
) -> responses.Message:
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

    return responses.Message(detail="article unliked successfully.")
