from pathlib import Path

from app.config import BASE_DIR, settings


class OptionalTensorRTYOLO:
    def __init__(self, engine_path: str | None = None) -> None:
        self.engine_path = Path(engine_path or settings.tensorrt_engine_path)
        if not self.engine_path.is_absolute():
            self.engine_path = BASE_DIR / self.engine_path
        self.enabled = settings.enable_gpu
        self.reason = "ENABLE_GPU=false"
        self._runtime = None

        if not self.enabled:
            return
        if not self.engine_path.exists():
            self.reason = f"TensorRT engine missing: {self.engine_path}"
            return

        try:
            import tensorrt as trt  # type: ignore

            self._runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING))
            self.reason = "TensorRT runtime loaded"
        except Exception as exc:
            self.reason = f"TensorRT unavailable: {exc}"

    @property
    def available(self) -> bool:
        return self._runtime is not None

    def infer(self, frame, context: dict | None = None) -> list[dict] | None:
        if not self.available:
            return None
        # Production code should allocate bindings, copy frame tensors to CUDA,
        # execute the engine, and decode YOLO boxes here.
        return None

    def describe(self) -> dict:
        return {
            "configured": self.enabled,
            "available": self.available,
            "backend": "tensorrt" if self.available else "simulated-yolov8",
            "engine_path": str(self.engine_path),
            "detail": self.reason,
        }
