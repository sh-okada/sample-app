from typing import List

from fastapi import APIRouter, Response, status
from pydantic import UUID4
from sqlmodel import func, select

from app.domain.entity.article import Article
from app.domain.repository.article_repository import ArticleRepositoryDep
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep
from app.interface import requests, responses
from app.shared.oauth2 import CurrentUserDep

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/count", response_model=responses.ArticleCount)
def get_article_count(session: SessionDep):
    statement = select(func.count(db_models.Article.id))
    count = session.exec(statement).one()

    return responses.ArticleCount(count=count)


@router.get("", response_model=List[responses.Article])
def get_articles(
    article_filter_query: requests.ArticleFilterQuery,
    session: SessionDep,
):
    offset = (article_filter_query.page - 1) * article_filter_query.limit
    statement = (
        select(db_models.Article).offset(offset).limit(article_filter_query.limit)
    )
    articles = session.exec(statement).all()

    return [
        responses.Article(
            id=article.id,
            title=article.title,
            text=article.text,
            user=responses.User(id=article.user.id, name=article.user.name),
        )
        for article in articles
    ]


@router.get("/{id}", response_model=responses.Article)
def get_article(id: UUID4, session: SessionDep):
    article = session.get_one(db_models.Article, id)

    return responses.Article(
        id=article.id,
        title=article.title,
        text=article.text,
        user=responses.User(id=article.user.id, name=article.user.name),
    )


@router.post("")
def post_article(
    form_data: requests.PostArticle,
    article_repository: ArticleRepositoryDep,
    current_user: CurrentUserDep,
):
    article = Article(
        title=form_data.title,
        text=form_data.text,
        user_id=current_user.id,
    )
    article_repository.create(article)

    return Response(status_code=status.HTTP_201_CREATED)
