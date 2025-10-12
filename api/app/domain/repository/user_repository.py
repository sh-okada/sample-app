from typing import Annotated

from fastapi import Depends

from app.domain.entity.article import Article
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
                Article(
                    id=like.article.id,
                    title=like.article.title,
                    text=like.article.text,
                    user_id=like.article.user_id,
                    published_at=like.article.published_at,
                )
                for like in user.likes
            ],
        )

    def update(self, user: User):
        update_user = self.__session.get(db_models.User, user.id)

        likes = [
            db_models.Like(
                user_id=user.id,
                article_id=liked_article.id,
            )
            for liked_article in user.liked_articles
        ]
        update_user.likes = likes
        self.__session.commit()


UserRepositoryDep = Annotated[UserRepository, Depends()]
