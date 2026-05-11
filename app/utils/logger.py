import logging
import logging.handlers
import sys
from datetime import datetime
from pathlib import Path
from pythonjsonlogger import json as jsonlogger

from app.config import get_settings

_initialized = False


def setup_logging() -> None:
    global _initialized
    if _initialized:
        return

    s = get_settings()
    log_dir = Path(s.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    app_log = log_dir / f"server-{ts}.log"
    err_log = log_dir / f"error-{ts}.log"
    acc_log = log_dir / f"access-{ts}.log"

    fmt = "%(asctime)s %(levelname)s %(name)s %(correlation_id)s %(message)s"
    formatter = jsonlogger.JsonFormatter(fmt) if s.LOG_JSON else logging.Formatter(fmt)

    root = logging.getLogger()
    root.setLevel(s.LOG_LEVEL)
    root.handlers.clear()

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root.addHandler(console)

    app_h = logging.handlers.TimedRotatingFileHandler(app_log, when="midnight", backupCount=7, encoding="utf-8")
    app_h.setFormatter(formatter)
    root.addHandler(app_h)

    err_h = logging.handlers.TimedRotatingFileHandler(err_log, when="midnight", backupCount=7, encoding="utf-8")
    err_h.setLevel(logging.ERROR)
    err_h.setFormatter(formatter)
    root.addHandler(err_h)

    access = logging.getLogger("access")
    access.setLevel(logging.INFO)
    access.propagate = False
    acc_h = logging.handlers.TimedRotatingFileHandler(acc_log, when="midnight", backupCount=7, encoding="utf-8")
    acc_h.setFormatter(formatter)
    access.addHandler(acc_h)
    access.addHandler(console)

    _initialized = True


class CorrelationFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        from asgi_correlation_id import correlation_id
        cid = correlation_id.get() or "-"
        record.correlation_id = cid
        return True
