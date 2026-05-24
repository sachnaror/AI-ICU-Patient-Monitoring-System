import math
import time

import cv2
import numpy as np


def synthetic_icu_frame(frame_index: int, width: int = 960, height: int = 540):
    frame = np.full((height, width, 3), (28, 32, 38), dtype=np.uint8)
    cv2.rectangle(frame, (42, 64), (width - 42, height - 50), (48, 55, 64), -1)
    cv2.rectangle(frame, (95, 170), (610, 385), (62, 75, 87), -1)
    cv2.rectangle(frame, (122, 205), (575, 348), (95, 115, 130), -1)
    cv2.rectangle(frame, (665, 90), (895, 248), (12, 18, 24), -1)
    cv2.rectangle(frame, (665, 278), (895, 392), (25, 35, 45), -1)

    phase = (frame_index // 70) % 4
    bob = int(math.sin(time.monotonic() * 3) * 4)
    if phase in (0, 1):
        patient_box = (230, 212 + bob, 505, 326 + bob)
        cv2.ellipse(frame, (366, 270 + bob), (132, 42), 0, 0, 360, (118, 170, 205), -1)
        cv2.circle(frame, (245, 255 + bob), 24, (88, 138, 172), -1)
    else:
        patient_box = (470, 358, 765, 430)
        cv2.ellipse(frame, (620, 395), (145, 35), 0, 0, 360, (76, 86, 180), -1)
        cv2.circle(frame, (490, 394), 24, (72, 96, 160), -1)

    spo2 = 97 if phase != 2 else 86
    heart_rate = 76 + int(math.sin(frame_index / 9) * 5)
    cv2.putText(frame, "ICU Bed 12", (68, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (230, 235, 240), 2)
    cv2.putText(frame, f"SpO2 {spo2}%", (690, 148), cv2.FONT_HERSHEY_SIMPLEX, 0.92, (70, 230, 140), 2)
    cv2.putText(frame, f"HR {heart_rate}", (690, 195), cv2.FONT_HERSHEY_SIMPLEX, 0.92, (80, 190, 245), 2)
    cv2.putText(frame, "NVIDIA Edge AI Demo", (690, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 210, 220), 1)

    return frame, {"patient_box": patient_box, "spo2": spo2, "heart_rate": heart_rate, "fall_phase": phase in (2, 3)}
