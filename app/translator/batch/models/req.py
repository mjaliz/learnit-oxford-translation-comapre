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

res_format_checking = {
    "type": "json_schema",
    "json_schema": {
        "name": "check_results",
        "schema": {
            "type": "object",
            "properties": {
                "selected_equivalents": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                },
            },
            "required": ["selected_equivalents"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}


res_format_udpated = {
    "type": "json_schema",
    "json_schema": {
        "name": "meaning_reasoning",
        "schema": {
            "type": "object",
            "properties": {
                "initial_list": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text of the persian equivalent",
                            }
                        },
                        "required": ["text"],
                        "additionalProperties": False,
                    },
                },
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "explanation": {"type": "string"},
                            "persian_eq": {
                                "type": "object",
                                "properties": {
                                    "text": {
                                        "type": "string",
                                        "description": "Text of the persian equivalent",
                                    }
                                },
                                "required": ["text"],
                                "additionalProperties": False,
                            },
                            "is_choosed": {"type": "boolean"},
                        },
                        "required": ["explanation", "persian_eq", "is_choosed"],
                        "additionalProperties": False,
                    },
                },
                "final_list": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text of the persian equivalent",
                            }
                        },
                        "required": ["text"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["initial_list", "steps", "final_list"],
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
    response_format: dict = Field(default=res_format_checking)


class Req(BaseModel):
    custom_id: str
    method: str
    url: str
    body: ReqBody
