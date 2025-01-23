import os
import httpx

from openai import AsyncOpenAI
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion
from loguru import logger

OPENAI_TIMEOUT = 30


class AsyncOpenAIClient:
    def __init__(self):
        self.__client = AsyncOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL"),
            http_client=httpx.AsyncClient(
                timeout=httpx.Timeout(timeout=OPENAI_TIMEOUT),
                limits=httpx.Limits(max_connections=1000, max_keepalive_connections=10),
                proxy=(
                    None
                    if os.getenv("THE_HTTP_PROXY") is None
                    else os.getenv("THE_HTTP_PROXY")
                ),
            ),
        )

    async def chat(
        self, *, model, system, messages, temperature, output
    ) -> ParsedChatCompletion:
        messages = [{"role": "system", "content": system}] + messages
        try:
            response: ParsedChatCompletion = (
                await self.__client.beta.chat.completions.parse(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    response_format=output,
                )
            )
            return response
        except Exception as e:
            logger.error("Unable to generate ChatCompletion response")
            return e
