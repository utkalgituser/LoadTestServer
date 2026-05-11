# Request Schemas

Authoritative definitions live in `app/schemas/common.py` (Pydantic) and are exported in `/openapi.json`.

## Headers

| Header | Type | Required | Notes |
|---|---|---|---|
| `Authorization`  | string | only on `/auth/mock` | Format `Bearer <token>`. Default token: `test-token-12345`. |
| `Content-Type`   | string | POST/PUT/PATCH | Use `application/json` |
| `X-Request-ID`   | UUID   | optional | Auto-generated if missing; echoed in response |
| `X-Scenario`     | string | optional | Drives `/mock/*` rule matching: `success`, `declined`, `timeout`, ... |
| `X-Debug-Mode`   | bool   | optional | `true` adds `X-Debug-*` headers in response |

## Query Parameters

| Endpoint | Param | Type | Default | Notes |
|---|---|---|---|---|
| `/status`        | `code` | int 100–599 | 200 | Echo status |
| `/delay/mock`    | `ms`   | int 0–60000 | 1000 | Capped at `TIMEOUT_SECONDS * 1000` |
| `/failure/mock`  | `code` | int (one of `FAILURES`) | random | See router for list |
| `/mock/{path}`   | `status` | int | — | Optional rule trigger |

## Request Body — `/mock/payment` (validated example)

```json
{
  "transactionId": "TXN12345",
  "amount": 1000.50,
  "currency": "USD",
  "metadata": { "userId": "u-1" }
}
```

| Field | Type | Required | Constraint |
|---|---|---|---|
| `transactionId` | string | yes | length 3–64 |
| `amount`        | number | yes | > 0 |
| `currency`      | string | yes | regex `^[A-Z]{3}$` |
| `metadata`      | object | no  | free-form |

Other `/mock/*` endpoints accept any JSON body (forwarded to rule matcher).

## Validation Errors

| Condition | Status | Body |
|---|---|---|
| Missing required field | 422 | `{ "error": "validation_error", "detail": [...] }` |
| Invalid JSON           | 422 | `{ "error": "invalid_json" }` |
| Payload > 1 MB         | 413 | `{ "error": "payload_too_large" }` |
| Missing Authorization  | 401 | `{ "error": "missing Authorization header" }` |
| Wrong token            | 403 | `{ "error": "invalid token" }` |
| Unknown mock path      | 404 | `{ "error": "mock_not_found" }` |
| Method not allowed     | 405 | FastAPI default |
| Rate limit exceeded    | 429 | `{ "error": "Rate limit exceeded: ..." }` |
