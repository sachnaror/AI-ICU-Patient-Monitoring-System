# API Reference

## Monitoring

`GET /api/monitoring/status`

Returns current telemetry, detections, runtime mode, vitals, and active alerts.

`POST /api/monitoring/source/demo`

Switches to synthetic ICU demo feed.

`POST /api/monitoring/source/webcam`

Attempts to use the local webcam as the ICU feed.

## Alerts

`GET /api/alerts`

Returns recent alert history.

`POST /api/alerts/{alert_id}/acknowledge`

Marks an alert as acknowledged.

## Health

`GET /api/health`

Returns server health and GPU availability.
