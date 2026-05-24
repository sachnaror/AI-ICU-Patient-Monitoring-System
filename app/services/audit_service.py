from threading import Lock


class AuditService:
    def __init__(self) -> None:
        self._events: list[dict] = []
        self._lock = Lock()

    def record(self, event: dict) -> None:
        with self._lock:
            self._events.insert(0, event)
            self._events = self._events[:500]

    def recent(self, limit: int = 50) -> list[dict]:
        with self._lock:
            return self._events[:limit]
