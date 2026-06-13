#!/usr/bin/env python3
"""AgentLife Config Validator — validates all YAML configs in the packs tree."""

import sys
import yaml
from pathlib import Path


REQUIRED_BASE_KEYS = {"persona", "version", "hermes"}
REQUIRED_HERMES_KEYS = {"model"}
OPTIONAL_PACK_KEYS = {"display_name", "description", "base", "cron", "skills", "channels", "install"}


def validate_yaml(path: Path) -> list[str]:
    """Validate a single YAML config file. Returns list of issues."""
    errors = []
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]

    if not isinstance(data, dict):
        return [f"Root must be a mapping, got {type(data).__name__}"]

    # Determine config type
    persona = data.get("persona", "")
    use_case = data.get("use_case", "")

    if persona == "base":
        # Base pack — must have Hermes config
        for key in REQUIRED_BASE_KEYS:
            if key not in data:
                errors.append(f"Missing required key: '{key}'")
        if "model" not in data.get("hermes", {}):
            errors.append("Missing 'hermes.model' configuration")
    elif persona and not use_case:
        # Persona pack — must have 'base' reference
        if "base" not in data:
            errors.append("Persona packs must declare a 'base' inheritance")
    elif use_case:
        # Use case config — must have 'persona' and optionally 'base'
        if "persona" not in data:
            errors.append("Use case configs must declare which 'persona' they belong to")
    else:
        errors.append("Config must declare 'persona', 'use_case', or both")

    # Check for unknown keys (typo prevention)
    known_keys = REQUIRED_BASE_KEYS | OPTIONAL_PACK_KEYS | {"use_case", "config", "use_cases", "dashboard", "cron"}
    unknown = [k for k in data if k not in known_keys]
    for key in unknown:
        errors.append(f"Unknown key: '{key}'")

    return errors


def main():
    pack_dir = Path(__file__).resolve().parents[3] / "packs"
    total_errors = 0
    total_files = 0

    print("🔍 AgentLife Config Validator")
    print("=" * 40)

    for yaml_file in sorted(pack_dir.rglob("*.yaml")):
        total_files += 1
        errors = validate_yaml(yaml_file)
        rel_path = yaml_file.relative_to(pack_dir.parent)
        if errors:
            total_errors += len(errors)
            print(f"\n❌ {rel_path}")
            for err in errors:
                print(f"   • {err}")
        else:
            print(f"  ✓ {rel_path}")

    print(f"\n{'=' * 40}")
    if total_errors:
        print(f"❌ {total_errors} issues across {total_files} files")
        sys.exit(1)
    else:
        print(f"✅ All {total_files} configs valid")
        sys.exit(0)


if __name__ == "__main__":
    main()