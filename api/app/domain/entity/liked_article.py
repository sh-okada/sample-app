from pydantic import BaseModel

from app.shared import pydantic_fields


class LikedArticle(BaseModel, frozen=True):
    id: pydantic_fields.LikedArticleId
    article_id: pydantic_fields.ArticleId
    user_id: pydantic_fields.UserId
