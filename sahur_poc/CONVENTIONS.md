# SAHUR CONVENTIONS

## 공통

- **모노레포**: 모든 컴포넌트는 sahur/ 하위에 위치, 공통 모듈은 sahur-core에 집중
- **의존성**: sahur-core는 pip install -e ../sahur-core로 editable install
- **커밋 메시지**: [타입] 컴포넌트: 요약 (예: feat(server): Slack 엔드포인트 추가)
- **폴더/파일명**: 소문자, 하이픈(-) 또는 언더스코어(_) 사용, PascalCase는 React 컴포넌트에만

---

## sahur-core (Python)

- **스타일**: PEP8, 2-space indent, type hint 적극 사용
- **네이밍**: snake_case 함수/변수, PascalCase 클래스
- **모듈 구조**: 기능별 파일 분리 (agent.py, langgraph_workflow.py 등)
- **Docstring**: Google 스타일

---

## sahur-server, sahur-batch, sahur-mcp (Python/FastAPI)

- **스타일**: PEP8, Black 포매터 권장
- **네이밍**: snake_case 함수/변수, PascalCase 클래스, main.py 엔트리포인트
- **엔드포인트**: RESTful, 소문자+하이픈(/slack/analyze, /get-cause-context)
- **의존성 관리**: pyproject.toml + requirements.txt 병행
- **환경변수**: UPPER_SNAKE_CASE

---

## sahur-web (Next.js/TypeScript)

- **스타일**: Prettier, 2-space indent, 세미콜론 사용, 싱글 쿼트
- **컴포넌트**: PascalCase, src/components/에 위치
- **페이지**: src/pages/에 파일 기반 라우팅
- **상태관리**: Context API 또는 Redux, hooks는 use 접두사
- **CSS**: TailwindCSS utility class 우선, globals.css에 최소 커스텀
- **props/type**: TypeScript interface/type 적극 사용

---

## 기타

- **로깅**: print/log.info 대신 logging 모듈 사용 (Python), console.log 대신 logger (JS)
- **에러 처리**: try/except, 에러 메시지 명확히
- **테스트**: (추후) tests/ 디렉토리, pytest/Jest 권장

---
