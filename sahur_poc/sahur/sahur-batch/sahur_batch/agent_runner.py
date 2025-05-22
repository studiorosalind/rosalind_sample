# agent_runner.py: 이슈 분석 에이전트 실행 로직
import asyncio
import logging
import os
from typing import Dict, Any, AsyncGenerator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import sahur_core components
try:
    from sahur_core.agent import analyze_issue, CauseContext, HistoryContext
    SAHUR_CORE_AVAILABLE = True
except ImportError:
    logger.error("sahur_core not found. Make sure it's installed with 'pip install -e ../sahur-core'")
    SAHUR_CORE_AVAILABLE = False

async def run_agent_analysis(issue_tracking_id: str) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Run the agent analysis for a given issue tracking ID.
    
    Args:
        issue_tracking_id: The ID of the issue to analyze.
        
    Yields:
        Dict[str, Any]: Updates about the analysis process.
    """
    logger.info(f"Starting agent analysis for issue: {issue_tracking_id}")
    
    # Check if sahur_core is available
    if not SAHUR_CORE_AVAILABLE:
        logger.error("Cannot run analysis: sahur_core not available")
        yield {"step": "error", "result": "sahur_core not available"}
        return
    
    # Check if LLM API keys are available
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_api_key and not anthropic_api_key:
        logger.warning("No LLM API keys found. Analysis will use fallback dummy data.")
        yield {"step": "warning", "result": "No LLM API keys found. Using fallback analysis."}
    
    # Yield initial status
    yield {"step": 0, "result": f"Starting analysis for issue {issue_tracking_id}"}
    await asyncio.sleep(0.5)
    
    try:
        # In a real implementation, you would fetch these from a database or API
        # For now, we'll create dummy data
        cause_context = CauseContext(
            event_transaction_id=issue_tracking_id,
            stack_trace="Error in app/main.py line 42: FileNotFoundError: [Errno 2] No such file or directory: 'config.json'",
            http_request={"method": "GET", "path": "/api/data", "headers": {"user-agent": "Mozilla/5.0"}},
            kafka_message=None
        )
        
        history_context = HistoryContext(
            similar_issues=[
                {"id": "issue-123", "title": "Config file missing", "solution": "Added config.json to deployment"},
                {"id": "issue-456", "title": "File permission error", "solution": "Fixed file permissions"}
            ]
        )
        
        # Yield progress updates
        yield {"step": 1, "result": "Retrieved cause context"}
        await asyncio.sleep(0.5)
        
        yield {"step": 2, "result": "Retrieved history context"}
        await asyncio.sleep(0.5)
        
        # Run the actual analysis using sahur_core
        yield {"step": 3, "result": "Running LLM analysis..."}
        
        # This will use the real LLM if API keys are available
        analysis_result = analyze_issue(cause_context, history_context)
        
        # Yield intermediate steps
        for i, step in enumerate(analysis_result.intermediate_steps):
            yield {"step": 4 + i, "result": step}
            await asyncio.sleep(0.5)
        
        # Yield final result
        yield {
            "step": "complete",
            "result": {
                "root_cause": analysis_result.root_cause,
                "solution_guide": analysis_result.solution_guide,
                "steps_count": len(analysis_result.intermediate_steps)
            }
        }
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        yield {"step": "error", "result": f"Analysis failed: {str(e)}"}
