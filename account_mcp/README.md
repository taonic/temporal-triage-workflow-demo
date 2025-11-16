# Account MCP Server

MCP server for account validation using FastMCP.

## Tool

- `validate_account(account_id: str)` - Validates if an account ID is valid

## Run Locally

```bash
uv run python main.py
```

## Docker

```bash
docker build -t account-mcp .
docker run -p 8002:8002 account-mcp
```
