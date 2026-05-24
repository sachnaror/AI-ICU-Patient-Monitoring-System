import time


class FrameScheduler:
    def __init__(self, target_fps: int = 18) -> None:
        self.delay = 1 / target_fps

    def wait(self) -> None:
        time.sleep(self.delay)
