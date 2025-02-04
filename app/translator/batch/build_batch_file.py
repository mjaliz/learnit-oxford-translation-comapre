import json
from pathlib import Path
from pydantic import TypeAdapter

from app.translator.batch.models.glossary import Word
from app.translator.batch.models.req import Req, ReqBody, ReqMsg
from app.translator.prompt import system_message_by_def

DATA_DIR = Path(__file__).parent.parent.parent.parent.joinpath("data")


def load_glossary_words() -> list[Word]:
    docs = TypeAdapter(list[Word])
    with open(DATA_DIR.joinpath("dictionary.words_100.json"), "r") as f:
        data = json.loads(f.read())
        words = docs.validate_python(data)
    return words


def build_batch_file():
    words = load_glossary_words()
    reqs = []
    for word in words:
        for item in word.items:
            if item.definition.text.strip() == "":
                continue
            req = Req(
                custom_id=f"{word.id.oid}:{item.id}",
                method="POST",
                url="/v1/chat/completions",
                body=ReqBody(
                    model="gpt-4o",
                    messages=[
                        ReqMsg(role="system", content=system_message_by_def),
                        ReqMsg(
                            role="user",
                            content=f"## Here is the word definition: {item.definition.text}",
                        ),
                    ],
                ),
            )
            reqs.append(req)
    with open("100_words.jsonl", "w") as f:
        for req in reqs:
            f.write(f"{req.model_dump_json()}\n")


if __name__ == "__main__":
    build_batch_file()
