import time
import uuid
from threading import Lock

from app.config import settings
from app.utils.constants import ALERT_FALL, ALERT_LOW_OXYGEN, ALERT_NO_PATIENT, SEVERITY_CRITICAL, SEVERITY_WARNING
from app.utils.helpers import utc_now_iso


class AlertService:
    def __init__(self) -> None:
        self._alerts: list[dict] = []
        self._lock = Lock()
        self._last_by_type: dict[str, float] = {}

    def evaluate(self, telemetry: dict) -> list[dict]:
        new_alerts: list[dict] = []

        if telemetry.get("fall_detected"):
            new_alerts.append(
                self.trigger(
                    ALERT_FALL,
                    SEVERITY_CRITICAL,
                    "Patient Fall Detected",
                    "Pose and motion anomaly indicate the patient may have fallen.",
                    telemetry,
                )
            )

        spo2 = telemetry.get("spo2")
        if spo2 is not None and spo2 < settings.low_spo2_threshold:
            severity = SEVERITY_CRITICAL if spo2 < settings.critical_spo2_threshold else SEVERITY_WARNING
            new_alerts.append(
                self.trigger(
                    ALERT_LOW_OXYGEN,
                    severity,
                    "Low Oxygen Saturation",
                    f"SpO2 reading is {spo2}%, below configured threshold.",
                    telemetry,
                    cooldown=12,
                )
            )

        if telemetry.get("patient_visible") is False:
            new_alerts.append(
                self.trigger(
                    ALERT_NO_PATIENT,
                    SEVERITY_WARNING,
                    "Patient Not Visible",
                    "The patient detector cannot locate the patient in the bed area.",
                    telemetry,
                    cooldown=12,
                )
            )

        return [alert for alert in new_alerts if alert]

    def trigger(
        self,
        alert_type: str,
        severity: str,
        title: str,
        message: str,
        telemetry: dict,
        cooldown: int | None = None,
    ) -> dict | None:
        now = time.monotonic()
        cooldown_seconds = cooldown or settings.fall_alert_cooldown_seconds
        if now - self._last_by_type.get(alert_type, 0) < cooldown_seconds:
            return None

        alert = {
            "id": str(uuid.uuid4()),
            "type": alert_type,
            "severity": severity,
            "title": title,
            "message": message,
            "bed_id": settings.bed_id,
            "created_at": utc_now_iso(),
            "acknowledged": False,
            "confidence": telemetry.get("confidence", 0.0),
            "spo2": telemetry.get("spo2"),
            "heart_rate": telemetry.get("heart_rate"),
        }

        with self._lock:
            self._alerts.insert(0, alert)
            self._alerts = self._alerts[:100]
            self._last_by_type[alert_type] = now
        return alert

    def recent_alerts(self, limit: int = 20) -> list[dict]:
        with self._lock:
            return self._alerts[:limit]

    def acknowledge(self, alert_id: str) -> dict:
        with self._lock:
            for alert in self._alerts:
                if alert["id"] == alert_id:
                    alert["acknowledged"] = True
                    alert["acknowledged_at"] = utc_now_iso()
                    return {"ok": True, "alert": alert}
        return {"ok": False, "message": "Alert not found"}
