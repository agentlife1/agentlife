"""AgentLife config — pack discovery, loading, and merging."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


# Where the framework lives (relative to this file)
FRAMEWORK_DIR = Path(__file__).resolve().parent.parent
PACKS_DIR = FRAMEWORK_DIR / "packs"


class Pack:
    """A persona or base pack loaded from disk."""

    def __init__(self, name: str, path: Path, config: dict[str, Any]):
        self.name = name
        self.path = path
        self.config = config
        self.display_name = config.get("display_name", name)
        self.description = config.get("description", "")
        self.is_base = config.get("persona") == "base"

    @property
    def use_cases(self) -> list[dict[str, str]]:
        """Return available use cases for this persona pack."""
        uc_dir = self.path / "use-cases"
        if not uc_dir.exists():
            return []
        cases: list[dict[str, str]] = []
        for f in sorted(uc_dir.glob("*.yaml")):
            try:
                data = yaml.safe_load(f.read_text())
                if data and data.get("use_case"):
                    cases.append({
                        "id": data["use_case"],
                        "name": data.get("display_name", data["use_case"]),
                        "description": data.get("description", ""),
                    })
            except Exception:
                pass
        return cases


def discover_packs() -> list[Pack]:
    """Discover all packs in the packs/ directory."""
    if yaml is None:
        print("Error: PyYAML is required. Install with: pip install pyyaml")
        sys.exit(1)

    packs: list[Pack] = []
    if not PACKS_DIR.exists():
        return packs

    for entry in sorted(PACKS_DIR.iterdir()):
        config_path = entry / "config.yaml"
        if config_path.exists():
            try:
                data = yaml.safe_load(config_path.read_text())
                if data and data.get("persona") in ("base",):
                    continue  # skip base, handled separately
                if data and data.get("persona"):
                    packs.append(Pack(data["persona"], entry, data))
            except Exception:
                pass
    return packs


def discover_base_pack() -> Pack | None:
    """Discover the base pack."""
    if yaml is None:
        return None
    config_path = PACKS_DIR / "base" / "config.yaml"
    if config_path.exists():
        try:
            data = yaml.safe_load(config_path.read_text())
            if data:
                return Pack(data.get("persona", "base"), config_path.parent, data)
        except Exception:
            pass
    return None


def find_pack(persona: str) -> Pack | None:
    """Find a pack by persona name."""
    for p in discover_packs():
        if p.name == persona:
            return p
    return None


def load_use_case_config(persona_name: str, use_case_id: str) -> dict[str, Any]:
    """Load a specific use case config."""
    uc_path = PACKS_DIR / persona_name / "use-cases" / f"{use_case_id}.yaml"
    if uc_path.exists():
        try:
            return yaml.safe_load(uc_path.read_text()) or {}
        except Exception:
            pass
    return {}


def merge_configs(base: dict, *overlays: dict) -> dict:
    """Deep merge configs. Later overlays win for conflicts.
    Lists are extended, not replaced.
    """
    result = base.copy()
    for overlay in overlays:
        for key, value in overlay.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_configs(result[key], value)
            elif key in result and isinstance(result[key], list) and isinstance(value, list):
                result[key] = result[key] + value
            else:
                result[key] = value
    return result


def generate_hermes_config(personas: list[str], use_cases: dict[str, list[str]]) -> dict[str, Any]:
    """Generate a full Hermes configuration from selected personas and use cases."""
    base_pack = discover_base_pack()
    if not base_pack:
        return {"error": "Base pack not found"}

    merged = base_pack.config.copy()

    for persona_name in personas:
        pack = find_pack(persona_name)
        if pack:
            merged = merge_configs(merged, pack.config)
            # Add use cases
            for uc_id in use_cases.get(persona_name, []):
                uc_config = load_use_case_config(persona_name, uc_id)
                if uc_config:
                    merged = merge_configs(merged, uc_config)

    return merged


def verify_hermes_installation() -> dict[str, str]:
    """Quick Hermes installation check."""
    checks = {}
    import shutil

    checks["hermes_cli"] = "pass" if shutil.which("hermes") else "fail"
    checks["config_file"] = "pass" if os.path.exists(os.path.expanduser("~/.hermes/config.yaml")) else "fail"
    checks["python_version"] = "pass" if sys.version_info >= (3, 10) else "fail"
    return checks