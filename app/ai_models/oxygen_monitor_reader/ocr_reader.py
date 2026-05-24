class OxygenMonitorOCR:
    def read(self, frame, context: dict | None = None) -> dict:
        context = context or {}
        return {
            "spo2": int(context.get("spo2", 97)),
            "heart_rate": int(context.get("heart_rate", 76)),
            "confidence": 0.91,
        }
