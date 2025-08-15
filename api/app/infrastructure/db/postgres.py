from typing import Annotated, Any, Generator

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from app.shared import config

db_config = config.DB()

engine = create_engine(
    f"postgresql://{db_config.db_user}:{db_config.db_password}@{db_config.db_host}:{db_config.db_port}/{db_config.db_name}",
)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        try:
            yield session
        except:
            session.rollback()
            raise


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


SessionDep = Annotated[Session, Depends(get_session)]
