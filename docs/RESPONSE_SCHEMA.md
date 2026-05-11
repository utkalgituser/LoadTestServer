# Response Schemas

## Common Response Headers

| Header | Description |
|---|---|
| `X-Request-ID`        | Correlation ID (echoed or generated) |
| `X-Response-Time-Ms`  | Server-side processing time |
| `X-Debug-*`           | Present only when `X-Debug-Mode: true` |

## Status Code Catalog

| Code | Meaning | Triggered by |
|---|---|---|
| 200  | OK                    | Default success path |
| 400  | Bad Request           | Malformed query / business rule |
| 401  | Unauthorized          | Missing Authorization header |
| 402  | Payment Required      | `X-Scenario: declined` |
| 403  | Forbidden             | Wrong token |
| 404  | Not Found             | Unknown `/mock/*` path |
| 405  | Method Not Allowed    | Wrong HTTP verb |
| 413  | Payload Too Large     | Body > `MAX_PAYLOAD_BYTES` |
| 415  | Unsupported Media     | Wrong Content-Type |
| 422  | Validation Error      | Pydantic / JSON parse |
| 429  | Too Many Requests     | Rate limit exceeded |
| 500  | Internal Server Error | Unhandled exception |
| 502  | Bad Gateway           | Failure simulation |
| 503  | Service Unavailable   | `?status=503` or scenario rule |
| 504  | Gateway Timeout       | `X-Scenario: timeout` |

## Standard Error Body

```json
{
  "error": "validation_error",
  "detail": "field 'amount' must be > 0",
  "correlation_id": "8f3c2..."
}
```

## Sample Bodies

### `/health`
```json
{ "status": "ok", "uptime_seconds": 142.7, "version": "1.0.0" }
```

### `/metrics`
```json
{
  "requests_total": 250,
  "requests_by_status": { "200": 220, "503": 10, "401": 20 },
  "requests_by_endpoint": { "GET /health": 50, "POST /mock/payment": 100 },
  "uptime_seconds": 600.5,
  "memory_mb": 145.2
}
```

### `/mock/payment` success
```json
{ "status": "ok", "message": "payment processed" }
```
