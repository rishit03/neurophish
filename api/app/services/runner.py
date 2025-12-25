# from typing import Dict, List, Any
# from ..routes.run import run as run_endpoint, RunRequest

# def run(provider: str, model: str, prompts_by_cat: Dict[str, List[Dict[str, Any]]], limit_per_category: int | None = None):
#     # Flatten prompts_by_cat into categories list that your /run expects
#     categories = list(prompts_by_cat.keys())
#     req = RunRequest(
#         provider=provider,
#         model=model,
#         categories=categories,
#         limit_per_category=limit_per_category,
#     )
#     return run_endpoint(req)

# api/app/services/runner.py
from typing import Dict, List, Any

from ..models import RunResultItem, RunResponse, RunSummary
from ..services.providers import ProviderClient
from ..services.scorer import Scorer

def run_inline_prompts(
    provider: str,
    model: str,
    prompts_by_cat: Dict[str, List[Dict[str, Any]]],
    limit_per_category: int | None = None
) -> RunResponse:
    client = ProviderClient(provider)
    scorer = Scorer()

    items: list[RunResultItem] = []
    summary = {k: 0 for k in ["BIASED","NEUTRAL","RESISTANT","SKIPPED","UNSCORED"]}
    by_cat: dict[str, dict[str, int]] = {}

    for cat, prompts in (prompts_by_cat or {}).items():
        by_cat.setdefault(cat, {k: 0 for k in summary})
        arr = prompts[:limit_per_category] if limit_per_category else prompts

        for obj in arr:
            pid = getattr(obj, "id", None) or obj.get("id")
            prompt = getattr(obj, "prompt", None) or obj.get("prompt") or ""

            if not prompt:
                items.append(RunResultItem(
                    prompt_id=pid,
                    category=cat,
                    prompt=prompt,
                    response=None,
                    score="SKIPPED",
                    score_reason=None,
                    error="Empty prompt"
                ))
                summary["SKIPPED"] += 1
                by_cat[cat]["SKIPPED"] += 1
                continue

            try:
                resp = client.chat(model, prompt)
                label, reason = scorer.score(prompt, resp)

                items.append(RunResultItem(
                    prompt_id=pid,
                    category=cat,
                    prompt=prompt,
                    response=resp,
                    score=label,
                    score_reason=reason
                ))
                summary[label] += 1
                by_cat[cat][label] += 1

            except Exception as e:
                items.append(RunResultItem(
                    prompt_id=pid,
                    category=cat,
                    prompt=prompt,
                    response=None,
                    score="SKIPPED",
                    score_reason=None,
                    error=str(e)
                ))
                summary["SKIPPED"] += 1
                by_cat[cat]["SKIPPED"] += 1

    return RunResponse(items=items, summary=RunSummary(counts=summary, by_category=by_cat))

# Backwards compatible: jobs.py imports `run as run_tests`
def run(
    provider: str,
    model: str,
    prompts_by_cat: Dict[str, List[Any]],
    limit_per_category: int | None = None
) -> RunResponse:
    """
    Keep the old entrypoint name used by /jobs.
    It runs whatever prompt objects are passed in (including those from load_many).
    """
    return run_inline_prompts(
        provider=provider,
        model=model,
        prompts_by_cat=prompts_by_cat,   # accepts dict of prompt objects too
        limit_per_category=limit_per_category
    )

