import logging
from temporalio.client import Client, Schedule, ScheduleActionStartWorkflow, ScheduleIntervalSpec, ScheduleSpec, ScheduleAlreadyRunningError
from temporalio.service import RPCError
from datetime import timedelta
from poller_workflow import EmailPollerWorkflow

async def create_schedule(client: Client):
    """Create email poller schedule idempotently"""
    try:
        await client.create_schedule(
            "email-poller-schedule",
            Schedule(
                action=ScheduleActionStartWorkflow(
                    EmailPollerWorkflow.run,
                    id="email-poller",
                    task_queue="triage-task-queue",
                ),
                spec=ScheduleSpec(
                    intervals=[ScheduleIntervalSpec(every=timedelta(seconds=5))]
                ),
            ),
        )
        logging.info("Email poller schedule created successfully!")
    except ScheduleAlreadyRunningError:
        logging.info("Email poller schedule already exists, skipping creation")
