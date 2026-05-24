class TritonInferenceClient:
    def __init__(self, url: str = "localhost:8001") -> None:
        self.url = url

    def is_available(self) -> bool:
        return False
