import asyncio
import time
from fastapi.background import P
from loguru import logger
import pandas as pd
from tqdm import tqdm
from app.glossary.fetch_word import extract_defs_and_pos, fetch_word
from app.llm.openai_client import AsyncOpenAIClient
from app.services.models.word_meaning import WordMeaning
from app.translator.meaning_generator import (
    check_meanings,
    generate_meaning,
    generate_meaning_by_def,
    generate_meaning_updated,
    join_res,
)


async def cot_word_meaning(word: str):
    openai_client = AsyncOpenAIClient()
    glossary_word = await fetch_word(word)

    if glossary_word is None:
        return None

    defs = extract_defs_and_pos(glossary_word)
    words = [word] * len(defs)
    meaning = await asyncio.gather(
        *[generate_meaning(openai_client, word, d["definition"]) for d in defs]
    )
    meaning_updated = await asyncio.gather(
        *[
            generate_meaning_updated(openai_client, word, d["pos"], d["definition"])
            for d in defs
        ]
    )
    checked = await asyncio.gather(
        *[
            check_meanings(
                openai_client,
                word,
                defs[i]["definition"],
                [meaning[i].persian_equivalent, meaning_updated[i].final_list],
            )
            for i in range(len(defs))
        ]
    )
    df = pd.DataFrame(
        {
            "word": words,
            "definition": [d["definition"] for d in defs],
            "meaning": [", ".join(m.persian_equivalent) for m in meaning],
            "meaning_updated": [
                ", ".join([p.text for p in mu.final_list]) for mu in meaning_updated
            ],
            "checked": [
                ", ".join([sp.text for sp in s.selected_equivalents]) for s in checked
            ],
        }
    )
    df.to_csv(f"{word}.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    # word = [
    #     "can",
    # ]
    # words = []
    # definitions = []
    # prompt1_res1 = []
    # prompt1_res2 = []
    # prompt2_res1 = []
    # prompt2_res2 = []
    # checked1_res1 = []
    # checked1_res2 = []
    # def_res = []
    # for w in word:
    #     meaning = asyncio.run(generate_word_meaning_service(w))
    #     words.extend([w] * len(meaning.definitions))
    #     definitions.extend(meaning.definitions)
    #     prompt1_res1.extend([", ".join(m) for m in meaning.prompt1_res1])
    #     prompt1_res2.extend([", ".join(mu) for mu in meaning.prompt1_res2])
    #     prompt2_res1.extend([", ".join(mu) for mu in meaning.prompt2_res1])
    #     prompt2_res2.extend([", ".join(mu) for mu in meaning.prompt2_res2])
    #     checked1_res1.extend([", ".join(mu) for mu in meaning.checked1_res1])
    #     checked1_res2.extend([", ".join(mu) for mu in meaning.checked1_res2])
    #     def_res.extend([", ".join(c) for c in meaning.def_res])

    # df = pd.DataFrame(
    #     {
    #         "word": words,
    #         "defintion": definitions,
    #         "prompt1_res1": prompt1_res1,
    #         "prompt2_res1": prompt2_res1,
    #         "checked1": checked1_res1,
    #     }
    # )
    # df.to_csv("can.csv", index=None)

    # print(meaning)
    asyncio.run(cot_word_meaning("off"))
