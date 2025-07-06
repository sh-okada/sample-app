import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.application import commands
from app.domain.entity.profile import Profile
from app.domain.value_object.department_id import DepartmentId
from app.domain.value_object.grade_id import GradeId
from app.domain.value_object.joining_date import JoiningDate
from app.domain.value_object.user_id import UserId
from app.domain.value_object.years import Years
from app.infrastructure.repository.profile_repository import ProfileRepositoryDep
from app.infrastructure.service.profile_service import ProfileServiceDep


class PostProfileUseCase:
    def __init__(
        self,
        profile_repository: ProfileRepositoryDep,
        profile_service: ProfileServiceDep,
    ):
        self.__profile_repository = profile_repository
        self.__profile_service = profile_service

    def execute(self, post_profile_command: commands.PostProfile):
        if self.__profile_service.exists(
            UserId(uuid.UUID(post_profile_command.user_id))
        ):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        profile = Profile(
            user_id=UserId(uuid.UUID(post_profile_command.user_id)),
            joining_date=JoiningDate(post_profile_command.joining_date),
            years=Years(post_profile_command.years),
            department_id=DepartmentId(uuid.UUID(post_profile_command.department_id)),
            grade_id=GradeId(uuid.UUID(post_profile_command.grade_id)),
        )

        self.__profile_repository.create(profile)


PostProfileUseCaseDep = Annotated[PostProfileUseCase, Depends()]
