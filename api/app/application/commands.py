from dataclasses import dataclass


@dataclass
class PostDoc:
    title: str
    text: str


@dataclass
class PostArticle:
    title: str
    text: str
    user_id: str


@dataclass(frozen=True)
class GetArticles(frozen=True):
    page: int
    limit: int


@dataclass(frozen=True)
class GetArticle:
    id: str
