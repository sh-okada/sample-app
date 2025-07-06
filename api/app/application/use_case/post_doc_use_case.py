from typing import Annotated

from fastapi import Depends

from app.application import commands
from app.domain.entity.doc import Doc
from app.domain.value_object.doc_id import DocId
from app.domain.value_object.doc_text import DocText
from app.domain.value_object.doc_title import DocTitle
from app.infrastructure.repository.doc_repository import DocRepositoryDep


class PostDocUseCase:
    def __init__(self, doc_repository: DocRepositoryDep):
        self.__doc_repository = doc_repository

    def execute(self, post_doc_command: commands.PostDoc):
        doc = Doc(
            id=DocId(),
            title=DocTitle(post_doc_command.title),
            text=DocText(post_doc_command.text),
        )

        self.__doc_repository.create(doc)


PostDocUseCaseDep = Annotated[PostDocUseCase, Depends()]
