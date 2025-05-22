from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid

from .agent_runner import run_agent_analysis

app = FastAPI()

class BatchAnalyzeRequest(BaseModel):
    eventTransactionId: Optional[str]
    description: str
    extra: Dict[str, Any] = {}

@app.post("/analyze")
async def analyze(req: BatchAnalyzeRequest):
    # CauseContext/HistoryContext 더미 생성
    if req.eventTransactionId:
        context = {"type": "cause", "eventTransactionId": req.eventTransactionId, "stackTrace": "FileNotFoundError: app/main.py"}
    else:
        context = {"type": "history", "similarIssues": [{"description": "DB 연결 실패", "solution": "DB 설정 확인"}]}
    # 에이전트 실행
    result = run_agent_analysis(context)
    return {"result": result}

@app.websocket("/ws/stream/{issue_tracking_id}")
async def ws_stream(websocket: WebSocket, issue_tracking_id: str):
    await websocket.accept()
    # 더미 사고 과정 스트림
    await websocket.send_json({"step": "에이전트 분석 시작", "issueTrackingId": issue_tracking_id})
    await websocket.send_json({"step": "CauseContext/HistoryContext 수집", "issueTrackingId": issue_tracking_id})
    await websocket.send_json({"step": "분석 완료", "issueTrackingId": issue_tracking_id, "solution": "app/main.py 파일 경로 및 권한 확인"})
    await websocket.close()
