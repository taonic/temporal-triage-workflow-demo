from temporalio import workflow
from pydantic_ai import Agent
from pydantic_ai.durable_exec.temporal import TemporalAgent
from pydantic_ai.mcp import MCPServerStreamableHTTP
import os

from typing import Dict, Any
from models import TriageResult

account_mcp_url = os.getenv('ACCOUNT_MCP_URL', 'http://localhost:8002/mcp')
account_mcp = MCPServerStreamableHTTP(account_mcp_url, id='account-status-mcp')
agent = Agent(
    'openai:gpt-4o-mini',
    name="triage-agent",
    output_type=TriageResult,
    toolsets=[account_mcp],
    system_prompt="""You are an email triage assistant. Analyze emails and categorize them.
    
    Categories: technical, billing, credit card, loan, debit card, general
    Extract account ID from the email content (starts with ACC)
    Always use account_status tool to get account status based on the ID
    Priority: 1 (low) to 5 (critical)
    Sentiment: positive, neutral, negative
    Confidence: 0.0 to 1.0"""
)

temporal_agent = TemporalAgent(agent)

@workflow.defn
class TriageAgentWorkflow:
    @workflow.run
    async def run(self, email: Dict[str, Any]) -> TriageResult:
        content = f"""
        Subject: {email.get('subject', '')}
        From: {email.get('sender', '')}
        Content: {email.get('body', '')}
        """
        
        result = await temporal_agent.run(content)
        triage_result = result.output
        triage_result.subject = email.get('subject', '')
        triage_result.content = email.get('body', '')
        triage_result.requester = email.get('sender', '')
        triage_result.recipient = email.get('recipient', '')
        return triage_result
