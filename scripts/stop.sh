#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f server.pid ]; then
  echo "no pid file"
  exit 0
fi

PID=$(cat server.pid)
if kill -0 "$PID" 2>/dev/null; then
  kill -TERM "$PID"
  for i in $(seq 1 10); do
    kill -0 "$PID" 2>/dev/null || break
    sleep 1
  done
  kill -0 "$PID" 2>/dev/null && kill -KILL "$PID" || true
  echo "stopped $PID"
else
  echo "stale pid $PID"
fi
rm -f server.pid
