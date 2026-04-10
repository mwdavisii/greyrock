"""Greyrock CLI — interactive roundtable chat via Claude Agent SDK."""

import asyncio

import click


@click.group()
def main():
    """Greyrock — Multi-agent wealth management advisory."""
    pass


@main.command()
def chat():
    """Start an interactive advisory session."""
    from greyrock.orchestrator.director import run_chat

    asyncio.run(run_chat())


@main.command()
def status():
    """Show current financial profile summary."""
    from greyrock.config import MEMORY_DIR

    profile_path = MEMORY_DIR / "shared_financial_profile.md"
    if profile_path.exists():
        click.echo(profile_path.read_text())
    else:
        click.echo("No financial profile found. Import data first.")


if __name__ == "__main__":
    main()
