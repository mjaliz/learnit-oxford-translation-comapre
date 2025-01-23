from pydantic import BaseModel, Field


class Group(BaseModel):
    id: int
    lemma_id: str
    part_of_speeches: list[str]
    item_ids: list[str]


class Definition(BaseModel):
    text: str


class WordItem(BaseModel):
    id: str
    word_text: str | None = Field(default=None)
    definition: Definition


class Word(BaseModel):
    text: str
    groups: list[Group]
    items: list[WordItem]
