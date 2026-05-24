# AI ICU Patient Monitoring System

Real-time ICU monitoring demo using FastAPI, OpenCV, WebSockets, and a Holoscan-inspired AI pipeline layout.

The app runs immediately in CPU demo mode. If `data/sample_videos/patient_fall_demo.mp4` is missing, it generates a synthetic ICU feed with simulated patient posture, oxygen readings, fall events, bounding boxes, and dashboard alerts.

## Features

- Live browser dashboard at `http://127.0.0.1:8000`
- MJPEG video stream with detection overlays
- WebSocket telemetry updates
- Fall detection and low oxygen alert simulation
- Alert acknowledgement API
- CPU fallback with clean GPU/TensorRT/DeepStream/Holoscan integration points
- Docker and Kubernetes starter files

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

## Use Webcam

Click `Webcam` in the dashboard, or set:

```env
USE_WEBCAM=true
```

If no webcam is available, the system keeps the demo feed alive.

## Add a Sample ICU Video

Place your file here:

```text
data/sample_videos/patient_fall_demo.mp4
```

The app will use it automatically. If absent, synthetic video is generated.

## API

- `GET /` dashboard
- `GET /video-feed` live MJPEG stream
- `GET /api/monitoring/status` latest telemetry
- `POST /api/monitoring/source/demo` switch to synthetic feed
- `POST /api/monitoring/source/webcam` switch to webcam
- `GET /api/alerts` recent alerts
- `POST /api/alerts/{alert_id}/acknowledge` acknowledge an alert
- `GET /api/health` runtime and GPU health

## GPU Path

The first version is intentionally runnable on my humble Mac. The file layout keeps upgrade points for:

- NVIDIA Holoscan orchestration
- CUDA preprocessing
- NVIDIA DeepStream input
- TensorRT YOLOv8 inference
- NVIDIA Triton model serving

We can ofcourse install the GPU stack on a compatible NVIDIA host.
