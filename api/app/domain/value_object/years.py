from pydantic import Field, RootModel


class Years(RootModel, frozen=True):
    root: int = Field(..., min=1, max=40)
