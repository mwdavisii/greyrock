# Greyrock

Personal wealth management advisory system with a multi-agent AI team.

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e "."
cp memory/agents/shared_financial_profile.example.md memory/agents/shared_financial_profile.md
# Edit shared_financial_profile.md with your actual data
greyrock chat
```

## Architecture

Orchestrator + Specialists pattern using the Claude Agent SDK.
- **Managing Director**: Routes questions, synthesizes roundtable responses
- **6 Specialists**: Accountant, Financial Planner, Tax Advisor, Broker, Investment Researcher, Portfolio Researcher

Each specialist is a Claude Agent SDK subagent dispatched by the Managing Director.
No API key needed — authenticates through the Claude Code CLI.

## Sensitive Data

- `memory/agents/shared_financial_profile.md` is **gitignored** — contains real financial data
- `memory/agents/shared_financial_profile.example.md` is the anonymized template
- Never commit real tax data, SSNs, account numbers, or income figures

## Testing

```bash
pytest -v                        # all unit tests
pytest -m integration            # integration tests
```

## Project Structure

- `greyrock/orchestrator/` — Managing Director and routing logic
- `greyrock/agents/` — Specialist agent definitions
- `greyrock/tools/` — Financial tools (importers, tax engine, research, analytics)
- `greyrock/memory/` — Per-agent persistent memory and session context
- `prompts/` — System prompts for each agent (tunable without code changes)
- `memory/` — Runtime financial profile data (gitignored)
