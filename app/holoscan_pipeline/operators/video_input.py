from app.video_processing.opencv_utils import synthetic_icu_frame
from app.video_processing.stream_loader import StreamLoader


class VideoInputOperator:
    def __init__(self) -> None:
        self.loader = StreamLoader()
        self.frame_index = 0
        self.loader.open()

    def switch_source(self, mode: str) -> None:
        self.loader.open(mode)

    def read(self):
        self.frame_index += 1
        if self.loader.source_mode == "demo":
            return synthetic_icu_frame(self.frame_index)

        ok, frame = self.loader.read()
        if not ok:
            return synthetic_icu_frame(self.frame_index)
        return frame, {"fall_phase": False, "spo2": 97, "heart_rate": 76}

    def close(self) -> None:
        self.loader.close()
