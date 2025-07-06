from pydantic import BaseModel

from app.domain.value_object.doc_id import DocId
from app.domain.value_object.doc_text import DocText
from app.domain.value_object.doc_title import DocTitle


class Doc(BaseModel, frozen=True):
    id: DocId
    title: DocTitle
    text: DocText
