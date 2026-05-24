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
