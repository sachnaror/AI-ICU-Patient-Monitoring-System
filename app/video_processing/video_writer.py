from pathlib import Path

import cv2


def save_snapshot(frame, output_dir: Path, name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{name}.jpg"
    cv2.imwrite(str(path), frame)
    return path
