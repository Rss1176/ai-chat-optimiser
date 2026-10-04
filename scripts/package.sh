#!/usr/bin/env bash
# Build dist/chat-optimiser.zip for upload to Claude (one top-level folder containing SKILL.md).
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$root/dist"
rm -f "$root/dist/chat-optimiser.zip"
cd "$root/skill"
zip -rq "$root/dist/chat-optimiser.zip" chat-optimiser -x '*/__pycache__/*' '*.pyc' '*/.DS_Store'
echo "Built dist/chat-optimiser.zip"
