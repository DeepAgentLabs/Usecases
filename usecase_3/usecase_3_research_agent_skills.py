#!/usr/bin/env python3
"""
USE CASE 3: Research Pipeline with Agent Skills (Anthropic Pattern)

Real-world scenario: Multi-agent research system using modular skills
- Query Optimizer Agent: Breaks down research questions
- Literature Fetcher Agent: Retrieves papers with RAG
- Content Summarizer Agent: Condenses long documents
- Synthesizer Agent: Combines findings into report
- Quality Checker Agent: Verifies and detects gaps

Token Usage Expected: 18K-25K tokens
Optimization Potential: 40-50%

Pattern: Uses Anthropic Agent Skills framework (progressive disclosure of context)

Run with AgentIceLens:
  uv run agenticlens profile examples/usecase_3_research_agent_skills.py --save usecase_3.json
  uv run agenticlens analyze usecase_3.json
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
    response.model = "claude-3-5-sonnet-20241022"
    return response


def query_optimizer_agent(query: str) -> Dict[str, Any]:
    """
    Agent 1: Optimizer - Breaks down research question into sub-queries.
    Cost: 1,200 tokens
    """
    print("\n[Agent 1] Query Optimizer breaking down research question...")

    response = create_mock_response(
        prompt_tokens=850,
        completion_tokens=250,
        content="Sub-queries: [1] Background, [2] Methods, [3] Findings, [4] Implications"
    )

    return {"response": response}


def literature_fetcher_agent(sub_queries: str) -> Dict[str, Any]:
    """
    Agent 2: Fetcher - Retrieves papers using RAG.
    Cost: 9,200 tokens (excessive!)
    Problem: Retrieves 30 papers, only 8 are used
    """
    print("[Agent 2] Literature Fetcher retrieving papers (RAG)...")

    response = create_mock_response(
        prompt_tokens=8500,
        completion_tokens=520,
        content="Retrieved 30 papers, ranked by relevance"
    )

    return {"papers_retrieved": 30, "response": response}


def summarizer_agent(papers: str) -> Dict[str, Any]:
    """
    Agent 3: Summarizer - Condenses papers.
    Cost: 6,800 tokens
    Problem: Receives 30 papers, only uses 8
    """
    print("[Agent 3] Content Summarizer condensing documents...")

    response = create_mock_response(
        prompt_tokens=6200,
        completion_tokens=410,
        content="Key findings extracted from papers"
    )

    return {"papers_used": 8, "response": response}


def synthesizer_agent(summaries: str) -> Dict[str, Any]:
    """
    Agent 4: Synthesizer - Combines findings.
    Cost: 5,100 tokens
    Problem: Receives full summaries, uses only 40%
    """
    print("[Agent 4] Synthesizer combining findings...")

    response = create_mock_response(
        prompt_tokens=4800,
        completion_tokens=380,
        content="Research report synthesized from findings"
    )

    return {"response": response}


def quality_checker_agent(report: str) -> Dict[str, Any]:
    """
    Agent 5: Quality Checker - Verifies claims.
    Cost: 3,800 tokens
    Problem: Re-reads full context unnecessarily
    """
    print("[Agent 5] Quality Checker verifying claims...")

    response = create_mock_response(
        prompt_tokens=3600,
        completion_tokens=240,
        content="Claims verified, 2 issues flagged"
    )

    return {"issues_found": 2, "response": response}


def run_use_case_3():
    """Execute Use Case 3: Research Pipeline with Agent Skills"""

    print("\n" + "="*70)
    print(f"USE CASE 3: Research Pipeline with Agent Skills")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*70)

    with profile("Research Pipeline with Agent Skills") as workflow:

        with step("Query Optimizer", type="planner", agent_name="optimizer", agent_role="query_specialist", provider="anthropic", model="claude-3-5-sonnet-20241022") as s:
            opt_result = query_optimizer_agent("Research question")
            s.record(opt_result["response"])

        with step("Literature Fetcher", type="retriever", agent_name="fetcher", agent_role="researcher", handoff_from="optimizer", handoff_tokens=1100, chunk_count=30, avg_tokens_per_chunk=280, provider="anthropic", model="claude-3-5-sonnet-20241022") as s:
            fetch_result = literature_fetcher_agent("")
            s.record(fetch_result["response"])

        with step("Content Summarizer", type="llm_call", agent_name="summarizer", agent_role="analyst", handoff_from="fetcher", handoff_tokens=9020, provider="anthropic", model="claude-3-5-sonnet-20241022") as s:
            sum_result = summarizer_agent("")
            s.record(sum_result["response"])

        with step("Synthesizer", type="llm_call", agent_name="synthesizer", agent_role="writer", handoff_from="summarizer", handoff_tokens=6610, provider="anthropic", model="claude-3-5-sonnet-20241022") as s:
            syn_result = synthesizer_agent("")
            s.record(syn_result["response"])

        with step("Quality Checker", type="llm_call", agent_name="quality_checker", agent_role="reviewer", handoff_from="synthesizer", handoff_tokens=5180, provider="anthropic", model="claude-3-5-sonnet-20241022") as s:
            qc_result = quality_checker_agent("")
            s.record(qc_result["response"])

    print("\n" + "="*70)
    print("WORKFLOW SUMMARY")
    print("="*70)
    print(f"Total Tokens Used: {workflow.total_tokens:,}")
    print(f"Expected Range: 18,000-25,000 tokens")
    print(f"Status: {'✓ WITHIN RANGE' if 18000 <= workflow.total_tokens <= 25000 else '⚠ OUT OF RANGE'}")
    print()
    print("Breakdown by Agent:")
    for step_obj in workflow.steps:
        pct = (step_obj.metrics.total_tokens / workflow.total_tokens * 100)
        print(f"  {step_obj.name:28s} {step_obj.metrics.total_tokens:6,} tokens ({pct:4.0f}%)")
    print("="*70)

    return {"total_tokens": workflow.total_tokens, "workflow": workflow}


if __name__ == "__main__":
    print("Starting Use Case 3: Research Pipeline with Agent Skills")
    print(f"Timestamp: {datetime.now().isoformat()}")

    result = run_use_case_3()

    print("\n" + "="*70)
    print("WORKFLOW COMPLETE ✓")
    print("="*70)
    print("\nNext steps:")
    print("  1. uv run agenticlens report usecase_3.json")
    print("  2. uv run agenticlens analyze usecase_3.json")
    print("\nAgentIceLens will identify:")
    print("  - Excessive paper retrieval (30 retrieved, 8 used)")
    print("  - Low context utilization (40% in synthesis)")
    print("  - Expected savings: 40-50%")
    print("="*70)
