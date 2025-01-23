from app.llm.openai_client import AsyncOpenAIClient
from app.translator.models.meaning import Meaning
from app.translator.prompt import system_message_updated, system_message


async def generate_meaning_updated(openai_client: AsyncOpenAIClient, word, definition):
    messages = []
    messages.append(
        {"role": "system", "content": f"## Here is the target English word: {word}"}
    )
    messages.append(
        {"role": "system", "content": f"## Here is the word definition: {definition}"}
    )
    try:
        meaning = await openai_client.chat(
            model="gpt-4o-2024-08-06",
            system=system_message_updated,
            messages=messages,
            temperature=0,
            output=Meaning,
        )
        return meaning.choices[0].message.parsed.persian_equivalent
    except Exception:
        raise ConnectionError("getting result from OpenAI failed")


async def generate_meaning(openai_client: AsyncOpenAIClient, word, definition):
    messages = [
        {
            "role": "user",
            "content": f"""
    Example

    word: state
    definition: a condition or way of being that exists at a particular time
    part of speech: noun
    persian_equivalent: وضعیت، وضع، حالت

    word: trouble
    definition: a problem, worry, difficulty, etc. or a situation causing this
    part of speech: noun
    persian_equivalent: مشکل، دردسر
            
    word: classic
    definition: accepted as one of the best or most important of its kind; having all the features that are typical of something
    part of speech: adjective
    persian_equivalent: عالی، برجسته، باستانی، کلاسیک، اصیل
            
    word: moan
    definition: to make a long, low sound because of pain, suffering, etc., or to say something in a complaining way
    part of speech: verb
    persian_equivalent: غر زدن،‌نالیدن، ناله کردن

    word: point
    definition: the purpose, usefulness, or aim of something
    part of speech: noun
    persian_equivalent: اهمیت، ارزش،‌ معنی، هدف
    
    word: complex
    definition: a feeling of worry or embarrassment about something that is not necessary or reasonable
    part of speech: noun
    persian_equivalent: ترس، حساسیت روانی
            
    word: {word}
    definition: {definition}
    """,
        },
    ]
    try:
        meaning = await openai_client.chat(
            model="gpt-4o-2024-08-06",
            system=system_message,
            messages=messages,
            temperature=0,
            output=Meaning,
        )
        return meaning.choices[0].message.parsed.persian_equivalent
    except Exception:
        raise ConnectionError("getting result from OpenAI failed")
