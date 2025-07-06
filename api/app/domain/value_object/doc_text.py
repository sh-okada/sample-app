from pydantic import Field, RootModel


class DocText(RootModel, frozen=True):
    root: str = Field(..., max_length=5000)
