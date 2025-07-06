from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str
    name: str


@dataclass(frozen=True)
class Article:
    id: str
    title: str
    text: str


@dataclass(frozen=True)
class ArticleCount:
    count: int
