# SAHUR COMPONENT TEMPLATE

## sahur-core (공통 모듈)

```
sahur-core/
├── __init__.py
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── agent.py              # 에이전트 로직
├── langgraph_workflow.py # LangGraph 워크플로우 예시
```

### 개발 패턴
- 기능별 모듈 분리, BaseModel 상속 데이터 클래스
- 분석 함수: analyze_issue(cause, history) → AnalysisResult

---

## sahur-server (API 서버)

```
sahur-server/
├── __init__.py
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── main.py         # FastAPI 엔트리포인트
├── db.py           # DB 연결/엔티티
├── websocket.py    # WebSocket 알림
```

### 개발 패턴
- main.py: 엔드포인트 정의, Slack webhook, 이슈 트래킹 관리
- db.py: SQLAlchemy/더미 DB, 엔티티 함수
- websocket.py: 상태 알림 함수

---

## sahur-batch (이슈 처리 인스턴스)

```
sahur-batch/
├── __init__.py
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── main.py           # FastAPI 엔트리포인트, WebSocket 스트림
├── agent_runner.py   # sahur-core 에이전트 실행
```

### 개발 패턴
- main.py: 분석 요청, WebSocket 스트림
- agent_runner.py: sahur-core analyze_issue 래핑

---

## sahur-mcp (MCP 프록시 서버)

```
sahur-mcp/
├── __init__.py
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── main.py           # FastAPI 엔트리포인트, MCP API
├── dummy_github.py   # GitHub MCP 더미
```

### 개발 패턴
- main.py: getCauseContext, getHistoryContext, GitHub MCP API
- dummy_github.py: 파일 내용 더미 반환

---

## sahur-web (Next.js 프론트엔드)

```
sahur-web/
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
├── postcss.config.js
├── Dockerfile
├── public/
└── src/
    ├── pages/
    │   ├── _app.tsx
    │   ├── index.tsx
    │   └── issue/tracking/[issueTrackingId].tsx
    ├── components/
    │   ├── ChatStream.tsx
    │   ├── CauseContext.tsx
    │   └── HistoryContext.tsx
    ├── context/
    └── styles/
        └── globals.css
```

### 개발 패턴
- pages/: 파일 기반 라우팅, 이슈별 실시간 페이지
- components/: 사고 과정, 컨텍스트, 히스토리 등 UI 분리
- WebSocket: sahur-batch와 실시간 연동
- 상태관리: Context API/Redux, hooks

---

## 확장 예시

- tests/ 디렉토리 추가, pytest/Jest
- MCP 도구/엔드포인트 추가
- 에이전트 워크플로우/프롬프트 커스터마이즈
- UI 컴포넌트 분리 및 디자인 시스템 적용

---
