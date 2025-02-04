import json
import pandas as pd
from pathlib import Path
from app.translator.batch.build_batch_file import load_glossary_words

CURRENT_DIR = Path(__file__).parent


def match_word_by_res():
    words = load_glossary_words()
    with open(CURRENT_DIR.joinpath("data").joinpath("res_100.json"), "r") as f:
        results = json.loads(f.read())
    wrds = []
    defs = []
    meanings = []
    for res in results:
        word_id, item_id = res["custom_id"].split(":")
        for word in words:
            if word.id.oid == word_id:
                for item in word.items:
                    if item.id == item_id:
                        eqs = json.loads(
                            res["response"]["body"]["choices"][0]["message"]["content"]
                        )
                        p_eqs = eqs["persian_equivalents"]
                        wrds.append(word.word)
                        defs.append(item.definition.text)
                        meanings.append(", ".join(p_eqs))

    df = pd.DataFrame({"word": wrds, "definition": defs, "meaning": meanings})
    df.to_csv(CURRENT_DIR.joinpath("data").joinpath("100_meaning.csv"), index=False)


if __name__ == "__main__":
    match_word_by_res()
