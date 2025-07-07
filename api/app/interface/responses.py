from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str


class UserWithAccessToken(User):
    id: str
    username: str
    access_token: str


class Article(BaseModel):
    id: str
    title: str
    text: str
    user: User


class ArticleCount(BaseModel):
    count: int
