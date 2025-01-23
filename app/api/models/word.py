from pydantic import BaseModel


class Word(BaseModel):
    text: str
