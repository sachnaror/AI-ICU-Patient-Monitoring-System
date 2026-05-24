from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR, settings
from app.holoscan_pipeline.pipeline import ICUMonitoringPipeline
from app.routes import alerts, health, monitoring
from app.services.websocket_service import websocket_manager

app = FastAPI(title=settings.app_name, version="1.0.0")
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "dashboard" / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "dashboard" / "static")), name="static")

pipeline = ICUMonitoringPipeline()
app.state.pipeline = pipeline

app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["monitoring"])
app.include_router(health.router, prefix="/api/health", tags=["health"])


@app.on_event("startup")
async def startup() -> None:
    pipeline.start()


@app.on_event("shutdown")
async def shutdown() -> None:
    pipeline.stop()


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "app_name": settings.app_name, "bed_id": settings.bed_id},
    )


@app.get("/alerts", response_class=HTMLResponse)
async def alerts_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "alerts.html",
        {"request": request, "app_name": settings.app_name, "bed_id": settings.bed_id},
    )


@app.get("/video-feed")
def video_feed() -> StreamingResponse:
    return StreamingResponse(
        pipeline.mjpeg_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
