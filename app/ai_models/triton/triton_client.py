from app.config import settings


class TritonInferenceClient:
    def __init__(self, url: str | None = None, model_name: str | None = None) -> None:
        self.url = url or settings.triton_url
        self.model_name = model_name or settings.triton_model_name
        self.enabled = settings.enable_triton
        self.reason = "ENABLE_TRITON=false"
        self._client = None

        if not self.enabled:
            return

        try:
            import tritonclient.grpc as grpcclient  # type: ignore

            self._client = grpcclient.InferenceServerClient(url=self.url)
            self.reason = "Triton client initialized"
        except Exception as exc:
            self.reason = f"Triton unavailable: {exc}"

    def is_available(self) -> bool:
        if self._client is None:
            return False
        try:
            return bool(self._client.is_server_live())
        except Exception:
            return False

    def infer(self, frame) -> list[dict] | None:
        if not self.is_available():
            return None
        # Production code should prepare Triton inputs/outputs and decode YOLO boxes here.
        return None

    def describe(self) -> dict:
        return {
            "configured": self.enabled,
            "available": self.is_available(),
            "backend": "triton-grpc" if self.is_available() else "local-detector",
            "url": self.url,
            "model_name": self.model_name,
            "detail": self.reason,
        }
