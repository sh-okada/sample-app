from fastapi import HTTPException, status

from app.domain.exceptions import ArticleAlreadyLikedError, MyPostArticleError
from app.domain.repository.article_repository import IArticleRepository
from app.domain.repository.user_repository import IUserRepository
from app.shared import pydantic_fields


class LikeArticleUseCase:
    def __init__(
        self, user_repository: IUserRepository, article_repository: IArticleRepository
    ):
        self.__user_repository = user_repository
        self.__article_repository = article_repository

    def execute(
        self, user_id: pydantic_fields.UserId, article_id: pydantic_fields.ArticleId
    ):
        user = self.__user_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        article = self.__article_repository.find_by_id(article_id)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Article not found."
            )

        try:
            user.like(article)
        except MyPostArticleError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot like own article.",
            )
        except ArticleAlreadyLikedError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already liked this article.",
            )

        self.__user_repository.update(user)
