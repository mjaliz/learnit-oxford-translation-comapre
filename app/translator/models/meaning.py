from pydantic import BaseModel, Field


class Meaning(BaseModel):
    persian_equivalent: list[str] = Field(
        description="This is the field for list of Persian equivalents."
    )
