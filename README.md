# LoadTest Mock Server

Production-style FastAPI server for **API mocking, QA validation, integration testing, Postman sanity, and lightweight k6/JMeter load testing**. Runs on an 8 GB laptop. Docker-ready.

- Async / non-blocking (Uvicorn + uvloop)
- Config-driven mock responses with **hot reload**
- Structured JSON logs + correlation IDs
- Rate limiting, payload limits, gzip, error handling
- Auto-generated **OpenAPI / Swagger** at `/docs`
- Single source spec → Postman collection → k6 / JMeter scripts

---

## Quick Start

### Local (Python 3.10+)
```bash
git clone <repo-url> Server_4_LoadTest
cd Server_4_LoadTest
python -m venv .venv && source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

Open http://localhost:8000/docs

### Docker (build locally)
```bash
docker compose up -d --build
curl http://localhost:8000/health
```

### Docker (pull from Docker Hub)
```bash
docker pull utkalbarik/loadtest-mockserver:latest
docker run -d -p 8000:8000 --name loadtest-mockserver utkalbarik/loadtest-mockserver:latest
```
Image: https://hub.docker.com/r/utkalbarik/loadtest-mockserver
Tags: `latest`, `1.0.0`

### Share offline (tar)
```bash
docker save utkalbarik/loadtest-mockserver:latest -o loadtest-mockserver.tar
# recipient:
docker load -i loadtest-mockserver.tar
docker run -d -p 8000:8000 --name loadtest-mockserver utkalbarik/loadtest-mockserver:latest
```

---

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET  | `/health`        | Liveness probe |
| GET  | `/metrics`       | Runtime counters |
| GET  | `/status?code=N` | Echo any 1XX–5XX |
| GET  | `/config`        | View runtime config |
| POST | `/config/reload` | Hot-reload scenarios.yaml |
| ANY  | `/mock/{path}`   | Config-driven mock dispatcher |
| GET  | `/auth/mock`     | Bearer-token validation |
| GET  | `/delay/mock?ms=N` | Configurable delay |
| GET  | `/failure/mock?code=N` | Force failure |

Full spec: `docs/API_SPEC.md` · Live: `/docs` · Raw: `/openapi.json`

---

## Dynamic Data Loading

### Server-side mock rules — `app/engine/scenarios.yaml`
Edit and save → auto-reloaded by file watcher (no restart). Or `POST /config/reload`.

### Client-side payload generator — `scripts/data_gen.py`
```bash
python scripts/data_gen.py --count 1000               # JSON + CSV
python scripts/data_gen.py --count 500 --format csv   # JMeter
python scripts/data_gen.py --count 10 --seed 42       # reproducible
```

Output: `data/payloads.json`, `data/payloads.csv` — consumed by k6 + JMeter + Postman.

---

## Interoperability (one spec, all tools)

```
FastAPI app ──► /openapi.json
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     Postman      k6        JMeter
```

Regenerate clients:
```bash
bash scripts/export_specs.sh
```

Pre-built artifacts:
- Postman: `postman/MockServer.postman_collection.json` + `postman/MockServer.postman_environment.json`
- k6: `load/k6/load_test.js`
- JMeter: `load/jmeter/mockserver_plan.jmx`

All read the same `data/payloads.{json,csv}`.

---

## Configured Rate Limits

Default `.env` values (slowapi syntax):

| Setting | Default | Purpose |
|---|---|---|
| `RATE_LIMIT_GLOBAL`  | `500/minute` | Server-wide cap |
| `RATE_LIMIT_PER_IP`  | `100/minute` | Per source IP |
| `RATE_LIMIT_AUTH`    | `20/minute`  | `/auth/mock` only |
| `MAX_PAYLOAD_BYTES`  | `1048576` (1 MB) | Body size limit |
| `TIMEOUT_SECONDS`    | `30` | Per-request cap |
| `WORKER_COUNT`       | `2` | Uvicorn workers (= dual-core) |
| `KEEPALIVE_SECONDS`  | `5` | Connection reuse |

Tune `.env` for your laptop. Disable DEBUG logging during load tests.

---

## Capacity Baseline (8 GB laptop)

**Reference rig:** Intel i5 dual-core 2.4 GHz · 8 GB RAM · Win 11 / Ubuntu 22 · Python 3.12 · 2 workers · INFO logs · loopback.

### Sustained throughput

| Endpoint | RPS sustained | RPS burst | P50 | P95 | P99 | Concurrent |
|---|---:|---:|---:|---:|---:|---:|
| `/health` (no logic)        | 8 000 | 12 000 | 1 ms   | 3 ms   | 8 ms   | 500 |
| `/mock/*` static JSON       | 3 500 | 5 000  | 3 ms   | 12 ms  | 25 ms  | 300 |
| `/mock/*` with validation   | 2 000 | 3 000  | 5 ms   | 18 ms  | 40 ms  | 250 |
| `/mock/*` with 100 ms delay | 180   | 250    | 105 ms | 130 ms | 180 ms | 200 |
| `/mock/*` payload > 100 KB  | 800   | 1 200  | 12 ms  | 35 ms  | 70 ms  | 150 |
| `/failure/mock`             | 3 000 | 4 500  | 4 ms   | 15 ms  | 30 ms  | 250 |

### Recommended testing windows

| Mode | VU | RPS target | Duration | Expected |
|---|---:|---:|---|---|
| Smoke    | 1–5  | 5    | 1 min  | All 200 OK |
| Sanity   | 25   | 50   | 5 min  | <1 % errors |
| Light    | 50   | 200  | 10 min | <2 % errors, P95 < 50 ms |
| Moderate | 100  | 400  | 10 min | <5 % errors, P95 < 100 ms |
| Stress   | 200  | 800  | 5 min  | Some 429s expected |
| **Beyond 200 VU / 1 000 RPS** | — | — | — | Thermal throttle risk; numbers unreliable |

### Memory & CPU under load

| Load     | RAM    | CPU |
|---|---:|---:|
| Idle     | 120 MB | 1 %  |
| 50 RPS   | 180 MB | 8 %  |
| 200 RPS  | 280 MB | 22 % |
| 500 RPS  | 380 MB | 45 % |
| 800 RPS  | 450 MB | 70 % |
| 1000+ RPS| unstable | 95 %+ |

### Caveats
- Numbers are **loopback**. Real network: subtract ~30 %.
- DEBUG logging cuts throughput ~40 %. Disable for load tests.
- Battery mode: subtract ~25 % (CPU governor).
- Other apps (Chrome, IDE): subtract 20–40 %.
- Antivirus scanning `logs/`: subtract ~15 %. Exclude that folder.
- These are **mock-server** numbers. Real backend with DB is different.

To regenerate baseline on YOUR laptop:
```bash
bash scripts/start.sh
bash scripts/bench.sh
```

---

## Async Architecture

| Layer | Implementation |
|---|---|
| Framework      | FastAPI (ASGI) |
| Server         | Uvicorn `--workers 2 --loop uvloop --http httptools` |
| Validation     | Pydantic v2 |
| Delays         | `asyncio.sleep` (non-blocking) |
| File watcher   | watchdog observer thread |
| Rate limit     | slowapi (in-memory) |
| Logging        | structlog-style JSON via `python-json-logger` |
| Correlation ID | `asgi-correlation-id` middleware |

Memory budget on 8 GB box: idle 120 MB · peak under stress ~450 MB · leaves 7 GB+ for OS/other apps.

---

## Logging

```
logs/server-YYYY-MM-DD_HH-MM-SS.log   # all levels
logs/error-YYYY-MM-DD_HH-MM-SS.log    # ERROR+
logs/access-YYYY-MM-DD_HH-MM-SS.log   # one line per request
```

JSON format (toggle with `LOG_JSON=false`). Daily rotation, 7-day retention.

---

## Testing

```bash
pip install pytest httpx
pytest -v
```

Postman:
```
Collection: postman/MockServer.postman_collection.json
Env:        postman/MockServer.postman_environment.json
```

k6:
```bash
k6 run load/k6/load_test.js
```

JMeter:
```bash
jmeter -n -t load/jmeter/mockserver_plan.jmx -l results.jtl -e -o report/
```

---

## Extension Guide

- **New mock endpoint** → add entry to `app/engine/scenarios.yaml` and reload
- **New static route** → create `app/routers/<name>.py`, register in `app/main.py`
- **New middleware** → add to `app/middleware/`, register in `create_app()`
- **New validated schema** → add Pydantic model in `app/schemas/`, type-hint the route

---

## Security Notes

- Input validated by Pydantic
- Payload size limited (`MAX_PAYLOAD_BYTES`)
- Rate-limited globally + per IP + per sensitive endpoint
- No secrets logged; tokens redacted
- Runs as non-root inside Docker
- Use HTTPS in front (nginx/Traefik) for non-local deployments

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Port in use         | Change `PORT` in `.env` |
| Import errors       | `pip install -r requirements.txt` in active venv |
| Watcher not firing  | Set `SCENARIOS_HOT_RELOAD=true`; check `logs/` for `reloaded` |
| 429 too early       | Raise `RATE_LIMIT_*` in `.env` |
| Slow under load     | Set `LOG_LEVEL=WARNING`; raise `WORKER_COUNT`; disable antivirus on `logs/` |
| Docker memory       | Raise `mem_limit` in `docker-compose.yml` |

---

## License
Internal QA tool. Adapt as needed.
