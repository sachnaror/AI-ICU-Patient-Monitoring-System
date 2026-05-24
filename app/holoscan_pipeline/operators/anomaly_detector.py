class AnomalyDetectorOperator:
    def evaluate(self, detections: list[dict], pose: dict, vitals: dict) -> dict:
        fall_detected = bool(pose.get("fall_detected"))
        patient_visible = bool(detections)
        severity = "critical" if fall_detected or vitals.get("oxygen_status") == "critical" else "normal"
        if vitals.get("oxygen_status") == "warning":
            severity = "warning"
        return {
            "fall_detected": fall_detected,
            "patient_visible": patient_visible,
            "severity": severity,
            "confidence": max((d.get("confidence", 0) for d in detections), default=0),
        }
