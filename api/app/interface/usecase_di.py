from typing import Annotated

from fastapi import Depends

from app.application.usecase.like_article_usecase import LikeArticleUseCase
from app.application.usecase.post_article_usecase import PostArticleUseCase
from app.application.usecase.unlike_article_usecase import UnlikeArticleUseCase
from app.infrastructure.db.postgres import SessionDep
from app.infrastructure.repository.article_repository import ArticleRepository
from app.infrastructure.repository.user_repository import UserRepository


def _get_post_article_usecase(session: SessionDep) -> PostArticleUseCase:
    return PostArticleUseCase(ArticleRepository(session))


def _get_like_article_usecase(session: SessionDep):
    return LikeArticleUseCase(
        user_repository=UserRepository(session),
        article_repository=ArticleRepository(session),
    )


def _get_unlike_article_usecase(session: SessionDep):
    return UnlikeArticleUseCase(
        user_repository=UserRepository(session),
        article_repository=ArticleRepository(session),
    )


PostArticleUseCaseDep = Annotated[
    PostArticleUseCase, Depends(_get_post_article_usecase)
]

LikeArticleUseCaseDep = Annotated[
    LikeArticleUseCase, Depends(_get_like_article_usecase)
]

UnlikeArticleUseCaseDep = Annotated[
    UnlikeArticleUseCase, Depends(_get_unlike_article_usecase)
]
