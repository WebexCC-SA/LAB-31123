# Lab 3 - Webex MCP Servers in Your IDE

In this section, you will configure official Webex MCP servers in your IDE and execute organizational tasks through natural language.

Reference: [Webex MCP Server Overview](https://developer.webex.com/mcp/docs/webex-mcp-server-overview){:target="_blank"}

## Learning Objectives

Upon completion of this section, you will be able to:

- Install and configure Webex MCP servers in Cursor or VS Code
- Discover available tools from Meetings, Messaging, and Webex Suite servers
- Execute read and write operations through MCP instead of direct API calls

## Available Webex MCP servers

As of this lab (verify before the event):

| Server | Example capabilities |
| --- | --- |
| Meetings MCP | Schedule meetings, list participants, transcripts |
| Messaging MCP | Spaces, messages, people lookup |
| Vidcast MCP | Video messaging workflows |
| Webex Suite MCP | Cross-suite admin and org operations |
| Workspaces MCP | Workspace and device management |

## Step 3.1: Configure MCP servers

1. Open your MCP configuration file (`~/.cursor/mcp.json` or VS Code equivalent).
2. Add the Webex servers provided for the lab:

```json
{
  "mcpServers": {
    "webex-messaging": {
      "command": "npx",
      "args": ["-y", "@webex/mcp-server-messaging"],
      "env": {
        "WEBEX_ACCESS_TOKEN": "YOUR_LAB_TOKEN"
      }
    },
    "webex-suite": {
      "command": "npx",
      "args": ["-y", "@webex/mcp-server-suite"],
      "env": {
        "WEBEX_ACCESS_TOKEN": "YOUR_LAB_TOKEN"
      }
    }
  }
}
```

3. Reload the IDE and confirm servers connect without authentication errors.

!!! Note "Screenshot needed"
    Add screenshot of MCP server list with green/connected status and tool count per server.

## Step 3.2: Verify connectivity

Run a smoke test in your terminal:

```bash
export WEBEX_ACCESS_TOKEN="YOUR_LAB_TOKEN"
curl -s -H "Authorization: Bearer $WEBEX_ACCESS_TOKEN" \
  https://webexapis.com/v1/people/me | python -m json.tool
```

In your IDE, ask:

```text
List the Webex MCP tools available to you and group them by server.
```

## Step 3.3: Execute tasks through MCP

Try these prompts (adjust for your lab tenant):

```text
Look up my Webex profile and show my display name and email.
```

```text
List my Webex spaces and show the title and ID for each one.
```

```text
Send a message to room ROOM_ID: "Hello from the Webex MCP lab!"
```

## Step 3.4: Compare MCP vs direct API

Review the equivalent direct API call in `samples/01_list_rooms.py`:

```python
import os
import requests

TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")
response = requests.get(
    "https://webexapis.com/v1/rooms",
    headers={"Authorization": f"Bearer {TOKEN}"},
    timeout=30,
)
response.raise_for_status()

for room in response.json().get("items", []):
    print(f"{room['title']} ({room['id']})")
```

Discuss with your neighbor: when would you still prefer direct REST calls over MCP?

## Exercise checklist

- [ ] At least two Webex MCP servers connected
- [ ] Successful people or rooms lookup via MCP
- [ ] One message sent to your lab space via MCP
- [ ] Notes on token scopes required for each action

## Content still to define

- Exact npm package names and versions for each Webex MCP server
- Lab tenant token scopes and approval steps
- Screenshots of successful tool invocations
