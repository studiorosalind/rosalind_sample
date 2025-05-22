# db.py: 이슈 트래킹 관련 임시 DB/로직 (실제 환경에서는 DB 연동 필요)
from typing import Dict

# 임시 인메모리 DB
ISSUE_TRACKING_DB: Dict[str, Dict] = {}

def create_issue_tracking(event_transaction_id: str, description: str) -> str:
    issue_tracking_id = f"issue-{event_transaction_id}"
    ISSUE_TRACKING_DB[issue_tracking_id] = {
        "eventTransactionId": event_transaction_id,
        "description": description,
        "status": "created"
    }
    return issue_tracking_id

def get_issue_tracking(issue_tracking_id: str) -> Dict:
    return ISSUE_TRACKING_DB.get(issue_tracking_id, {})
