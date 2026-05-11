#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p logs
[ -f .env ] || cp .env.example .env

if [ -f server.pid ] && kill -0 "$(cat server.pid)" 2>/dev/null; then
  echo "already running (pid $(cat server.pid))"
  exit 0
fi

WORKERS="${WORKER_COUNT:-2}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

nohup uvicorn app.main:app \
  --host "$HOST" --port "$PORT" \
  --workers "$WORKERS" \
  --loop uvloop --http httptools \
  > logs/uvicorn.out 2>&1 &

echo $! > server.pid
echo "started pid $(cat server.pid) on $HOST:$PORT"
