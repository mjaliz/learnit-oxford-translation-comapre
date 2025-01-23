from pydantic import BaseModel, Field


class WordMeaning(BaseModel):
    definitions: list[str]
    meaning: list[list[str]]
    meaning_updated: list[list[str]]
