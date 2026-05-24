from app.nvidia.deepstream_impl import OptionalDeepStreamInput


class DeepStreamInputOperator:
    def __init__(self) -> None:
        self.backend = OptionalDeepStreamInput()

    def build_pipeline(self, source: str) -> str:
        if self.backend.available:
            return self.backend.build_rtsp_pipeline(source)
        return f"deepstream-placeholder source={source}"

    def describe(self) -> dict:
        return self.backend.describe()
