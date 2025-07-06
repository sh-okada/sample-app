from pydantic import BaseModel

from app.domain.value_object.department_id import DepartmentId
from app.domain.value_object.grade_id import GradeId
from app.domain.value_object.joining_date import JoiningDate
from app.domain.value_object.user_id import UserId
from app.domain.value_object.years import Years


class Profile(BaseModel, frozen=True):
    user_id: UserId
    joining_date: JoiningDate
    years: Years
    department_id: DepartmentId
    grade_id: GradeId
