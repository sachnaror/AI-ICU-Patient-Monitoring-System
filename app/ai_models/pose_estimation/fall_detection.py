def detect_fall_from_pose(pose: dict) -> dict:
    is_horizontal = pose.get("orientation") == "horizontal"
    near_floor = pose.get("center_y", 0) > 330
    confidence = 0.94 if is_horizontal and near_floor else 0.08
    return {"fall_detected": confidence > 0.8, "confidence": confidence}
