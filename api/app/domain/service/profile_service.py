import abc
import uuid


class IProfileService(abc.ABC):
    @abc.abstractmethod
    def exists(self, user_id: uuid.UUID) -> bool:
        raise NotImplementedError()
