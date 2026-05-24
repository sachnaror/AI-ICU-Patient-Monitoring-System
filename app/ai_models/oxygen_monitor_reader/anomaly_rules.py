from app.config import settings


def oxygen_status(spo2: int) -> str:
    if spo2 < settings.critical_spo2_threshold:
        return "critical"
    if spo2 < settings.low_spo2_threshold:
        return "warning"
    return "normal"
