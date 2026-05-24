class YOLOv8PatientDetector:
    def __init__(self, engine_path: str = "app/ai_models/patient_detection/model.engine") -> None:
        self.engine_path = engine_path
        self.runtime = "tensorrt-placeholder"

    def detect(self, frame, context: dict | None = None) -> list[dict]:
        context = context or {}
        box = context.get("patient_box") or (180, 180, 540, 360)
        confidence = 0.96 if context.get("patient_visible", True) else 0.0
        if confidence == 0:
            return []
        return [{"label": "patient", "confidence": confidence, "box": box}]
