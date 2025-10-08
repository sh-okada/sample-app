from fastapi import APIRouter, HTTPException, Response, status
from pydantic import UUID4
from sqlmodel import func, select

from app.domain.entity.article import Article
from app.domain.repository.article_repository import ArticleRepositoryDep
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep
from app.interface import requests, responses
from app.shared.oauth2 import CurrentUserDep

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=responses.Articles)
def get_articles(
    article_filter_query: requests.ArticleFilterQuery,
    session: SessionDep,
) -> responses.Articles:
    # キーワード検索は空文字検索の可能性があり得るため、キーワードが指定された場合のみフィルターにかける
    search_query = (
        [db_models.Article.title.contains(article_filter_query.q)]
        if article_filter_query.q
        else []
    )

    offset = (article_filter_query.page - 1) * article_filter_query.limit
    statement = (
        select(db_models.Article)
        .where(*search_query)
        .offset(offset)
        .limit(article_filter_query.limit)
    )
    articles = session.exec(statement).all()

    count = session.exec(
        select(func.count(db_models.Article.id)).where(*search_query)
    ).one()

    total_pages = (
        (count + article_filter_query.limit - 1) // article_filter_query.limit
        if count > 0
        else 0
    )

    return responses.Articles(
        values=[
            responses.Article(
                id=article.id,
                title=article.title,
                text=article.text,
                user=responses.User(id=article.user.id, name=article.user.name),
            )
            for article in articles
        ],
        count=count,
        total_pages=total_pages,
    )


@router.get("/{id}", response_model=responses.Article)
def get_article(id: UUID4, session: SessionDep) -> responses.Article:
    article = session.get(db_models.Article, id)

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

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
) -> Response:
    article = Article(
        title=form_data.title,
        text=form_data.text,
        user_id=current_user.id,
    )
    article_repository.create(article)

    return Response(status_code=status.HTTP_201_CREATED)
