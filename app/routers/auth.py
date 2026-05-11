from fastapi import APIRouter, Header, HTTPException

from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["simulation"])


@router.get("/mock", summary="Validate Authorization: Bearer <token>")
async def auth_mock(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="missing Authorization header")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="must be Bearer token")
    token = authorization.split(" ", 1)[1].strip()
    if token != get_settings().MOCK_AUTH_TOKEN:
        raise HTTPException(status_code=403, detail="invalid token")
    return {"status": "authenticated", "token_prefix": token[:6] + "..."}
