import uuid
from datetime import datetime
from typing import TypeVar

import pytest
from freezegun import freeze_time
from pydantic import RootModel
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


def valid_jwt_token(id: str):
    return jwt.create_access_token(id)


@freeze_time(datetime(2025, 1, 1, 0, 0, 0))
def expired_jwt_token(id: str):
    return jwt.create_access_token(id)


T_RootModel = TypeVar("T_RootModel", bound=RootModel)


@pytest.fixture
def mock_uuid(mocker: MockerFixture):
    def func(model: type[T_RootModel], value: str):
        mocker.patch.object(
            model.model_fields["root"], "default_factory", lambda: uuid.UUID(value)
        )
        model.model_rebuild(force=True)

    return func


@pytest.fixture(autouse=True)
def use_mock_db():
    app.dependency_overrides[get_session] = get_mock_session
    create_mock_db_and_tables()

    yield

    SQLModel.metadata.drop_all(engine)
    app.dependency_overrides.clear()
