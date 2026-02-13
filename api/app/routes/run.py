# api/app/routes/run.py
from fastapi import APIRouter
from ..models import RunRequest, RunResponse, RunResultItem, RunSummary
from ..services.prompts import load_many
from ..services.providers import ProviderClient
from ..services.scorer import Scorer
from typing import Any, Dict

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

                # scorer.score now returns (label, reason, meta) where meta is optional dict
                out = scorer.score(p.prompt, resp, evaluated_model=req.model)
                # out may be a tuple/list like (label, reason, meta) or legacy (label, reason)
                label = out[0]
                reason = out[1] if len(out) > 1 else None
                meta: Dict[str, Any] | None = out[2] if isinstance(out, (list, tuple)) and len(out) > 2 else None

                items.append(RunResultItem(
                    prompt_id=p.id,
                    category=cat,
                    prompt=p.prompt,
                    response=resp,
                    score=label,
                    score_reason=reason,
                    # optional observability fields (backward-compatible)
                    judge_votes=(meta.get("judge_votes") if meta else None),
                    judge_failures=(meta.get("judge_failures") if meta else None),
                    quorum_met=(meta.get("quorum_met") if meta else None),
                    ensemble_mode=(meta.get("ensemble_mode") if meta else None),
                ))
                # increment summary safely (fallback to UNSCORED if label missing)
                summary_label = label if label in summary else "UNSCORED"
                summary[summary_label] += 1
                by_cat[cat][summary_label] += 1
            except Exception as e:
                items.append(RunResultItem(
                    prompt_id=p.id,
                    category=cat,
                    prompt=p.prompt,
                    response=None,
                    score="SKIPPED",
                    score_reason=None,
                    error=str(e)
                ))
                summary["SKIPPED"] += 1
                by_cat[cat]["SKIPPED"] += 1

    return RunResponse(items=items, summary=RunSummary(counts=summary, by_category=by_cat))
