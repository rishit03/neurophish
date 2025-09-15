from fastapi import APIRouter
from ..models import RunRequest, RunResponse, RunResultItem, RunSummary
from ..services.prompts import load_many
from ..services.providers import ProviderClient
from ..services.scorer import Scorer

router = APIRouter(prefix="/run", tags=["run"])

@router.post("", response_model=RunResponse)
async def run(req: RunRequest):
    prompts_by_cat = load_many(req.categories)
    provider = ProviderClient(req.provider)
    scorer = Scorer()

    items: list[RunResultItem] = []
    summary = {k: 0 for k in ["BIASED","NEUTRAL","RESISTANT","SKIPPED","UNSCORED"]}
    by_cat: dict[str, dict[str,int]] = {}

    for cat, prompts in prompts_by_cat.items():
        by_cat.setdefault(cat, {k:0 for k in summary})
        for p in prompts:
            try:
                resp = provider.chat(req.model, p.prompt)
                label, reason = scorer.score(p.prompt, resp)
                items.append(RunResultItem(
                    prompt_id=p.id,
                    category=cat,
                    prompt=p.prompt,        # NEW
                    response=resp,
                    score=label,
                    score_reason=reason     # NEW
                ))
                summary[label] += 1
                by_cat[cat][label] += 1
            except Exception as e:
                items.append(RunResultItem(
                    prompt_id=p.id,
                    category=cat,
                    prompt=p.prompt,        # still return the prompt
                    response=None,
                    score="SKIPPED",
                    score_reason=None,
                    error=str(e)
                ))
                summary["SKIPPED"] += 1
                by_cat[cat]["SKIPPED"] += 1

    return RunResponse(items=items, summary=RunSummary(counts=summary, by_category=by_cat))
    