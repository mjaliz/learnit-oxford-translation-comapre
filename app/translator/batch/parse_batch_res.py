import json
import pandas as pd
from loguru import logger
from pathlib import Path
from tqdm import tqdm


from app.translator.batch.build_batch_file import load_glossary_words

CURRENT_DIR = Path(__file__).parent


def match_word_by_res():
    words = load_glossary_words()
    results = list()
    with open(CURRENT_DIR.joinpath("data").joinpath("res_50_000.json"), "r") as f:
        results.extend(json.loads(f.read()))
    with open(CURRENT_DIR.joinpath("data").joinpath("res_100_000.json"), "r") as f:
        results.extend(json.loads(f.read()))
    with open(
        CURRENT_DIR.joinpath("data").joinpath("res_100_000_to_end.json"), "r"
    ) as f:
        results.extend(json.loads(f.read()))
    custom_ids = []
    wrds = []
    defs = []
    meanings = []
    for res in tqdm(results):
        word_id, item_id = res["custom_id"].split(":")
        for word in words:
            if word.id.oid == word_id:
                for item in word.items:
                    if item.id == item_id:
                        try:
                            eqs = json.loads(
                                res["response"]["body"]["choices"][0]["message"][
                                    "content"
                                ]
                            )
                            p_eqs = eqs["persian_equivalents"]
                            wrds.append(word.word)
                            defs.append(item.definition.text)
                            custom_ids.append(res["custom_id"])
                            meanings.append(", ".join(p_eqs))
                        except Exception as e:
                            logger.error(f"parsing item_id {item_id} failed: {e}")
                            continue

    df = pd.DataFrame(
        {"custom_id": custom_ids, "word": wrds, "definition": defs, "meaning": meanings}
    )
    df.to_csv(CURRENT_DIR.joinpath("data").joinpath("prompt1_res.csv"), index=False)


if __name__ == "__main__":
    match_word_by_res()
