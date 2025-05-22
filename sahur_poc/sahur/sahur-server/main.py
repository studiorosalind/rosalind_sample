from fastapi import FastAPI, WebSocket, Request
from pydantic import BaseModel
from typing import Dict, Any
import uuid

from .db import create_issue_tracking, get_issue_tracking
from .websocket import notify_issue_update

app = FastAPI()

class SlackAnalyzeRequest(BaseModel):
    eventTransactionId: str
    description: str
    extra: Dict[str, Any] = {}

@app.post("/slack/analyze")
async def slack_analyze(req: SlackAnalyzeRequest):
    # 1. 이슈 트래킹 생성
    issue_tracking_id = str(uuid.uuid4())
    create_issue_tracking(issue_tracking_id, req.eventTransactionId, req.description, req.extra)
    # 2. sahur-batch 인스턴스 생성 (더미: 실제로는 컨테이너/프로세스 동적 생성)
    # 3. WebSocket/프론트엔드에 실시간 알림
    notify_issue_update(issue_tracking_id, status="created")
    return {"issueTrackingId": issue_tracking_id}

@app.get("/issue/tracking/{issue_tracking_id}")
async def get_issue(issue_tracking_id: str):
    # 이슈 트래킹 상태 반환
    return get_issue_tracking(issue_tracking_id)

@app.websocket("/ws/issue/{issue_tracking_id}")
async def ws_issue(websocket: WebSocket, issue_tracking_id: str):
    await websocket.accept()
    # 더미: 상태 업데이트 스트림
    await websocket.send_json({"status": "created", "issueTrackingId": issue_tracking_id})
    await websocket.close()
