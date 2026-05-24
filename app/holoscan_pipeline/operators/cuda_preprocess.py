from app.video_processing.frame_resize import resize_frame


class CUDAPreprocessOperator:
    def preprocess(self, frame):
        return resize_frame(frame, width=960)
