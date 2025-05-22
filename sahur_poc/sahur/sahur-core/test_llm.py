#!/usr/bin/env python3
"""
Test script to verify LLM integration in sahur-core.
"""

import os
import logging
from dotenv import load_dotenv
from sahur_core.agent import CauseContext, HistoryContext, analyze_issue

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    """Test the LLM integration by running a sample analysis."""
    logger.info("Testing sahur-core LLM integration")
    
    # Check if API keys are available
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_api_key and not anthropic_api_key:
        logger.warning("No LLM API keys found. Test will use fallback dummy analysis.")
    else:
        if openai_api_key:
            logger.info("OpenAI API key found")
        if anthropic_api_key:
            logger.info("Anthropic API key found")
    
    # Create test data
    cause_context = CauseContext(
        event_transaction_id="test-123",
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
    
    # Run analysis
    logger.info("Running analysis...")
    result = analyze_issue(cause_context, history_context)
    
    # Print results
    logger.info("Analysis complete!")
    logger.info(f"Root Cause: {result.root_cause}")
    logger.info(f"Solution Guide: {result.solution_guide}")
    logger.info("Intermediate Steps:")
    for step in result.intermediate_steps:
        logger.info(f"  - {step}")

if __name__ == "__main__":
    main()
