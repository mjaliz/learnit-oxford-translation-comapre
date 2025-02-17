import json
from pathlib import Path
from loguru import logger
from pydantic import TypeAdapter
import pandas as pd
from app.glossary.fetch_word import extract_defs_and_pos
from app.translator.batch.models.glossary import Word
from app.translator.batch.models.req import Req, ReqBody, ReqMsg
from app.translator.meaning_generator import (
    build_prompt,
    build_prompt_updated,
    build_prmopt_check_res,
)
from app.translator.prompt import (
    system_message_meaning_steps,
    system_message,
    system_message_combine_res,
)

DATA_DIR = Path(__file__).parent.parent.parent.parent.joinpath("data")


def load_glossary_words() -> list[Word]:
    docs = TypeAdapter(list[Word])
    with open(DATA_DIR.joinpath("dictionary.words.json"), "r") as f:
        data = json.loads(f.read())
        words = docs.validate_python(data)
    return words


def build_batch_file():
    words = load_glossary_words()
    cids = []
    with open(
        Path(__file__).parent.joinpath("data").joinpath("error_100_000-2.jsonl"), "r"
    ) as f:
        for line in f.readlines():
            err = json.loads(line)
            cids.append(err["custom_id"])
    with open(
        Path(__file__).parent.joinpath("data").joinpath("error_100_000_to_end-2.jsonl"),
        "r",
    ) as f:
        for line in f.readlines():
            err = json.loads(line)
            cids.append(err["custom_id"])
    reqs = []
    for word in words:
        defs = extract_defs_and_pos(word)
        for d in defs:
            custom_id = f"{word.id.oid}:{d["id"]}"
            if custom_id not in cids:
                logger.info("res already exits")
                continue
            req = Req(
                custom_id=custom_id,
                method="POST",
                url="/v1/chat/completions",
                body=ReqBody(
                    model="gpt-4o-2024-11-20",
                    messages=[ReqMsg(role="system", content=system_message_combine_res)]
                    + [
                        ReqMsg(**msg)
                        for msg in build_prompt_updated(
                            word.word, d["pos"], d["definition"]
                        )
                    ],
                ),
            )
            reqs.append(req)
    with open("words_failed-2.jsonl", "w") as f:
        for req in reqs:
            f.write(f"{req.model_dump_json()}\n")


def build_check_batch_file():
    words = pd.read_csv("combined_res.csv")
    reqs = []
    for word in words.iterrows():
        custom_id = word["custom_id"]
        req = Req(
            custom_id=custom_id,
            method="POST",
            url="/v1/chat/completions",
            body=ReqBody(
                model="gpt-4o-2024-11-20",
                messages=[ReqMsg(role="system", content=system_message_combine_res)]
                + [
                    ReqMsg(**msg)
                    for msg in build_prmopt_check_res(
                        word["word"],
                        word["definition"],
                        [word["prompt1"].split(", "), word["prompt2"].split(", ")],
                    )
                ],
            ),
        )
        reqs.append(req)
    with open("words_failed-2.jsonl", "w") as f:
        for req in reqs:
            f.write(f"{req.model_dump_json()}\n")


if __name__ == "__main__":
    build_batch_file()
