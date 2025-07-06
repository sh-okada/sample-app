import abc

from app.domain.entity.doc import Doc


class IDocRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, doc: Doc):
        raise NotImplementedError()
