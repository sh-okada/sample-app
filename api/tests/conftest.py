import uuid
from datetime import datetime
from typing import Callable, TypeAlias, TypeVar

import pytest
from freezegun import freeze_time
from pydantic import BaseModel, RootModel
from pydantic.fields import FieldInfo
from pytest_mock import MockerFixture
from sqlmodel import SQLModel

from app.infrastructure.db.postgres import get_session
from app.infrastructure.db.sqlite import (
    create_mock_db_and_tables,
    engine,
    get_mock_session,
)
from app.main import app
from app.shared import jwt


def valid_jwt_token(id: str) -> str:
    return jwt.create_access_token(id)


@freeze_time(datetime(2025, 1, 1, 0, 0, 0))
def expired_jwt_token(id: str) -> str:
    return jwt.create_access_token(id)


T_RootModel = TypeVar("T_RootModel", bound=RootModel)
T_BaseModel = TypeVar("T_BaseModel", bound=BaseModel)
MockUUID: TypeAlias = Callable[
    [type[T_RootModel] | type[T_BaseModel], FieldInfo, str | uuid.UUID], None
]


@pytest.fixture
def mock_uuid(mocker: MockerFixture) -> MockUUID:
    def func(
        model: type[T_RootModel] | type[T_BaseModel],
        model_field: dict[str, FieldInfo],
        value: str | uuid.UUID,
    ):
        mocker.patch.object(model_field, "default_factory", lambda: value)
        model.model_rebuild(force=True)

    return func


@pytest.fixture(autouse=True)
def use_mock_db():
    app.dependency_overrides[get_session] = get_mock_session
    create_mock_db_and_tables()

    yield

    SQLModel.metadata.drop_all(engine)
    app.dependency_overrides.clear()
