from dataclasses import dataclass


@dataclass
class PostArticle:
    title: str
    text: str
    user_id: str


@dataclass(frozen=True)
class GetArticles:
    page: int
    limit: int


@dataclass(frozen=True)
class GetArticle:
    id: str
