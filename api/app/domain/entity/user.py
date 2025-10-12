from typing import List

from pydantic import BaseModel

from app.domain.entity.article import Article
from app.domain.exceptions import (
    ArticleAlreadyLikedError,
    ArticleAlreadyUnLikedError,
    MyPostArticleError,
)
from app.shared import pydantic_fields


class User(BaseModel, frozen=True):
    id: pydantic_fields.UserId
    liked_articles: List[Article]

    def like(self, article: Article):
        if article.user_id == self.id:
            raise MyPostArticleError()

        if article in self.liked_articles:
            raise ArticleAlreadyLikedError()

        self.liked_articles.append(article)

    def unlike(self, article: Article):
        if article not in self.liked_articles:
            raise ArticleAlreadyUnLikedError()

        self.liked_articles.remove(article)
