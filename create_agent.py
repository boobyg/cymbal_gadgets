#!/usr/bin/env python3
"""
Task 1, Step 1: Create Conversational Analytics Agent
Runs from root repository directory with zero external dependencies.
"""
import os
import sys
from pathlib import Path

# Add agentic_web_app directory to Python module search path
APP_DIR = Path(__file__).resolve().parent / "agentic_web_app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from create_agent import main

if __name__ == "__main__":
    main()
