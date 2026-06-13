"""AgentLife CLI — setup, update, verify commands."""

import argparse
import sys


def cmd_setup(args):
    """Interactive setup: select persona(s) → generate Hermes config."""
    print("⚙️  AgentLife Setup")
    print("  Coming soon — interactive persona selector")
    print("  For now, see guides/ for platform install docs")
    return 0


def cmd_update(args):
    """Pull latest persona packs from GitHub."""
    print("🔄 agentlife update — coming soon")
    return 0


def cmd_verify(args):
    """Check Hermes is running and AgentLife config is valid."""
    print("🔍 agentlife verify — coming soon")
    return 0


def main():
    parser = argparse.ArgumentParser(prog="agentlife", description="AgentLife Framework CLI")
    sub = parser.add_subparsers(dest="command")

    p_setup = sub.add_parser("setup", help="Interactive persona setup")
    p_setup.set_defaults(func=cmd_setup)

    p_update = sub.add_parser("update", help="Update persona packs")
    p_update.set_defaults(func=cmd_update)

    p_verify = sub.add_parser("verify", help="Verify Hermes + AgentLife config")
    p_verify.set_defaults(func=cmd_verify)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())