import asyncio
from app.glossary.fetch_word import fetch_word
from app.llm.openai_client import AsyncOpenAIClient
from app.services.models.word_meaning import WordMeaning
from app.translator.meaning_generator import generate_meaning, generate_meaning_updated


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
    meanings = [
        generate_meaning(openai_client, word, definition) for definition in definitions
    ]
    meanings_update = [
        generate_meaning_updated(openai_client, word, definition)
        for definition in definitions
    ]
    meaining_res = await asyncio.gather(*meanings)
    meaning_updated_res = await asyncio.gather(*meanings_update)
    return WordMeaning(
        definitions=definitions,
        meaning=meaining_res,
        meaning_updated=meaning_updated_res,
    )
