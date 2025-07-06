from pydantic import Field, RootModel


class ArticleText(RootModel, frozen=True):
    root: str = Field(..., max_length=20000)
