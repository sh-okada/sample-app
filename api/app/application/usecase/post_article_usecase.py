from app.domain.entity.article import Article
from app.domain.repository.article_repository import IArticleRepository
from app.shared import pydantic_fields


class PostArticleUseCase:
    def __init__(
        self,
        article_repository: IArticleRepository,
    ):
        self.__article_repository = article_repository

    def execute(
        self,
        title: pydantic_fields.ArticleTitle,
        text: pydantic_fields.ArticleText,
        user_id: pydantic_fields.UserId,
    ):
        article = Article(
            title=title,
            text=text,
            user_id=user_id,
        )

        self.__article_repository.create(article)
