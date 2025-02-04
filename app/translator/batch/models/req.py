from pydantic import BaseModel, Field

res_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "meaning",
        "schema": {
            "type": "object",
            "properties": {
                "persian_equivalents": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                },
            },
            "required": ["persian_equivalents"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}


class ReqMsg(BaseModel):
    role: str
    content: str


class ReqBody(BaseModel):
    model: str
    messages: list[ReqMsg]
    response_format: dict = Field(default=res_format)


class Req(BaseModel):
    custom_id: str
    method: str
    url: str
    body: ReqBody
