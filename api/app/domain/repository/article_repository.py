from typing import Annotated

from fastapi import Depends

from app.domain.entity.article import Article
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep


class ArticleRepository:
    def __init__(self, session: SessionDep):
        self.__session = session

    def create(self, article: Article):
        self.__session.add(
            db_models.Article(
                id=article.id,
                title=article.title,
                text=article.text,
                user_id=article.user_id,
            )
        )
        self.__session.commit()


ArticleRepositoryDep = Annotated[ArticleRepository, Depends()]
