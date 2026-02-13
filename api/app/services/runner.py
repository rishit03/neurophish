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
    summary = {k: 0 for k in ["BIASED", "NEUTRAL", "RESISTANT", "SKIPPED", "UNSCORED"]}
    by_cat: dict[str, dict[str, int]] = {}

    for cat, prompts in (prompts_by_cat or {}).items():
        by_cat.setdefault(cat, {k: 0 for k in summary})
        arr = prompts[:limit_per_category] if limit_per_category else prompts

        for obj in arr:
            # Support both dict prompt objects and pydantic-like objects
            pid = getattr(obj, "id", None) or (obj.get("id") if isinstance(obj, dict) else None)
            pid = str(pid) if pid is not None else ""

            # Primary should be "prompt" (run_inline normalizes prompt_text -> prompt)
            # Backup accepts prompt_text just in case anything bypasses normalization.
            prompt = (
                getattr(obj, "prompt", None)
                or (obj.get("prompt") if isinstance(obj, dict) else None)
                or (obj.get("prompt_text") if isinstance(obj, dict) else None)
                or ""
            )

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

                # ✅ minimal fairness patch: pass evaluated_model so scorer can exclude self / same-family
                out = scorer.score(prompt, resp, evaluated_model=model)

                # Unpack safely (support legacy 2-tuple or new 3-tuple)
                if isinstance(out, (list, tuple)):
                    label = out[0]
                    reason = out[1] if len(out) > 1 else None
                    meta = out[2] if len(out) > 2 else None
                else:
                    # defensive fallback: try to unpack (rare)
                    try:
                        label, reason = out
                        meta = None
                    except Exception:
                        label, reason, meta = "UNSCORED", None, None

                meta = meta if isinstance(meta, dict) else None

                items.append(RunResultItem(
                    prompt_id=pid,
                    category=cat,
                    prompt=prompt,
                    response=resp,
                    score=label,
                    score_reason=reason,
                    judge_votes=(meta.get("judge_votes") if meta else None),
                    judge_failures=(meta.get("judge_failures") if meta else None),
                    quorum_met=(meta.get("quorum_met") if meta else None),
                    ensemble_mode=(meta.get("ensemble_mode") if meta else None),
                    fallback_used=(meta.get("fallback_used") if meta else None),
                ))

                # Update summary and by_cat safely (handle unexpected labels)
                summary_label = label if label in summary else "UNSCORED"
                summary[summary_label] += 1
                by_cat[cat][summary_label] += 1

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
        prompts_by_cat=prompts_by_cat,
        limit_per_category=limit_per_category
    )
