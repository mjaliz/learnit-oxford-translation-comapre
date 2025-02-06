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
    words = []
    meaning = []
    definitons = []
    for d in tqdm(defs):
        try:
            meaning.append(
                join_res(
                    await generate_meaning_updated(
                        openai_client,
                        word,
                        d["pos"],
                        d["definition"],
                    )
                )
            )
            definitons.append(d["definition"])
            words.append(word)
        except Exception as e:
            logger.error(e)
            continue
    df = pd.DataFrame({"word": words, "definition": definitons, "meaning": meaning})
    df.to_csv(f"{word}3.csv", index=False, encoding="utf-8")


async def generate_word_meaning_service(word: str) -> WordMeaning:
    openai_client = AsyncOpenAIClient()
    glossary_word = await fetch_word(word)

    if glossary_word is None:
        return None
    definitions = [
        item.definition.text
        for item in glossary_word.items
        if item.definition.text != ""
    ]
    prompt1_res1 = []
    prompt1_res2 = []
    for definition in tqdm(definitions):
        res1, res2 = await generate_meaning(openai_client, word, definition)
        prompt1_res1.append(res1.message.parsed.persian_equivalent)
        prompt1_res2.append(res2.message.parsed.persian_equivalent)

    prompt2_res1 = []
    prompt2_res2 = []
    for definition in tqdm(definitions):
        res1, res2 = await generate_meaning_updated(openai_client, word, definition)
        prompt2_res1.append(res1.message.parsed.persian_equivalent)
        prompt2_res2.append(res2.message.parsed.persian_equivalent)

    def_res1 = []
    for definition in tqdm(definitions):
        res1 = await generate_meaning_by_def(openai_client, definition)
        def_res1.append(res1[0].message.parsed.persian_equivalent)

    checked1_res1 = []
    checked1_res2 = []
    for i in range(len(definitions)):
        res1, res2 = await check_meanings(
            openai_client,
            word,
            definitions[i],
            [prompt1_res1[i], prompt2_res1[i]],
        )
        checked1_res1.append(res1.message.parsed.persian_equivalent)
        checked1_res2.append(res2.message.parsed.persian_equivalent)

    return WordMeaning(
        definitions=definitions,
        prompt1_res1=prompt1_res1,
        prompt1_res2=prompt1_res2,
        prompt2_res1=prompt2_res1,
        prompt2_res2=prompt2_res2,
        checked1_res1=checked1_res1,
        checked1_res2=checked1_res2,
        def_res=def_res1,
    )


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
    asyncio.run(cot_word_meaning("take"))
