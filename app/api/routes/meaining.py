from fastapi import APIRouter

from app.api.models.word import Word
from app.services.generate_word_meaning import generate_word_meaning_service


router = APIRouter(prefix="/meaning")


@router.post("")
async def meaning(word: Word):
    results = await generate_word_meaning_service(word.text)
    return results
