from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str


class UserWithAccessToken(User):
    access_token: str


class ArticleUser(BaseModel):
    id: str
    name: str


class Article(BaseModel):
    id: str
    title: str
    text: str
    user: ArticleUser


class ArticleCount(BaseModel):
    count: int
