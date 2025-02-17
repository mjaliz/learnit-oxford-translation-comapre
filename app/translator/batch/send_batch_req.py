import os
from pathlib import Path
from loguru import logger
from openai import OpenAI

from app.translator.batch.batch import BatchReq

DATA_DIR = Path(__file__).parent.joinpath("data")

if __name__ == "__main__":
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL"),
    )
    batcher = BatchReq(client)
    # batcher.create_batch(
    #     "words_failed-2.jsonl",
    #     DATA_DIR.joinpath("batch_words_failed-2.json"),
    #     "failed words prompt 2",
    # )
    batch_id = "batch_67ada93137b481908ba86c7336334821"
    batch = batcher.retrieve(batch_id)
    logger.info(batch)
    batcher.get_result(
        batch_id,
        DATA_DIR.joinpath("res_failed_words-2.json"),
    )
    # batcher.get_error(batch_id, DATA_DIR.joinpath("error_100_000_to_end-2.jsonl"))
