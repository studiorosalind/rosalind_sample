from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import LLM libraries with error handling
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    logger.warning("OpenAI package not installed. OpenAI integration will not be available.")
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    logger.warning("Anthropic package not installed. Anthropic integration will not be available.")
    ANTHROPIC_AVAILABLE = False

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

def get_openai_client():
    """Initialize and return an OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    return OpenAI(api_key=api_key)

def get_anthropic_client():
    """Initialize and return an Anthropic client."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY environment variable not set")
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    return anthropic.Anthropic(api_key=api_key)

def create_prompt(cause: Optional[CauseContext], history: Optional[HistoryContext]) -> str:
    """Create a prompt for the LLM based on the cause and history context."""
    prompt = "You are an expert software engineer analyzing an issue. "
    
    if cause:
        prompt += f"\n\nEvent Transaction ID: {cause.event_transaction_id}"
        
        if cause.stack_trace:
            prompt += f"\n\nStack Trace:\n{cause.stack_trace}"
        
        if cause.http_request:
            prompt += f"\n\nHTTP Request:\n{json.dumps(cause.http_request, indent=2)}"
        
        if cause.kafka_message:
            prompt += f"\n\nKafka Message:\n{json.dumps(cause.kafka_message, indent=2)}"
    
    if history and history.similar_issues:
        prompt += "\n\nSimilar Issues:"
        for i, issue in enumerate(history.similar_issues):
            prompt += f"\n{i+1}. {json.dumps(issue, indent=2)}"
    
    prompt += "\n\nBased on the information provided, please analyze this issue and provide:"
    prompt += "\n1. The root cause of the issue"
    prompt += "\n2. A solution guide to fix the issue"
    prompt += "\n3. Your step-by-step reasoning process"
    
    return prompt

def analyze_with_openai(prompt: str) -> Dict[str, Any]:
    """Analyze the issue using OpenAI's API."""
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert software engineer analyzing technical issues."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=2000
        )
        return {"content": response.choices[0].message.content, "success": True}
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        return {"content": str(e), "success": False}

def analyze_with_anthropic(prompt: str) -> Dict[str, Any]:
    """Analyze the issue using Anthropic's API."""
    try:
        client = get_anthropic_client()
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0.1,
            system="You are an expert software engineer analyzing technical issues.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return {"content": response.content[0].text, "success": True}
    except Exception as e:
        logger.error(f"Error calling Anthropic API: {str(e)}")
        return {"content": str(e), "success": False}

def parse_llm_response(response_text: str) -> AnalysisResult:
    """Parse the LLM response into structured analysis result."""
    try:
        # Simple parsing logic - can be enhanced for more complex responses
        lines = response_text.split('\n')
        root_cause = ""
        solution_guide = ""
        steps = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if "root cause" in line.lower() or "1." in line:
                current_section = "root_cause"
                root_cause = line.split(":", 1)[1].strip() if ":" in line else line
            elif "solution" in line.lower() or "2." in line:
                current_section = "solution"
                solution_guide = line.split(":", 1)[1].strip() if ":" in line else line
            elif "step" in line.lower() or "reasoning" in line.lower() or "3." in line:
                current_section = "steps"
                steps.append(line)
            elif current_section == "root_cause":
                root_cause += " " + line
            elif current_section == "solution":
                solution_guide += " " + line
            elif current_section == "steps":
                steps.append(line)
        
        # If parsing failed, use default sections
        if not root_cause:
            root_cause = "Unable to determine root cause from LLM response"
        if not solution_guide:
            solution_guide = "Unable to determine solution from LLM response"
        if not steps:
            steps = ["LLM analysis completed but steps could not be parsed"]
            
        return AnalysisResult(
            root_cause=root_cause,
            solution_guide=solution_guide,
            intermediate_steps=steps
        )
    except Exception as e:
        logger.error(f"Error parsing LLM response: {str(e)}")
        return AnalysisResult(
            root_cause="Error parsing LLM response",
            solution_guide="Please check logs for details",
            intermediate_steps=[f"Error: {str(e)}"]
        )

def analyze_issue(cause: Optional[CauseContext], history: Optional[HistoryContext]) -> AnalysisResult:
    """
    Analyze an issue using LLM (OpenAI or Anthropic) based on cause and history context.
    
    Args:
        cause: The cause context containing stack trace, HTTP request, etc.
        history: The history context containing similar issues.
        
    Returns:
        AnalysisResult: The analysis result containing root cause, solution guide, and steps.
    """
    logger.info(f"Starting issue analysis for event: {cause.event_transaction_id if cause else 'Unknown'}")
    
    # Create prompt for LLM
    prompt = create_prompt(cause, history)
    logger.debug(f"Generated prompt: {prompt}")
    
    # Try OpenAI first, then fall back to Anthropic if available
    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        logger.info("Using OpenAI for analysis")
        result = analyze_with_openai(prompt)
    elif ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
        logger.info("Using Anthropic for analysis")
        result = analyze_with_anthropic(prompt)
    else:
        logger.warning("No LLM integration available. Using fallback dummy analysis.")
        # Fallback to dummy analysis if no LLM is available
        return fallback_analysis(cause, history)
    
    # Check if LLM call was successful
    if not result["success"]:
        logger.error(f"LLM analysis failed: {result['content']}")
        return AnalysisResult(
            root_cause="LLM analysis failed",
            solution_guide=f"Error: {result['content']}",
            intermediate_steps=["Error occurred during LLM analysis"]
        )
    
    # Parse LLM response
    logger.info("LLM analysis completed successfully, parsing response")
    return parse_llm_response(result["content"])

def fallback_analysis(cause: Optional[CauseContext], history: Optional[HistoryContext]) -> AnalysisResult:
    """Fallback dummy analysis when LLM integration is not available."""
    logger.warning("Using fallback dummy analysis")
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
