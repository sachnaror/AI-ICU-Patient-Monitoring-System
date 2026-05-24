from app.config import settings
from app.utils.gpu_metrics import read_gpu_metrics


class ResourceManager:
    def describe(self) -> dict:
        gpu = read_gpu_metrics()
        return {
            "gpu_requested": settings.enable_gpu,
            "gpu_available": gpu["available"],
            "execution_mode": "cuda/tensorrt-ready" if gpu["available"] else "cpu-demo",
            "gpu": gpu,
        }
