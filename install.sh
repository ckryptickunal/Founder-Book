#!/usr/bin/env bash
# Founder Book — one-command installer.
# Installs Python dependencies, then runs the guided setup (API keys, models,
# and your terminal launch keyword).
set -e
cd "$(dirname "$0")"

echo "▸ Installing Python dependencies…"
python3 -m pip install -q -r requirements.txt

echo
echo "▸ Starting guided setup…"
python3 setup_cli.py

echo
echo "Tip: you can re-run setup anytime with  python3 setup_cli.py"
