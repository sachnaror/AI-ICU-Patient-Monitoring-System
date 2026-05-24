# Architecture

The runtime follows the same flow as a production edge-AI healthcare system:

```text
Video/Webcam/Demo Source
  -> Frame Decoder
  -> CUDA Preprocess Operator
  -> TensorRT YOLOv8 Inference Operator
  -> Pose Estimation Operator
  -> Oxygen OCR Operator
  -> Anomaly Detector
  -> Alert Operator
  -> FastAPI Dashboard + WebSocket
```

In local mode the CUDA, TensorRT, and Holoscan-specific pieces are represented by Python operators with compatible boundaries. This keeps the app working without a GPU while preserving the architecture needed for an NVIDIA deployment.

The dashboard receives:

- `/video-feed` for continuous MJPEG frames
- `/ws` for live telemetry
- `/api/alerts` for persistent alert history
