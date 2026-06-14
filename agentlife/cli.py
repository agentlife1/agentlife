"""AgentLife CLI — interactive persona setup, verification, and updates.

The `setup` command is a guided wizard that walks a beginner through
configuring Hermes Agent with AgentLife persona packs, step by step.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from .config import (
    discover_packs,
    discover_base_pack,
    find_pack,
    generate_hermes_config,
    load_use_case_config,
    verify_hermes_installation,
    FRAMEWORK_DIR,
    PACKS_DIR,
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


def subheader(text: str):
    print(f"\n  {c(BOLD + text, YELLOW)}")


def info(text: str):
    print(f"  {c(BULLET, BLUE)} {text}")


def ok(text: str):
    print(f"  {c(CHECK, GREEN)} {text}")


def fail(text: str):
    print(f"  {c(CROSS, RED)} {text}")


def warn(text: str):
    print(f"  {c('!', YELLOW)} {text}")


def divider():
    print(c("\u2500" * 50, DIM))


def prompt(text: str) -> str:
    return input(f"  {c('>>', MAGENTA)} {text}: ").strip()


def prompt_int(text: str, default: int | None = None) -> int | None:
    raw = input(f"  {c('>>', MAGENTA)} {text}: ").strip()
    if not raw and default is not None:
        return default
    if raw.isdigit():
        return int(raw)
    return None


def prompt_multi(text: str, options: list[tuple[str, str]]) -> list[int]:
    """Multi-select via comma-separated numbers or named keywords."""
    print(f"\n  {c(BOLD + text, YELLOW)}")
    for i, (label, desc) in enumerate(options, 1):
        print(f"    {c(f'[{i}]', CYAN)} {label}")
        if desc:
            print(f"         {c(desc, DIM)}")
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


def select_single(text: str, options: list[str]) -> int | None:
    """Single-select via number."""
    print(f"\n  {c(BOLD + text, YELLOW)}")
    for i, opt in enumerate(options, 1):
        print(f"    {c(f'[{i}]', CYAN)} {opt}")
    raw = input(f"  {c('>>', MAGENTA)} Number: ").strip()
    if raw.isdigit():
        idx = int(raw) - 1
        if 0 <= idx < len(options):
            return idx
    return None


# ── Known data ────────────────────────────────────────────────────

USE_CASE_DETAILS: dict[str, dict[str, Any]] = {
    "portfolio-tracking": {
        "name": "Portfolio Tracking",
        "desc": "Net worth snapshots, asset allocation, rebalance alerts",
        "icon": "📊",
        "accounts": True,
        "mcp_servers": [
            {
                "id": "time",
                "name": "Time Server",
                "desc": "Current time queries (free, no API key)",
                "command": "uvx",
                "args": ["mcp-server-time"],
                "runtime": "uvx",
            },
            {
                "id": "filesystem",
                "name": "Filesystem Server",
                "desc": "Read/write portfolio data files (local, no API key)",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "~/agentlife/data"],
                "runtime": "npx",
            },
        ],
    },
    "expense-tracking": {
        "name": "Expense Tracking",
        "desc": "Spending categorization, budget vs. actual, trends",
        "icon": "💳",
        "accounts": False,
        "mcp_servers": [
            {
                "id": "puppeteer",
                "name": "Browser Automation",
                "desc": "Fetch statements from bank websites (needs setup)",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
                "runtime": "npx",
            },
        ],
    },
    "calendar-ops": {
        "name": "Calendar Ops",
        "desc": "Daily agenda, time audit, focus suggestions",
        "icon": "📅",
        "accounts": False,
        "mcp_servers": [],
    },
    "bill-subscriptions": {
        "name": "Bills & Subscriptions",
        "desc": "Renewal tracking, 14-day alerts, annual cost totals",
        "icon": "📋",
        "accounts": False,
        "mcp_servers": [],
    },
}

# Which MCP servers need which runtime check
MCP_RUNTIME_CHECK: dict[str, str] = {
    "uvx": "uvx --version 2>/dev/null",
    "npx": "npx --version 2>/dev/null",
}

MCP_RUNTIME_INSTALL: dict[str, str] = {
    "uvx": "pip install uv",
    "npx": "npm install -g npx",
}


# ── Phase: Welcome & Environment ─────────────────────────────────


def _phase_welcome() -> bool:
    """Display welcome banner and check environment. Returns False if blocking issues found."""
    print()
    print(c(f"  {'╔' + '═'*48 + '╗'}", CYAN))
    print(c(f"  {'║'}{' '*48}{'║'}", CYAN))
    print(c(f"  {'║'}{'  AgentLife Setup Wizard':^48}{'║'}", BOLD + CYAN))
    print(c(f"  {'║'}{'  Turn your Hermes agent into':^48}{'║'}", CYAN + DIM))
    print(c(f"  {'║'}{'  a personal AI operator.':^48}{'║'}", CYAN + DIM))
    print(c(f"  {'║'}{' '*48}{'║'}", CYAN))
    print(c(f"  {'╚' + '═'*48 + '╝'}", CYAN))
    print()

    header("Environment Check")

    all_good = True

    # Python version
    py_ok = sys.version_info >= (3, 10)
    if py_ok:
        ok(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    else:
        fail(f"Python {sys.version_info.major}.{sys.version_info.minor} (need 3.10+)")
        all_good = False

    # Hermes CLI
    hermes_path = shutil.which("hermes")
    if hermes_path:
        try:
            ver = subprocess.run([hermes_path, "--version"], capture_output=True, text=True, timeout=5)
            ver_str = ver.stdout.strip() or ver.stderr.strip() or "installed"
            ok(f"Hermes Agent found ({ver_str})")
        except Exception:
            ok(f"Hermes Agent found at {hermes_path}")
    else:
        fail("Hermes CLI not found in PATH")
        info("Install: curl -fsSL https://raw.githubusercontent.com/")
        info("  NousResearch/hermes-agent/main/scripts/install.sh | bash")
        all_good = False

    # Hermes config
    hermes_config = Path.home() / ".hermes" / "config.yaml"
    if hermes_config.exists():
        ok("Hermes config found")
    else:
        fail("No Hermes config (run 'hermes setup' or 'hermes init')")
        all_good = False

    # API key check
    hermes_env = Path.home() / ".hermes" / ".env"
    api_key_found = False
    if hermes_env.exists():
        content = hermes_env.read_text()
        if "OPENROUTER_API_KEY" in content or "ANTHROPIC_API_KEY" in content:
            api_key_found = True
            ok("API key configured")
    if not api_key_found and hermes_config.exists():
        # Also check config.yaml for inline keys
        try:
            cfg_text = hermes_config.read_text()
            if "api_key" in cfg_text:
                api_key_found = True
                ok("API key configured")
        except Exception:
            pass
    if not api_key_found:
        fail("No API key found")
        info("Set one up: https://openrouter.ai/keys")
        info("Then add to ~/.hermes/.env: OPENROUTER_API_KEY=sk-or-...")
        if not confirm("Continue anyway? (setup will save config but won't work until key is set)", default=False):
            return False

    # AgentLife framework
    if FRAMEWORK_DIR.exists():
        ok(f"AgentLife framework at {FRAMEWORK_DIR}")
    else:
        fail("AgentLife framework not found")
        info("Clone: git clone https://github.com/agentlife1/agentlife.git")
        return False

    # pip install mcp for MCP support
    mcp_ok = False
    try:
        import mcp  # noqa: F401
        mcp_ok = True
    except ImportError:
        pass
    if not mcp_ok:
        warn("MCP SDK not installed (needed for MCP server support)")
        info("Fix: pip install mcp")

    if not all_good:
        warn("Some checks failed. You can continue, but things may not work until fixed.")

    print()
    if not confirm("Ready to configure AgentLife?"):
        return False

    return True


# ── Phase: Persona Selection ─────────────────────────────────────


def _phase_personas() -> tuple[list[Any], dict[str, list[str]]]:
    """Let user pick personas and their use cases."""
    header("Persona Selection")
    info("Persona packs configure your agent for specific areas of your life.")
    info("You can enable multiple and they merge together.")
    print()

    persona_packs = [p for p in discover_packs()]
    if not persona_packs:
        fail("No persona packs found")
        info(f"Create them in: {PACKS_DIR}")
        return [], {}

    # Show available personas
    opts: list[tuple[str, str]] = []
    for p in persona_packs:
        icon = ""
        if p.name == "life-ops":
            icon = "\U0001f4ca "
        opts.append((f"{icon}{p.display_name}", p.description))

    selected = prompt_multi("Which personas fit your life?", opts)
    if not selected:
        info("No personas selected. The base pack will still be installed.")
        return [], {}

    chosen = [persona_packs[i] for i in selected]
    for p in chosen:
        ok(f"{p.display_name}")

    # Use cases per persona
    header("Use Case Selection")
    chosen_use_cases: dict[str, list[str]] = {}

    for pack in chosen:
        use_cases = pack.use_cases
        if not use_cases:
            chosen_use_cases[pack.name] = []
            continue

        print(f"\n  {c(BOLD + pack.display_name, GREEN)} — available use cases:")
        uc_opts: list[tuple[str, str]] = []
        uc_map: list[dict] = []
        for uc in use_cases:
            uc_id = uc["id"]
            details = USE_CASE_DETAILS.get(uc_id, {})
            icon = details.get("icon", "\u25cf")
            label = f"{icon} {details.get('name', uc.get('name', uc_id))}"
            desc = details.get("desc") or uc.get("description", "")
            uc_opts.append((label, desc))
            uc_map.append(uc)

        uc_selected = prompt_multi("Which use cases do you want?", uc_opts)
        chosen_use_cases[pack.name] = [uc_map[i]["id"] for i in uc_selected]
        for uc_id in chosen_use_cases[pack.name]:
            details = USE_CASE_DETAILS.get(uc_id, {})
            ok(f"  {c(details.get('icon', ''), CYAN)} {details.get('name', uc_id)} — {details.get('desc', '')}")

    return chosen, chosen_use_cases


# ── Phase: Account Setup ─────────────────────────────────────────


def _phase_accounts(chosen_use_cases: dict[str, list[str]]) -> list[dict[str, str]]:
    """If portfolio tracking selected, ask about accounts."""
    all_ucs = []
    for uc_list in chosen_use_cases.values():
        all_ucs.extend(uc_list)

    if "portfolio-tracking" not in all_ucs:
        return []

    header("Account Setup")
    info("Portfolio Tracking needs to know about your accounts.")
    info("You can add them now or skip and do it later.")
    print()

    if not confirm("Add your accounts now?", default=True):
        return []

    accounts: list[dict[str, str]] = []
    account_types = [
        "retirement (401k, IRA)",
        "brokerage (taxable investments)",
        "cash (checking, savings)",
        "crypto",
        "real estate",
    ]
    providers = [
        "fidelity", "vanguard", "schwab", "robinhood",
        "chase", "bank of america", "wells fargo",
        "manual (enter balance myself)",
    ]

    while True:
        print()
        divider()
        name = prompt(f"Account name (e.g., \"401k\", \"Robinhood\")")
        if not name:
            break

        type_idx = select_single("Account type?", account_types)
        acct_type = account_types[type_idx].split(" ")[0] if type_idx is not None else "manual"

        prov_idx = select_single("Provider?", providers)
        provider = providers[prov_idx].split(" ")[0] if prov_idx is not None else "manual"

        balance = prompt("Current balance (leave blank for manual entry)")

        accounts.append({
            "name": name,
            "type": acct_type,
            "provider": provider,
            "balance": balance or "",
        })
        ok(f"Added: {name} ({acct_type})")

        if not confirm("Add another account?", default=False):
            break

    if accounts:
        print()
        ok(f"{len(accounts)} account(s) configured")
        for a in accounts:
            bal = f" — ${a['balance']}" if a["balance"] else ""
            info(f"  {a['name']} ({a['type']}, {a['provider']}){bal}")

    return accounts


# ── Phase: MCP Server Setup ──────────────────────────────────────


def _check_runtime(runtime: str) -> bool:
    """Check if a MCP runtime is available."""
    cmd = MCP_RUNTIME_CHECK.get(runtime)
    if not cmd:
        return False
    try:
        subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
        return True
    except Exception:
        return False


def _install_runtime(runtime: str) -> bool:
    """Attempt to install a MCP runtime."""
    install_cmd = MCP_RUNTIME_INSTALL.get(runtime)
    if not install_cmd:
        return False
    info(f"Installing {runtime}...")
    try:
        subprocess.run(install_cmd, shell=True, capture_output=True, timeout=60)
        return _check_runtime(runtime)
    except Exception:
        return False


def _phase_mcp(chosen_use_cases: dict[str, list[str]]) -> list[dict[str, Any]]:
    """Recommend and configure MCP servers based on selected use cases."""
    all_ucs = []
    for uc_list in chosen_use_cases.values():
        all_ucs.extend(uc_list)

    # Gather recommended servers
    recommended: list[dict[str, Any]] = []
    seen = set()
    for uc_id in all_ucs:
        details = USE_CASE_DETAILS.get(uc_id, {})
        for server in details.get("mcp_servers", []):
            srv_id = server["id"]
            if srv_id not in seen:
                recommended.append(server)
                seen.add(srv_id)

    if not recommended:
        return []

    header("MCP Server Setup")
    info("MCP servers give your agent more tools — time lookups, file access, web search.")
    info("Your selected use cases would benefit from:")
    print()

    for srv in recommended:
        runtime_avail = _check_runtime(srv["runtime"])
        runtime_str = c("available", GREEN) if runtime_avail else c("not found", YELLOW)

        print(f"    {c(srv['name'], BOLD)}")
        print(f"      {srv['desc']}")
        print(f"      Runtime: {srv['runtime']} ({runtime_str})")

        if confirm(f"  Install {srv['name']}?", default=runtime_avail):
            if not runtime_avail:
                if confirm(f"  Install {srv['runtime']} runtime first?"):
                    _install_runtime(srv["runtime"])
            srv["enabled"] = True
            ok(f"{srv['name']} configured")
        else:
            srv["enabled"] = False
        print()

    enabled = [s for s in recommended if s.get("enabled")]
    if enabled:
        ok(f"{len(enabled)} MCP server(s) configured")

    return enabled


# ── Phase: Delivery Platform ─────────────────────────────────────


def _phase_delivery() -> dict[str, Any]:
    """Configure where the daily brief and alerts are delivered."""
    header("Delivery & Messaging")
    info("Your agent can send you daily briefs, alerts, and reply to you")
    info("on messaging platforms.")
    print()

    delivery: dict[str, Any] = {
        "platforms": [],
        "gateway_configured": False,
    }

    # Check if Hermes gateway is already configured
    hermes_config = Path.home() / ".hermes" / "config.yaml"
    gateway_configured = False
    if hermes_config.exists():
        try:
            import yaml
            cfg = yaml.safe_load(hermes_config.read_text())
            gateway_section = cfg.get("gateway", {})
            platforms = gateway_section.get("platforms", {})
            if platforms:
                gateway_configured = True
                delivery["gateway_configured"] = True
                configured = [k for k, v in platforms.items() if isinstance(v, dict) and v.get("enabled", True)]
                if configured:
                    ok(f"Gateway already configured: {', '.join(configured)}")
                    if confirm("Use existing gateway setup?"):
                        delivery["platforms"] = configured
                        return delivery
        except Exception:
            pass

    if not gateway_configured:
        info("Hermes Gateway connects your agent to messaging platforms.")
        print()

    # Suggest platforms
    opts = [
        ("Telegram", "Best for quick updates and chat — free, popular"),
        ("Local file only", "Save to ~/.hermes/agentlife/daily-brief/ — no setup needed"),
    ]
    selected = prompt_multi("Where should your agent deliver updates?", opts)
    delivery["selected_platforms"] = selected

    if 0 in selected:
        # Telegram selected
        header("Telegram Setup")
        info("To connect Telegram:")
        info("1. Open Telegram and message @BotFather")
        info("2. Send /newbot and follow the prompts")
        info("3. Copy the bot token (looks like: 123456:ABC-DEF...")
        print()

        if confirm("Do you have a bot token ready?"):
            token = prompt("Paste your bot token")
            if token:
                delivery["telegram_token"] = token
                info("Bot token saved")

            user_id = prompt("Your Telegram user ID (numeric, or leave blank to auto-detect)")
            if user_id:
                delivery["telegram_user_id"] = user_id
                info("User ID saved")

            ok("Telegram configured")
            delivery["platforms"].append("telegram")

            info("After setup completes, message your bot to test it.")
        else:
            warn("Telegram setup skipped — configure later with: hermes gateway setup")
            delivery["platforms"].append("telegram_deferred")

    if 1 in selected or (not selected and not gateway_configured):
        delivery["platforms"].append("local")
        ok("Local file output configured")

    return delivery


# ── Phase: Schedule ──────────────────────────────────────────────


def _phase_schedule() -> dict[str, Any]:
    """Configure the daily brief schedule."""
    header("Daily Brief Schedule")
    info("Your agent can send you a morning brief with portfolio,")
    info("expenses, calendar, and subscription updates.")
    print()

    schedule: dict[str, Any] = {
        "enabled": False,
        "cron": "",
        "time": "",
    }

    if confirm("Enable the daily morning brief?", default=True):
        print()
        info("Recommended: Weekdays at 6:30 AM")
        info("Custom: any cron schedule (e.g., '0 9 * * 1-5' = weekdays at 9 AM)")
        print()

        cron_input = prompt("Cron schedule (Enter for default: 30 6 * * 1-5)")
        if not cron_input:
            cron_input = "30 6 * * 1-5"
            time_str = "6:30 AM weekdays"
        else:
            # Try to parse a readable version
            parts = cron_input.split()
            time_str = cron_input

        schedule["enabled"] = True
        schedule["cron"] = cron_input
        schedule["time"] = time_str
        ok(f"Daily brief scheduled: {time_str}")

    return schedule


# ── Phase: Summary & Generate ────────────────────────────────────


def _show_summary(
    personas: list[Any],
    use_cases: dict[str, list[str]],
    accounts: list[dict[str, str]],
    mcp_servers: list[dict[str, Any]],
    delivery: dict[str, Any],
    schedule: dict[str, Any],
):
    """Display a final summary before generating config."""
    print()
    header("Configuration Summary")
    print()

    # Persona table
    print(f"  {c('Personas:', BOLD)}")
    if personas:
        for p in personas:
            ucs = use_cases.get(p.name, [])
            uc_names = []
            for uc_id in ucs:
                details = USE_CASE_DETAILS.get(uc_id, {})
                uc_names.append(details.get("name", uc_id))
            uc_str = f" → {', '.join(uc_names)}" if uc_names else ""
            print(f"    {c(CHECK, GREEN)} {p.display_name}{uc_str}")
    else:
        print(f"    {c(BULLET, DIM)} Base pack only")

    # Accounts
    if accounts:
        print(f"  {c('Accounts:', BOLD)}")
        for a in accounts:
            bal = f" (${a['balance']})" if a["balance"] else ""
            print(f"    {c(BULLET, CYAN)} {a['name']} — {a['type']} on {a['provider']}{bal}")

    # MCP servers
    if mcp_servers:
        enabled = [s for s in mcp_servers if s.get("enabled")]
        if enabled:
            print(f"  {c('MCP Servers:', BOLD)}")
            for s in enabled:
                print(f"    {c(BULLET, GREEN)} {s['name']}")

    # Delivery
    print(f"  {c('Delivery:', BOLD)}")
    for plat in delivery.get("platforms", []):
        if plat == "telegram":
            print(f"    {c(BULLET, CYAN)} Telegram")
        elif plat == "local":
            print(f"    {c(BULLET, CYAN)} Local files")
        elif plat == "telegram_deferred":
            print(f"    {c(BULLET, YELLOW)} Telegram (needs setup)")

    # Schedule
    if schedule.get("enabled"):
        print(f"  {c('Schedule:', BOLD)}")
        print(f"    {c(BULLET, CYAN)} Daily brief at {schedule['time']}")

    print()
    return confirm("Generate configuration?", default=True)


def _generate_and_save(
    personas: list[Any],
    use_cases: dict[str, list[str]],
    accounts: list[dict[str, str]],
    mcp_servers: list[dict[str, Any]],
    delivery: dict[str, Any],
    schedule: dict[str, Any],
) -> bool:
    """Generate merged config and save all files."""
    header("Generating Configuration")

    # 1. Generate Hermes config overlay
    merged = generate_hermes_config(
        [p.name for p in personas],
        use_cases,
    )

    # 2. Add MCP servers
    enabled_mcp = [s for s in mcp_servers if s.get("enabled")]
    if enabled_mcp:
        mcp_config = {}
        for srv in enabled_mcp:
            entry: dict[str, Any] = {"command": srv["command"]}
            if srv.get("args"):
                entry["args"] = srv["args"]
            if srv.get("env"):
                entry["env"] = srv["env"]
            mcp_config[srv["id"]] = entry
        merged["mcp_servers"] = mcp_config

    # 3. Add accounts
    if accounts:
        merged.setdefault("life-ops", {})
        merged["life-ops"]["portfolio"] = {"accounts": accounts}

    # 4. Add delivery config
    if delivery.get("telegram_token"):
        merged.setdefault("gateway", {}).setdefault("platforms", {})
        merged["gateway"]["platforms"]["telegram"] = {
            "bot_token": delivery["telegram_token"],
        }
        if delivery.get("telegram_user_id"):
            merged["gateway"]["platforms"]["telegram"]["allowed_users"] = [delivery["telegram_user_id"]]

    # 5. Add cron schedule
    if schedule.get("enabled"):
        brief_cron = {
            "name": "daily-brief",
            "schedule": schedule["cron"],
            "command": "hermes chat -q 'Run the Life Ops daily brief'",
            "description": "Daily morning brief — portfolio, spending, calendar, renewals",
        }
        merged.setdefault("cron", [])
        # Replace existing daily-brief if present
        merged["cron"] = [c for c in merged.get("cron", []) if c.get("name") != "daily-brief"]
        merged["cron"].append(brief_cron)

    # 6. Save config
    hermes_dir = Path.home() / ".hermes"
    agentlife_dir = hermes_dir / "agentlife"
    agentlife_dir.mkdir(parents=True, exist_ok=True)

    config_path = agentlife_dir / "config.json"
    config_path.write_text(json.dumps(merged, indent=2))
    ok(f"Config saved to {config_path}")

    # 7. Save MCP config to Hermes config if possible
    if enabled_mcp and hermes_config_exists():
        try:
            _inject_mcp_into_hermes_config(enabled_mcp)
        except Exception as e:
            warn(f"Could not auto-add MCP servers to Hermes config: {e}")
            info("Manually add the MCP servers block from the MCP Integration Guide.")

    return True


def hermes_config_exists() -> bool:
    return (Path.home() / ".hermes" / "config.yaml").exists()


def _inject_mcp_into_hermes_config(servers: list[dict[str, Any]]):
    """Add MCP server configs to ~/.hermes/config.yaml."""
    import yaml

    config_path = Path.home() / ".hermes" / "config.yaml"
    if not config_path.exists():
        return

    raw = config_path.read_text()
    cfg = yaml.safe_load(raw) or {}

    # Add or update mcp_servers section
    mcp_servers = cfg.setdefault("mcp_servers", {})
    for srv in servers:
        srv_id = srv["id"]
        if srv_id not in mcp_servers:
            entry: dict[str, Any] = {"command": srv["command"]}
            if srv.get("args"):
                entry["args"] = srv["args"]
            mcp_servers[srv_id] = entry

    # Write back preserving comments as much as possible
    config_path.write_text(yaml.dump(cfg, default_flow_style=False, sort_keys=False))
    ok(f"MCP servers added to {config_path}")


# ── Phase: Verify ────────────────────────────────────────────────


def _phase_verify() -> bool:
    """Run verification checks and guide the user through fixing issues."""
    header("Verification")

    checks = verify_hermes_installation()
    all_pass = True
    for name, status in checks.items():
        display = name.replace("_", " ").title()
        if status == "pass":
            ok(display)
        else:
            fail(display)
            all_pass = False

    # Config present
    config_path = Path.home() / ".hermes" / "agentlife" / "config.json"
    if config_path.exists():
        ok("AgentLife config present")
    else:
        fail("No AgentLife config — something went wrong saving")
        all_pass = False

    # Cron check
    if config_path.exists():
        try:
            cfg = json.loads(config_path.read_text())
            cron_count = len(cfg.get("cron", []))
            if cron_count > 0:
                ok(f"{cron_count} cron job(s) configured")
                for cj in cfg["cron"]:
                    info(f"  {cj.get('name', 'job')} → {cj.get('schedule', '')}")
        except Exception:
            pass

    # MCP SDK check
    try:
        import mcp  # noqa: F401
        ok("MCP SDK installed")
    except ImportError:
        warn("MCP SDK not installed")
        info("Install: pip install mcp")

    print()
    return all_pass


# ── Phase: First Run ─────────────────────────────────────────────


def _phase_first_run(personas: list[Any], use_cases: dict[str, list[str]]):
    """Offer to run a first test."""
    header("First Run")
    info("Let's test that everything works.")

    all_ucs = []
    for uc_list in use_cases.values():
        all_ucs.extend(uc_list)

    if "portfolio-tracking" in all_ucs and confirm("Run a portfolio check?", default=True):
        print()
        info("Asking Hermes to check your portfolio...")
        try:
            result = subprocess.run(
                ["hermes", "chat", "-q", "Check my portfolio and tell me the summary"],
                capture_output=True, text=True, timeout=60,
            )
            output = result.stdout.strip() or result.stderr.strip()
            if output:
                ok("Portfolio check complete!")
                # Show a preview
                lines = output.split("\n")
                preview = "\n".join(lines[:8])
                if len(lines) > 8:
                    preview += "\n    ..."
                print(f"\n{c('  ' + preview, DIM)}")
            else:
                warn("No output from Hermes. It may need configuration.")
        except subprocess.TimeoutExpired:
            warn("Portfolio check timed out — Hermes may be starting up")
        except FileNotFoundError:
            fail("Hermes CLI not available for test")
        except Exception as e:
            warn(f"Test run error: {e}")


# ── Setup Command ────────────────────────────────────────────────


def cmd_setup(args: argparse.Namespace) -> int:
    """Interactive wizard — full persona, use case, MCP, and delivery setup."""

    # Phase 0: Welcome + Environment
    if not _phase_welcome():
        return 1

    # Phase 1: Personas
    personas, use_cases = _phase_personas()
    if not personas:
        warn("No personas selected. Only base config will be generated.")

    # Phase 2: Use Cases (done inside _phase_personas)

    # Phase 3: Accounts
    accounts = _phase_accounts(use_cases)

    # Phase 4: MCP Servers
    mcp_servers = _phase_mcp(use_cases)

    # Phase 5: Delivery
    delivery = _phase_delivery()

    # Phase 6: Schedule
    schedule = _phase_schedule()

    # Phase 7: Summary + Generate
    if not _show_summary(personas, use_cases, accounts, mcp_servers, delivery, schedule):
        info("Setup cancelled. No configuration was saved.")
        return 1

    success = _generate_and_save(personas, use_cases, accounts, mcp_servers, delivery, schedule)
    if not success:
        fail("Configuration generation failed")
        return 1

    # Phase 8: Verify
    _phase_verify()

    # Phase 9: First run
    _phase_first_run(personas, use_cases)

    # Done
    print()
    print(c(f"  {'╔' + '═'*48 + '╗'}", GREEN))
    print(c(f"  {'║'}{'  Setup Complete!':^48}{'║'}", BOLD + GREEN))
    print(c(f"  {'║'}{'  Your AI agent is ready.':^48}{'║'}", GREEN))
    print(c(f"  {'╚' + '═'*48 + '╝'}", GREEN))
    print()
    info("What to do next:")
    info("  1. Wait for your first daily brief (or check Telegram)")
    info(f"  2. Run {c('agentlife verify', CYAN)} anytime to check health")
    info(f"  3. Run {c('agentlife update', CYAN)} to get the latest persona packs")
    info(f"  4. Read the guides: {c(str(FRAMEWORK_DIR / 'guides'), DIM)}")
    print()

    return 0


# ── Update Command ───────────────────────────────────────────────


def cmd_update(args: argparse.Namespace) -> int:
    """Pull latest persona packs from GitHub."""
    header("AgentLife Update")

    git_dir = FRAMEWORK_DIR / ".git"
    if not git_dir.exists():
        fail("Framework not in a git repo")
        info("Clone the repo to get updates:")
        info("  git clone https://github.com/agentlife1/agentlife.git ~/agentlife/framework")
        return 1

    # Check for local changes
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

    # Check remote
    remote_check = subprocess.run(
        ["git", "ls-remote", "--exit-code", "origin"],
        cwd=FRAMEWORK_DIR,
        capture_output=True,
        text=True,
    )
    if remote_check.returncode != 0:
        fail("Cannot reach GitHub — check your network")
        return 1

    # Pull
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

            # Re-validate configs after update
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
                    info("Run 'python3 packs/base/scripts/config-validate.py' for details")
        return 0
    else:
        fail(f"Update failed: {result.stderr.strip()}")
        info("Try: cd ~/agentlife/framework && git pull")
        return 1


# ── Verify Command ───────────────────────────────────────────────


def cmd_verify(args: argparse.Namespace) -> int:
    """Check Hermes is running and AgentLife config is valid."""
    return 0 if _phase_verify() else 1


# ── Main ─────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="agentlife",
        description="AgentLife Framework — configure Hermes Agent for your life",
    )
    parser.add_argument(
        "--version", action="version", version="agentlife 0.2.0"
    )

    sub = parser.add_subparsers(dest="command")

    p_setup = sub.add_parser("setup", help="Interactive persona setup wizard")
    p_setup.set_defaults(func=cmd_setup)

    p_update = sub.add_parser("update", help="Update persona packs from GitHub")
    p_update.set_defaults(func=cmd_update)

    p_verify = sub.add_parser("verify", help="Verify Hermes + AgentLife configuration")
    p_verify.set_defaults(func=cmd_verify)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    try:
        return args.func(args)
    except KeyboardInterrupt:
        print()
        info("Setup cancelled.")
        return 1


if __name__ == "__main__":
    sys.exit(main())