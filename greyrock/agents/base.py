"""Specialist agent definitions for the Claude Agent SDK."""

from pathlib import Path

from greyrock.config import PROMPTS_DIR, MEMORY_DIR


def _load_text(path: Path) -> str:
    if path.exists():
        return path.read_text()
    return ""


def _load_financial_profile() -> str:
    profile_path = MEMORY_DIR / "shared_financial_profile.md"
    return _load_text(profile_path)


def build_specialist_prompt(prompt_file: str) -> str:
    """Build the full system prompt for a specialist agent."""
    base = _load_text(PROMPTS_DIR / prompt_file)
    profile = _load_financial_profile()
    return (
        f"{base}\n\n"
        f"<financial_profile>\n{profile}\n</financial_profile>\n\n"
        "## Response Format\n"
        "Respond with your perspective on the user's question from your domain expertise.\n"
        "If the question is outside your domain, say RELEVANCE: none and stop.\n"
        "If you have caveats or disagree with likely advice from other specialists, "
        "note them as FLAGS at the end.\n"
    )


# Specialist definitions: name -> (description, prompt_file)
SPECIALISTS = {
    "accountant": (
        "Net worth tracker — reports account balances, holdings, and financial data.",
        "accountant.md",
    ),
    "financial_planner": (
        "Lead advisor — big-picture goals, budgets, savings strategy, and routing guidance.",
        "financial_planner.md",
    ),
    "tax_advisor": (
        "Tax implications, penalties, deductions, timing strategies, and tax optimization.",
        "tax_advisor.md",
    ),
    "broker": (
        "Trade recommendations, rebalancing, asset allocation, and specific holdings analysis.",
        "broker.md",
    ),
    "investment_researcher": (
        "Individual asset analysis — stocks, funds, crypto, bonds, fundamentals.",
        "investment_researcher.md",
    ),
    "portfolio_researcher": (
        "Portfolio-level analysis — diversification, risk, correlation, benchmarking.",
        "portfolio_researcher.md",
    ),
}
