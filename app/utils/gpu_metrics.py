import shutil
import subprocess


def read_gpu_metrics() -> dict:
    if not shutil.which("nvidia-smi"):
        return {"available": False, "name": "CPU fallback", "utilization": 0, "memory_used_mb": 0}

    try:
        output = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,utilization.gpu,memory.used",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            timeout=2,
        ).strip()
        name, utilization, memory = [part.strip() for part in output.split(",", maxsplit=2)]
        return {
            "available": True,
            "name": name,
            "utilization": int(utilization),
            "memory_used_mb": int(memory),
        }
    except Exception:
        return {"available": False, "name": "GPU metrics unavailable", "utilization": 0, "memory_used_mb": 0}
