from typing import Annotated

from fastapi import Depends

from app.domain.entity.article import Article
from app.domain.repository.article_repository import IArticleRepository
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep


class ArticleRepository(IArticleRepository):
    def __init__(self, session: SessionDep):
        self.__session = session

    def create(self, article: Article):
        self.__session.add(
            db_models.Article(
                id=str(article.id.root),
                title=article.title.root,
                text=article.text.root,
                user_id=str(article.user_id.root),
            )
        )
        self.__session.commit()


ArticleRepositoryDep = Annotated[ArticleRepository, Depends()]
