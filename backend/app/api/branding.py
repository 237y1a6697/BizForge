import re
from fastapi import APIRouter, HTTPException
from app.models.schemas import BrandRequest, BrandResponse
from app.services.branding_service import BrandingService

router = APIRouter()
service = BrandingService()


def is_valid_idea(text: str) -> bool:
    """
    Return False if the input looks like gibberish / an invalid entry.
    Checks:
    - Too short (< 3 chars)
    - Mostly non-alphabetic (symbols/number spam)
    - No word >= 2 chars long
    - Repeated-character spam (aaaaaaa)
    - Key: every word longer than 2 chars must contain at least 1 vowel
      (real English words always have vowels; 'jyvtgf', 'xyz', 'qwrty' have none)
    - Any word with 5+ consecutive consonants is likely gibberish
    """
    VOWELS = set("aeiouAEIOU")
    text = text.strip()

    if len(text) < 3:
        return False

    # Alpha chars must be >= 50% of total
    alpha_chars = sum(1 for c in text if c.isalpha())
    if alpha_chars / len(text) < 0.5:
        return False

    words = re.findall(r"[a-zA-Z]+", text)
    if not words or all(len(w) < 2 for w in words):
        return False

    # Reject repeated-character spam (e.g. "aaaaaaa")
    if re.fullmatch(r"(.)\1{4,}", text.replace(" ", "")):
        return False

    # Every word longer than 2 chars must have at least 1 vowel
    for word in words:
        if len(word) > 2 and not any(c in VOWELS for c in word):
            return False

    # Reject words with 5+ consecutive consonants (e.g. "strntgph")
    for word in words:
        if re.search(r"[^aeiouAEIOU]{5,}", word):
            return False

    return True



@router.post("/", response_model=BrandResponse)
def brand(req: BrandRequest):
    """Create a complete brand with name, slogan, logo, and guide"""
    if not req.idea or len(req.idea.strip()) == 0:
        raise HTTPException(status_code=400, detail="Idea cannot be empty")

    if not is_valid_idea(req.idea):
        raise HTTPException(
            status_code=422,
            detail="Invalid input: please enter a meaningful business idea (e.g. 'AI healthcare startup')."
        )

    try:
        return service.create_brand(req.idea)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))