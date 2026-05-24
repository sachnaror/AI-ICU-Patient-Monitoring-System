class MediaPipePoseEstimator:
    def estimate(self, detections: list[dict], context: dict | None = None) -> dict:
        context = context or {}
        if not detections:
            return {"orientation": "unknown", "center_y": 0}
        x1, y1, x2, y2 = detections[0]["box"]
        width = x2 - x1
        height = y2 - y1
        orientation = "horizontal" if width > height * 1.6 or context.get("fall_phase") else "vertical"
        return {"orientation": orientation, "center_y": int((y1 + y2) / 2)}
