from app.config import settings
from app.utils.gpu_metrics import read_gpu_metrics
from app.video_processing.frame_resize import resize_frame


class OptionalCUDAPreprocessor:
    def __init__(self, width: int = 960) -> None:
        self.width = width
        self.gpu = read_gpu_metrics()
        self.enabled = settings.enable_gpu
        self.reason = "ENABLE_GPU=false" if not self.enabled else "CUDA Python/OpenCV CUDA unavailable"

    @property
    def available(self) -> bool:
        return self.enabled and self.gpu["available"]

    def preprocess(self, frame):
        if not self.available:
            return resize_frame(frame, width=self.width)

        try:
            import cv2

            gpu_frame = cv2.cuda_GpuMat()
            gpu_frame.upload(frame)
            ratio = self.width / float(frame.shape[1])
            resized = cv2.cuda.resize(gpu_frame, (self.width, int(frame.shape[0] * ratio)))
            return resized.download()
        except Exception:
            return resize_frame(frame, width=self.width)

    def describe(self) -> dict:
        return {
            "configured": self.enabled,
            "available": self.available,
            "backend": "opencv-cuda" if self.available else "opencv-cpu",
            "detail": "CUDA preprocess active" if self.available else self.reason,
        }
