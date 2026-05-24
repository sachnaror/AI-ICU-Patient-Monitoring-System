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
    fall_alert_cooldown_seconds: int = 8
    low_spo2_threshold: int = 92
    critical_spo2_threshold: int = 88

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8")


settings = Settings()
