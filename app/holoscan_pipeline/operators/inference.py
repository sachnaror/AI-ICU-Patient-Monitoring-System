from app.ai_models.patient_detection.yolov8_detector import YOLOv8PatientDetector
from app.ai_models.triton.triton_client import TritonInferenceClient
from app.nvidia.tensorrt_yolo_impl import OptionalTensorRTYOLO


class TensorRTInferenceOperator:
    def __init__(self) -> None:
        self.detector = YOLOv8PatientDetector()
        self.tensorrt = OptionalTensorRTYOLO()
        self.triton = TritonInferenceClient()

    def infer(self, frame, context: dict) -> list[dict]:
        triton_result = self.triton.infer(frame)
        if triton_result is not None:
            return triton_result

        tensorrt_result = self.tensorrt.infer(frame, context)
        if tensorrt_result is not None:
            return tensorrt_result

        return self.detector.detect(frame, context)

    def describe(self) -> dict:
        return {
            "triton": self.triton.describe(),
            "tensorrt": self.tensorrt.describe(),
            "fallback": {"backend": self.detector.runtime, "available": True},
        }
