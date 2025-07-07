from typing import Annotated, List

from fastapi import Depends
from sqlmodel import func, select

from app.application import commands, query_models
from app.application.query_service.article_query_service import IArticleQueryService
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep


class ArticleQueryService(IArticleQueryService):
    def __init__(self, session: SessionDep):
        self.__session = session

    def get_article_count(self) -> query_models.ArticleCount:
        statement = select(func.count(db_models.Article.id))
        count = self.__session.exec(statement).one()

        return query_models.ArticleCount(count)

    def get_article(
        self, get_article_command: commands.GetArticle
    ) -> query_models.Article:
        article = self.__session.get_one(db_models.Article, get_article_command.id)

        return query_models.Article(
            article.id,
            article.title,
            article.text,
            query_models.User(article.user.id, article.user.name),
        )

    def get_articles(
        self,
        get_article_command: commands.GetArticles,
    ) -> List[query_models.Article]:
        offset = (get_article_command.page - 1) * get_article_command.limit
        statement = (
            select(db_models.Article).offset(offset).limit(get_article_command.limit)
        )
        articles = self.__session.exec(statement).all()

        return [
            query_models.Article(
                article.id,
                article.title,
                article.text,
                query_models.User(article.user.id, article.user.name),
            )
            for article in articles
        ]


ArticleQueryServiceDep = Annotated[ArticleQueryService, Depends()]
