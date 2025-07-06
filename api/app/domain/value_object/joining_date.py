from datetime import date, datetime

from pydantic import Field, RootModel, field_validator


class JoiningDate(RootModel, frozen=True):
    root: date = Field(...)

    @field_validator("root")
    def is_past_or_today(cls, v: date):
        if v > datetime.now().date():
            raise ValueError("The date must be before the current date")
        return v
