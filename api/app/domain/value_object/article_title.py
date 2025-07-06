from pydantic import Field, RootModel


class ArticleTitle(RootModel, frozen=True):
    root: str = Field(..., max_length=200)
