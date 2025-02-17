import json
from pathlib import Path
from loguru import logger
from openai import OpenAI
from openai.types.batch import Batch
from tempfile import NamedTemporaryFile


class BatchReq:
    def __init__(self, client: OpenAI):
        self._client = client

    def create_batch(self, batch_file: Path, batch_res_dest: Path, desc):
        batch_input_file = self._client.files.create(
            file=open(batch_file, "rb"), purpose="batch"
        )
        logger.info(batch_input_file)
        batch = self._client.batches.create(
            input_file_id=batch_input_file.id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={"description": desc},
        )

        with open(batch_res_dest, "w") as f:
            f.write(batch.model_dump_json())

    def retrieve(self, batch_id) -> Batch:
        return self._client.batches.retrieve(batch_id)

    def get_error(self, batch_id, error_file_path: Path):
        batch = self.retrieve(batch_id)
        error_response = self._client.files.content(batch.error_file_id)
        with open(error_file_path, "wb") as f:
            f.write(error_response.content)

    def get_result(self, batch_id, res_file_path: Path):
        batch = self.retrieve(batch_id)
        file_response = self._client.files.content(batch.output_file_id)
        temp_file = NamedTemporaryFile()
        try:
            temp_file.write(file_response.content)

            # Loading data from saved file
            results = []
            temp_file.seek(0)
            for line in temp_file.readlines():
                # Parsing the JSON string into a dict and appending to the list of results
                json_object = json.loads(line.strip())
                results.append(json_object)

            with open(res_file_path, "w") as f:
                f.write(json.dumps(results, ensure_ascii=False))
        finally:
            temp_file.close()
