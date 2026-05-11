from typing import Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    uptime_seconds: float
    version: str = "1.0.0"


class MetricsResponse(BaseModel):
    requests_total: int
    requests_by_status: dict[str, int]
    requests_by_endpoint: dict[str, int]
    uptime_seconds: float
    memory_mb: float


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
    correlation_id: str | None = None


class PaymentRequest(BaseModel):
    transactionId: str = Field(..., min_length=3, max_length=64)
    amount: float = Field(..., gt=0)
    currency: str = Field(..., pattern=r"^[A-Z]{3}$")
    metadata: dict[str, Any] | None = None


class GenericMockRequest(BaseModel):
    payload: dict[str, Any] | None = None
