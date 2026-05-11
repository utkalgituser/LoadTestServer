from fastapi import APIRouter, HTTPException, Query

router = APIRouter(tags=["simulation"])


@router.get("/status", summary="Echo arbitrary status code")
async def status_echo(
    code: int = Query(200, ge=100, le=599, description="HTTP status to return"),
):
    if code >= 400:
        raise HTTPException(status_code=code, detail=f"simulated {code}")
    return {"status": code, "message": f"returning {code}"}
