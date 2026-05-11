import os
import time
from fastapi import APIRouter

from app.middleware.metrics_mw import get_metrics_state
from app.schemas.common import MetricsResponse

router = APIRouter(tags=["system"])


def _mem_mb() -> float:
    try:
        import resource
        return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 2)
    except Exception:
        try:
            import psutil
            return round(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024, 2)
        except Exception:
            return 0.0


@router.get("/metrics", response_model=MetricsResponse, summary="Runtime metrics")
async def metrics() -> MetricsResponse:
    s = get_metrics_state()
    return MetricsResponse(
        requests_total=s.requests_total,
        requests_by_status=dict(s.by_status),
        requests_by_endpoint=dict(s.by_endpoint),
        uptime_seconds=round(time.time() - s.start_time, 2),
        memory_mb=_mem_mb(),
    )
