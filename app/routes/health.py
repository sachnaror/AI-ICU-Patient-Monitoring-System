from fastapi import APIRouter

from app.services.gpu_monitor_service import get_system_health

router = APIRouter()


@router.get("")
def health() -> dict:
    return get_system_health()
