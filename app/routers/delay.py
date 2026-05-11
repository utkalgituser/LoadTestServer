import asyncio
from fastapi import APIRouter, Query

from app.config import get_settings

router = APIRouter(prefix="/delay", tags=["simulation"])


@router.get("/mock", summary="Configurable delay response")
async def delay_mock(
    ms: int = Query(1000, ge=0, le=60000, description="Delay in milliseconds (0-60000)"),
):
    timeout_ms = get_settings().TIMEOUT_SECONDS * 1000
    capped = min(ms, timeout_ms)
    await asyncio.sleep(capped / 1000)
    return {"delayed_ms": capped, "requested_ms": ms}
