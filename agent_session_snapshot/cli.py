"""CLI for agent-session-snapshot."""
import sys
import argparse
from .snapshot import SessionSnapshot


def main():
    parser = argparse.ArgumentParser(description="Agent Session Snapshot")
    parser.add_argument("--demo", action="store_true", help="Run snapshot demo")
    args = parser.parse_args()

    snap = SessionSnapshot()
    chk_id, h = snap.capture_snapshot("agent_1", {"step": 10, "goal": "refactor_api"})
    print(f"Captured checkpoint: {chk_id} with SHA256: {h[:16]}...")
    sys.exit(0)


if __name__ == "__main__":
    main()
