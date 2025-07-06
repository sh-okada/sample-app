import abc

from app.domain.entity.article import Article


class IArticleRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, article: Article):
        raise NotImplementedError()
