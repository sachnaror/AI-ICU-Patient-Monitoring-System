from app.nvidia.cuda_preprocess_impl import OptionalCUDAPreprocessor


class CUDAPreprocessOperator:
    def __init__(self) -> None:
        self.backend = OptionalCUDAPreprocessor(width=960)

    def preprocess(self, frame):
        return self.backend.preprocess(frame)

    def describe(self) -> dict:
        return self.backend.describe()
