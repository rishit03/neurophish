from typing import Dict, List, Any
from ..routes.run import run as run_endpoint, RunRequest

def run(provider: str, model: str, prompts_by_cat: Dict[str, List[Dict[str, Any]]], limit_per_category: int | None = None):
    # Flatten prompts_by_cat into categories list that your /run expects
    categories = list(prompts_by_cat.keys())
    req = RunRequest(
        provider=provider,
        model=model,
        categories=categories,
        limit_per_category=limit_per_category,
    )
    return run_endpoint(req)