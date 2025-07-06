from pydantic import Field, RootModel


class DocTitle(RootModel, frozen=True):
    root: str = Field(..., max_length=200)
