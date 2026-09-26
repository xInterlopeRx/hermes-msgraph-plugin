from pathlib import Path

from mcp_server.policy_api import policy_check
from packages.policy_engine import evaluate_action, load_policy_bundle


ROOT = Path(__file__).parents[1]


def test_document_reads_are_allowed_without_approval():
    bundle = load_policy_bundle(ROOT / "policies/documents.yaml")
    decision = evaluate_action(bundle, "document.read")
    assert decision.allowed is True
    assert decision.requires_approval is False


def test_document_deletion_is_denied_even_with_approval():
    decision = policy_check("documents", "document.delete", approved=True)
    assert decision["allowed"] is False


def test_mail_send_requires_explicit_approval_but_sample_denies_it():
    decision = policy_check("communications", "mail.send", approved=True)
    assert decision["allowed"] is False
    assert decision["requires_approval"] is True


def test_unknown_actions_default_to_deny():
    decision = policy_check("communications", "mail.unknown")
    assert decision["allowed"] is False
