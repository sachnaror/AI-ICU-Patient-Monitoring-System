class NotificationService:
    def send(self, alert: dict) -> dict:
        return {
            "delivered": True,
            "channels": ["dashboard", "websocket"],
            "alert_id": alert["id"],
        }
