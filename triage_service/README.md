# Triage Service

Temporal-based service that polls the Graph API for new emails and starts triage workflows.

## Setup

```bash
cd triage_service
uv sync
```

## Run

1. Start the worker:
```bash
uv run python worker.py
```

2. Create Temporal schedules:
```bash
./start_schedules.sh
```

## Workflows

- **EmailPollerWorkflow**: Polls Graph API every 10 seconds for new emails
- **EmailTriageWorkflow**: Processes individual emails for triage

The poller workflow starts a new triage workflow for each new email found.