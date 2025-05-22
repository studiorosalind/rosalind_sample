# SAHUR DEVELOPMENT GUIDE

## 1. 로컬 개발 환경 준비

- Python 3.11+, Node.js 20+, Docker, Docker Compose 필요
- 권장: VSCode + Python, ESLint, Prettier 확장

## 2. 의존성 설치

### 전체 일괄 실행 (권장)
```bash
docker-compose up --build
```

### 개별 컴포넌트 개발
- **sahur-core**  
  ```bash
  cd sahur/sahur-core
  pip install -e .
  ```
- **sahur-server, sahur-batch, sahur-mcp**  
  ```bash
  pip install -e ../sahur-core
  pip install -r requirements.txt
  ```
- **sahur-web**  
  ```bash
  npm install
  ```

## 3. 개발 서버 실행

- **전체 통합**  
  ```bash
  docker-compose up
  ```
- **프론트엔드만**  
  ```bash
  cd sahur/sahur-web
  npm run dev
  ```
- **백엔드만**  
  ```bash
  cd sahur/sahur-server && uvicorn main:app --reload
  cd sahur/sahur-batch && uvicorn main:app --reload --port 8010
  cd sahur/sahur-mcp && uvicorn main:app --reload --port 8020
  ```

## 4. 빌드/배포

- **Docker 이미지 빌드**
  ```bash
  docker-compose build
  ```
- **배포**
  - 각 서비스는 독립적으로 컨테이너화되어 배포 가능
  - 환경변수로 DB, MCP, VectorDB 주소 지정

## 5. 데이터베이스

- **PostgreSQL**: docker-compose로 자동 실행, 기본 포트 5432
- **VectorDB(Qdrant)**: 6333 포트, 유사 이슈 검색용

## 6. 주요 개발 패턴

- **공통 모듈**: sahur-core에서 관리, pip install -e ../sahur-core로 연결
- **실시간 통신**: WebSocket (sahur-batch ↔ sahur-web)
- **MCP 연동**: sahur-mcp API로 외부/내부 도구 호출

## 7. 트러블슈팅

- **포트 충돌**: 3000(웹), 8000(서버), 8010(배치), 8020(MCP), 5432(DB), 6333(VectorDB)
- **의존성 문제**: requirements.txt, package.json, pyproject.toml 동기화 확인
- **빌드 실패**: Dockerfile, 볼륨 경로, 권한 확인
- **WebSocket 연결 안됨**: sahur-batch 컨테이너 상태, 포트 매핑 확인

## 8. 테스트/확장

- 각 컴포넌트별 tests/ 디렉토리 추가 권장
- MCP, 에이전트, UI 등 모듈화 구조로 확장 용이

---
