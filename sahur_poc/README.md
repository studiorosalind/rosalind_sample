# SAHUR

AI 기반 상호작용형 이슈 분석 및 해결 시스템  
개발 조직의 이슈 대응 리소스를 획기적으로 줄이고, 사고 과정을 실시간으로 투명하게 제공합니다.

---

## 주요 컴포넌트

- **sahur-core**: LangGraph 기반 에이전트 로직, 공통 라이브러리
- **sahur-server**: FastAPI 메인 API 서버, Slack webhook, 이슈 트래킹
- **sahur-batch**: 이슈별 동적 분석 인스턴스, 실시간 WebSocket 스트림
- **sahur-web**: Next.js 프론트엔드, 실시간 모니터링/상호작용 UI
- **sahur-mcp**: MCP 프록시 서버, 외부/내부 도구 연동

---

## 빠른 시작

### 1. 의존성 설치 및 실행

```bash
docker-compose up --build
```

- 웹: http://localhost:3000
- API: http://localhost:8000
- Batch: ws://localhost:8010
- MCP: http://localhost:8020
- DB: localhost:5432 (user: sahur, pw: sahurpw, db: sahurdb)
- VectorDB(Qdrant): localhost:6333

### 2. 데모 시나리오

1. **Slack 요청 처리**
   - `/slack/analyze` 엔드포인트로 eventTransactionId, description 전달
   - sahur-server가 이슈 트래킹 생성, sahur-batch 인스턴스 동적 생성

2. **실시간 프론트엔드 페이지 활성화**
   - `/issue/tracking/{issueTrackingId}` 접속
   - 사고 과정, CauseContext, HistoryContext, 리포트 실시간 표시

3. **사고 과정**
   - sahur-batch가 sahur-mcp에 getCauseContext/getHistoryContext 요청
   - MCP 서버가 더미 StackTrace/유사 이슈/파일 정보 반환

4. **의사결정 및 해결책 생성**
   - StackTrace/HistoryContext 기반 반복 분석, 해결 가이드 리포트 생성

---

## 주요 명령어

- 프론트엔드 개발:  
  ```bash
  cd sahur/sahur-web && npm install && npm run dev
  ```
- 백엔드 개발:  
  ```bash
  cd sahur/sahur-server && pip install -e ../sahur-core && pip install -r requirements.txt && uvicorn main:app --reload
  ```

---

## 문서

- [ARCHITECTURE.md](./ARCHITECTURE.md)  
- [CONVENTIONS.md](./CONVENTIONS.md)  
- [DEVELOPMENT.md](./DEVELOPMENT.md)  
- [COMPONENT_TEMPLATE.md](./COMPONENT_TEMPLATE.md)  

---

## 확장/참고

- 각 컴포넌트별 모듈화 구조, MCP 도구/엔드포인트 추가, UI/에이전트 커스터마이즈 용이
- 실제 운영 환경에 맞게 DB, VectorDB, MCP, Slack, GitHub 연동 확장 가능

---
