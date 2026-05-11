# LoadTest Mock Server

Lightweight, async FastAPI HTTP mock & failure-simulation server for **API mocking, QA, integration testing, Postman sanity, and lightweight k6/JMeter load testing**. Runs on an 8 GB laptop. ~60 MB image.

[![Source](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/utkalgituser/LoadTestServer)

---

## Quick Start

```bash
docker run -d -p 8000:8000 --name loadtest-mockserver utkalbarik/loadtest-mockserver:latest
curl http://localhost:8000/health
```

Open http://localhost:8000/docs for Swagger UI.

### docker-compose

```yaml
services:
  loadtest-mockserver:
    image: utkalbarik/loadtest-mockserver:latest
    container_name: loadtest-mockserver
    ports:
      - "8000:8000"
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.5"
```

---

## Tags

| Tag | Description |
|---|---|
| `latest` | Most recent stable build |
| `1.0.0`  | Pinned semantic version |

Image: `linux/amd64` · Base: `python:3.12-slim` · Runs as non-root user `app`.

---

## Features

- Dynamic 1XX–5XX response simulation via query / header / body
- **Config-driven mocks** (`scenarios.yaml`) with **hot reload**
- Configurable delays, timeouts, auth failures
- Auto-generated **OpenAPI / Swagger** at `/docs`
- Structured JSON logs + correlation IDs
- Built-in rate limiting, payload limits, gzip
- Async / non-blocking (Uvicorn + uvloop + httptools)
- Postman collection + k6 script + JMeter plan in source repo

---

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET  | `/`              | Service index |
| GET  | `/health`        | Liveness probe (Docker healthcheck) |
| GET  | `/metrics`       | Runtime counters |
| GET  | `/status?code=N` | Echo any 1XX–5XX |
| GET  | `/config`        | View runtime config |
| POST | `/config/reload` | Hot-reload `scenarios.yaml` |
| ANY  | `/mock/{path}`   | Config-driven mock dispatcher |
| GET  | `/auth/mock`     | Bearer-token validation |
| GET  | `/delay/mock?ms=N`     | Configurable delay (0–60000 ms) |
| GET  | `/failure/mock?code=N` | Force failure status |
| GET  | `/docs`          | Swagger UI |
| GET  | `/openapi.json`  | OpenAPI 3.x spec |

---

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

### 3-second async delay
```bash
curl http://localhost:8000/delay/mock?ms=3000
```

### Authorized request
```bash
curl -H "Authorization: Bearer test-token-12345" http://localhost:8000/auth/mock
```

---

## Configuration (env vars)

| Variable | Default | Purpose |
|---|---|---|
| `HOST`               | `0.0.0.0`   | Bind address |
| `PORT`               | `8000`      | Listen port |
| `WORKER_COUNT`       | `2`         | Uvicorn workers |
| `LOG_LEVEL`          | `INFO`      | DEBUG/INFO/WARNING/ERROR |
| `LOG_JSON`           | `true`      | Toggle JSON log format |
| `MAX_PAYLOAD_BYTES`  | `1048576`   | Body size cap (1 MB) |
| `TIMEOUT_SECONDS`    | `30`        | Per-request timeout |
| `RATE_LIMIT_GLOBAL`  | `500/minute`| Server-wide cap |
| `RATE_LIMIT_PER_IP`  | `100/minute`| Per source IP |
| `RATE_LIMIT_AUTH`    | `20/minute` | Auth endpoint cap |
| `MOCK_AUTH_TOKEN`    | `test-token-12345` | Valid bearer token |
| `ENABLE_GZIP`        | `true`      | Gzip responses ≥ 1 KB |
| `SCENARIOS_HOT_RELOAD` | `true`    | Watch `scenarios.yaml` |

Override via `-e KEY=value` or `--env-file .env`:

```bash
docker run -d -p 8000:8000 \
  -e WORKER_COUNT=4 \
  -e RATE_LIMIT_GLOBAL=10000/minute \
  -e LOG_LEVEL=WARNING \
  utkalbarik/loadtest-mockserver:latest
```

---

## Custom Scenarios

Mount your own `scenarios.yaml` over the default:

```bash
docker run -d -p 8000:8000 \
  -v $(pwd)/scenarios.yaml:/app/app/engine/scenarios.yaml:ro \
  utkalbarik/loadtest-mockserver:latest
```

`scenarios.yaml` example:

```yaml
mocks:
  - path: /mock/payment
    methods: [POST]
    rules:
      - when: { header: { X-Scenario: success } }
        respond: { status: 200, delay_ms: 50, body: { status: ok } }
      - when: { header: { X-Scenario: declined } }
        respond: { status: 402, body: { reason: insufficient funds } }
      - when: { query: { status: "503" } }
        respond: { status: 503 }
    default:
      respond: { status: 200, body: { status: ok } }
```

Edit and `POST /config/reload` (or save the file when watcher is enabled) — no restart.

---

## Capacity Baseline (8 GB / dual-core laptop)

Reference: 2 workers, INFO logs, loopback, default rate limits raised.

| Endpoint | RPS sustained | P95 |
|---|---:|---:|
| `/health`                   | 8 000 | 3 ms   |
| `/mock/*` static JSON       | 3 500 | 12 ms  |
| `/mock/*` with validation   | 2 000 | 18 ms  |
| `/mock/*` with 100 ms delay | 180   | 130 ms |
| `/failure/mock`             | 3 000 | 15 ms  |

Memory: idle 120 MB · peak under stress ~450 MB. Image disk: 259 MB. Compressed pull: ~62 MB.

Recommended testing windows:

| Mode | VU | RPS | Duration | Expected |
|---|---:|---:|---|---|
| Smoke    | 1–5 | 5    | 1 min  | All 200 OK |
| Sanity   | 25  | 50   | 5 min  | <1 % errors |
| Light    | 50  | 200  | 10 min | <2 %, P95 < 50 ms |
| Moderate | 100 | 400  | 10 min | <5 %, P95 < 100 ms |
| Stress   | 200 | 800  | 5 min  | Some 429s expected |

---

## Health Check

Image ships with built-in healthcheck (`curl -f /health` every 30 s).

```bash
docker inspect --format='{{.State.Health.Status}}' loadtest-mockserver
```

---

## Logs

```bash
docker logs -f loadtest-mockserver
# or persist:
docker run -v $(pwd)/logs:/app/logs ...
```

Files inside container at `/app/logs/`:
- `server-YYYY-MM-DD_*.log` — all levels
- `error-YYYY-MM-DD_*.log`  — ERROR+
- `access-YYYY-MM-DD_*.log` — one line per request

---

## Security

- Runs as non-root user (`app`)
- Pydantic input validation
- Payload size limited
- Rate-limited globally + per IP + per sensitive endpoint
- No secrets logged
- Use HTTPS reverse proxy (nginx / Traefik) for non-local deployments

---

## Source & Documentation

- **GitHub:** https://github.com/utkalgituser/LoadTestServer
- **Postman collection:** in `postman/` directory of source repo
- **k6 + JMeter scripts:** in `load/` directory of source repo
- **Full docs:** `docs/` (API_SPEC, REQUEST_SCHEMA, RESPONSE_SCHEMA, Instructions)

---

## License

Internal QA tool. Adapt as needed.

---

**Report issues:** https://github.com/utkalgituser/LoadTestServer/issues
