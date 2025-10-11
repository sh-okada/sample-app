from typing import Annotated

from fastapi import Depends

from app.domain.entity.liked_article import LikedArticle
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep
from app.shared import pydantic_fields


class LikedArticleRepository:
    def __init__(self, session: SessionDep):
        self.__session = session

    def find_by_id(self, id: pydantic_fields.LikedArticleId) -> LikedArticle | None:
        like = self.__session.get(db_models.Like, id)

        if not like:
            return None

        return LikedArticle(
            id=like.id, article_id=like.article_id, user_id=like.user_id
        )

    def create(self, liked_article: LikedArticle):
        self.__session.add(
            db_models.Like(
                id=liked_article.id,
                user_id=liked_article.user_id,
                article_id=liked_article.article_id,
            )
        )
        self.__session.commit()

    def delete(self, liked_article: LikedArticle):
        like = self.__session.get(db_models.Like, liked_article.id)

        self.__session.delete(like)
        self.__session.commit()


LikedArticleRepositoryDep = Annotated[LikedArticleRepository, Depends()]
