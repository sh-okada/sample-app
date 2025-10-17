from typing import List

from sqlmodel import Session, and_, desc, func, select

from app.infrastructure.db import db_models
from app.interface import requests, responses


def get_articles_with_pagination(
    session: Session,
    article_filter_params: requests.ArticleFilterParams,
    where_clauses: List[bool] = [],
) -> responses.Articles:
    # 空文字検索はパフォーマンスを低下させる可能性があるため、キーワードが指定された場合のみフィルターにかける
    if article_filter_params.q:
        where_clauses.append(db_models.Article.title.contains(article_filter_params.q))

    offset = (article_filter_params.page - 1) * article_filter_params.limit
    statement = (
        select(db_models.Article)
        .order_by(desc(db_models.Article.published_at))
        .offset(offset)
        .limit(article_filter_params.limit)
    )
    if where_clauses:
        statement = statement.where(and_(*where_clauses))

    articles = session.exec(statement).all()

    statement = select(func.count(db_models.Article.id))
    if where_clauses:
        statement = statement.where(and_(*where_clauses))

    count = session.exec(statement).one()

    total_pages = (
        (count + article_filter_params.limit - 1) // article_filter_params.limit
        if count > 0
        else 0
    )

    return responses.Articles(
        values=[
            responses.Article(
                id=article.id,
                title=article.title,
                text=article.text,
                published_at=article.published_at,
                user=responses.User(id=article.user.id, name=article.user.name),
            )
            for article in articles
        ],
        count=count,
        total_pages=total_pages,
    )
