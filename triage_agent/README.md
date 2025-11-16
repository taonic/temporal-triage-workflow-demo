# Triage Agent

AI-powered Temporal worker that analyzes and categorizes emails using PydanticAI.

## Setup

```bash
cd triage_agent
uv sync
```

## Run

```bash
uv run python main.py
```

## Workflow

- **TriageAgentWorkflow**: Analyzes email content and returns structured triage results (category, priority, sentiment, confidence)

Uses OpenAI GPT-4o-mini to classify emails into categories: technical, billing, credit card, loan, debit card, general.
