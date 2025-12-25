# api/app/routes/run_inline.py
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, field_validator
from typing import Dict, List, Any
import inspect
import traceback

# from ..services.runner import run as run_tests
from ..services.runner import run_inline_prompts as run_tests

from ..services.providers import PROVIDERS

router = APIRouter()

class InlineRunReq(BaseModel):
    provider: str
    model: str
    prompts_by_cat: Dict[str, List[Any]]  # tolerate strings/objects
    limit_per_category: int | None = None

    # Be forgiving: accept strings or simplified objects and coerce
    @field_validator("prompts_by_cat", mode="before")
    @classmethod
    def coerce_prompts(cls, v: Any) -> Dict[str, List[Dict[str, str]]]:
        import json
        if isinstance(v, str):
            v = json.loads(v)
        out: Dict[str, List[Dict[str, str]]] = {}
        for cat, arr in (v or {}).items():
            norm: List[Dict[str, str]] = []
            for i, item in enumerate(arr or []):
                if isinstance(item, str):
                    norm.append({"id": f"{cat}_{i}", "prompt": item})
                elif isinstance(item, dict):
                    pid = item.get("id") or f"{cat}_{i}"
                    pr = item.get("prompt") or item.get("text") or ""
                    desc = item.get("description")
                    norm.append({"id": pid, "prompt": pr, "description": desc})
            out[cat] = norm
        return out

@router.post("/run_inline")
async def run_inline(req: InlineRunReq):
    if req.provider not in PROVIDERS:
        raise HTTPException(400, "Unknown provider")
    if not req.prompts_by_cat:
        raise HTTPException(400, "No prompts provided")

    prompts = req.prompts_by_cat
    if req.limit_per_category:
        prompts = {k: v[:req.limit_per_category] for k, v in prompts.items()}

    try:
        maybe = run_tests(provider=req.provider, model=req.model, prompts_by_cat=prompts)
        # handle sync or async runner
        result = await maybe if inspect.isawaitable(maybe) else maybe
        # ensure JSON-serializable
        return jsonable_encoder(result)
    except Exception as e:
        # log full traceback to Render logs and return a readable JSON error
        tb = traceback.format_exc()
        print(f"[run_inline] ERROR: {e}\n{tb}", flush=True)
        raise HTTPException(500, f"{type(e).__name__}: {e}")