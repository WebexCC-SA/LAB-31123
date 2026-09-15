# Lab 7 - Build a Custom MCP Server

In this section, you will build a custom MCP server that exposes Webex API operations your organization needs — beyond what the official Webex MCP servers provide out of the box.

## Learning Objectives

Upon completion of this section, you will be able to:

- Scaffold an MCP server with tool catalog and execution handlers
- Map a Webex REST API operation to an MCP tool with JSON Schema
- Handle credentials inside the server (never expose tokens to the LLM)
- Register the custom server in your IDE MCP configuration

## Step 7.1: Project structure

```text
custom-mcp-server/
  server.py
  tools/
    status.py
    audit.py
  schemas/
    list_audit_events.json
  requirements.txt
```

## Step 7.2: Define your first tool

Example tool definition for listing unresolved Webex status incidents:

```python
TOOLS = [
    {
        "name": "webex_status_unresolved",
        "description": "List unresolved Webex platform incidents.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    }
]
```

## Step 7.3: Implement tool execution

```python
import os
import requests

WEBEX_TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")

def call_tool(name: str, arguments: dict) -> dict:
    if name == "webex_status_unresolved":
        response = requests.get(
            "https://status.webex.com/api/v2/incidents/unresolved.json",
            timeout=30,
        )
        response.raise_for_status()
        return {"content": [{"type": "text", "text": response.text}]}

    raise ValueError(f"Unknown tool: {name}")
```

!!! Note
    Production MCP servers should validate arguments against JSON Schema, apply rate limits, redact sensitive fields, and use elicitation for destructive operations.

## Step 7.4: Add a Webex API tool

Add a tool that calls an org-specific endpoint (placeholder — update for lab tenant):

```python
{
    "name": "list_admin_audit_events",
    "description": "List recent admin audit events for troubleshooting.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "max": {"type": "integer", "default": 10}
        },
    },
}
```

```python
def list_admin_audit_events(max_results: int = 10) -> dict:
    response = requests.get(
        "https://webexapis.com/v1/adminAudit/events",
        headers={"Authorization": f"Bearer {WEBEX_TOKEN}"},
        params={"max": max_results},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
```

## Step 7.5: Register in your IDE

```json
{
  "mcpServers": {
    "webex-custom-lab": {
      "command": "python",
      "args": ["/path/to/custom-mcp-server/server.py"],
      "env": {
        "WEBEX_ACCESS_TOKEN": "YOUR_LAB_TOKEN"
      }
    }
  }
}
```

## Step 7.6: Test discovery and execution

In your IDE:

```text
Use the webex-custom-lab server to list unresolved platform incidents.
```

```text
Use list_admin_audit_events to show the last 5 admin changes in our org.
```

## Exercise

Add one additional tool relevant to your organization, such as:

- Queue health summary
- Address book validation
- Device provisioning status

Document the tool name, input schema, and sample prompt in your lab notes.

## Content still to define

- Official MCP Python/TypeScript SDK version for the lab
- Starter repository with `server.py` boilerplate
- CI check that tool schemas validate
