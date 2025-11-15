import asyncio
import logging
import tracemalloc
import uvicorn
from temporalio.client import Client
from temporalio.worker import Worker
from poller_workflow import EmailPollerWorkflow, poll_graph_api
from triage_workflow import EmailTriageWorkflow, TriageActivities
from database import TriageDatabase
from schedule_manager import create_schedule

interrupt_event = asyncio.Event()

async def run_worker(db: TriageDatabase):
    client = await Client.connect("localhost:7233")
    await create_schedule(client)
    activities = TriageActivities(db)
    
    async with Worker(
        client,
        task_queue="triage-task-queue",
        workflows=[EmailPollerWorkflow, EmailTriageWorkflow],
        activities=[poll_graph_api, activities.save_task],
    ):
        logging.info("Worker started")
        await interrupt_event.wait()

def run_api(db: TriageDatabase):
    import api
    api.db = db
    uvicorn.run("api:app", host="0.0.0.0", port=8000, log_level="info")

async def main():
    tracemalloc.start()
    logging.basicConfig(level=logging.INFO)
    
    db = TriageDatabase()
    
    loop = asyncio.get_event_loop()
    api_task = loop.run_in_executor(None, run_api, db)
    worker_task = asyncio.create_task(run_worker(db))
    
    try:
        await asyncio.gather(api_task, worker_task)
    finally:
        logging.info("Shutting down")

if __name__ == "__main__":
    asyncio.run(main())
