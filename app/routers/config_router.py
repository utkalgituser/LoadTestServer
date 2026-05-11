from fastapi import APIRouter

from app.config import get_settings
from app.engine.response_builder import reload_scenarios, get_store

router = APIRouter(prefix="/config", tags=["config"])


@router.get("", summary="View runtime config (sanitized)")
async def view_config():
    s = get_settings()
    return {
        "host": s.HOST,
        "port": s.PORT,
        "workers": s.WORKER_COUNT,
        "log_level": s.LOG_LEVEL,
        "max_payload_bytes": s.MAX_PAYLOAD_BYTES,
        "timeout_seconds": s.TIMEOUT_SECONDS,
        "rate_limits": {
            "global": s.RATE_LIMIT_GLOBAL,
            "per_ip": s.RATE_LIMIT_PER_IP,
            "auth": s.RATE_LIMIT_AUTH,
        },
        "scenarios_loaded": len(get_store().mocks),
    }


@router.post("/reload", summary="Hot-reload scenarios.yaml")
async def reload():
    count = reload_scenarios()
    return {"status": "reloaded", "mocks": count}
