from typing import Annotated

from fastapi import Depends

from app.domain.service.profile_service import IProfileService
from app.domain.value_object.user_id import UserId
from app.infrastructure.repository.profile_repository import ProfileRepositoryDep


class ProfileService(IProfileService):
    def __init__(self, profile_repository: ProfileRepositoryDep):
        self.__profile_repository = profile_repository

    def exists(self, user_id: UserId) -> bool:
        profile = self.__profile_repository.find(user_id)

        return profile is not None


ProfileServiceDep = Annotated[ProfileService, Depends()]
