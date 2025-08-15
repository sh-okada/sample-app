from pydantic import BaseModel

from app.shared import pydantic_fields


class Article(BaseModel, frozen=True):
    id: pydantic_fields.ArticleId
    title: pydantic_fields.ArticleTitle
    text: pydantic_fields.ArticleText
    user_id: pydantic_fields.UserId
