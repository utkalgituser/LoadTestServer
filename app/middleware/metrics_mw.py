import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class MetricsState:
    def __init__(self) -> None:
        self.start_time = time.time()
        self.requests_total = 0
        self.by_status: dict[str, int] = defaultdict(int)
        self.by_endpoint: dict[str, int] = defaultdict(int)


_state = MetricsState()


def get_metrics_state() -> MetricsState:
    return _state


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        _state.requests_total += 1
        _state.by_status[str(response.status_code)] += 1
        _state.by_endpoint[f"{request.method} {request.url.path}"] += 1
        return response
