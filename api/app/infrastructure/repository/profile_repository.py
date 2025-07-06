import uuid
from typing import Annotated

from fastapi import Depends

from app.domain.entity.profile import Profile
from app.domain.repository.profile_repository import IProfileRepository
from app.domain.value_object.department_id import DepartmentId
from app.domain.value_object.grade_id import GradeId
from app.domain.value_object.joining_date import JoiningDate
from app.domain.value_object.user_id import UserId
from app.domain.value_object.years import Years
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep


class ProfileRepository(IProfileRepository):
    def __init__(self, session: SessionDep):
        self.__session = session

    def find(self, user_id: UserId) -> Profile | None:
        user_profile = self.__session.get(db_models.UserProfile, str(user_id.root))

        if user_profile is None:
            return None

        return Profile(
            user_id=UserId(uuid.UUID(user_profile.user_id)),
            joining_date=JoiningDate(user_profile.joining_date),
            years=Years(user_profile.years),
            department_id=DepartmentId(user_profile.department_id),
            grade_id=GradeId(user_profile.grade_id),
        )

    def create(self, profile: Profile):
        user_profile = db_models.UserProfile(
            user_id=str(profile.user_id.root),
            years=profile.years.root,
            joining_date=profile.joining_date.root,
            grade_id=str(profile.grade_id.root),
            department_id=str(profile.department_id.root),
        )

        self.__session.add(user_profile)
        self.__session.commit()


ProfileRepositoryDep = Annotated[ProfileRepository, Depends()]
