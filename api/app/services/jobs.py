import uuid, threading, time
from typing import Any

_jobs: dict[str, dict[str, Any]] = {}

def create_job() -> str:
    jid = uuid.uuid4().hex
    _jobs[jid] = {"status": "queued", "result": None, "error": None, "started_at": time.time()}
    return jid

def set_status(jid: str, status: str, **kwargs):
    if jid in _jobs:
        _jobs[jid].update({"status": status, **kwargs})

def get_job(jid: str) -> dict[str, Any] | None:
    return _jobs.get(jid)

def run_in_thread(target, *args, **kwargs):
    t = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    t.start()