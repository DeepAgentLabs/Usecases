#!/usr/bin/env python3
"""
USE CASE 5: Automated Code Review System (Multi-Agent Parallel)

Real-world scenario: AI-powered code review workflow
- Code Analyzer: Identifies structure and issues
- Security Auditor: Checks vulnerabilities
- Test Planner: Designs test coverage
- Documentation Generator: Creates docstrings
- Feedback Synthesizer: Combines all reviews

Token Usage Expected: 12K-18K tokens
Optimization Potential: 40-50%

Pattern: Parallel agent analysis (can run simultaneously) with synthesis

Run with AgentIceLens:
  uv run agenticlens profile examples/usecase_5_code_review.py --save usecase_5.json
  uv run agenticlens analyze usecase_5.json
"""

from datetime import datetime
from typing import Any, Dict
from unittest.mock import Mock

from agenticlens import profile, step


def create_mock_response(prompt_tokens: int, completion_tokens: int, content: str) -> Mock:
    response = Mock()
    response.usage.prompt_tokens = prompt_tokens
    response.usage.completion_tokens = completion_tokens
    response.content = content
    response.model = "gpt-4o"
    return response


def code_analyzer_agent(code: str) -> Dict[str, Any]:
    """
    Agent 1: Analyzes code structure.
    Cost: 2,100 tokens
    """
    print("\n[Agent 1] Code Analyzer examining structure...")

    response = create_mock_response(
        prompt_tokens=1950,
        completion_tokens=320,
        content="Code quality: 7.5/10, Complexity: Medium, Maintainability: Good"
    )

    return {"response": response}


def security_auditor_agent(code: str) -> Dict[str, Any]:
    """
    Agent 2: Checks security.
    Cost: 1,800 tokens
    """
    print("[Agent 2] Security Auditor scanning for vulnerabilities...")

    response = create_mock_response(
        prompt_tokens=1650,
        completion_tokens=280,
        content="Security issues: 2 (medium severity), Fix: Input validation"
    )

    return {"response": response}


def test_planner_agent(code: str) -> Dict[str, Any]:
    """
    Agent 3: Plans tests.
    Cost: 1,600 tokens
    """
    print("[Agent 3] Test Planner designing coverage...")

    response = create_mock_response(
        prompt_tokens=1480,
        completion_tokens=260,
        content="Test plan: 12 unit tests, 5 integration tests, 2 e2e tests"
    )

    return {"response": response}


def documentation_generator_agent(code: str) -> Dict[str, Any]:
    """
    Agent 4: Generates documentation.
    Cost: 1,400 tokens
    """
    print("[Agent 4] Documentation Generator creating docstrings...")

    response = create_mock_response(
        prompt_tokens=1280,
        completion_tokens=240,
        content="Generated: 8 function docstrings, 1 module docstring"
    )

    return {"response": response}


def feedback_synthesizer_agent(all_reviews: str) -> Dict[str, Any]:
    """
    Agent 5: Combines all feedback.
    Cost: 2,200 tokens
    Problem: Receives all analyses, uses only key points
    """
    print("[Agent 5] Feedback Synthesizer combining reviews...")

    response = create_mock_response(
        prompt_tokens=2050,
        completion_tokens=380,
        content="Overall: Good code. Priority fixes: 2 security issues, add tests. Minor: add docstrings"
    )

    return {"response": response}


def run_use_case_5():
    """Execute Use Case 5: Code Review System"""

    print("\n" + "="*70)
    print(f"USE CASE 5: Automated Code Review System")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*70)

    with profile("Automated Code Review System") as workflow:

        with step("Code Analyzer", type="planner", agent_name="analyzer", agent_role="code_expert", provider="openai", model="gpt-4o") as s:
            ana_result = code_analyzer_agent("code.py")
            s.record(ana_result["response"])

        with step("Security Auditor", type="llm_call", agent_name="security_auditor", agent_role="security_expert", handoff_from="analyzer", handoff_tokens=2420, provider="openai", model="gpt-4o") as s:
            sec_result = security_auditor_agent("code.py")
            s.record(sec_result["response"])

        with step("Test Planner", type="llm_call", agent_name="test_planner", agent_role="qa_engineer", handoff_from="analyzer", handoff_tokens=2420, provider="openai", model="gpt-4o") as s:
            test_result = test_planner_agent("code.py")
            s.record(test_result["response"])

        with step("Documentation Generator", type="llm_call", agent_name="doc_generator", agent_role="technical_writer", handoff_from="analyzer", handoff_tokens=2420, provider="openai", model="gpt-4o") as s:
            doc_result = documentation_generator_agent("code.py")
            s.record(doc_result["response"])

        with step("Feedback Synthesizer", type="final_response", agent_name="synthesizer", agent_role="review_lead", handoff_from="security_auditor,test_planner,doc_generator", handoff_tokens=1930 + 1860 + 1720, provider="openai", model="gpt-4o") as s:
            syn_result = feedback_synthesizer_agent("")
            s.record(syn_result["response"])

    print("\n" + "="*70)
    print("WORKFLOW SUMMARY")
    print("="*70)
    print(f"Total Tokens Used: {workflow.total_tokens:,}")
    print(f"Expected Range: 12,000-18,000 tokens")
    print(f"Status: {'✓ WITHIN RANGE' if 12000 <= workflow.total_tokens <= 18000 else '⚠ OUT OF RANGE'}")
    print()
    print("Breakdown by Agent:")
    for step_obj in workflow.steps:
        pct = (step_obj.metrics.total_tokens / workflow.total_tokens * 100)
        print(f"  {step_obj.name:28s} {step_obj.metrics.total_tokens:6,} tokens ({pct:4.0f}%)")
    print("="*70)

    return {"total_tokens": workflow.total_tokens, "workflow": workflow}


if __name__ == "__main__":
    print("Starting Use Case 5: Automated Code Review System")
    print(f"Timestamp: {datetime.now().isoformat()}")

    result = run_use_case_5()

    print("\n" + "="*70)
    print("WORKFLOW COMPLETE ✓")
    print("="*70)
    print("\nNext steps:")
    print("  1. uv run agenticlens report usecase_5.json")
    print("  2. uv run agenticlens analyze usecase_5.json")
    print("\nAgentIceLens will identify:")
    print("  - Parallel agent handoffs")
    print("  - Context duplication (3 agents get same code)")
    print("  - Expected savings: 40-50%")
    print("="*70)
