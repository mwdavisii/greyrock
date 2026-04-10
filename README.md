# Greyrock Wealth Management

A personal wealth management advisory system powered by a multi-agent AI team. Ask financial questions and get coordinated perspectives from six specialist agents, orchestrated by a Managing Director that synthesizes their responses into a unified roundtable format.

## How It Works

Greyrock uses the [Claude Agent SDK](https://docs.anthropic.com/en/docs/agents) to run a team of AI specialists, each with domain expertise in a different area of personal finance:

| Specialist | Role |
|---|---|
| **Financial Planner** | Big-picture goals, budgets, savings strategy |
| **Accountant** | Net worth tracking, account balances, financial data |
| **Tax Advisor** | Tax implications, deductions, timing strategies |
| **Broker** | Trade recommendations, rebalancing, asset allocation |
| **Investment Researcher** | Individual asset analysis (stocks, funds, crypto, bonds) |
| **Portfolio Researcher** | Portfolio-level diversification, risk, and benchmarking |

When you ask a question, the **Managing Director** determines which specialists are relevant, dispatches them in parallel, and synthesizes their responses. Disagreements between specialists are surfaced explicitly so you can make informed decisions.

## Prerequisites

- Python 3.12+
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated (no separate API key needed)

## Quick Start

```bash
# Clone and install
git clone <repo-url> && cd greyrock
python -m venv .venv && source .venv/bin/activate
pip install -e "."

# Set up your financial profile
cp memory/agents/shared_financial_profile.example.md memory/agents/shared_financial_profile.md
# Edit shared_financial_profile.md with your actual financial data

# Start a session
greyrock chat
```

## Usage

### Interactive Chat

```bash
greyrock chat
```

Opens an interactive session where you can ask questions like:

- "Should I max out my 401(k) or pay down my mortgage faster?"
- "What are the tax implications of converting my rollover IRA to a Roth?"
- "How diversified is my portfolio and where are the gaps?"

Type `quit` or `exit` to end the session.

### View Financial Profile

```bash
greyrock status
```

Displays your current financial profile summary.

## Financial Profile

The system uses a shared financial profile (`memory/agents/shared_financial_profile.md`) to give each specialist context about your situation. This file includes household details, income, tax information, accounts, and holdings.

An example template is provided at `memory/agents/shared_financial_profile.example.md`. Copy it and fill in your real data to get personalized advice.

**Important:** The real profile is gitignored and will never be committed. Do not commit files containing real tax data, SSNs, account numbers, or income figures.

## Customizing Specialists

Each specialist's behavior is controlled by a prompt file in the `prompts/` directory. You can tune these without changing any code:

```
prompts/
  managing_director.md
  accountant.md
  financial_planner.md
  tax_advisor.md
  broker.md
  investment_researcher.md
  portfolio_researcher.md
```

## Project Structure

```
greyrock/
  cli.py                 # CLI entry point (click)
  config.py              # Path configuration
  orchestrator/
    director.py          # Managing Director — routes and synthesizes
  agents/
    base.py              # Specialist definitions and prompt building
  tools/                 # Financial tools (importers, tax engine, etc.)
  memory/                # Per-agent persistent memory
prompts/                 # System prompts for each agent
memory/
  agents/
    shared_financial_profile.example.md   # Template (committed)
    shared_financial_profile.md           # Your real data (gitignored)
tests/                   # Unit and integration tests
```

## Testing

```bash
pip install -e ".[dev]"
pytest -v                    # unit tests
pytest -m integration        # integration tests (calls Claude API)
```

## Disclaimer

Greyrock is a personal tool, not a licensed financial advisor. The specialist agents provide analysis and perspectives to help inform your decisions, but their output should not be treated as professional financial, tax, or legal advice. Always consult qualified professionals for significant financial decisions.
