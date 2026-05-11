from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import get_settings


class PayloadLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        max_bytes = get_settings().MAX_PAYLOAD_BYTES
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > max_bytes:
            return JSONResponse(
                status_code=413,
                content={"error": "payload_too_large", "max_bytes": max_bytes},
            )
        return await call_next(request)
