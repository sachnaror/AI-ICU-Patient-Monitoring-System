class AlertOperator:
    def __init__(self, alert_service, notification_service) -> None:
        self.alert_service = alert_service
        self.notification_service = notification_service

    def process(self, telemetry: dict) -> list[dict]:
        alerts = self.alert_service.evaluate(telemetry)
        for alert in alerts:
            self.notification_service.send(alert)
        return alerts
