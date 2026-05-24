import platform

from app.nvidia.runtime import runtime_status
from app.utils.gpu_metrics import read_gpu_metrics


def get_system_health() -> dict:
    gpu = read_gpu_metrics()
    return {
        "status": "ok",
        "runtime": "gpu" if gpu["available"] else "cpu-fallback",
        "gpu": gpu,
        "nvidia": runtime_status(),
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
    }
