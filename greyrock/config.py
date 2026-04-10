import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# Financial data lives on an encrypted mount — set GREYROCK_DATA_DIR env var
# Falls back to the local memory/agents/ directory for development
MEMORY_DIR = Path(os.environ.get(
    "GREYROCK_DATA_DIR",
    str(PROJECT_ROOT / "memory" / "agents"),
))
