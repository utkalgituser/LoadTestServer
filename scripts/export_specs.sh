#!/usr/bin/env bash
# Pull OpenAPI from running server and regenerate Postman collection + k6 stub.
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${PORT:-8000}"
mkdir -p out postman load/k6

curl -fsS "http://localhost:${PORT}/openapi.json" -o out/openapi.json
echo "openapi -> out/openapi.json"

if command -v openapi2postmanv2 >/dev/null 2>&1; then
  openapi2postmanv2 -s out/openapi.json -o postman/collection.json -p
  echo "postman -> postman/collection.json"
else
  echo "skip postman: install with 'npm i -g openapi-to-postmanv2'"
fi

if command -v openapi-generator-cli >/dev/null 2>&1; then
  openapi-generator-cli generate -i out/openapi.json -g k6 -o load/k6/generated/
  echo "k6 -> load/k6/generated/"
else
  echo "skip k6 gen: install openapi-generator-cli (optional, manual k6 script provided)"
fi
