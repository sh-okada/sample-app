from typing import List

from pydantic import BaseModel

from app.domain.entity.article import Article
from app.domain.entity.liked_article import LikedArticle
from app.domain.exceptions import ArticleAlreadyLikedError, MyPostArticleError
from app.shared import pydantic_fields


class User(BaseModel, frozen=True):
    id: pydantic_fields.UserId
    liked_articles: List[LikedArticle]

    def like(self, article: Article) -> LikedArticle:
        if article.user_id == self.id:
            raise MyPostArticleError()

        article_ids = [
            liked_article.article_id for liked_article in self.liked_articles
        ]
        if article.id in article_ids:
            raise ArticleAlreadyLikedError()

        return LikedArticle(article_id=article.id, user_id=self.id)
