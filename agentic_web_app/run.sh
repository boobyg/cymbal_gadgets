#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "🚀 SME Academy: Looker Conversational Analytics Agent App"
echo "   Directory: $SCRIPT_DIR"
echo "============================================================"

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    echo "   Please install python3 to continue."
    exit 1
fi

# Initialize .env if missing
if [ ! -f .env ] && [ -f .env.example ]; then
    echo "📋 Creating .env from .env.example..."
    cp .env.example .env
    echo "ℹ️  Tip: You can configure your Looker credentials in .env or via"
    echo "   the 'Student Credentials' modal in the web UI at http://localhost:8080"
fi

echo "Starting server on port ${PORT:-8080}..."
echo "If running in Google Cloud Shell in Argolis:"
echo "👉 Click the 'Web Preview' icon in the top right -> 'Preview on port 8080'"
echo "============================================================"

python3 server.py
