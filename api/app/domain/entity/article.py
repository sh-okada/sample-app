from pydantic import BaseModel

from app.domain.value_object.article_id import ArticleId
from app.domain.value_object.article_text import ArticleText
from app.domain.value_object.article_title import ArticleTitle
from app.domain.value_object.user_id import UserId


class Article(BaseModel, frozen=True):
    id: ArticleId
    title: ArticleTitle
    text: ArticleText
    user_id: UserId
