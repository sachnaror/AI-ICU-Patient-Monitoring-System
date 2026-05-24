# GPU Pipeline

## Holoscan

Holoscan should own production scheduling and operator orchestration. In this app, `app/holoscan_pipeline/pipeline.py` mirrors that operator graph so the demo can run locally.

## CUDA Preprocessing

`CUDAPreprocessOperator` currently resizes frames using OpenCV. On an NVIDIA target, replace the internals with CUDA kernels or GPU-accelerated preprocessing.

## DeepStream

`DeepStreamInputOperator` is a placeholder for RTSP/multi-camera ingest. It is the right place for a GStreamer/DeepStream pipeline.

## TensorRT

`YOLOv8PatientDetector` exposes the detection interface. Replace the placeholder implementation with a TensorRT engine loader that reads `model.engine`.

## Triton

`TritonInferenceClient` is included for deployments where inference runs as a model server instead of inside the app process.

## Local Safety

All NVIDIA integrations are optional and guarded by environment flags:

```env
ENABLE_GPU=false
ENABLE_HOLOSCAN=false
ENABLE_DEEPSTREAM=false
ENABLE_TRITON=false
```

On macOS or any machine without NVIDIA libraries, the app continues to run with:

- CPU thread scheduler instead of Holoscan
- OpenCV CPU preprocessing instead of CUDA
- OpenCV video input instead of DeepStream
- simulated YOLO detections instead of TensorRT
- local detector instead of Triton
