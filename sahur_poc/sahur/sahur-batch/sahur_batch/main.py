import asyncio
from fastapi import FastAPI, WebSocket
from .agent_runner import run_agent_analysis

app = FastAPI()

@app.websocket("/ws/issue/{issueTrackingId}")
async def websocket_endpoint(websocket: WebSocket, issueTrackingId: str):
    await websocket.accept()
    # 실제 환경에서는 이슈 분석 결과를 실시간으로 스트림
    async for update in run_agent_analysis(issueTrackingId):
        await websocket.send_json(update)
