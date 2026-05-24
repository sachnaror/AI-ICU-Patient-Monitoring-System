from app.config import settings


class OptionalHoloscanOrchestrator:
    def __init__(self) -> None:
        self.enabled = settings.enable_holoscan
        self.reason = "ENABLE_HOLOSCAN=false"
        self._app = None

        if not self.enabled:
            return

        try:
            from holoscan.core import Application  # type: ignore

            self._app = Application()
            self.reason = "Holoscan SDK loaded"
        except Exception as exc:
            self.reason = f"Holoscan unavailable: {exc}"

    @property
    def available(self) -> bool:
        return self._app is not None

    def describe(self) -> dict:
        return {
            "configured": self.enabled,
            "available": self.available,
            "backend": "nvidia-holoscan" if self.available else "cpu-thread-scheduler",
            "detail": self.reason,
        }
