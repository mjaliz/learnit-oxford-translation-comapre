from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class ObjectIdModel(BaseModel):
    # Represents the MongoDB _id field which is a dict with key "$oid"
    oid: str = Field(..., alias="$oid")


class DateModel(BaseModel):
    # Represents a MongoDB date field which is a dict with key "$date"
    date: datetime = Field(..., alias="$date")


class Phonetic(BaseModel):
    accent: str
    text: str
    audio: str


class Group(BaseModel):
    id: int
    lemma_id: str
    part_of_speeches: List[str] | None
    phonetics: List[Phonetic] | None
    item_ids: List[str]


class Definition(BaseModel):
    text: str


class Translation(BaseModel):
    language: str
    texts: List[str]


class Example(BaseModel):
    text: str
    translations: list[Translation]


class Item(BaseModel):
    id: str
    creator_id: int
    deleted_by_id: int
    definition: Definition
    translations: List[Translation] | None
    examples: List[Example] | None


class Word(BaseModel):
    id: ObjectIdModel = Field(..., alias="_id")
    created_at: DateModel
    updated_at: DateModel
    state: str
    creator_id: int
    encoded_word: str
    word: str
    groups: List[Group] | None
    items: List[Item]

    class Config:
        # Allow population by field name or alias.
        allow_population_by_field_name = True
        # For nested models to correctly use aliases in dict representation.
        json_encoders = {datetime: lambda dt: dt.isoformat()}
