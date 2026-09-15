# Lab 6 - Build a Custom MCP Server

In this section, you will build a custom MCP server that exposes Webex API operations your organization needs — beyond what the official Webex MCP servers provide out of the box.

In this case, we will build an MCP Server that will help us to do --- actions in our organization.

## Step 6.1: Define your first tool

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

## Step 6.2: Implement tool execution

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

## Step 6.3: Register in your IDE

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

In your IDE:

```text
Use the webex-custom-lab server to list unresolved platform incidents.
```

```text
Use list_admin_audit_events to show the last 5 admin changes in our org.
```

## Step 6.4: Integrate with your AI Assistant




---



