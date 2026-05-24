import cv2


def resize_frame(frame, width: int = 960):
    height, current_width = frame.shape[:2]
    ratio = width / float(current_width)
    return cv2.resize(frame, (width, int(height * ratio)))
