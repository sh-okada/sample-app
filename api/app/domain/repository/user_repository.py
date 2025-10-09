from typing import Annotated

from fastapi import Depends

from app.domain.entity.liked_article import LikedArticle
from app.domain.entity.user import User
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep
from app.shared import pydantic_fields


class UserRepository:
    def __init__(self, session: SessionDep):
        self.__session = session

    def find_by_id(self, id: pydantic_fields.UserId) -> User | None:
        user = self.__session.get(db_models.User, id)

        if not user:
            return None

        return User(
            id=user.id,
            liked_articles=[
                LikedArticle(
                    id=like.id, article_id=like.article_id, user_id=like.user_id
                )
                for like in user.likes
            ],
        )


UserRepositoryDep = Annotated[UserRepository, Depends()]
