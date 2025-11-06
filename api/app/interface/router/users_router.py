from fastapi import APIRouter, HTTPException, status
from sqlmodel import and_, select

from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep
from app.interface import queries, requests, responses
from app.interface.usecase_di import LikeArticleUseCaseDep, UnlikeArticleUseCaseDep
from app.shared import pydantic_fields
from app.shared.oauth2 import CurrentUserDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=responses.User)
def read_users_me(
    current_user: CurrentUserDep,
) -> responses.User:
    return current_user


@router.get("/me/articles", response_model=responses.Articles)
def get_my_articles(
    article_filter_query: requests.ArticleFilterQuery,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> responses.Articles:
    return queries.get_articles_with_pagination(
        session=session,
        article_filter_params=article_filter_query,
        where_clauses=[db_models.Article.user_id == current_user.id],
    )


@router.get("/{id}/articles", response_model=responses.Articles)
def get_articles_by_user_id(
    id: pydantic_fields.UserId,
    article_filter_query: requests.ArticleFilterQuery,
    session: SessionDep,
) -> responses.Articles:
    return queries.get_articles_with_pagination(
        session=session,
        article_filter_params=article_filter_query,
        where_clauses=[db_models.Article.user_id == id],
    )


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
    like_article_usecase: LikeArticleUseCaseDep,
    current_user: CurrentUserDep,
) -> responses.Message:
    like_article_usecase.execute(
        user_id=current_user.id, article_id=form_data.article_id
    )

    return responses.Message(detail="Article liked successfully.")


@router.delete("/me/liked-articles/{id}", response_model=responses.Message)
def unlike_article(
    id: pydantic_fields.ArticleId,
    unlike_article_usecase: UnlikeArticleUseCaseDep,
    current_user: CurrentUserDep,
) -> responses.Message:
    unlike_article_usecase.execute(user_id=current_user.id, article_id=id)

    return responses.Message(detail="article unliked successfully.")
