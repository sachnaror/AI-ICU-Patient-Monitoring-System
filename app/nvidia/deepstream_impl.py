from app.config import settings


class OptionalDeepStreamInput:
    def __init__(self) -> None:
        self.enabled = settings.enable_deepstream
        self.reason = "ENABLE_DEEPSTREAM=false"
        self._gst = None

        if not self.enabled:
            return

        try:
            import gi  # type: ignore

            gi.require_version("Gst", "1.0")
            from gi.repository import Gst  # type: ignore

            Gst.init(None)
            self._gst = Gst
            self.reason = "GStreamer loaded; configure NVIDIA DeepStream plugins on target host"
        except Exception as exc:
            self.reason = f"DeepStream/GStreamer unavailable: {exc}"

    @property
    def available(self) -> bool:
        return self._gst is not None

    def build_rtsp_pipeline(self, source: str) -> str:
        return (
            f"rtspsrc location={source} latency=100 ! "
            "rtph264depay ! h264parse ! nvv4l2decoder ! "
            "nvstreammux batch-size=1 ! nvinfer ! nvdsosd ! appsink"
        )

    def describe(self) -> dict:
        return {
            "configured": self.enabled,
            "available": self.available,
            "backend": "deepstream-gstreamer" if self.available else "opencv-videocapture",
            "detail": self.reason,
        }
