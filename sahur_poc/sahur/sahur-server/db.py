# 더미 DB 연결 및 이슈 트래킹 엔티티 관리
from typing import Dict, Any

# 실제 환경에서는 SQLAlchemy + PostgreSQL 사용
ISSUE_TRACKING_DB: Dict[str, Dict[str, Any]] = {}

def create_issue_tracking(issue_tracking_id: str, event_transaction_id: str, description: str, extra: Dict[str, Any]):
    ISSUE_TRACKING_DB[issue_tracking_id] = {
        "issueTrackingId": issue_tracking_id,
        "eventTransactionId": event_transaction_id,
        "description": description,
        "extra": extra,
        "status": "created"
    }

def get_issue_tracking(issue_tracking_id: str) -> Dict[str, Any]:
    return ISSUE_TRACKING_DB.get(issue_tracking_id, {"error": "not found"})
