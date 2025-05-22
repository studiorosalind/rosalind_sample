# sahur-core 에이전트 실행 래퍼
from sahur_core.agent import analyze_issue, CauseContext, HistoryContext

def run_agent_analysis(context):
    if context.get("type") == "cause":
        cause = CauseContext(
            event_transaction_id=context.get("eventTransactionId"),
            stack_trace=context.get("stackTrace"),
            http_request=None,
            kafka_message=None
        )
        history = None
    else:
        cause = None
        history = HistoryContext(
            similar_issues=context.get("similarIssues", [])
        )
    result = analyze_issue(cause, history)
    return result.dict()
