import abc

from app.domain.entity.article import Article
from app.shared import pydantic_fields


class IArticleRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find_by_id(self, article_id: pydantic_fields.ArticleId) -> Article | None:
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, article: Article) -> Article:
        raise NotImplementedError()
