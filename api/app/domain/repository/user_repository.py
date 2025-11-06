import abc

from app.domain.entity.user import User
from app.shared import pydantic_fields


class IUserRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find_by_id(self, id: pydantic_fields.UserId) -> User | None:
        raise NotImplementedError()

    def update(self, user: User):
        raise NotImplementedError()
