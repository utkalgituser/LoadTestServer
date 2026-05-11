# Operating Instructions

## First-time setup

```bash
cd /d/Data4Tests/Server_4_LoadTest
python -m venv .venv
source .venv/Scripts/activate     # Windows Git Bash
# or:  .\.venv\Scripts\Activate.ps1   (PowerShell)
pip install -r requirements.txt
cp .env.example .env
```

## Run (local Python)

```bash
# foreground
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2

# background (Linux/macOS/Git Bash)
bash scripts/start.sh
bash scripts/status.sh
bash scripts/stop.sh

# background (Windows PowerShell)
powershell -File scripts\start.ps1
powershell -File scripts\status.ps1
powershell -File scripts\stop.ps1
```

## Run (Docker)

```bash
docker compose up -d --build
docker compose logs -f
docker compose down
```

Image is exportable:
```bash
docker save mockserver:latest -o mockserver.tar
# share the .tar; recipient: docker load -i mockserver.tar
```

## Verify

- Browser: http://localhost:8000/docs
- Health:  `curl http://localhost:8000/health`
- Mock:    `curl -X POST http://localhost:8000/mock/payment -H 'Content-Type: application/json' -d '{}'`

## Generate test data

```bash
python scripts/data_gen.py --count 1000              # both formats
python scripts/data_gen.py --count 500 --format csv  # JMeter
```

## Edit scenarios live

Edit `app/engine/scenarios.yaml` — server auto-reloads (or `POST /config/reload`).

## Run tests

```bash
pip install pytest httpx
pytest -v
```

## Run load tests

```bash
# k6
k6 run load/k6/load_test.js
k6 run --env BASE_URL=http://localhost:8000 load/k6/load_test.js

# JMeter (CLI mode recommended)
jmeter -n -t load/jmeter/mockserver_plan.jmx -l load/results/jmeter.jtl -e -o load/results/html
```
