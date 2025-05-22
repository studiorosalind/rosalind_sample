from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from .dummy_github import get_github_file

app = FastAPI()

class CauseContextRequest(BaseModel):
    eventTransactionId: str

class HistoryContextRequest(BaseModel):
    issueDescription: str

@app.post("/getCauseContext")
async def get_cause_context(req: CauseContextRequest):
    # 현실적인 더미 StackTrace/HTTP/Kafka 데이터 반환
    return {
        "eventTransactionId": req.eventTransactionId,
        "stackTrace": "FileNotFoundError: app/main.py\n  at main (app/main.py:10)\n  at handler (app/handler.py:5)",
        "httpRequest": {
            "method": "POST",
            "url": "/api/data",
            "body": {"key": "value"},
            "headers": {"Authorization": "Bearer ..."}
        },
        "kafkaMessage": {
            "topic": "issue-events",
            "payload": {"event": "ERROR", "id": req.eventTransactionId}
        }
    }

@app.post("/getHistoryContext")
async def get_history_context(req: HistoryContextRequest):
    # 현실적인 더미 유사 이슈 데이터 반환
    return {
        "similarIssues": [
            {
                "description": "DB 연결 실패",
                "solution": "DB 설정 및 네트워크 확인",
                "stackTrace": "psycopg2.OperationalError: could not connect to server"
            },
            {
                "description": "HTTP 500 에러",
                "solution": "서버 로그 확인 및 재시작"
            }
        ]
    }

@app.get("/github/file")
async def github_file(path: str):
    # 더미 GitHub 파일 내용 반환
    return get_github_file(path)
