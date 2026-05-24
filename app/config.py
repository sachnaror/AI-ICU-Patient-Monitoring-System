from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "AI ICU Patient Monitoring System"
    app_env: str = "local"
    host: str = "127.0.0.1"
    port: int = 8000
    bed_id: str = "ICU-12"
    video_source: str = "data/sample_videos/patient_fall_demo.mp4"
    use_webcam: bool = False
    enable_gpu: bool = False
    enable_holoscan: bool = False
    enable_deepstream: bool = False
    enable_triton: bool = False
    tensorrt_engine_path: str = "app/ai_models/patient_detection/model.engine"
    triton_url: str = "localhost:8001"
    triton_model_name: str = "icu_patient_detector"
    fall_alert_cooldown_seconds: int = 8
    low_spo2_threshold: int = 92
    critical_spo2_threshold: int = 88

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8")


settings = Settings()
