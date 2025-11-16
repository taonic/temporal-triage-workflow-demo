# Graph Service

A minimal dummy service that exposes new emails through Graph API for polling-based consumption.

## Setup

```bash
cd graph_service
uv sync
uv run python main.py
```

## API Endpoints

- `GET /v1.0/me/messages/delta` - Poll for new emails (Microsoft Graph API format)
- `GET /health` - Health check endpoint

The service runs on `http://localhost:6001`
