import random
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/failure", tags=["simulation"])

FAILURES = {
    400: "bad request",
    401: "unauthorized",
    403: "forbidden",
    404: "not found",
    409: "conflict",
    415: "unsupported media type",
    422: "unprocessable entity",
    429: "too many requests",
    500: "internal server error",
    502: "bad gateway",
    503: "service unavailable",
    504: "gateway timeout",
}


@router.get("/mock", summary="Force a failure status")
async def failure_mock(
    code: int | None = Query(None, description="Specific failure code; random if omitted"),
):
    if code is None:
        code = random.choice(list(FAILURES.keys()))
    if code not in FAILURES:
        raise HTTPException(status_code=400, detail=f"unsupported failure code: {code}")
    raise HTTPException(status_code=code, detail=FAILURES[code])
