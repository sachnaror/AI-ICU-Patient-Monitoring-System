from app.services.alert_service import AlertService


def test_fall_alert_created():
    service = AlertService()
    alerts = service.evaluate(
        {
            "fall_detected": True,
            "patient_visible": True,
            "spo2": 98,
            "heart_rate": 78,
            "confidence": 0.96,
        }
    )
    assert alerts
    assert alerts[0]["type"] == "PATIENT_FALL_DETECTED"


def test_acknowledge_alert():
    service = AlertService()
    alert = service.evaluate({"fall_detected": True, "spo2": 97, "confidence": 0.9})[0]
    result = service.acknowledge(alert["id"])
    assert result["ok"] is True
    assert result["alert"]["acknowledged"] is True
