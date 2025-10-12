from typing import Annotated

from fastapi import Depends

from app.domain.entity.article import Article
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep
from app.shared import pydantic_fields


class ArticleRepository:
    def __init__(self, session: SessionDep):
        self.__session = session

    def find_by_id(self, article_id: pydantic_fields.ArticleId) -> Article | None:
        article = self.__session.get(db_models.Article, article_id)
        if article is None:
            return None

        return Article(
            id=article.id,
            title=article.title,
            text=article.text,
            user_id=article.user_id,
            published_at=article.published_at,
        )

    def create(self, article: Article) -> Article:
        self.__session.add(
            db_models.Article(
                id=article.id,
                title=article.title,
                text=article.text,
                user_id=article.user_id,
                published_at=article.published_at,
            )
        )
        self.__session.commit()

        return article


ArticleRepositoryDep = Annotated[ArticleRepository, Depends()]
