# Monorepo layout

This repository contains the native Hermes plugin, shared policy code, and the
future MCP adapter. The native plugin remains installable from the repository
root because Hermes requires `plugin.yaml` and `__init__.py` directly under the
plugin directory.

```text
root plugin files       Native Hermes plugin contract
packages/policy_engine  Pure, side-effect-free policy evaluation
mcp_server              MCP-facing adapter code
policies                Versioned conservative sample policies
tests                   Cross-package behavior tests
```

The MCP adapter must call `policy_check` before any consequential Graph action.
The sample policies allow read-only document and communication operations,
require explicit approval for reversible mutations, and deny destructive or
sharing operations. These are examples, not legal, security, retention, or
compliance advice; deployers must review them before production use.

Secrets are not stored in this repository. The Hermes MCP catalog should prompt
for `MSGRAPH_TENANT_ID`, `MSGRAPH_CLIENT_ID`, `MSGRAPH_CLIENT_SECRET`, and the
optional `MSGRAPH_DEFAULT_USER_ID`, then save them to the active profile's
`.env`.
