from fastapi import APIRouter, Request

router = APIRouter()


@router.get("")
def list_alerts(request: Request) -> dict:
    pipeline = request.app.state.pipeline
    return {"alerts": pipeline.alert_service.recent_alerts(limit=50)}


@router.post("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: str, request: Request) -> dict:
    pipeline = request.app.state.pipeline
    return pipeline.alert_service.acknowledge(alert_id)
