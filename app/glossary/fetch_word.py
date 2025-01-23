import os
import httpx
import json

from loguru import logger

from app.utils.generate_internal_token import generate_internal_token
from app.glossary.models.word import Word


async def post(url, data, query=None, headers=None):
    if headers is None:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {generate_internal_token()}",
        }
    if query is not None:
        url = f"{url}?{query}"
    if os.getenv("API_KEY") is not None and os.getenv("API_KEY") != "":
        headers["Apikey"] = os.getenv("API_KEY")
    payload = json.dumps(data)
    async with httpx.AsyncClient() as client:
        res = await client.post(url=url, data=payload, headers=headers)
    if res.status_code == httpx.codes.OK or res.status_code == httpx.codes.NOT_FOUND:
        return res
    raise Exception(f"POST request to {url} returned {res.status_code}")


async def fetch_word(word: str) -> Word | None:
    url = os.getenv("GLOSSARY_PANEL_URL")
    payload = {"word": word, "state": "published"}
    resp = await post(url, data=payload)
    if resp.status_code == httpx.codes.NOT_FOUND:
        return None

    logger.info("Found in the dictionary.")
    glossary_word = Word(**resp.json()["data"])
    return glossary_word
