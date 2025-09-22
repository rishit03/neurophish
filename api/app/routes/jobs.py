# app/routes/jobs.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.jobs import create_job, set_status, get_job, run_in_thread
from ..services.prompts import load_many
from ..services.runner import run as run_tests  # may be async
import asyncio, json
from typing import Any

router = APIRouter()

class JobReq(BaseModel):
    provider: str
    model: str
    categories: list[str]
    limit_per_category: int | None = None


def _to_jsonable(obj: Any) -> Any:
    """
    Make sure whatever we got back is JSON-serializable.
    - If it's a FastAPI/Starlette Response, extract body.
    - If it's a Pydantic model, use model_dump().
    - If it's bytes, decode.
    - Else return as-is (dict/list/str/number/None are OK).
    """
    # Starlette/FastAPI Response-like
    if hasattr(obj, "body"):
        try:
            return json.loads(obj.body.decode())
        except Exception:
            return obj.body.decode()

    # Pydantic v2
    if hasattr(obj, "model_dump"):
        return obj.model_dump()

    # Pydantic v1
    if hasattr(obj, "dict"):
        return obj.dict()

    if isinstance(obj, (bytes, bytearray)):
        return obj.decode()

    return obj


def _do_job(jid: str, req: JobReq):
    try:
        set_status(jid, "running")

        prompts_by_cat = load_many(req.categories)
        if req.limit_per_category:
            for k, v in prompts_by_cat.items():
                prompts_by_cat[k] = v[: req.limit_per_category]

        # run_tests might be async or sync – handle both
        if asyncio.iscoroutinefunction(run_tests):
            result = asyncio.run(
                run_tests(
                    provider=req.provider,
                    model=req.model,
                    prompts_by_cat=prompts_by_cat,
                )
            )
        else:
            result = run_tests(
                provider=req.provider,
                model=req.model,
                prompts_by_cat=prompts_by_cat,
            )

        set_status(jid, "done", result=_to_jsonable(result))

    except Exception as e:
        # store a safe string so status/result endpoints never 500
        set_status(jid, "error", error=f"{type(e).__name__}: {e}")


@router.post("/jobs")
def create(req: JobReq):
    jid = create_job()
    run_in_thread(_do_job, jid, req)  # returns immediately
    return {"job_id": jid, "status": "queued"}


@router.get("/jobs/{job_id}")
def status(job_id: str):
    j = get_job(job_id)
    if not j:
        raise HTTPException(404, "job not found")
    return {"job_id": job_id, "status": j["status"], "has_result": j["result"] is not None}


@router.get("/jobs/{job_id}/result")
def result(job_id: str):
    j = get_job(job_id)
    if not j:
        raise HTTPException(404, "job not found")
    if j["status"] != "done":
        # 202 = Accepted (not ready)
        raise HTTPException(202, "not ready")
    return j["result"]