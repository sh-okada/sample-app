from fastapi import APIRouter, HTTPException, Response, status

from app.domain.entity.liked_article import LikedArticle
from app.domain.repository.user_repository import UserRepositoryDep
from app.shared import pydantic_fields
from app.shared.oauth2 import CurrentUserDep

router = APIRouter(prefix="/likes", tags=["likes"])


@router.post("/{article_id}")
def like(
    article_id: pydantic_fields.ArticleId,
    user_repository: UserRepositoryDep,
    current_user: CurrentUserDep,
) -> Response:
    user = user_repository.find_by_id(current_user.id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found."
        )

    user.like(LikedArticle(article_id=article_id, user_id=user.id))

    return Response(status_code=status.HTTP_201_CREATED)
