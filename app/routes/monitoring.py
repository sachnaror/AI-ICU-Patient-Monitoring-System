from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/status")
def monitoring_status(request: Request) -> dict:
    return request.app.state.pipeline.snapshot()


@router.post("/source/demo")
def switch_to_demo(request: Request) -> dict:
    request.app.state.pipeline.switch_source("demo")
    return {"source": "demo", "message": "Synthetic ICU demo feed enabled"}


@router.post("/source/webcam")
def switch_to_webcam(request: Request) -> dict:
    request.app.state.pipeline.switch_source("webcam")
    return {"source": "webcam", "message": "Webcam ICU feed requested"}
