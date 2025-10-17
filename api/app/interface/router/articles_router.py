from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4

from app.domain.entity.article import Article
from app.domain.repository.article_repository import ArticleRepositoryDep
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep
from app.interface import queries, requests, responses
from app.shared.oauth2 import CurrentUserDep

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=responses.Articles)
def get_articles(
    article_filter_query: requests.ArticleFilterQuery,
    session: SessionDep,
) -> responses.Articles:
    return queries.get_articles_with_pagination(
        session=session,
        article_filter_params=article_filter_query,
    )


@router.get("/{id}", response_model=responses.Article)
def get_article(id: UUID4, session: SessionDep) -> responses.Article:
    article = session.get(db_models.Article, id)

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found."
        )

    return responses.Article(
        id=article.id,
        title=article.title,
        text=article.text,
        published_at=article.published_at,
        user=responses.User(id=article.user.id, name=article.user.name),
    )


@router.post("", response_model=responses.Message)
def post_article(
    form_data: requests.PostArticle,
    article_repository: ArticleRepositoryDep,
    current_user: CurrentUserDep,
) -> JSONResponse:
    article = Article(
        title=form_data.title,
        text=form_data.text,
        user_id=current_user.id,
    )
    article_repository.create(article)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(
            responses.Message(detail="Article created successfully.")
        ),
    )
