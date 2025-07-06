from typing import Annotated

from fastapi import Depends

from app.domain.entity.doc import Doc
from app.domain.repository.doc_repository import IDocRepository
from app.infrastructure.db import db_models
from app.infrastructure.db.postgres import SessionDep


class DocRepository(IDocRepository):
    def __init__(self, session: SessionDep):
        self.__session = session

    def create(self, doc: Doc):
        doc_db_model = db_models.Doc(
            id=str(doc.id.root), title=doc.title.root, text=doc.text.root
        )

        self.__session.add(doc_db_model)
        self.__session.commit()


DocRepositoryDep = Annotated[DocRepository, Depends()]
