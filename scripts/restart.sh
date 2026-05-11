#!/usr/bin/env bash
set -euo pipefail
DIR="$(dirname "$0")"
"$DIR/stop.sh" || true
sleep 1
"$DIR/start.sh"
