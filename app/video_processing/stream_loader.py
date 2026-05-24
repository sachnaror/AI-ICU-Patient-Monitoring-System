from pathlib import Path

import cv2

from app.config import BASE_DIR, settings


class StreamLoader:
    def __init__(self) -> None:
        self.capture = None
        self.source_mode = "demo"

    def open(self, mode: str | None = None):
        self.close()
        self.source_mode = mode or ("webcam" if settings.use_webcam else "video")
        if self.source_mode == "webcam":
            self.capture = cv2.VideoCapture(0)
        elif self.source_mode == "video":
            path = Path(settings.video_source)
            if not path.is_absolute():
                path = BASE_DIR / path
            if path.exists():
                self.capture = cv2.VideoCapture(str(path))
            else:
                self.source_mode = "demo"
                self.capture = None
        return self.capture

    def read(self):
        if self.capture is None:
            return False, None
        ok, frame = self.capture.read()
        if not ok and self.source_mode == "video":
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = self.capture.read()
        return ok, frame

    def close(self) -> None:
        if self.capture is not None:
            self.capture.release()
            self.capture = None
