from fastapi import APIRouter
from ..services.prompts import load_many

router = APIRouter(prefix="/prompts", tags=["prompts"])

@router.get("")
def get_prompts(categories: str):
    cats = [c.strip() for c in categories.split(",") if c.strip()]
    return load_many(cats)
