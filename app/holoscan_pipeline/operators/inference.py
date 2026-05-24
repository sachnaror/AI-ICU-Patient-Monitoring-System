from app.ai_models.patient_detection.yolov8_detector import YOLOv8PatientDetector


class TensorRTInferenceOperator:
    def __init__(self) -> None:
        self.detector = YOLOv8PatientDetector()

    def infer(self, frame, context: dict) -> list[dict]:
        return self.detector.detect(frame, context)
