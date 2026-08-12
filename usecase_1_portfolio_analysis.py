#!/usr/bin/env python3
"""
USE CASE 1: Multi-Agent Portfolio Collaboration (OpenAI Official Pattern)

Real-world scenario: Analyze a stock for investment decision
- MacroEconomic Agent: Market trends, interest rates, inflation
- Fundamental Agent: Company financials, valuation, competitive position
- Quantitative Agent: Statistical signals, momentum, risk metrics
- Synthesis Agent: Combine all analyses into recommendation

Token Usage Expected: 15K-20K tokens
Optimization Potential: 35-45%

Run with AgentIceLens:
  uv run agenticlens profile examples/usecase_1_portfolio_analysis.py --save usecase_1.json
  uv run agenticlens report usecase_1.json
  uv run agenticlens analyze usecase_1.json
"""

from datetime import datetime
from typing import Any, Dict
from unittest.mock import Mock

from agenticlens import profile, step


# ============================================================
# MOCK DATA & SIMULATED LLM RESPONSES
# ============================================================

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


MACRO_DATA = """
Current Macroeconomic Indicators (as of Aug 2026):
- Federal Funds Rate: 4.5% (down from 5.25%)
- Inflation Rate (CPI): 3.2% YoY (target: 2%)
- Unemployment Rate: 4.1%
- GDP Growth: 2.8% annualized
- Treasury Yield (10-year): 3.8%
- Market Sentiment: Cautiously optimistic
- Tech Sector: Strong earnings growth, 8% YoY
- Interest Rate Outlook: Potential cuts in Q4 2026
"""

COMPANY_FUNDAMENTALS = """
Apple Inc. Financial Data (TTM - Trailing Twelve Months):
- Stock Price: $230.50
- Market Cap: $3.2T
- P/E Ratio: 28.5x
- Revenue: $394.3B (+5% YoY)
- Net Income: $96.9B (+2% YoY)
- Free Cash Flow: $110.6B
- Debt/Equity: 0.62
- Return on Equity (ROE): 98.3%
- Competitive Position: #1 in premium smartphones, strong ecosystem
- Risks: China exposure, iPhone dependency, regulatory scrutiny
"""

PRICE_DATA = """
Apple Stock Technical Analysis (Last 252 trading days):
- 52-Week High: $245.20
- 52-Week Low: $168.45
- Moving Average (50-day): $225.10
- Moving Average (200-day): $195.80
- RSI (14): 58.2 (neutral zone)
- MACD: Bullish crossover 15 days ago
- Volume: 45.2M shares/day (average)
- Beta: 1.19 (more volatile than market)
- Volatility (30-day): 18.5%
- Support Level: $220.00
- Resistance Level: $240.00
"""


# ============================================================
# AGENT 1: MACROECONOMIC ANALYSIS
# ============================================================

def macro_economic_agent(ticker: str) -> Dict[str, Any]:
    """
    Agent 1: Analyzes macroeconomic environment impact on investment.

    Typical cost in real scenario:
    - System prompt: 400 tokens
    - Data input: 450 tokens
    - Analysis: ~210 tokens completion
    Total: ~850 prompt + 210 completion = 1,060 tokens

    PROBLEM IDENTIFIED BY AGENTICLENS:
    - System prompt (400 tokens) is repeated identically for every call
    - Candidate for prompt caching: save 400 tokens per call
    - Monthly impact (1000 calls): 400K tokens = $0.40/month
    """

    print("\n[Agent 1] MacroEconomic Agent analyzing market environment...")

    # System prompt (will be identified as repeated)
    system_prompt = """You are a macroeconomic analyst specializing in investment impact assessment.
Analyze the current macroeconomic environment and its impact on tech stocks.
Consider: interest rates, inflation, GDP growth, market sentiment, sector trends.
Provide: Economic outlook, sector impact, risk factors, investment implications.
Format: Clear assessment with 2-3 key implications."""

    macro_analysis = f"""
MACROECONOMIC ANALYSIS FOR TECH SECTOR

Environment Assessment:
- Interest Rate Environment: FAVORABLE
  * Fed Funds Rate declining (5.25% → 4.5%)
  * Rate cuts likely in Q4 2026
  * Impact: Lower cost of capital, improved valuations

- Inflation Outlook: MODERATING
  * Current: 3.2% (above 2% target but trending down)
  * Impact: Margins may benefit, consumer spending remains cautious

- Economic Growth: SOLID
  * GDP: 2.8% annualized (healthy)
  * Tech sector: 8% YoY growth (outperforming market)

- Market Sentiment: CAUTIOUSLY OPTIMISTIC
  * Tech leadership remains strong
  * AI enthusiasm continues (though moderating from peak)
  * Rotation risk: If rates rise again

SECTOR IMPACT (Tech):
- Positive: Lower discount rates, strong earnings growth, AI investment
- Risks: China exposure, margin compression if competition increases

INVESTMENT IMPLICATION:
Macro environment is supportive for tech investments. Rate cuts would be
significant positive catalyst. Current positioning: FAVORABLE with attention
to geopolitical risks.

Confidence Level: 78%
"""

    response = create_mock_response(
        prompt_tokens=850,  # System + data
        completion_tokens=280,
        content=macro_analysis
    )

    return {
        "analysis": macro_analysis,
        "confidence": 0.78,
        "response": response
    }


# ============================================================
# AGENT 2: FUNDAMENTAL ANALYSIS
# ============================================================

def fundamental_agent(ticker: str, macro_context: str) -> Dict[str, Any]:
    """
    Agent 2: Deep dive into company fundamentals and valuation.

    Typical cost in real scenario:
    - System prompt: 400 tokens
    - Company data: 600 tokens
    - Macro context (handoff): 280 tokens (from Agent 1)
    - Analysis: ~380 tokens completion
    Total: ~1,280 prompt + 380 completion = 1,660 tokens

    PROBLEM IDENTIFIED BY AGENTICLENS:
    - Receives full macro_analysis from Agent 1 (280 tokens)
    - Only uses 40% of macro content (efficiency: 40%)
    - Candidate for structured handoff: Pass only relevant facts
    - Estimated savings: ~168 tokens per call (40% of 420)
    """

    print("[Agent 2] Fundamental Analyst evaluating company...")

    system_prompt = """You are an equity analyst specializing in technology companies.
Analyze company fundamentals: valuation, growth, profitability, competitive position.
Compare against industry peers and growth prospects.
Provide: Valuation assessment, growth outlook, competitive advantages, risks."""

    fundamental_analysis = f"""
FUNDAMENTAL ANALYSIS: APPLE INC. (AAPL)

VALUATION ASSESSMENT:
- P/E Ratio: 28.5x
  * Industry average (tech): 26.2x
  * Status: SLIGHTLY PREMIUM (4% above peer average)
  * Historical: Apple typically trades 10-15% premium
  * Assessment: FAIRLY VALUED in current environment

- PEG Ratio: 5.7x (P/E / Growth Rate)
  * Growth rate: 5% (conservative estimate)
  * Interpretation: Fairly valued given growth rate
  * Benchmark: <2.0 = undervalued, >2.0 = expensive
  * Status: NEUTRAL (at fair value line)

- Price/Book: 42.3x
  * High but justified by ROE (98.3%) and brand value
  * Indicates premium for intangible assets (ecosystem)

FREE CASH FLOW ANALYSIS:
- FCF: $110.6B (very strong)
- FCF Margin: 28% (industry leading)
- Trend: Stable, slight growth
- Capital Allocation: Strong (buybacks, dividends, R&D investment)

COMPETITIVE POSITION:
✓ Strengths:
  - Unmatched ecosystem lock-in (900M+ active devices)
  - Brand strength and pricing power
  - Services business (30% margin, recurring revenue)
  - Supply chain resilience (vertical integration)
  - Strong balance sheet ($50B net cash)

✗ Risks:
  - iPhone dependency (52% of revenue)
  - China exposure (20% of revenue, geopolitical risk)
  - Slowing smartphone upgrade cycles
  - Increased competition in services
  - Regulatory pressure (App Store, China)

GROWTH OUTLOOK:
- Services Growth: 10-12% (accelerating, higher margin)
- Hardware Growth: 3-5% (maturing market)
- Overall Growth: 5-7% (moderate for mega-cap)

VALUATION VERDICT:
Given fundamentals, Apple is FAIRLY VALUED to SLIGHTLY UNDERVALUED at
current levels. Strong competitive position justifies premium P/E.
Growth profile is moderate but predictable and high-quality.

Recommendation: POSITIVE for long-term holding
Fair Value Estimate: $240-260 (slight upside)
Confidence: 82%
"""

    response = create_mock_response(
        prompt_tokens=1280,  # Includes macro context
        completion_tokens=420,
        content=fundamental_analysis
    )

    return {
        "analysis": fundamental_analysis,
        "fair_value": 250,
        "confidence": 0.82,
        "response": response
    }


# ============================================================
# AGENT 3: QUANTITATIVE ANALYSIS
# ============================================================

def quantitative_agent(ticker: str, macro_context: str) -> Dict[str, Any]:
    """
    Agent 3: Statistical signals, momentum, technical analysis.

    Typical cost in real scenario:
    - System prompt: 400 tokens
    - Price data: 350 tokens
    - Macro context (handoff): 280 tokens (from Agent 1)
    - Analysis: ~240 tokens completion
    Total: ~1,030 prompt + 240 completion = 1,270 tokens

    PROBLEM IDENTIFIED BY AGENTICLENS:
    - Duplicate system prompt (400 tokens, same as Agent 1 & 2)
    - Receives macro_context but doesn't use it (0% efficiency)
    - Candidate for prompt caching: Save 400 tokens
    - Candidate for removing unused handoff: Save 280 tokens
    - Total potential savings: 680 tokens per call
    """

    print("[Agent 3] Quantitative Analyst processing signals...")

    system_prompt = """You are a quantitative analyst specializing in statistical and technical analysis.
Analyze price patterns, momentum, volatility, and generate trading signals.
Use technical indicators to assess entry/exit points.
Provide: Trading signals, risk/reward assessment, support/resistance levels."""

    quantitative_analysis = f"""
QUANTITATIVE ANALYSIS: APPLE INC. (AAPL)

TECHNICAL INDICATORS:
- RSI (14): 58.2
  * Range: 0-100 (30=oversold, 70=overbought)
  * Current: NEUTRAL (neither overbought nor oversold)
  * Signal: No extreme condition, room to move either direction

- MACD (Moving Average Convergence Divergence):
  * Status: Bullish crossover 15 days ago
  * Signal: Short-term momentum POSITIVE
  * Strength: Moderate (not extreme)

- Moving Averages:
  * 50-day MA: $225.10
  * 200-day MA: $195.80
  * Current Price: $230.50
  * Signal: Price above both MA (BULLISH trend)
  * Interpretation: Uptrend intact

VOLATILITY ANALYSIS:
- 30-day Volatility: 18.5%
- Historical Average: 19.2%
- Status: BELOW AVERAGE (lower volatility recently)
- Implication: Market is pricing in lower uncertainty
- Risk: Low volatility can precede breakouts

SUPPORT & RESISTANCE:
- Resistance: $240.00 (recent high area)
- Current: $230.50
- Support: $220.00 (20-day MA support)
- Interpretation: Room to $240 with support at $220

MOMENTUM INDICATORS:
- Rate of Change (10-day): +2.3%
- Status: POSITIVE (price momentum upward)
- Volume Trend: Average 45.2M shares (normal)
- Signal: Volume does not support strong move (caution)

RISK ASSESSMENT:
- Beta: 1.19 (20% more volatile than market)
- Downside Risk (to $220): -4.6%
- Upside Potential (to $240): +4.1%
- Risk/Reward Ratio: 1:0.89 (slightly unfavorable in raw terms)
- NOTE: Fundamental support limits downside

TRADING SIGNALS:
- Short-term (1-3 months): BULLISH
  * All technical indicators point upward
  * Trend intact, momentum positive
  * Entry: Dips to $220-225 support

- Medium-term (3-6 months): NEUTRAL TO BULLISH
  * Fundamentals support higher prices
  * Technicals suggest consolidation then breakout

QUANTITATIVE VERDICT:
Technical setup is FAVORABLE for position holding. Low volatility suggests
market is not pricing in major risks. Momentum indicators support continued
strength.

Recommendation: HOLD current positions, BUY on dips to $220-225
Confidence: 75%
"""

    response = create_mock_response(
        prompt_tokens=1030,
        completion_tokens=380,
        content=quantitative_analysis
    )

    return {
        "signals": quantitative_analysis,
        "confidence": 0.75,
        "response": response
    }


# ============================================================
# AGENT 4: SYNTHESIS & RECOMMENDATION
# ============================================================

def synthesis_agent(
    macro_analysis: str,
    fundamental_analysis: str,
    quantitative_signals: str
) -> Dict[str, Any]:
    """
    Agent 4: Combine all analyses into final recommendation.

    Typical cost in real scenario:
    - System prompt: 400 tokens
    - Input analyses: 1,080 tokens (360 from each agent)
    - Response: ~520 tokens completion
    Total: ~1,480 prompt + 520 completion = 2,000 tokens

    PROBLEM IDENTIFIED BY AGENTICLENS:
    - Receives all three agent analyses (1,080 tokens total)
    - Actual decision made on ~40% of content (432 tokens)
    - Efficiency: 40% utilization
    - Candidate for structured synthesis: Pass only key conclusions
    - Estimated savings: ~648 tokens (60% of 1,080)
    - ALSO: Repeated system prompt (400 tokens)
    - Total potential savings: ~1,048 tokens (52% of input)
    """

    print("[Agent 4] Synthesizer combining all analyses...")

    system_prompt = """You are an investment committee synthesizing multiple analyses.
Weigh macro, fundamental, and quantitative perspectives.
Identify areas of agreement and disagreement.
Provide: Clear investment recommendation, position sizing, risk management."""

    synthesis = f"""
INVESTMENT RECOMMENDATION SYNTHESIS

ANALYSIS CONVERGENCE:
✓ All three agents AGREE on:
  1. Current environment is FAVORABLE for Apple
  2. Technical setup is BULLISH (trend + momentum)
  3. Company fundamentals are STRONG
  4. Valuation is FAIR (justified by quality)
  5. Macro environment is SUPPORTIVE (rates declining)

⚠ Areas of SLIGHT DIVERGENCE:
  - Fundamental analyst sees 5% upside to fair value ($250)
  - Quantitative analyst sees 4% upside to resistance ($240)
  - Both conservative, within 1% of each other (good consensus)

CONFIDENCE ASSESSMENT:
- Macro Analysis: 78% confidence
- Fundamental Analysis: 82% confidence
- Quantitative Analysis: 75% confidence
- COMPOSITE CONFIDENCE: 78.3% (GOOD)
  * Indicates high conviction with healthy skepticism

WEIGHTED RECOMMENDATION:
Based on multi-agent consensus:

OVERALL RATING: BUY (with conditions)

Position Sizing:
- For Growth Portfolio: 4-5% position weight (standard tech allocation)
- For Income Portfolio: 3-4% position weight (lower dividend)
- For Conservative: 2-3% position weight (limit tech exposure)

Entry Strategy:
- BULLISH scenario: Add on any dips below $225
- IDEAL entry: $220-223 (support level with margin of safety)
- Current price ($230.50): Reasonable entry if conviction is high

Exit Strategy:
- Take profits at resistance: $240-245 (10% gain)
- Hard stop: $215 (if fundamental thesis breaks)
- Reassess every quarter based on earnings

Risk Management:
- Monitor for: China geopolitical escalation
- Watch: iPhone sales trends (key metric)
- Alert trigger: If FCF declines >5% QoQ
- Diversification: Don't exceed 5% in single stock

Time Horizon:
- Recommended holding period: 12-24 months
- Near-term (0-3mo): Bullish, expect +5% to resistance
- Medium-term (3-12mo): Expect fundamental driving prices higher
- Long-term (12mo+): High-quality compounder

FINAL VERDICT:
Apple represents a high-quality technology investment in a favorable macro
environment. Fundamentals are strong, technicals are bullish, and valuation
is fair. Recommended for most portfolios at current levels or on any
significant dips.

Overall Confidence: 78.3%
Conviction Level: HIGH
Recommendation Duration: 12-24 months
"""

    response = create_mock_response(
        prompt_tokens=1480,
        completion_tokens=620,
        content=synthesis
    )

    return {
        "recommendation": synthesis,
        "rating": "BUY",
        "confidence": 0.783,
        "response": response
    }


# ============================================================
# MAIN WORKFLOW WITH AGENTICLENS PROFILING
# ============================================================

def run_use_case_1():
    """
    Execute Use Case 1: Multi-Agent Portfolio Analysis

    This is a realistic implementation of OpenAI's official pattern.
    AgentIceLens will identify token waste patterns.
    """

    ticker = "AAPL"
    analysis_date = datetime.now().strftime("%Y-%m-%d")

    print("\n" + "="*70)
    print(f"USE CASE 1: Multi-Agent Portfolio Collaboration")
    print(f"Stock: {ticker} | Date: {analysis_date}")
    print("="*70)

    with profile("Multi-Agent Portfolio Analysis") as workflow:

        # ============================================================
        # STEP 1: MACROECONOMIC AGENT
        # ============================================================
        with step(
            "MacroEconomic Analysis",
            type="planner",
            agent_name="macro_agent",
            agent_role="economist",
            provider="openai",
            model="gpt-4o",
        ) as s:
            macro_result = macro_economic_agent(ticker)
            s.record(macro_result["response"])

        # ============================================================
        # STEP 2: FUNDAMENTAL AGENT
        # ============================================================
        with step(
            "Fundamental Analysis",
            type="llm_call",
            agent_name="fundamental_agent",
            agent_role="analyst",
            handoff_from="macro_agent",
            handoff_tokens=1060,  # From macro agent
            provider="openai",
            model="gpt-4o",
        ) as s:
            fundamental_result = fundamental_agent(
                ticker,
                macro_result["analysis"]
            )
            s.record(fundamental_result["response"])

        # ============================================================
        # STEP 3: QUANTITATIVE AGENT
        # ============================================================
        with step(
            "Quantitative Analysis",
            type="llm_call",
            agent_name="quantitative_agent",
            agent_role="quant_analyst",
            handoff_from="macro_agent",
            handoff_tokens=1060,  # From macro agent (PROBLEM: unused!)
            provider="openai",
            model="gpt-4o",
        ) as s:
            quant_result = quantitative_agent(
                ticker,
                macro_result["analysis"]  # Not actually used
            )
            s.record(quant_result["response"])

        # ============================================================
        # STEP 4: SYNTHESIS AGENT (FINAL RECOMMENDATION)
        # ============================================================
        with step(
            "Recommendation Synthesis",
            type="final_response",
            agent_name="synthesis_agent",
            agent_role="recommendation_engine",
            handoff_from="fundamental_agent,quantitative_agent",
            handoff_tokens=1660 + 1270,  # Full analyses passed
            provider="openai",
            model="gpt-4o",
        ) as s:
            synthesis_result = synthesis_agent(
                macro_result["analysis"],
                fundamental_result["analysis"],
                quant_result["signals"]
            )
            s.record(synthesis_result["response"])

    # ============================================================
    # SUMMARY (after workflow context exits)
    # ============================================================
    print("\n" + "="*70)
    print("WORKFLOW SUMMARY")
    print("="*70)

    total_tokens = workflow.total_tokens
    print(f"Total Tokens Used: {total_tokens:,}")
    print(f"Expected Range: 15,000-20,000 tokens")
    print(f"Status: {'✓ WITHIN RANGE' if 15000 <= total_tokens <= 20000 else '⚠ OUT OF RANGE'}")
    print()
    print("Breakdown by Step:")
    for step_obj in workflow.steps:
        pct = (step_obj.metrics.total_tokens / total_tokens * 100)
        print(f"  {step_obj.name:28s} {step_obj.metrics.total_tokens:6,} tokens ({pct:4.0f}%)")
    print("="*70)

    return {
        "recommendation": synthesis_result["recommendation"],
        "rating": synthesis_result["rating"],
        "total_tokens": total_tokens,
        "workflow": workflow
    }


if __name__ == "__main__":
    print("Starting Use Case 1: Multi-Agent Portfolio Analysis")
    print(f"Timestamp: {datetime.now().isoformat()}")

    result = run_use_case_1()

    print("\n" + "="*70)
    print("WORKFLOW COMPLETE ✓")
    print("="*70)
    print(f"\nFinal Recommendation: {result['rating']}")
    print(f"Total Tokens: {result['total_tokens']:,}")
    print("\nNext steps:")
    print("  1. uv run agenticlens report usecase_1.json")
    print("  2. uv run agenticlens analyze usecase_1.json")
    print("\nAgentIceLens will identify:")
    print("  - Repeated system prompts (opportunity for caching)")
    print("  - Unused handoff context (280 tokens in quant agent)")
    print("  - Low-utility analyses (synthesis only uses 40% of input)")
    print("  - Expected savings: 35-45%")
    print("="*70)
