import json
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.engine.response_builder import build_response, get_store

router = APIRouter(tags=["mock"])


@router.api_route("/mock/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], summary="Dynamic mock dispatcher")
async def mock_dispatcher(full_path: str, request: Request):
    path = f"/mock/{full_path}"
    mock = get_store().find(path, request.method)

    body = None
    if request.method in {"POST", "PUT", "PATCH"}:
        raw = await request.body()
        if raw:
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                return JSONResponse(
                    status_code=422,
                    content={"error": "invalid_json", "detail": "request body is not valid JSON"},
                )

    if mock is None:
        return JSONResponse(
            status_code=404,
            content={"error": "mock_not_found", "path": path, "method": request.method},
        )

    return await build_response(mock, request, body)
