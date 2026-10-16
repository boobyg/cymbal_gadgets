#!/usr/bin/env python3
"""
Create Agent Script for Looker Conversational Analytics Lab (Task 1, Step 1)
----------------------------------------------------------------------------
Pure Python 3 standard library implementation (Zero external dependencies).
Works in Google Cloud Shell without installing looker-sdk or any other packages.
"""

import os
import sys
from pathlib import Path

# Ensure agentic_web_app directory is on sys.path so config and looker_client can be imported
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import config
from looker_client import LookerClient


def main():
    print("=" * 64)
    print("🤖 Task 1, Step 1: Create Conversational Analytics Agent")
    print("   Looker API 4.0 | Zero External Dependencies")
    print("=" * 64)

    client_id = config.LOOKER_CLIENT_ID
    client_secret = config.LOOKER_CLIENT_SECRET
    base_url = config.LOOKER_BASE_URL

    # Verify credentials
    if (
        not client_id
        or not client_secret
        or client_id == "specify your own user id / secret"
        or client_secret == "specify your own user id / secret"
    ):
        print("\n⚠️ Looker API credentials not configured in .env.")
        print(f"Base URL: {base_url}")
        print("Please enter your assigned student credentials:")
        try:
            client_id = input("  Looker Client ID: ").strip()
            client_secret = input("  Looker Client Secret: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            sys.exit(1)

        if not client_id or not client_secret:
            print("❌ Error: Client ID and Client Secret are required.")
            sys.exit(1)

    print(f"\n1. Authenticating to Looker API at {base_url}...")
    client = LookerClient(base_url, client_id, client_secret)

    try:
        token = client.login()
        print("   ✅ Authentication successful!")
    except Exception as e:
        print(f"   ❌ Authentication failed: {e}")
        print("   Please check your client_id and client_secret.")
        sys.exit(1)

    model_name = config.DEFAULT_MODEL or "cymbal_gadgets_boris"
    explore_name = config.DEFAULT_EXPLORE or "transactions"
    try:
        student_name = input("\nPlease enter your First Name, Last Name: ").strip()
    except (KeyboardInterrupt, EOFError):
        student_name = ""
    if not student_name:
        student_name = "First Name Last Name"
    agent_name = f"Cymbal Retail Analytics Agent - {student_name}"
    instructions = (
        "- Always use Gross Margin Percentage when asked about profitability, margin, or sales performance.\n"
        "- When asked for trends over time, group by transaction date or transaction month.\n"
        "- If the user asks for store performance, breakdown by store country.\n"
        "- Keep executive summaries concise with key metrics highlighted in bold."
    )

    print(f"\n2. Calling POST /api/4.0/agents...")
    print(f"   Agent Name: {agent_name}")
    print(f"   Model:      {model_name}")
    print(f"   Explore:    {explore_name}")

    try:
        agent = client.create_agent(
            name=agent_name,
            description="Conversational BI agent providing governed retail insights for Cymbal Gadgets",
            model=model_name,
            explore=explore_name,
            instructions=instructions,
        )
        agent_id = agent.get("id")

        print("\n" + "=" * 64)
        print("🎉 SUCCESS! Your Looker Conversational Agent is created!")
        print("=" * 64)
        print(f"👉 Agent ID: {agent_id}")
        print("=" * 64)
        print("\n📋 Next Steps:")
        print(f"1. Copy the 32-character Agent ID above: {agent_id}")
        print("2. In the web portal (port 8080), paste it into:")
        print("   'Task 1 Agent ID Memory & Tracker' -> click 'Remember Agent ID'.")
        print("3. Proceed to Task 1, Step 2 (Supplying a Golden Query)!\n")
        return agent_id
    except Exception as e:
        print(f"   ❌ Failed to create agent: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
