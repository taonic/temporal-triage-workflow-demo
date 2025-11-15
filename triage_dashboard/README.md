# Triage Dashboard

A Vue.js dashboard backed by a Python service that displays triage cases.

## Usage

1. Start the triage service API:
   ```bash
   cd triage_service
   uvicorn api:app --reload
   ```

2. Start the dashboard service:
   ```bash
   cd triage_dashboard
   uv run uvicorn server:app --reload --port 8001
   ```

3. Open http://localhost:8001 in a web browser

The dashboard will automatically poll the API every second to display cases ordered by priority.
