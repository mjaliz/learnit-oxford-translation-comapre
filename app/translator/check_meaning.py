import asyncio
import pandas as pd

from app.llm.openai_client import AsyncOpenAIClient
from app.translator.meaning_generator import check_meanings

if __name__ == "__main__":
    openai_client = AsyncOpenAIClient()
    df = pd.read_csv("take.csv")
    df["checked_claude"] = df.apply(
        lambda d: asyncio.run(
            check_meanings(
                openai_client,
                d["word"],
                d["definition"],
                [d["meaning_1"], d["meaning_2"]],
            )
        ),
        axis=1,
    )
    df.to_csv("take.csv", index=False, encoding="utf-8-sig")
