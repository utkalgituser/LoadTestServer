import logging
from pathlib import Path
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

from app.engine.response_builder import reload_scenarios

log = logging.getLogger(__name__)


class _Handler(FileSystemEventHandler):
    def __init__(self, target: Path):
        self.target = target.resolve()

    def on_modified(self, event: FileSystemEvent) -> None:
        try:
            if Path(event.src_path).resolve() == self.target:
                count = reload_scenarios()
                log.info(f"scenarios reloaded: {count} mocks")
        except Exception as e:
            log.error(f"reload failed: {e}")


def start_watcher(scenarios_path: str) -> Observer:
    p = Path(scenarios_path)
    obs = Observer()
    obs.schedule(_Handler(p), str(p.parent), recursive=False)
    obs.start()
    log.info(f"watching {p} for changes")
    return obs
