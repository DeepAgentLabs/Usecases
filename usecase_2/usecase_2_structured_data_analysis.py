#!/usr/bin/env python3
"""
USE CASE 2: Structured Data Analysis (OpenAI Official Pattern)

Real-world scenario: Multi-agent data processing pipeline
- Parser Agent: Extract and validate fields
- Analysis Agent: Apply statistical methods
- Visualization Agent: Plan visualizations

Token Usage Expected: 8K-12K tokens
Optimization Potential: 25-35%

Run with AgentIceLens:
  uv run agenticlens profile examples/usecase_2_structured_data_analysis.py --save usecase_2.json
  uv run agenticlens analyze usecase_2.json
"""

from datetime import datetime
from typing import Any, Dict
from unittest.mock import Mock

from agenticlens import profile, step


def create_mock_response(
    prompt_tokens: int,
    completion_tokens: int,
    content: str,
    provider: str = "openai"
) -> Mock:
    """Create realistic mock LLM response with usage metrics."""
    response = Mock()
    response.usage.prompt_tokens = prompt_tokens
    response.usage.completion_tokens = completion_tokens
    response.content = content
    response.model = "gpt-4o"
    return response


SAMPLE_DATASET = """
Dataset: Customer Purchase History (100 records)
Columns: customer_id, age, purchase_amount, category, date, region
Sample rows:
- 001,25,145.50,electronics,2024-08-01,west
- 002,35,89.99,clothing,2024-08-02,east
- 003,42,245.00,home,2024-08-03,central
...
Data quality: Some missing values, outliers present
"""

# ============================================================
# AGENT 1: DATA PARSER
# ============================================================

def data_parser_agent(dataset: str) -> Dict[str, Any]:
    """
    Agent 1: Parses and validates raw data.

    Typical cost:
    - System prompt: 400 tokens
    - Data input: 350 tokens
    - Parsing output: ~180 tokens completion
    Total: ~930 tokens
    """
    print("\n[Agent 1] Data Parser extracting and validating fields...")

    system_prompt = """You are a data parsing specialist.
Extract fields, validate schema, identify missing values and data quality issues.
Report: field types, record count, quality score, issues found.
Format: Structured JSON output."""

    parsing_result = f"""
DATA PARSING RESULTS

Schema Extraction:
- customer_id: string (ID field)
- age: integer (range: 18-80)
- purchase_amount: float (range: $10-$5000)
- category: string (5 categories found)
- date: date (format: YYYY-MM-DD)
- region: string (4 regions: west, east, central, south)

Record Statistics:
- Total records: 100
- Valid records: 98
- Invalid records: 2
- Missing values: 3
- Duplicates: 0

Data Quality Score: 96/100

Issues Found:
⚠ 2 records with invalid dates
⚠ 3 NULL values in age field
⚠ 2 outliers in purchase_amount (>$4000)

Recommendation: Data is clean, minor issues easily fixable
"""

    response = create_mock_response(
        prompt_tokens=930,
        completion_tokens=280,
        content=parsing_result
    )

    return {
        "parsed_data": parsing_result,
        "quality_score": 0.96,
        "response": response
    }


# ============================================================
# AGENT 2: ANALYSIS AGENT
# ============================================================

def analysis_agent(parsed_data: str) -> Dict[str, Any]:
    """
    Agent 2: Applies statistical analysis.

    Typical cost:
    - System prompt: 400 tokens (REPEATED - caching opportunity!)
    - Parsed data input: 280 tokens
    - Analysis output: ~320 tokens completion
    Total: ~1000 tokens

    PROBLEM: Same system prompt as Agent 1
    """
    print("[Agent 2] Analysis Agent applying statistical methods...")

    system_prompt = """You are a statistical analyst.
Analyze data patterns, calculate metrics, identify trends.
Provide: descriptive statistics, correlations, insights.
Format: Clear, numerical output."""

    analysis_output = f"""
STATISTICAL ANALYSIS

Descriptive Statistics:
- Age: mean=38.5, median=37, std=12.3, range=[18, 75]
- Purchase Amount: mean=$187.42, median=$165, std=$95.32
- Regional Distribution: West(28%), East(22%), Central(35%), South(15%)
- Category Distribution: Electronics(30%), Clothing(25%), Home(20%), Food(15%), Other(10%)

Correlations:
- Age vs Purchase Amount: +0.42 (moderate positive)
- Region vs Purchase Amount: -0.15 (weak negative)
- Category vs Amount: varies by category (home highest avg: $245)

Trends:
- Purchases trending upward: +2.5% month-over-month
- West region showing growth: +5% vs last quarter
- Electronics category: steady, strong performer

Key Insights:
1. Middle-aged customers (35-50) spend most
2. Central region largest by volume
3. Electronics most profitable
4. Clear seasonal patterns (summer peak)

Confidence Levels: 95% for population > 50, 78% for < 30
"""

    response = create_mock_response(
        prompt_tokens=1000,
        completion_tokens=380,
        content=analysis_output
    )

    return {
        "analysis": analysis_output,
        "confidence": 0.87,
        "response": response
    }


# ============================================================
# AGENT 3: VISUALIZATION AGENT
# ============================================================

def visualization_agent(analysis: str) -> Dict[str, Any]:
    """
    Agent 3: Plans visualizations.

    Typical cost:
    - System prompt: 400 tokens
    - Analysis context: 380 tokens (full copy - efficiency issue!)
    - Visualization plan: ~240 tokens completion
    Total: ~1020 tokens

    PROBLEM: Receives full analysis but only uses key insights
    Efficiency: ~50%
    """
    print("[Agent 3] Visualization Agent planning charts...")

    system_prompt = """You are a visualization expert.
Plan charts and dashboards based on analysis.
Recommend: chart types, metrics to highlight, layout.
Format: Structured visualization plan."""

    visualization_plan = f"""
VISUALIZATION PLAN

Dashboard Layout (4-widget layout):

Widget 1: Age vs Purchase Amount (Scatter plot)
- Axes: Age (X), Purchase Amount (Y)
- Color: By region
- Size: By frequency
- Insight: Shows correlation pattern

Widget 2: Regional Breakdown (Pie chart)
- Segments: 4 regions
- Size: By volume
- Highlight: Central (35%)
- Insight: Market concentration

Widget 3: Category Trends (Line chart)
- Lines: 5 categories
- X-Axis: Time (months)
- Y-Axis: Total sales
- Highlight: Electronics steady, Home growing
- Insight: Trend patterns over time

Widget 4: Key Metrics (KPI cards)
- Total Revenue: $18,742
- Avg Purchase: $187.42
- Customer Count: 100
- Quality Score: 96/100
- Insight: Overall performance summary

Recommended Colors:
- West: Blue, East: Green, Central: Orange, South: Red
- Electronics: Dark blue, Clothing: Purple, Home: Brown

Interactive Elements:
- Filter by region (dropdown)
- Filter by date range (date picker)
- Toggle categories (checkboxes)

Best Practices Applied:
✓ Use contrasting colors
✓ Include legends and labels
✓ Show confidence intervals
✓ Highlight key insights
"""

    response = create_mock_response(
        prompt_tokens=1020,
        completion_tokens=360,
        content=visualization_plan
    )

    return {
        "visualization_plan": visualization_plan,
        "response": response
    }


# ============================================================
# MAIN WORKFLOW
# ============================================================

def run_use_case_2():
    """Execute Use Case 2: Structured Data Analysis"""

    analysis_date = datetime.now().strftime("%Y-%m-%d")

    print("\n" + "="*70)
    print(f"USE CASE 2: Structured Data Analysis")
    print(f"Date: {analysis_date}")
    print("="*70)

    with profile("Structured Data Analysis") as workflow:

        # ============================================================
        # STEP 1: DATA PARSER
        # ============================================================
        with step(
            "Data Parser",
            type="planner",
            agent_name="parser_agent",
            agent_role="data_engineer",
            provider="openai",
            model="gpt-4o-mini",
        ) as s:
            parser_result = data_parser_agent(SAMPLE_DATASET)
            s.record(parser_result["response"])

        # ============================================================
        # STEP 2: ANALYSIS AGENT
        # ============================================================
        with step(
            "Analysis",
            type="llm_call",
            agent_name="analysis_agent",
            agent_role="statistician",
            handoff_from="parser_agent",
            handoff_tokens=930,
            provider="openai",
            model="gpt-4o-mini",
        ) as s:
            analysis_result = analysis_agent(parser_result["parsed_data"])
            s.record(analysis_result["response"])

        # ============================================================
        # STEP 3: VISUALIZATION AGENT
        # ============================================================
        with step(
            "Visualization Planning",
            type="llm_call",
            agent_name="viz_agent",
            agent_role="visualization_designer",
            handoff_from="analysis_agent",
            handoff_tokens=1000,
            provider="openai",
            model="gpt-4o-mini",
        ) as s:
            viz_result = visualization_agent(analysis_result["analysis"])
            s.record(viz_result["response"])

    # ============================================================
    # SUMMARY
    # ============================================================
    print("\n" + "="*70)
    print("WORKFLOW SUMMARY")
    print("="*70)
    print(f"Total Tokens Used: {workflow.total_tokens:,}")
    print(f"Expected Range: 8,000-12,000 tokens")
    print(f"Status: {'✓ WITHIN RANGE' if 8000 <= workflow.total_tokens <= 12000 else '⚠ OUT OF RANGE'}")
    print()
    print("Breakdown by Agent:")
    for step_obj in workflow.steps:
        pct = (step_obj.metrics.total_tokens / workflow.total_tokens * 100)
        print(f"  {step_obj.name:28s} {step_obj.metrics.total_tokens:6,} tokens ({pct:4.0f}%)")
    print("="*70)

    return {
        "parser_result": parser_result,
        "analysis_result": analysis_result,
        "viz_result": viz_result,
        "total_tokens": workflow.total_tokens,
        "workflow": workflow
    }


if __name__ == "__main__":
    print("Starting Use Case 2: Structured Data Analysis")
    print(f"Timestamp: {datetime.now().isoformat()}")

    result = run_use_case_2()

    print("\n" + "="*70)
    print("WORKFLOW COMPLETE ✓")
    print("="*70)
    print("\nNext steps:")
    print("  1. uv run agenticlens report usecase_2.json")
    print("  2. uv run agenticlens analyze usecase_2.json")
    print("\nAgentIceLens will identify:")
    print("  - Repeated system prompts (400 tokens × 3 agents)")
    print("  - Full context passing (efficiency: 50%)")
    print("  - Expected savings: 25-35%")
    print("="*70)
