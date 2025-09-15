from pydantic import BaseModel
from typing import List, Literal, Dict

BiasLabel = Literal["BIASED", "NEUTRAL", "RESISTANT", "SKIPPED", "UNSCORED"]

class RunRequest(BaseModel):
    provider: str
    model: str
    categories: List[str]

class CompareRequest(BaseModel):
    provider1: str
    model1: str
    provider2: str
    model2: str
    categories: List[str]

class PromptItem(BaseModel):
    id: str
    description: str
    prompt: str
    expected_effect: str | None = None

class RunResultItem(BaseModel):
    prompt_id: str
    category: str
    prompt: str                 # NEW
    response: str | None
    score: BiasLabel
    score_reason: str | None = None   # NEW
    error: str | None = None

class RunSummary(BaseModel):
    counts: Dict[BiasLabel, int]
    by_category: Dict[str, Dict[BiasLabel, int]]

class RunResponse(BaseModel):
    items: List[RunResultItem]
    summary: RunSummary
