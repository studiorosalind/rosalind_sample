# 더미 WebSocket 알림 함수
def notify_issue_update(issue_tracking_id: str, status: str):
    # 실제 환경에서는 WebSocket 브로드캐스트 또는 Pub/Sub 사용
    print(f"[WebSocket] Issue {issue_tracking_id} status: {status}")
