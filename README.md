# AI ICU Patient Monitoring System

Real-time ICU patient monitoring demo using FastAPI, OpenCV, WebSockets, and a Holoscan-inspired AI pipeline layout.

The app is designed to run immediately on a local Mac in CPU demo mode. If `data/sample_videos/patient_fall_demo.mp4` is missing, it generates a synthetic ICU feed with simulated patient posture, oxygen readings, fall events, detection boxes, and dashboard alerts.

## Current Status

This project has two runtime layers:

- CPU demo runtime: active by default and fully working locally.
- Optional NVIDIA runtime adapters: present in the codebase, guarded by feature flags, and safe to leave disabled on macOS.

The optional NVIDIA adapters live in `app/nvidia/`:

- `holoscan_app.py` for NVIDIA Holoscan orchestration
- `cuda_preprocess_impl.py` for CUDA/OpenCV-CUDA preprocessing
- `deepstream_impl.py` for DeepStream/GStreamer RTSP pipeline construction
- `tensorrt_yolo_impl.py` for TensorRT YOLOv8 engine loading hooks
- `runtime.py` for accelerator availability reporting

## Features

- Live browser dashboard at `http://127.0.0.1:8000`
- MJPEG video stream with detection overlays
- WebSocket telemetry updates
- Synthetic ICU feed fallback
- Webcam feed option
- Fall detection and low oxygen alert simulation
- Alert acknowledgement API
- Accelerator status panel for Holoscan, CUDA, DeepStream, TensorRT, and Triton
- CPU fallback that keeps the app working without NVIDIA libraries
- Docker, Kubernetes, and nginx starter files

## Pipeline

```text
Video/Webcam/Demo Source
  -> OpenCV / optional DeepStream input
  -> Frame decoder
  -> CPU resize / optional CUDA preprocess
  -> simulated YOLO / optional TensorRT or Triton inference
  -> pose estimation
  -> oxygen monitor OCR simulation
  -> anomaly detection
  -> alert operator
  -> FastAPI dashboard + WebSocket
```

## Run Locally

```bash
cd /Users/homesachin/Desktop/zoneone/AI-ICU-Patient-Monitoring-System
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Or use:

```bash
bash scripts/start_local_demo.sh
```

## Environment

Copy `.env.example` to `.env` when setting up a new environment.

For local Mac CPU demo mode, keep these disabled:

```env
ENABLE_GPU=false
ENABLE_HOLOSCAN=false
ENABLE_DEEPSTREAM=false
ENABLE_TRITON=false
```

Main settings:

```env
BED_ID=ICU-12
VIDEO_SOURCE=data/sample_videos/patient_fall_demo.mp4
USE_WEBCAM=false
TENSORRT_ENGINE_PATH=app/ai_models/patient_detection/model.engine
TRITON_URL=localhost:8001
TRITON_MODEL_NAME=icu_patient_detector
LOW_SPO2_THRESHOLD=92
CRITICAL_SPO2_THRESHOLD=88
```

## Use Webcam

Click `Webcam` in the dashboard, or set:

```env
USE_WEBCAM=true
```

If camera access is unavailable, the system continues with the demo feed.

## Add a Sample ICU Video

Place your file here:

```text
data/sample_videos/patient_fall_demo.mp4
```

The app will use it automatically. If absent, synthetic video is generated.

## Optional NVIDIA Path

On a compatible NVIDIA host, you can enable the GPU path gradually:

```env
ENABLE_GPU=true
ENABLE_HOLOSCAN=true
ENABLE_DEEPSTREAM=true
ENABLE_TRITON=false
```

Expected production additions:

- Install NVIDIA Holoscan SDK
- Install CUDA-compatible OpenCV or CUDA preprocessing kernels
- Install DeepStream and GStreamer Python bindings
- Provide a TensorRT YOLOv8 engine at `app/ai_models/patient_detection/model.engine`
- Optionally run Triton Inference Server and set `ENABLE_TRITON=true`

If any NVIDIA dependency is unavailable, the app falls back to the CPU demo path instead of crashing.

## API

- `GET /` dashboard
- `GET /alerts` alert log page
- `GET /video-feed` live MJPEG stream
- `GET /api/monitoring/status` latest telemetry
- `POST /api/monitoring/source/demo` switch to synthetic feed
- `POST /api/monitoring/source/webcam` switch to webcam
- `GET /api/alerts` recent alerts
- `POST /api/alerts/{alert_id}/acknowledge` acknowledge an alert
- `GET /api/health` runtime, GPU, and NVIDIA adapter health

## Testing

```bash
source .venv/bin/activate
pytest app/tests
```

Expected result:

```text
5 passed
```


## 📩 Contact

| Name              | Details                             |
|-------------------|-------------------------------------|
| **👨‍💻 Developer**  | Sachin Arora                      |
| **📧 Email**      | [sachnaror@gmail.com](mailto:sacinaror@gmail.com) |
| **📍 Location**   | Noida, India                       |
| **📂 GitHub**     | [Link](https://github.com/sachnaror) |
| **🌐 Youtube**    | [Link](https://www.youtube.com/@sachnaror4841/videos) |
| **🌐 Blog**       | [Link](https://medium.com/@schnaror) |
| **🌐 Website**    | [Link](https://about.me/sachin-arora) |
| **🌐 Twitter**    | [Link](https://twitter.com/sachinhep) |
| **📱 Phone**      | [+91 9560330483](tel:+919560330483) |
