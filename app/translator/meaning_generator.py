import asyncio
import time
from loguru import logger
import pandas as pd

from app.llm.openai_client import AsyncOpenAIClient
from app.translator.models.meaning import CheckRes, Meaning, MeaningReasoning
from app.translator.prompt import (
    system_message_updated,
    system_message,
    system_message_by_def,
    system_message_combine_res,
    system_message_meaning_steps,
)


def build_prmopt_check_res(word, definition, persian_eqs):
    messages = []
    messages.extend(
        [
            {"role": "user", "content": f"## Here is the target word: {word}"},
            {
                "role": "user",
                "content": f"## Here is the word definition: {definition}",
            },
            {
                "role": "user",
                "content": f"## Here is the first list of Persian equivalents: {persian_eqs[0]}",
            },
            {
                "role": "user",
                "content": f"## Here is the second list of Persian equivalents: {persian_eqs[1]}",
            },
        ]
    )
    return messages


async def check_meanings(
    openai_client: AsyncOpenAIClient, word, definition, persian_eqs
):
    messages = build_prmopt_check_res(word, definition, persian_eqs)
    try:
        meaning = await openai_client.chat(
            model="gpt-4o-2024-11-20",
            system=system_message_combine_res,
            messages=messages,
            temperature=0,
            output=CheckRes,
            n=1,
        )
        return meaning.choices[0].message.parsed
    except Exception:
        raise ConnectionError("getting result from OpenAI failed")


def build_prompt(word, definition):
    return [
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


def build_prompt_updated(word, pos, definition):
    messages = []
    messages.append(
        {"role": "user", "content": f"## Here is the target English word: {word}"}
    )
    messages.append(
        {
            "role": "user",
            "content": f"## Here is the part of speech of the targe word: {pos}",
        }
    )
    messages.append(
        {"role": "user", "content": f"## Here is the word definition: {definition}"}
    )
    return messages


async def generate_meaning_updated(
    openai_client: AsyncOpenAIClient, word, pos, definition
):
    messages = build_prompt_updated(word, pos, definition)
    try:
        meaning = await openai_client.chat(
            model="gpt-4o-2024-11-20",
            system=system_message_meaning_steps,
            messages=messages,
            temperature=0,
            output=MeaningReasoning,
            n=1,
        )
        return meaning.choices[0].message.parsed
    except Exception as e:
        logger.error(e)
        raise ConnectionError("getting result from OpenAI failed")


async def generate_meaning_by_def(openai_client: AsyncOpenAIClient, definition):
    messages = []
    messages.append(
        {"role": "user", "content": f"## Here is the word definition: {definition}"}
    )
    try:
        meaning = await openai_client.chat(
            model="gpt-4o-2024-11-20",
            system=system_message_by_def,
            messages=messages,
            temperature=0,
            output=Meaning,
            n=1,
        )
        return meaning.choices
    except Exception:
        raise ConnectionError("getting result from OpenAI failed")


async def combine_word_by_def(openai_client: AsyncOpenAIClient, word, definition, pes):
    messages = []
    messages.append({"role": "user", "content": f"## Here is the target word: {word}"})
    messages.append(
        {"role": "user", "content": f"## Here is the word definition: {definition}"}
    )
    messages.append(
        {
            "role": "user",
            "content": f"## Here is the first list of persian equivalnets: {pes[0]}",
        }
    )
    messages.append(
        {
            "role": "user",
            "content": f"## Here is the second list of persian equivalnets: {pes[1]}",
        }
    )
    try:
        meaning = await openai_client.chat(
            model="gpt-4o-2024-11-20",
            system=system_message_by_def,
            messages=messages,
            temperature=0,
            output=Meaning,
        )
        time.sleep(2)
        return meaning.choices[0].message.parsed.persian_equivalent
    except Exception:
        raise ConnectionError("getting result from OpenAI failed")


async def generate_meaning(openai_client: AsyncOpenAIClient, word, definition):
    messages = build_prompt(word, definition)
    try:
        meaning = await openai_client.chat(
            model="gpt-4o-2024-11-20",
            system=system_message,
            messages=messages,
            temperature=0,
            output=Meaning,
            n=1,
        )
        return meaning.choices[0].message.parsed
    except Exception:
        raise ConnectionError("getting result from OpenAI failed")


def join_res(res):
    return ", ".join([f.text for f in res[0].message.parsed.final_list])


if __name__ == "__main__":
    from ast import literal_eval

    openai_client = AsyncOpenAIClient()
    res = asyncio.run(
        generate_meaning_updated(
            openai_client,
            "take",
            "verb",
            "to remove something/somebody from a place or a person",
        )
    )
    paresed_res = res[0].message.parsed
    print(paresed_res)
    # df = pd.read_csv("can.csv")
    # df["cot"] = df.apply(
    #     lambda d: join_res(
    #         asyncio.run(
    #             generate_meaning_updated(
    #                 openai_client,
    #                 d["word"],
    #                 d["defintion"],
    #             )
    #         )
    #     ),
    #     axis=1,
    # )
    # df.to_csv("can.csv", index=False)
