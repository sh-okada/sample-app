from typing import List

from pydantic import BaseModel

from app.domain.entity.liked_article import LikedArticle
from app.shared import pydantic_fields


class User(BaseModel, frozen=True):
    id: pydantic_fields.UserId
    liked_articles: List[LikedArticle]
