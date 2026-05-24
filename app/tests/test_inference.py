import numpy as np

from app.ai_models.patient_detection.yolov8_detector import YOLOv8PatientDetector
from app.ai_models.pose_estimation.fall_detection import detect_fall_from_pose


def test_patient_detector_returns_detection():
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    detections = YOLOv8PatientDetector().detect(frame, {"patient_box": (10, 20, 100, 140)})
    assert detections[0]["label"] == "patient"
    assert detections[0]["box"] == (10, 20, 100, 140)


def test_fall_detection_from_horizontal_pose():
    result = detect_fall_from_pose({"orientation": "horizontal", "center_y": 390})
    assert result["fall_detected"] is True
