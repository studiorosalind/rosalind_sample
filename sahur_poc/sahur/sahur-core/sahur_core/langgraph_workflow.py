# LangGraph 워크플로우 더미 예시
from langgraph.graph import StateGraph

def build_dummy_workflow():
    graph = StateGraph()
    # 더미 노드 및 엣지 추가
    graph.add_node("start", lambda x: x)
    graph.add_node("analyze", lambda x: {"result": "분석 완료"})
    graph.add_edge("start", "analyze")
    return graph
