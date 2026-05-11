# API Specification

Master spec auto-generated at `/openapi.json` when server runs.
Open browser to `/docs` for interactive Swagger UI, or `/redoc` for ReDoc.

## Endpoint Summary

| Method | Path | Purpose |
|---|---|---|
| GET  | `/`             | Service index |
| GET  | `/health`       | Liveness probe |
| GET  | `/metrics`      | Runtime counters |
| GET  | `/status`       | Echo arbitrary HTTP status (`?code=503`) |
| GET  | `/config`       | View runtime config |
| POST | `/config/reload`| Hot-reload `scenarios.yaml` |
| ANY  | `/mock/{path}`  | Dynamic mock dispatcher (config-driven) |
| GET  | `/auth/mock`    | Bearer-token validation simulation |
| GET  | `/delay/mock`   | Configurable delay (`?ms=2000`) |
| GET  | `/failure/mock` | Force failure status (`?code=500`) |

## Scenarios (config-driven)

Defined in `app/engine/scenarios.yaml`. Reload via `POST /config/reload` or save the file (auto-reload).

Match order: rules top-to-bottom; first match wins; falls back to `default`.

Match keys:
- `header: { Name: value }`
- `query: { name: value }`
- `body: { field: value }`

Response keys:
- `status`     — int 100–599
- `delay_ms`   — async sleep before response
- `headers`    — dict of response headers
- `body`       — JSON body

## Examples

### Success
```bash
curl -X POST http://localhost:8000/mock/payment \
  -H "Content-Type: application/json" \
  -H "X-Scenario: success" \
  -d '{"transactionId":"TXN1","amount":10,"currency":"USD"}'
```

### Force 503
```bash
curl http://localhost:8000/status?code=503
```

### Delay 3 seconds
```bash
curl http://localhost:8000/delay/mock?ms=3000
```

### Authorized
```bash
curl -H "Authorization: Bearer test-token-12345" http://localhost:8000/auth/mock
```
