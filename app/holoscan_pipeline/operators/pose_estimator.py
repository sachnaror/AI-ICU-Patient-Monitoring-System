from app.ai_models.pose_estimation.fall_detection import detect_fall_from_pose
from app.ai_models.pose_estimation.mediapipe_pose import MediaPipePoseEstimator


class PoseEstimatorOperator:
    def __init__(self) -> None:
        self.estimator = MediaPipePoseEstimator()

    def analyze(self, detections: list[dict], context: dict) -> dict:
        pose = self.estimator.estimate(detections, context)
        fall = detect_fall_from_pose(pose)
        return {**pose, **fall}
