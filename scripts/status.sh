#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [ -f server.pid ] && kill -0 "$(cat server.pid)" 2>/dev/null; then
  echo "running pid $(cat server.pid)"
else
  echo "stopped"
fi

PORT="${PORT:-8000}"
curl -fsS "http://localhost:${PORT}/health" || echo "health check failed"
