from fastapi import FastAPI, WebSocket, Request
from pydantic import BaseModel
from typing import Dict, Any
import uuid

from .db import create_issue_tracking, get_issue_tracking
from .websocket import notify_issue_update

app = FastAPI()

class IssueRequest(BaseModel):
    eventTransactionId: str
    description: str

@app.post("/slack/analyze")
async def analyze_issue(request: IssueRequest):
    issue_tracking_id = create_issue_tracking(request.eventTransactionId, request.description)
    # sahur-batch 인스턴스 동적 생성 로직 필요 (예시)
    # batch_instance = create_batch_instance(issue_tracking_id)
    return {"issueTrackingId": issue_tracking_id}

@app.get("/issue/tracking/{issueTrackingId}")
async def get_issue_tracking_info(issueTrackingId: str):
    info = get_issue_tracking(issueTrackingId)
    return info

@app.websocket("/ws/issue/{issueTrackingId}")
async def websocket_endpoint(websocket: WebSocket, issueTrackingId: str):
    await websocket.accept()
    # 실시간 이슈 업데이트 스트림 예시
    while True:
        update = notify_issue_update(issueTrackingId)
        await websocket.send_json(update)
