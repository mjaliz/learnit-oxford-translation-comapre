from pydantic import BaseModel, Field


class WordMeaning(BaseModel):
    definitions: list[str]
    prompt1_res1: list[list[str]]
    prompt1_res2: list[list[str]]
    prompt2_res1: list[list[str]]
    prompt2_res2: list[list[str]]
    checked1_res1: list[list[str]]
    checked1_res2: list[list[str]]
    def_res: list[list[str]]
