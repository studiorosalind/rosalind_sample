# agent_runner.py: 이슈 분석 에이전트 더미 로직
import asyncio

async def run_agent_analysis(issue_tracking_id: str):
    # 실제 환경에서는 LangGraph/분석 로직 연동
    for i in range(5):
        await asyncio.sleep(1)
        yield {"step": i, "result": f"분석 결과 {i} for {issue_tracking_id}"}
