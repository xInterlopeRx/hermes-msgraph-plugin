"""Framework-neutral API used by the MCP server's policy_check tool."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.policy_engine import evaluate_action, load_policy_bundle


POLICY_ROOT = Path(__file__).resolve().parents[1] / "policies"


def policy_check(domain: str, action: str, *, approved: bool = False) -> dict[str, Any]:
    """Return a deny-by-default decision without performing the requested action."""
    path = POLICY_ROOT / f"{domain}.yaml"
    if not path.is_file():
        return {
            "allowed": False,
            "requires_approval": True,
            "reason": f"Unknown policy domain: {domain}",
            "policy_version": "unknown",
            "rule_id": None,
        }
    return evaluate_action(load_policy_bundle(path), action, approved=approved).as_dict()
