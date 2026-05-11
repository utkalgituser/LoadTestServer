#!/usr/bin/env bash
# Quick benchmark using k6. Outputs summary to load/results/.
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p load/results
TS=$(date +%Y-%m-%d_%H-%M-%S)

if ! command -v k6 >/dev/null 2>&1; then
  echo "install k6 first: https://k6.io/docs/getting-started/installation/"
  exit 1
fi

k6 run --summary-export "load/results/bench-${TS}.json" load/k6/load_test.js
echo "results -> load/results/bench-${TS}.json"
