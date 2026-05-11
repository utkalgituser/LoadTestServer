import time
from fastapi import APIRouter

from app.schemas.common import HealthResponse

router = APIRouter(tags=["system"])
_start = time.time()


@router.get("/health", response_model=HealthResponse, summary="Liveness probe")
async def health() -> HealthResponse:
    return HealthResponse(status="ok", uptime_seconds=round(time.time() - _start, 2))
