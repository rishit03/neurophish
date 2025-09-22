# app/routes/jobs.py
import asyncio
import inspect
import traceback
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from ..services.jobs import create_job, set_status, get_job, run_in_thread
from ..services.prompts import load_many
from ..services.runner import run as run_tests  # may be sync or async

router = APIRouter()


class JobReq(BaseModel):
    provider: str
    model: str
    categories: list[str]
    limit_per_category: int | None = None


def _run_coroutine_safe(coro: Any) -> Any:
    """
    Run a coroutine from a synchronous context and return its result.
    Uses asyncio.run normally; if an event loop is already running,
    create a temporary loop to run the coroutine.
    """
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            try:
                loop.close()
            except Exception:
                pass


def _do_job(jid: str, req: JobReq) -> None:
    """
    Worker function that performs the job and updates job status.
    It handles both sync and async run_tests and ensures the stored
    result is JSON-serializable (or a safe fallback).
    """
    try:
        set_status(jid, "running")

        prompts_by_cat = load_many(req.categories)
        if req.limit_per_category:
            for k, v in prompts_by_cat.items():
                prompts_by_cat[k] = v[: req.limit_per_category]

        # run_tests may be synchronous or return an awaitable (coroutine)
        maybe_result = run_tests(provider=req.provider, model=req.model, prompts_by_cat=prompts_by_cat)

        if inspect.isawaitable(maybe_result):
            result = _run_coroutine_safe(maybe_result)
        else:
            result = maybe_result

        # Try to make the result JSON-serializable. If it fails, fallback to a safe dict.
        try:
            serializable = jsonable_encoder(result)
        except Exception:
            serializable = {"_unserializable_result": True, "value": str(result)}

        set_status(jid, "done", result=serializable)
    except Exception as e:
        tb = traceback.format_exc()
        # Print to stdout/stderr so render logs capture it
        print(f"[jobs] _do_job FAILED for job {jid}: {e}\n{tb}", flush=True)
        set_status(jid, "error", error=f"{type(e).__name__}: {e}")


@router.post("/jobs")
def create(req: JobReq):
    jid = create_job()
    run_in_thread(_do_job, jid, req)
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
        raise HTTPException(202, "not ready")
    return j["result"]