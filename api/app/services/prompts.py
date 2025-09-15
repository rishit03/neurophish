import json, os
from pathlib import Path
from typing import Dict, List
from ..models import PromptItem

PROMPT_DIR = Path(os.getenv("PROMPT_DIR", Path(__file__).resolve().parents[3] / "prompts"))

def load_category(cat: str) -> List[PromptItem]:
    path = PROMPT_DIR / f"{cat}.json"
    data = json.loads(path.read_text())
    return [PromptItem(**x) for x in data]

def load_many(cats: list[str]) -> Dict[str, list[PromptItem]]:
    return {c: load_category(c) for c in cats}
