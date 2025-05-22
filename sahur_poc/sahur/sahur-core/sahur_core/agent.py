from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class CauseContext(BaseModel):
    event_transaction_id: str
    stack_trace: Optional[str]
    http_request: Optional[Dict[str, Any]]
    kafka_message: Optional[Dict[str, Any]]

class HistoryContext(BaseModel):
    similar_issues: List[Dict[str, Any]]

class AnalysisResult(BaseModel):
    root_cause: str
    solution_guide: str
    intermediate_steps: List[str]

def analyze_issue(cause: Optional[CauseContext], history: Optional[HistoryContext]) -> AnalysisResult:
    # 더미 분석 로직: StackTrace가 있으면 파일명 추출, 없으면 유사 이슈 기반
    steps = []
    if cause and cause.stack_trace:
        steps.append("StackTrace 분석: 원인 파일 추출")
        root_cause = "FileNotFoundError in app/main.py"
        solution = "app/main.py 파일 경로 및 권한 확인"
    elif history and history.similar_issues:
        steps.append("유사 이슈 검색: 과거 해결책 참조")
        root_cause = "HTTP 500 에러 - DB 연결 실패"
        solution = "DB 연결 설정 및 네트워크 상태 점검"
    else:
        steps.append("컨텍스트 부족: 추가 정보 필요")
        root_cause = "원인 미상"
        solution = "추가 로그 및 입력 필요"
    return AnalysisResult(
        root_cause=root_cause,
        solution_guide=solution,
        intermediate_steps=steps
    )
