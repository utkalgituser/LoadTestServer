import asyncio
import logging
from pathlib import Path
from typing import Any
import yaml
from fastapi import Request
from fastapi.responses import JSONResponse

from app.config import get_settings

log = logging.getLogger(__name__)


class ScenarioStore:
    def __init__(self, path: str):
        self.path = Path(path)
        self.mocks: list[dict[str, Any]] = []
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            log.warning(f"scenarios file missing: {self.path}")
            self.mocks = []
            return
        with self.path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        self.mocks = data.get("mocks", [])
        log.info(f"loaded {len(self.mocks)} mock definitions from {self.path}")

    def find(self, path: str, method: str) -> dict[str, Any] | None:
        for m in self.mocks:
            if m["path"] == path and method.upper() in [x.upper() for x in m.get("methods", ["GET"])]:
                return m
        return None


_store: ScenarioStore | None = None


def get_store() -> ScenarioStore:
    global _store
    if _store is None:
        _store = ScenarioStore(get_settings().SCENARIOS_FILE)
    return _store


def reload_scenarios() -> int:
    s = get_store()
    s.load()
    return len(s.mocks)


def _match_rule(rule: dict[str, Any], request: Request, body: dict[str, Any] | None) -> bool:
    when = rule.get("when", {})
    if not when:
        return False

    hdr = when.get("header")
    if hdr:
        for k, v in hdr.items():
            if request.headers.get(k) != str(v):
                return False

    qry = when.get("query")
    if qry:
        for k, v in qry.items():
            if request.query_params.get(k) != str(v):
                return False

    body_match = when.get("body")
    if body_match and body:
        for k, v in body_match.items():
            if body.get(k) != v:
                return False

    return True


async def build_response(mock: dict[str, Any], request: Request, body: dict[str, Any] | None) -> JSONResponse:
    chosen = None
    for rule in mock.get("rules", []):
        if _match_rule(rule, request, body):
            chosen = rule.get("respond")
            break
    if chosen is None:
        chosen = mock.get("default", {}).get("respond", {"status": 200, "body": {}})

    delay = chosen.get("delay_ms", 0)
    if delay > 0:
        await asyncio.sleep(delay / 1000)

    headers = chosen.get("headers", {})
    if request.headers.get("X-Debug-Mode") == "true":
        headers["X-Debug-Matched-Rule"] = "true"
        headers["X-Debug-Path"] = mock["path"]

    return JSONResponse(
        status_code=chosen.get("status", 200),
        content=chosen.get("body", {}),
        headers=headers,
    )
