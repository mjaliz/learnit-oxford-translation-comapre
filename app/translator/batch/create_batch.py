import json
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL"),
)

# batch_input_file = client.files.create(
#     file=open("100_words.jsonl", "rb"), purpose="batch"
# )

# print(batch_input_file)

# batch_input_file_id = batch_input_file.id
# batch = client.batches.create(
#     input_file_id=batch_input_file_id,
#     endpoint="/v1/chat/completions",
#     completion_window="24h",
#     metadata={"description": "test def translation"},
# )

# with open("100_words_batch.json", "w") as f:
#     f.write(batch.model_dump_json())


if __name__ == "__main__":
    batch = client.batches.retrieve("batch_679f0c13297c81908619d090e7ca506b")
    print(batch)
    file_response = client.files.content(batch.error_file_id)
    with open("res_1000.jsonl", "wb") as f:
        f.write(file_response.content)

    # Loading data from saved file
    results = []
    with open("res_1000.jsonl", "r") as file:
        for line in file:
            # Parsing the JSON string into a dict and appending to the list of results
            json_object = json.loads(line.strip())
            results.append(json_object)

    with open("res_1000.json", "w") as f:
        f.write(json.dumps(results, ensure_ascii=False))
