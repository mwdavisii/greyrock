"""Managing Director — orchestrates the specialist roundtable via Claude Agent SDK."""

import asyncio

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AgentDefinition,
    AssistantMessage,
    ResultMessage,
)
from claude_agent_sdk.types import TextBlock

from greyrock.config import PROMPTS_DIR, MEMORY_DIR
from greyrock.agents.base import SPECIALISTS, build_specialist_prompt, _load_text, _load_financial_profile


def _build_director_prompt() -> str:
    base = _load_text(PROMPTS_DIR / "managing_director.md")
    profile = _load_financial_profile()
    specialist_list = "\n".join(
        f"- **{name}**: {desc}" for name, (desc, _) in SPECIALISTS.items()
    )
    return (
        f"{base}\n\n"
        f"<financial_profile>\n{profile}\n</financial_profile>\n\n"
        f"## Available Specialists\n{specialist_list}\n\n"
        "You have access to specialist subagents. For each user question, "
        "dispatch the relevant specialists by using their agent names. "
        "Always include the financial_planner. Bias toward inclusion.\n\n"
        "After receiving specialist responses, synthesize them into a clear "
        "roundtable format. Present each specialist's perspective under their name. "
        "Surface disagreements explicitly. Note follow-up questions.\n"
    )


def _build_agent_definitions() -> dict[str, AgentDefinition]:
    """Build AgentDefinition for each specialist."""
    agents = {}
    for name, (desc, prompt_file) in SPECIALISTS.items():
        agents[name] = AgentDefinition(
            description=desc,
            prompt=build_specialist_prompt(prompt_file),
            tools=["Read"],
        )
    return agents


async def run_roundtable(question: str) -> str:
    """Run a single roundtable consultation and return the synthesized response."""
    options = ClaudeAgentOptions(
        system_prompt=_build_director_prompt(),
        allowed_tools=["Agent", "Read"],
        agents=_build_agent_definitions(),
        max_turns=20,
        cwd=str(PROMPTS_DIR.parent),
    )

    result_text = ""
    async for message in query(prompt=question, options=options):
        if isinstance(message, ResultMessage):
            result_text = message.result or ""
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    result_text = block.text

    return result_text


async def run_chat():
    """Interactive chat loop using ClaudeSDKClient for session continuity."""
    from claude_agent_sdk import ClaudeSDKClient

    options = ClaudeAgentOptions(
        system_prompt=_build_director_prompt(),
        allowed_tools=["Agent", "Read"],
        agents=_build_agent_definitions(),
        max_turns=20,
        cwd=str(PROMPTS_DIR.parent),
    )

    print("\n  Greyrock Wealth Management")
    print("  Your advisory roundtable is ready.\n")
    print("  Type your question, or 'quit' to exit.\n")

    async with ClaudeSDKClient(options=options) as client:
        while True:
            try:
                question = input("  You: ")
            except (EOFError, KeyboardInterrupt):
                print("\n")
                break

            question = question.strip()
            if not question:
                continue
            if question.lower() in ("quit", "exit", "q"):
                break

            print("\n  Consulting the team...\n")

            await client.query(question)
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(block.text)
                elif isinstance(message, ResultMessage):
                    if message.result:
                        print(message.result)

            print()
