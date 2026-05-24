from app.ai_models.oxygen_monitor_reader.anomaly_rules import oxygen_status
from app.ai_models.oxygen_monitor_reader.ocr_reader import OxygenMonitorOCR


class OxygenReaderOperator:
    def __init__(self) -> None:
        self.reader = OxygenMonitorOCR()

    def read(self, frame, context: dict) -> dict:
        vitals = self.reader.read(frame, context)
        vitals["oxygen_status"] = oxygen_status(vitals["spo2"])
        return vitals
