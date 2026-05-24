import threading
import time
from typing import Generator

from app.holoscan_pipeline.operators.alert_operator import AlertOperator
from app.holoscan_pipeline.operators.anomaly_detector import AnomalyDetectorOperator
from app.holoscan_pipeline.operators.cuda_preprocess import CUDAPreprocessOperator
from app.holoscan_pipeline.operators.frame_decoder import FrameDecoderOperator
from app.holoscan_pipeline.operators.inference import TensorRTInferenceOperator
from app.holoscan_pipeline.operators.oxygen_reader import OxygenReaderOperator
from app.holoscan_pipeline.operators.pose_estimator import PoseEstimatorOperator
from app.holoscan_pipeline.operators.stream_output import StreamOutputOperator
from app.holoscan_pipeline.operators.video_input import VideoInputOperator
from app.holoscan_pipeline.resource_manager import ResourceManager
from app.holoscan_pipeline.scheduler import FrameScheduler
from app.services.alert_service import AlertService
from app.services.audit_service import AuditService
from app.services.notification_service import NotificationService
from app.services.websocket_service import websocket_manager
from app.utils.fps_counter import FPSCounter
from app.utils.helpers import utc_now_iso


class ICUMonitoringPipeline:
    def __init__(self) -> None:
        self.video_input = VideoInputOperator()
        self.decoder = FrameDecoderOperator()
        self.preprocess = CUDAPreprocessOperator()
        self.inference = TensorRTInferenceOperator()
        self.pose = PoseEstimatorOperator()
        self.oxygen = OxygenReaderOperator()
        self.anomaly = AnomalyDetectorOperator()
        self.alert_service = AlertService()
        self.audit_service = AuditService()
        self.notification_service = NotificationService()
        self.alert_operator = AlertOperator(self.alert_service, self.notification_service)
        self.output = StreamOutputOperator()
        self.resources = ResourceManager()
        self.scheduler = FrameScheduler()
        self.fps = FPSCounter()
        self._lock = threading.Lock()
        self._running = False
        self._thread: threading.Thread | None = None
        self._latest_jpeg = b""
        self._latest_snapshot: dict = {}

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        self.video_input.close()

    def switch_source(self, mode: str) -> None:
        source = "demo" if mode == "demo" else "webcam"
        self.video_input.switch_source(source)

    def _run(self) -> None:
        while self._running:
            frame, context = self.video_input.read()
            decoded = self.decoder.decode(frame)
            processed = self.preprocess.preprocess(decoded)
            detections = self.inference.infer(processed, context)
            pose = self.pose.analyze(detections, context)
            vitals = self.oxygen.read(processed, context)
            telemetry = {
                **self.anomaly.evaluate(detections, pose, vitals),
                **vitals,
                "pose": pose,
                "detections": detections,
                "fps": self.fps.tick(),
                "updated_at": utc_now_iso(),
                "pipeline": self.resources.describe(),
                "source": self.video_input.loader.source_mode,
            }
            alerts = self.alert_operator.process(telemetry)
            telemetry["active_alerts"] = self.alert_service.recent_alerts(limit=5)
            telemetry["new_alerts"] = alerts
            jpeg = self.output.render_jpeg(processed, telemetry, detections)

            with self._lock:
                self._latest_jpeg = jpeg
                self._latest_snapshot = telemetry

            if alerts:
                self.audit_service.record({"type": "alerts", "alerts": alerts, "created_at": utc_now_iso()})
            websocket_manager.broadcast_from_thread({"type": "telemetry", "payload": telemetry})
            self.scheduler.wait()

    def mjpeg_frames(self) -> Generator[bytes, None, None]:
        while True:
            with self._lock:
                frame = self._latest_jpeg
            if frame:
                yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            time.sleep(0.05)

    def snapshot(self) -> dict:
        with self._lock:
            snapshot = dict(self._latest_snapshot)
        if not snapshot:
            snapshot = {"status": "starting", "pipeline": self.resources.describe(), "active_alerts": []}
        return snapshot
