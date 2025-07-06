import uuid

from pydantic import UUID4, Field, RootModel


class UserId(RootModel, frozen=True):
    root: UUID4 = Field(..., default_factory=uuid.uuid4)
