import pytest
from sqlmodel import SQLModel

from app.infrastructure.db.postgres import get_session
from app.infrastructure.db.sqlite import (
    create_mock_db_and_tables,
    engine,
    get_mock_session,
)
from app.main import app


@pytest.fixture(autouse=True)
def use_mock_db():
    app.dependency_overrides[get_session] = get_mock_session
    create_mock_db_and_tables()

    yield

    SQLModel.metadata.drop_all(engine)
    app.dependency_overrides.clear()
