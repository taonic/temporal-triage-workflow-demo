from datetime import timedelta
from temporalio import workflow, activity
from database import TriageDatabase
from triage_models import TriageResult

class TriageActivities:
    def __init__(self, db: TriageDatabase):
        self.db = db
    
    @activity.defn
    async def save_task(self, case_id: str, result: TriageResult) -> str:
        """Save task to database"""
        self.db.store_triage(
            case_id=case_id,
            channel='email',
            category=result.category,
            account_status=result.account_status,
            sentiment=result.sentiment,
            priority=result.priority,
            subject=result.subject,
            content=result.content,
            requester=result.requester,
            recipient=result.recipient
        )
        return f"Saved triage for case {case_id}"

@workflow.defn
class EmailTriageWorkflow:
    @workflow.run
    async def run(self, email: dict) -> str:
        # Run child workflow to triage email
        result = await workflow.execute_child_workflow(
            "TriageAgentWorkflow",
            email,
            id=f"triage-agent-{email['id']}",
            task_queue="triage-agent-queue"
        )
        
        # Save triage result to database
        save_result = await workflow.execute_activity(
            TriageActivities.save_task,
            args=[email['id'], result],
            start_to_close_timeout=timedelta(seconds=30)
        )
        
        return save_result
