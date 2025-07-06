import abc

from app.domain.entity.profile import Profile
from app.domain.value_object.user_id import UserId


class IProfileRepository(abc.ABC):
    @abc.abstractmethod
    def find(self, user_id: UserId) -> Profile | None:
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, profile: Profile):
        raise NotImplementedError()
