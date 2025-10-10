from typing import Annotated

from fastapi import Depends

from app.domain.entity.liked_article import LikedArticle
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep


class LikedArticleRepository:
    def __init__(self, session: SessionDep):
        self.__session = session

    def create(self, liked_article: LikedArticle):
        self.__session.add(
            db_models.Like(
                id=liked_article.id,
                user_id=liked_article.user_id,
                article_id=liked_article.article_id,
            )
        )
        self.__session.commit()


LikedArticleRepositoryDep = Annotated[LikedArticleRepository, Depends()]
