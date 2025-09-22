# api/app/routes/run_inline.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List

from ..services.runner import run as run_tests
from ..services.providers import PROVIDERS

router = APIRouter()

class InlineRunReq(BaseModel):
    provider: str                  # e.g., "Groq"
    model: str                     # e.g., "llama-3.1-8b-instant"
    prompts_by_cat: Dict[str, List[Dict[str, str]]]  # {category: [{id, prompt, ...}], ...}
    limit_per_category: int | None = None

@router.post("/run_inline")
def run_inline(req: InlineRunReq):
    if req.provider not in PROVIDERS:
        raise HTTPException(400, "Unknown provider")
    if not req.prompts_by_cat:
        raise HTTPException(400, "No prompts provided")

    prompts = req.prompts_by_cat
    if req.limit_per_category:
        prompts = {k: v[:req.limit_per_category] for k, v in prompts.items()}

    try:
        # Returns the same structure your /run returns: {items: [...], summary: {...}}
        return run_tests(provider=req.provider, model=req.model, prompts_by_cat=prompts)
    except Exception as e:
        raise HTTPException(500, str(e))