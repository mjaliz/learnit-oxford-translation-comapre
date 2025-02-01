import asyncio
import time
import pandas as pd
from tqdm import tqdm
from app.glossary.fetch_word import fetch_word
from app.llm.openai_client import AsyncOpenAIClient
from app.services.models.word_meaning import WordMeaning
from app.translator.meaning_generator import (
    check_meanings,
    generate_meaning,
    generate_meaning_updated,
)


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
    meaining_res = []
    for definition in tqdm(definitions):
        meaining_res.append(await generate_meaning(openai_client, word, definition))
        time.sleep(10)

    meaning_updated_res = []
    for definition in tqdm(definitions):
        meaning_updated_res.append(
            await generate_meaning_updated(openai_client, word, definition)
        )
        time.sleep(10)

    checked = []
    for i in range(len(definitions)):
        checked.append(
            await check_meanings(
                openai_client,
                word,
                definitions[i],
                [meaining_res[i], meaning_updated_res[i]],
            )
        )
        time.sleep(10)

    return WordMeaning(
        definitions=definitions,
        meaning=meaining_res,
        meaning_updated=meaning_updated_res,
        checked=checked,
    )


if __name__ == "__main__":
    word = [
        "tie",
        # "suit",
        # "wearing",
        "match",
        # "progress",
        # "kick",
        "primaeval",
        "take",
        "go",
        "place",
        # "figure",
        "represent",
        "guard",
        "aggressive",
        "develop",
        "land",
        "company",
        # "heavily",
        "bear",
        "turn",
    ]
    words = []
    definitions = []
    prompt1 = []
    prompt2 = []
    checked = []
    for w in word:
        meaning = asyncio.run(generate_word_meaning_service(w))
        words.extend([w] * len(meaning.definitions))
        definitions.extend(meaning.definitions)
        prompt1.extend([", ".join(m) for m in meaning.meaning])
        prompt2.extend([", ".join(mu) for mu in meaning.meaning_updated])
        checked.extend([", ".join(c) for c in meaning.checked])
        time.sleep(10)

    df = pd.DataFrame(
        {
            "word": words,
            "defintion": definitions,
            "prompt1": prompt1,
            "prompt2": prompt2,
            "checked_meaining": checked,
        }
    )
    df.to_csv("meaning.csv", index=None)

    print(meaning)
