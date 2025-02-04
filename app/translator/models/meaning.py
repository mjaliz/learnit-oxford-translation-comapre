from pydantic import BaseModel, Field


class Meaning(BaseModel):
    persian_equivalent: list[str] = Field(
        description="This is the field for list of Persian equivalents."
    )


class PesrianEq(BaseModel):
    text: str = Field(description="Text of the persian equivalent")


class Step(BaseModel):
    explanation: str
    persian_eq: PesrianEq


class MeaningReasoning(BaseModel):
    initial_list: list[PesrianEq]
    steps: list[Step]
    final_list: list[PesrianEq]
