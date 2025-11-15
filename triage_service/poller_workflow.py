from datetime import timedelta
from temporalio import workflow, activity
from triage_workflow import EmailTriageWorkflow

with workflow.unsafe.imports_passed_through():
    import requests

@activity.defn
async def poll_graph_api() -> list:
    """Poll the graph API for new emails"""
    try:
        response = requests.get("http://localhost:6001/v1.0/me/messages/delta")
        response.raise_for_status()
        data = response.json()
        return data.get("value", [])
    except Exception as e:
        print(f"Error polling graph API: {e}")
        return []

@workflow.defn
class EmailPollerWorkflow:
    @workflow.run
    async def run(self) -> None:
        emails = await workflow.execute_activity(
            poll_graph_api,
            start_to_close_timeout=timedelta(seconds=30)
        )
        
        for email in emails:
            await workflow.start_child_workflow(
                EmailTriageWorkflow.run,
                email,
                id=f"triage-{email['id']}",
                parent_close_policy=workflow.ParentClosePolicy.ABANDON,
            )
