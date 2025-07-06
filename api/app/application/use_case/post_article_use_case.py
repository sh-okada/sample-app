import uuid
from typing import Annotated

from fastapi import Depends

from app.application import commands
from app.domain.entity.article import Article
from app.domain.value_object.article_id import ArticleId
from app.domain.value_object.article_text import ArticleText
from app.domain.value_object.article_title import ArticleTitle
from app.domain.value_object.user_id import UserId
from app.infrastructure.repository.article_repository import ArticleRepositoryDep


class PostArticleUseCase:
    def __init__(self, article_repository: ArticleRepositoryDep):
        self.__article_repository = article_repository

    def execute(self, post_article_command: commands.PostArticle):
        article = Article(
            id=ArticleId,
            title=ArticleTitle(post_article_command.title),
            text=ArticleText(post_article_command.text),
            user_id=UserId(uuid.UUID(post_article_command.user_id)),
        )

        self.__article_repository.create(article)


PostArticleUseCaseDep = Annotated[PostArticleUseCase, Depends()]
