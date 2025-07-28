from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

engine = create_engine("sqlite:///./sqlite.db")


def get_mock_session():
    with Session(engine) as session:
        yield session


def create_mock_db_and_tables():
    SQLModel.metadata.create_all(engine)


MockSessionDep = Annotated[Session, Depends(get_mock_session)]
