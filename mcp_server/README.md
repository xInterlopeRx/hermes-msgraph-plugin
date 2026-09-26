# Microsoft Graph MCP adapter

This package is the adapter boundary for a standalone MCP server. It currently
provides the framework-neutral `policy_check` API in `policy_api.py`; wiring it
to the MCP SDK should expose that function as a tool and the YAML policy files
as MCP resources.

The adapter must enforce the policy result before performing any write,
send, delete, share, or permission-changing Graph operation. A model-readable
policy document alone is not an enforcement boundary.

Install the policy dependency with:

```bash
python -m pip install -r requirements-mcp.txt
```
