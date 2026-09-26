"""Small policy engine shared by the native plugin and future MCP server.

The sample policy format is intentionally conservative: unknown domains/actions
are denied, and every mutating action requires an explicit approval value.
This module does not perform Graph calls or mutate state.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class PolicyBundle:
    version: str
    domain: str
    default_effect: str
    default_requires_approval: bool
    rules: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class Decision:
    allowed: bool
    requires_approval: bool
    reason: str
    policy_version: str
    rule_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "requires_approval": self.requires_approval,
            "reason": self.reason,
            "policy_version": self.policy_version,
            "rule_id": self.rule_id,
        }


def load_policy_bundle(path: str | Path) -> PolicyBundle:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    defaults = raw.get("defaults") or {}
    return PolicyBundle(
        version=str(raw.get("version", "unknown")),
        domain=str(raw.get("domain", "unknown")),
        default_effect=str(defaults.get("effect", "deny")),
        default_requires_approval=bool(defaults.get("requires_human_approval", True)),
        rules=tuple(raw.get("rules") or ()),
    )


def evaluate_action(bundle: PolicyBundle, action: str, *, approved: bool = False) -> Decision:
    rule = next((r for r in bundle.rules if action in (r.get("actions") or [])), None)
    if rule is None:
        return Decision(
            allowed=False,
            requires_approval=bundle.default_requires_approval,
            reason="No rule matches this action; default deny applies.",
            policy_version=bundle.version,
        )

    effect = str(rule.get("effect", bundle.default_effect)).lower()
    requires_approval = bool(rule.get("requires_human_approval", bundle.default_requires_approval))
    if effect != "allow":
        return Decision(False, requires_approval, str(rule.get("reason", "Policy denies this action.")), bundle.version, rule.get("id"))
    if requires_approval and not approved:
        return Decision(False, True, "Explicit human approval is required before this action.", bundle.version, rule.get("id"))
    return Decision(True, requires_approval, str(rule.get("reason", "Policy allows this action.")), bundle.version, rule.get("id"))
