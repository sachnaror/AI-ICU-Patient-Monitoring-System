import cv2

from app.video_processing.overlay_renderer import draw_overlay


class StreamOutputOperator:
    def render_jpeg(self, frame, telemetry: dict, detections: list[dict]) -> bytes:
        rendered = draw_overlay(frame.copy(), telemetry, detections)
        ok, encoded = cv2.imencode(".jpg", rendered, [int(cv2.IMWRITE_JPEG_QUALITY), 82])
        if not ok:
            return b""
        return encoded.tobytes()
