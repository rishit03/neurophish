from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.jobs import create_job, set_status, get_job, run_in_thread
from ..services.prompts import load_many
from ..services.runner import run as run_tests  # your existing function

router = APIRouter()

class JobReq(BaseModel):
    provider: str
    model: str
    categories: list[str]
    limit_per_category: int | None = None

def _do_job(jid: str, req: JobReq):
    try:
        set_status(jid, "running")
        prompts_by_cat = load_many(req.categories)
        if req.limit_per_category:
            for k, v in prompts_by_cat.items():
                prompts_by_cat[k] = v[: req.limit_per_category]

        result = run_tests(provider=req.provider,
                           model=req.model,
                           prompts_by_cat=prompts_by_cat)

        # If run_tests returns a Response, extract the JSON
        if hasattr(result, "body"):   # FastAPI Response
            import json
            data = json.loads(result.body.decode())
        else:
            data = result  # assume dict

        set_status(jid, "done", result=data)
    except Exception as e:
        set_status(jid, "error", error=str(e))

@router.post("/jobs")
def create(req: JobReq):
    jid = create_job()
    run_in_thread(_do_job, jid, req)  # returns immediately
    return {"job_id": jid, "status": "queued"}

@router.get("/jobs/{job_id}")
def status(job_id: str):
    j = get_job(job_id)
    if not j: raise HTTPException(404, "job not found")
    return {"job_id": job_id, "status": j["status"], "has_result": j["result"] is not None}

@router.get("/jobs/{job_id}/result")
def result(job_id: str):
    j = get_job(job_id)
    if not j: raise HTTPException(404, "job not found")
    if j["status"] != "done": raise HTTPException(202, "not ready")
    return j["result"]