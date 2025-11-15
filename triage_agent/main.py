import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker
from pydantic_ai.durable_exec.temporal import (
    AgentPlugin,
    PydanticAIPlugin,
)
from agent import TriageAgentWorkflow, temporal_agent

async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect(  
        'localhost:7233',  
        plugins=[PydanticAIPlugin()],  
    )
    
    async with Worker(
        client,
        task_queue="triage-agent-queue",
        workflows=[TriageAgentWorkflow],
        plugins=[AgentPlugin(temporal_agent)]
    ):
        logging.info("Triage agent worker started, ctrl+c to exit")
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
