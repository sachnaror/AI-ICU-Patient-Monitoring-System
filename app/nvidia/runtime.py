from dataclasses import dataclass
from importlib.util import find_spec

from app.config import BASE_DIR, settings
from app.utils.gpu_metrics import read_gpu_metrics


@dataclass(frozen=True)
class NvidiaRuntimeStatus:
    name: str
    configured: bool
    available: bool
    backend: str
    detail: str


def package_available(package_name: str) -> bool:
    return find_spec(package_name) is not None


def engine_exists() -> bool:
    path = BASE_DIR / settings.tensorrt_engine_path
    return path.exists()


def runtime_status() -> dict:
    gpu = read_gpu_metrics()
    cuda_ready = settings.enable_gpu and gpu["available"]
    statuses = [
        NvidiaRuntimeStatus(
            "Holoscan",
            settings.enable_holoscan,
            settings.enable_holoscan and package_available("holoscan"),
            "nvidia-holoscan",
            "Optional graph orchestration. CPU scheduler is active when unavailable.",
        ),
        NvidiaRuntimeStatus(
            "CUDA Preprocess",
            settings.enable_gpu,
            cuda_ready,
            "cuda",
            "Optional GPU frame preprocessing. OpenCV CPU resize is active when unavailable.",
        ),
        NvidiaRuntimeStatus(
            "DeepStream",
            settings.enable_deepstream,
            settings.enable_deepstream and package_available("gi"),
            "gstreamer/deepstream",
            "Optional RTSP/multi-camera ingest. OpenCV input is active when unavailable.",
        ),
        NvidiaRuntimeStatus(
            "TensorRT YOLOv8",
            settings.enable_gpu,
            cuda_ready and engine_exists(),
            "tensorrt",
            "Optional TensorRT engine inference. Simulated detector is active when unavailable.",
        ),
        NvidiaRuntimeStatus(
            "Triton",
            settings.enable_triton,
            settings.enable_triton and package_available("tritonclient"),
            "triton-grpc",
            "Optional remote model serving. Local detector is active when unavailable.",
        ),
    ]
    return {
        "gpu": gpu,
        "components": [status.__dict__ for status in statuses],
        "active_acceleration": [status.name for status in statuses if status.available],
    }
