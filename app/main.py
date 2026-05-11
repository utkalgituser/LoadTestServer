import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from asgi_correlation_id import CorrelationIdMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import get_settings
from app.utils.logger import setup_logging, CorrelationFilter
from app.middleware.errors import register_error_handlers
from app.middleware.logging_mw import AccessLogMiddleware
from app.middleware.metrics_mw import MetricsMiddleware
from app.middleware.payload_limit import PayloadLimitMiddleware
from app.engine.response_builder import get_store
from app.routers import health, metrics, status, config_router, mock, auth, delay, failure

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    for h in logging.getLogger().handlers:
        h.addFilter(CorrelationFilter())
    for h in logging.getLogger("access").handlers:
        h.addFilter(CorrelationFilter())

    s = get_settings()
    get_store()

    observer = None
    if s.SCENARIOS_HOT_RELOAD:
        try:
            from app.engine.watcher import start_watcher
            observer = start_watcher(s.SCENARIOS_FILE)
        except Exception as e:
            log.warning(f"watcher failed to start: {e}")

    log.info(f"server ready on {s.HOST}:{s.PORT}")
    yield

    if observer is not None:
        observer.stop()
        observer.join(timeout=2)
    log.info("server shutting down")


def create_app() -> FastAPI:
    s = get_settings()

    app = FastAPI(
        title="LoadTest Mock Server",
        description=(
            "Production-style FastAPI mock server for QA, integration testing, "
            "Postman sanity, and lightweight k6/JMeter load testing."
        ),
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    limiter = Limiter(key_func=get_remote_address, default_limits=[s.RATE_LIMIT_GLOBAL])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(MetricsMiddleware)
    app.add_middleware(AccessLogMiddleware)
    app.add_middleware(PayloadLimitMiddleware)
    app.add_middleware(CorrelationIdMiddleware, header_name="X-Request-ID")
    if s.ENABLE_GZIP:
        app.add_middleware(GZipMiddleware, minimum_size=1024)

    register_error_handlers(app)

    app.include_router(health.router)
    app.include_router(metrics.router)
    app.include_router(status.router)
    app.include_router(config_router.router)
    app.include_router(mock.router)
    app.include_router(auth.router)
    app.include_router(delay.router)
    app.include_router(failure.router)

    @app.get("/", tags=["system"], summary="Service index")
    async def root():
        return {
            "service": "loadtest-mockserver",
            "version": "1.0.0",
            "docs": "/docs",
            "openapi": "/openapi.json",
            "endpoints": ["/health", "/metrics", "/status", "/config", "/mock/*", "/auth/mock", "/delay/mock", "/failure/mock"],
        }

    return app


app = create_app()
