#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# Point to your encrypted mount for financial data
export GREYROCK_DATA_DIR="${GREYROCK_DATA_DIR:-/mnt/core_nas/secure_storage/Finances/Greyrock}"

if [ ! -d .venv ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
    source .venv/bin/activate
    pip install -e "." -q
else
    source .venv/bin/activate
fi

if [ ! -f "$GREYROCK_DATA_DIR/shared_financial_profile.md" ]; then
    echo "No financial profile found at: $GREYROCK_DATA_DIR/shared_financial_profile.md"
    echo ""
    echo "Either:"
    echo "  1. Copy the example to your data dir:"
    echo "     mkdir -p $GREYROCK_DATA_DIR"
    echo "     cp memory/agents/shared_financial_profile.example.md $GREYROCK_DATA_DIR/shared_financial_profile.md"
    echo ""
    echo "  2. Or set GREYROCK_DATA_DIR to a different path"
    exit 1
fi

greyrock chat
