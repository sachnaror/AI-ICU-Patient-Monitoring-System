import cv2


def draw_overlay(frame, telemetry: dict, detections: list[dict]):
    severity = telemetry.get("severity", "normal")
    color = (30, 210, 90) if severity == "normal" else (0, 90, 255)

    for detection in detections:
        x1, y1, x2, y2 = detection["box"]
        label = f"{detection['label']} {int(detection['confidence'] * 100)}%"
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.rectangle(frame, (x1, max(0, y1 - 28)), (x1 + 170, y1), color, -1)
        cv2.putText(frame, label, (x1 + 8, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)

    status = "CRITICAL" if telemetry.get("fall_detected") else "MONITORING"
    cv2.putText(frame, status, (34, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.putText(frame, f"FPS {telemetry.get('fps', 0)}", (805, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (220, 225, 230), 2)
    return frame
