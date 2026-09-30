"""
SME Academy Lab Teardown & Resource Cleanup Script
--------------------------------------------------
Cleans up resources created during the Looker Conversational Analytics lab:
1. Reverts / removes agent patch (resets context instructions and unlinks golden queries)
2. Deletes golden query record (DELETE /api/4.0/golden_queries/{id})
3. Deletes conversation session (DELETE /api/4.0/conversations/{id})
4. Deletes agent (DELETE /api/4.0/agents/{id})

Usage:
  python3 cleanup.py [AGENT_ID] [CONVERSATION_ID] [GOLDEN_QUERY_ID]
"""

import sys
import config
from looker_client import LookerClient

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Usage: python3 cleanup.py [AGENT_ID] [CONVERSATION_ID] [GOLDEN_QUERY_ID] [--clear-creds]")
        print("Teardown Looker lab artifacts: reverts patch, deletes golden query, deletes conversation, deletes agent.")
        return

    print("=" * 65)
    print("🧹 SME Academy: Looker Lab Teardown & Resource Cleanup")
    print("=" * 65)

    client_id = config.LOOKER_CLIENT_ID
    client_secret = config.LOOKER_CLIENT_SECRET
    if not client_id or client_id == "specify your own user id / secret":
        client_id = input("Enter Looker Client ID: ").strip()
    if not client_secret or client_secret == "specify your own user id / secret":
        client_secret = input("Enter Looker Client Secret: ").strip()

    client = LookerClient(
        base_url=config.LOOKER_BASE_URL,
        client_id=client_id,
        client_secret=client_secret
    )

    agent_id = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    conv_id = sys.argv[2].strip() if len(sys.argv) > 2 else ""
    gq_id = sys.argv[3].strip() if len(sys.argv) > 3 else ""

    if not agent_id:
        agent_id = input("Enter Agent ID to remove (or press Enter to skip): ").strip()
    if not conv_id:
        conv_id = input("Enter Conversation ID to remove (or press Enter to skip): ").strip()
    if not gq_id:
        gq_id = input("Enter Golden Query ID to remove (or press Enter to skip): ").strip()

    if not agent_id and not conv_id and not gq_id:
        print("⚠️ No resource IDs provided. Exiting cleanup.")
        return

    print("\nStarting teardown sequence...")
    results = client.cleanup_lab_resources(
        agent_id=agent_id or None,
        conversation_id=conv_id or None,
        golden_query_id=gq_id or None
    )

    print("\n" + "=" * 65)
    print("📋 TEARDOWN SUMMARY:")
    print("=" * 65)
    print(f"• Agent Patch Reverted     : {'✅ Done' if results['patch_reverted'] else '⏭️ Skipped / Not applied'}")
    print(f"• Golden Query Deleted     : {'✅ Done' if results['golden_query_deleted'] else '⏭️ Skipped / Not found'}")
    print(f"• Conversation Deleted     : {'✅ Done' if results['conversation_deleted'] else '⏭️ Skipped / Not found'}")
    print(f"• Agent Deleted            : {'✅ Done' if results['agent_deleted'] else '⏭️ Skipped / Not found'}")

    if results["errors"]:
        print("\n⚠️ Notices during cleanup:")
        for err in results["errors"]:
            print(f"  - {err}")
    else:
        print("\n🎉 ALL TARGETED LAB RESOURCES CLEANED UP SUCCESSFULLY!")

if __name__ == "__main__":
    main()
