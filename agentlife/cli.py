"""AgentLife CLI — interactive persona setup, update, and verify."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from .config import (
    discover_packs,
    generate_hermes_config,
    verify_hermes_installation,
    FRAMEWORK_DIR,
)


# ── Terminal helpers ──────────────────────────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CHECK = "\u2713"
CROSS = "\u2717"
BULLET = "\u25cf"


def c(text: str, color: str) -> str:
    return f"{color}{text}{RESET}"


def header(text: str):
    print(f"\n{c(BOLD + text, CYAN)}")
    print(c("\u2500" * 50, DIM))


def info(text: str):
    print(f"  {c(BULLET, BLUE)} {text}")


def ok(text: str):
    print(f"  {c(CHECK, GREEN)} {text}")


def fail(text: str):
    print(f"  {c(CROSS, RED)} {text}")


def warn(text: str):
    print(f"  {c('!', YELLOW)} {text}")


def prompt(text: str) -> str:
    return input(f"  {c('>>', MAGENTA)} {text}: ").strip()


def prompt_multi(text: str, options: list[str]) -> list[int]:
    """Multi-select via comma-separated numbers."""
    print(f"\n  {c(BOLD + text, YELLOW)}")
    for i, opt in enumerate(options, 1):
        print(f"    {c(f'[{i}]', CYAN)} {opt}")
    raw = input(f"  {c('>>', MAGENTA)} Numbers (comma-separated, or 'all'): ").strip()
    if raw.lower() == "all":
        return list(range(len(options)))
    selected: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            idx = int(part) - 1
            if 0 <= idx < len(options):
                selected.append(idx)
    return sorted(set(selected))


def confirm(text: str, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    raw = input(f"  {c('>>', MAGENTA)} {text} [{hint}]: ").strip().lower()
    if not raw:
        return default
    return raw.startswith("y")


# ── Setup Flow ────────────────────────────────────────────────────


def cmd_setup(args: argparse.Namespace) -> int:
    """Interactive persona and use case setup."""
    print(f"\n{c(BOLD + 'AgentLife Setup', CYAN)}")
    print(c("  Your Life, Orchestrated by AI", BLUE))
    print(c("\u2500" * 50, DIM))

    # Step 1: Platform detection
    header("Platform")
    os_name = sys.platform
    arch = os.uname().machine if hasattr(os, "uname") else "unknown"
    is_rpi = os.path.isfile("/etc/rpi-issue") if sys.platform == "linux" else False
    if is_rpi:
        platform = "raspberry-pi"
    elif os_name == "linux":
        platform = "linux"
    elif os_name == "darwin":
        platform = "macos"
    else:
        platform = os_name
    info(f"Detected: {os_name} ({arch}) → {platform}")

    # Step 2: Hermes check
    header("Hermes Agent")
    hermes_path = shutil.which("hermes")
    if hermes_path:
        ok(f"Found at {hermes_path}")
    else:
        fail("Hermes CLI not found in PATH")
        info("Install Hermes first, then run 'agentlife setup' again")
        info("See: guides/{platform}.md")
        if not confirm("Continue anyway? (config will be saved for later)"):
            return 1

    # Step 3: Available persona packs
    header("Personas")
    persona_packs = [p for p in discover_packs()]
    if not persona_packs:
        info("No persona packs found. Create them in:")
        info(str(FRAMEWORK_DIR / "packs"))
        return 1

    persona_names = [f"{p.display_name:20} — {p.description}" for p in persona_packs]
    selected = prompt_multi("Which persona(s) fit your life?", persona_names)
    if not selected:
        fail("No personas selected. Nothing to configure.")
        return 1

    chosen_personas = [persona_packs[i] for i in selected]
    for p in chosen_personas:
        ok(f"{p.display_name}")

    # Step 4: Use cases per persona
    header("Use Cases")
    chosen_use_cases: dict[str, list[str]] = {}
    for pack in chosen_personas:
        use_cases = pack.use_cases
        if not use_cases:
            chosen_use_cases[pack.name] = []
            ok(f"{pack.display_name}: no use cases to configure")
            continue

        uc_names = [f"{uc['name']:30} — {uc.get('description', '')}" for uc in use_cases]
        info(f"\n{pack.display_name} — available use cases:")
        uc_selected = prompt_multi("Select use cases", uc_names)
        chosen_use_cases[pack.name] = [use_cases[i]["id"] for i in uc_selected]
        for uc_id in chosen_use_cases[pack.name]:
            ok(f"  {pack.display_name} → {uc_id}")

    # Step 5: Generate config
    header("Generating Config")
    
    # Check for conflicts when multiple personas selected
    if len(chosen_personas) > 1:
        info("Multiple personas selected — checking for conflicts...")
        # Load all configs and check for overlapping keys
        conflicts = []
        for i, p1 in enumerate(chosen_personas):
            for p2 in chosen_personas[i+1:]:
                common_keys = set(p1.config.get("hermes", {}).keys()) & set(p2.config.get("hermes", {}).keys())
                if common_keys:
                    for key in common_keys:
                        if p1.config["hermes"].get(key) != p2.config["hermes"].get(key):
                            conflicts.append((p1.name, p2.name, key))
        if conflicts:
            warn(f"Found {len(conflicts)} config conflict(s):")
            for p1, p2, key in conflicts:
                info(f"  {p1}/{p2} differ on '{key}' — {p2} wins (last selected)")
        else:
            ok("No conflicts detected")
    
    merged = generate_hermes_config(
        [p.name for p in chosen_personas],
        chosen_use_cases,
    )

    # Write config
    hermes_dir = Path.home() / ".hermes"
    agentlife_dir = hermes_dir / "agentlife"
    agentlife_dir.mkdir(parents=True, exist_ok=True)

    config_path = agentlife_dir / "config.json"
    config_path.write_text(json.dumps(merged, indent=2))
    ok(f"Config saved to {config_path}")

    # Step 6: Summary
    header("Summary")
    info(f"Personas: {', '.join(p.display_name for p in chosen_personas)}")
    total_uc = sum(len(v) for v in chosen_use_cases.values())
    info(f"Use cases: {total_uc}")
    info(f"Config: {config_path}")

    # Check if cron jobs exist
    cron_count = len(merged.get("cron", []))
    if cron_count:
        info(f"Cron jobs: {cron_count}")

    if not hermes_path:
        fail("Hermes not installed — saved config for later")
        return 1

    print(f"\n{c(BOLD + 'Ready to go! Run: agentlife verify', GREEN)}")
    return 0


# ── Update ─────────────────────────────────────────────────────────


def cmd_update(args: argparse.Namespace) -> int:
    """Pull latest persona packs from GitHub."""
    import subprocess

    header("AgentLife Update")

    git_dir = FRAMEWORK_DIR / ".git"
    if not git_dir.exists():
        fail("Framework not in a git repo")
        info("Clone the repo to get updates:")
        info("  git clone https://github.com/agentlife/agentlife.git ~/agentlife/framework")
        return 1

    # Check for local changes that might be overwritten
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=FRAMEWORK_DIR,
        capture_output=True,
        text=True,
    )
    if status.stdout.strip():
        warn("You have uncommitted changes:")
        for line in status.stdout.strip().split("\n"):
            info(f"  {line.strip()}")
        stash = confirm("Stash changes and continue?", default=False)
        if stash:
            subprocess.run(["git", "stash"], cwd=FRAMEWORK_DIR)
            ok("Changes stashed")
        else:
            info("Update cancelled. Commit or stash your changes first.")
            return 1

    # Check remote connectivity
    remote_check = subprocess.run(
        ["git", "ls-remote", "--exit-code", "origin"],
        cwd=FRAMEWORK_DIR,
        capture_output=True,
        text=True,
    )
    if remote_check.returncode != 0:
        fail("Cannot reach GitHub — check your network connection")
        return 1

    # Fetch and pull
    result = subprocess.run(
        ["git", "pull", "--ff-only"],
        cwd=FRAMEWORK_DIR,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        if "Already up to date" in result.stdout:
            ok("Framework is up to date")
        else:
            ok("Framework updated")
            if result.stdout.strip():
                info(result.stdout.strip())
            # Re-run config validation after update
            validator = FRAMEWORK_DIR / "packs" / "base" / "scripts" / "config-validate.py"
            if validator.exists():
                v_result = subprocess.run(
                    [sys.executable, str(validator)],
                    cwd=FRAMEWORK_DIR,
                    capture_output=True,
                    text=True,
                )
                if v_result.returncode == 0:
                    ok("Configs valid after update")
                else:
                    fail("Config validation failed after update!")
                    info("Run 'python3 packs/base/scripts/config-validate.py' to see details")
        return 0
    else:
        fail(f"Update failed: {result.stderr.strip()}")
        info("Try: cd ~/agentlife/framework && git pull")
        return 1


# ── Verify ────────────────────────────────────────────────────────


def cmd_verify(args: argparse.Namespace) -> int:
    """Check Hermes is running and AgentLife config is valid."""
    header("AgentLife Verify")

    checks = verify_hermes_installation()
    all_pass = True
    for name, status in checks.items():
        if status == "pass":
            ok(name.replace("_", " "))
        else:
            fail(name.replace("_", " "))
            all_pass = False

    # Check saved config
    config_path = Path.home() / ".hermes" / "agentlife" / "config.json"
    if config_path.exists():
        ok("AgentLife config present")
    else:
        fail("No AgentLife config — run 'agentlife setup' first")
        all_pass = False

    # Validate YAML configs
    validator = FRAMEWORK_DIR / "packs" / "base" / "scripts" / "config-validate.py"
    if validator.exists():
        import subprocess
        result = subprocess.run(
            [sys.executable, str(validator)],
            cwd=FRAMEWORK_DIR,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            ok("All pack configs valid")
        else:
            fail("Config validation failed:")
            for line in result.stdout.strip().split("\n"):
                if "❌" in line or "•" in line:
                    print(f"    {line.strip()}")
            # Error recovery suggestions
            info("Fix errors and re-run: python3 packs/base/scripts/config-validate.py")

    # Check cron jobs are scheduled
    if config_path.exists():
        try:
            cfg = json.loads(config_path.read_text())
            cron_count = len(cfg.get("cron", []))
            if cron_count > 0:
                ok(f"{cron_count} cron jobs configured")
            else:
                warn("No cron jobs configured — select use cases to enable them")
        except (json.JSONDecodeError, Exception):
            warn("Could not read AgentLife config for cron check")

    # Print recovery guide if failures
    if not all_pass:
        print(f"\n{c(BOLD + 'Recovery Guide', YELLOW)}")
        fail("Some checks failed. Here's how to fix:")
        if not shutil.which("hermes"):
            info("Install Hermes: pipx install hermes-agent")
        if not Path.home().joinpath(".hermes/config.yaml").exists():
            info("Init config: hermes init")
        if not config_path.exists():
            info("Setup: agentlife setup")
        print()

    return 0 if all_pass else 1


# ── Main ──────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="agentlife",
        description="AgentLife Framework — configure Hermes Agent for your life",
    )
    parser.add_argument(
        "--version", action="version", version="agentlife 0.1.0"
    )

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