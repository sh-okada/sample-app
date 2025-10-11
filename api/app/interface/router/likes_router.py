from fastapi import APIRouter, HTTPException, Response, status

from app.domain.exceptions import ArticleAlreadyLikedError, MyPostArticleError
from app.domain.repository.article_repository import ArticleRepositoryDep
from app.domain.repository.liked_article_repository import LikedArticleRepositoryDep
from app.domain.repository.user_repository import UserRepositoryDep
from app.interface import responses
from app.shared import pydantic_fields
from app.shared.oauth2 import CurrentUserDep

router = APIRouter(prefix="/likes", tags=["likes"])


@router.post("")
def like_article(
    form_data: responses.LikeArticle,
    user_repository: UserRepositoryDep,
    article_repository: ArticleRepositoryDep,
    liked_article_repository: LikedArticleRepositoryDep,
    current_user: CurrentUserDep,
) -> Response:
    user = user_repository.find_by_id(current_user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    article = article_repository.find_by_id(form_data.article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found."
        )

    try:
        liked_article = user.like(article)
        liked_article_repository.create(liked_article)
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

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/{id}")
def unlike_article(
    id: pydantic_fields.LikedArticleId,
    liked_article_repository: LikedArticleRepositoryDep,
    _: CurrentUserDep,
):
    liked_article = liked_article_repository.find_by_id(id)
    if not liked_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Liked article not found."
        )

    liked_article_repository.delete(liked_article)

    return Response(status_code=status.HTTP_200_OK)
