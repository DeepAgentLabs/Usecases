#!/usr/bin/env python3
"""
USE CASE 4: Multimodal Photo Analysis (Google Gemini Pattern)

Real-world scenario: E-commerce product catalog processing
- Image Analyzer: Processes product photos (vision)
- Quality Inspector: Checks for defects and issues
- Metadata Extractor: Pulls name, price, SKU
- Catalog Formatter: Structures data for database

Token Usage Expected: 3K-5K tokens
Optimization Potential: 20-30%

Pattern: Uses Google Gemini multimodal capabilities (vision + text)

Run with AgentIceLens:
  uv run agenticlens profile examples/usecase_4_multimodal_analysis.py --save usecase_4.json
  uv run agenticlens analyze usecase_4.json
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
    response.model = "gemini-2.0-flash"
    return response


def image_analyzer_agent(image_path: str) -> Dict[str, Any]:
    """
    Agent 1: Analyzes product image using vision.
    Cost: 1,100 tokens (vision tokens included)
    """
    print("\n[Agent 1] Image Analyzer processing product photo...")

    response = create_mock_response(
        prompt_tokens=1050,
        completion_tokens=200,
        content="Product: Laptop, Color: Silver, Condition: Excellent"
    )

    return {"response": response}


def quality_inspector_agent(image_analysis: str) -> Dict[str, Any]:
    """
    Agent 2: Checks for defects.
    Cost: 820 tokens
    """
    print("[Agent 2] Quality Inspector checking for defects...")

    response = create_mock_response(
        prompt_tokens=750,
        completion_tokens=180,
        content="Quality: Excellent (99/100), No defects detected"
    )

    return {"response": response}


def metadata_extractor_agent(analysis: str) -> Dict[str, Any]:
    """
    Agent 3: Extracts metadata.
    Cost: 680 tokens
    Problem: Receives full analysis, uses only key fields
    """
    print("[Agent 3] Metadata Extractor pulling structured data...")

    response = create_mock_response(
        prompt_tokens=620,
        completion_tokens=150,
        content="SKU: LP-2024-001, Price: $899, Category: Electronics"
    )

    return {"response": response}


def catalog_formatter_agent(metadata: str) -> Dict[str, Any]:
    """
    Agent 4: Formats for database.
    Cost: 540 tokens
    """
    print("[Agent 4] Catalog Formatter structuring output...")

    response = create_mock_response(
        prompt_tokens=480,
        completion_tokens=120,
        content='{"sku":"LP-2024-001","name":"Laptop","price":899,"category":"Electronics"}'
    )

    return {"response": response}


def run_use_case_4():
    """Execute Use Case 4: Multimodal Photo Analysis"""

    print("\n" + "="*70)
    print(f"USE CASE 4: Multimodal Photo Analysis")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*70)

    with profile("Multimodal Photo Analysis") as workflow:

        with step("Image Analyzer", type="llm_call", agent_name="image_analyzer", agent_role="vision_processor", provider="google", model="gemini-2.0-flash") as s:
            img_result = image_analyzer_agent("product.jpg")
            s.record(img_result["response"])

        with step("Quality Inspector", type="llm_call", agent_name="quality_inspector", agent_role="qa_specialist", handoff_from="image_analyzer", handoff_tokens=1250, provider="google", model="gemini-2.0-flash") as s:
            qual_result = quality_inspector_agent("")
            s.record(qual_result["response"])

        with step("Metadata Extractor", type="llm_call", agent_name="metadata_extractor", agent_role="data_engineer", handoff_from="quality_inspector", handoff_tokens=930, provider="google", model="gemini-2.0-flash") as s:
            meta_result = metadata_extractor_agent("")
            s.record(meta_result["response"])

        with step("Catalog Formatter", type="final_response", agent_name="formatter", agent_role="data_formatter", handoff_from="metadata_extractor", handoff_tokens=770, provider="google", model="gemini-2.0-flash") as s:
            format_result = catalog_formatter_agent("")
            s.record(format_result["response"])

    print("\n" + "="*70)
    print("WORKFLOW SUMMARY")
    print("="*70)
    print(f"Total Tokens Used: {workflow.total_tokens:,}")
    print(f"Expected Range: 3,000-5,000 tokens")
    print(f"Status: {'✓ WITHIN RANGE' if 3000 <= workflow.total_tokens <= 5000 else '⚠ OUT OF RANGE'}")
    print()
    print("Breakdown by Agent:")
    for step_obj in workflow.steps:
        pct = (step_obj.metrics.total_tokens / workflow.total_tokens * 100)
        print(f"  {step_obj.name:28s} {step_obj.metrics.total_tokens:6,} tokens ({pct:4.0f}%)")
    print("="*70)

    return {"total_tokens": workflow.total_tokens, "workflow": workflow}


if __name__ == "__main__":
    print("Starting Use Case 4: Multimodal Photo Analysis")
    print(f"Timestamp: {datetime.now().isoformat()}")

    result = run_use_case_4()

    print("\n" + "="*70)
    print("WORKFLOW COMPLETE ✓")
    print("="*70)
    print("\nNext steps:")
    print("  1. uv run agenticlens report usecase_4.json")
    print("  2. uv run agenticlens analyze usecase_4.json")
    print("\nAgentIceLens will identify:")
    print("  - Efficient workflow (only 3.7K tokens)")
    print("  - Good context distribution")
    print("  - Model efficiency optimization")
    print("="*70)
