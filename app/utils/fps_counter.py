import time
from collections import deque


class FPSCounter:
    def __init__(self, window: int = 30) -> None:
        self.timestamps: deque[float] = deque(maxlen=window)

    def tick(self) -> float:
        self.timestamps.append(time.monotonic())
        return self.value

    @property
    def value(self) -> float:
        if len(self.timestamps) < 2:
            return 0.0
        elapsed = self.timestamps[-1] - self.timestamps[0]
        return round((len(self.timestamps) - 1) / elapsed, 1) if elapsed > 0 else 0.0
