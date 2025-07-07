import abc
from typing import List

from app.application import commands, query_models


class IArticleQueryService(abc.ABC):
    @abc.abstractmethod
    def get_article_count(self) -> query_models.ArticleCount:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_article(get_article_command: commands.GetArticle) -> query_models.Article:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_articles(
        get_article_command: commands.GetArticles,
    ) -> List[query_models.Article]:
        raise NotImplementedError()
