# Getting Started

Welcome to **LAB-31123: Troubleshoot and Manage Your Organization with an AI Assistant**. This section prepares your lab workstation, credentials, and development environment.

## Tools used in this lab

- **Webex Client** — interact with your bot and verify assistant responses
- **Cursor or VS Code** — MCP host and development environment
- **Webex for Developers** — create bots and review API documentation
- **Python 3.10+** — run bot and MCP server samples

## Webex lab credentials

Use the credentials provided by your lab instructor:

| Item | Value |
| --- | --- |
| Username | `podX@cb127.dc-02.com` (replace X with your pod number) |
| Password | Provided in the lab handout |

## Clone the lab repository

1. Open **Visual Studio Code** or **Cursor** on your lab workstation.
2. Clone the lab code repository:

    ```bash
    git clone https://github.com/diegomjimenez/WebexOne2026_AI_Assistant.git
    cd WebexOne2026_AI_Assistant
    ```

3. Create a virtual environment and install dependencies:

    ```bash
    python -m venv .venv
    source .venv/bin/activate   # macOS/Linux
    # .\.venv\Scripts\activate  # Windows PowerShell
    pip install -r requirements.txt
    ```

4. Copy the environment template:

    ```bash
    cp .env.example .env
    ```

    ```env
    BOT_TOKEN=
    WEBEX_ACCESS_TOKEN=
    WEBEX_ORG_ID=
    OPENAI_API_KEY=
    MCP_SERVER_COMMAND=
    ```

## Configure your MCP host

Add Webex MCP servers to your IDE configuration file.

**Cursor** (`~/.cursor/mcp.json` on macOS/Linux):

```json
{
  "mcpServers": {
    "webex-suite": {
      "command": "npx",
      "args": ["-y", "@webex/mcp-server-suite"],
      "env": {
        "WEBEX_ACCESS_TOKEN": "YOUR_LAB_ACCESS_TOKEN"
      }
    }
  }
}
```

!!! Note "Screenshot needed"
    Add screenshot of Cursor Settings → MCP showing connected Webex MCP servers and available tools.

## Create your lab Webex space

1. In Webex Client, create a space named **[Your Name] - AI Assistant Lab**.
2. Save the space ID — you will use it when testing the bot integration in Lab 5.

## Lab flow

| Section | Focus |
| --- | --- |
| Lab 1 | AI assistants, agents, and session architecture |
| Lab 2 | MCP host, client, server, tools, resources, and prompts |
| Lab 3 | Connect and use official Webex MCP servers in your IDE |
| Lab 4 | Webex APIs for status, audit, reports, and troubleshooting |
| Lab 5 | Wire a Webex Bot to your AI assistant |
| Lab 6 | Agent Skills for operational runbooks |
| Lab 7 | Build a custom MCP server with Webex API tools |
| Lab 8 | Capstone — investigate and resolve an org issue end-to-end |

## Content still to define

- Final lab code repository URL and branch
- Pod-specific credential table
- Exact MCP server package names and versions for the event
- Slido / Q&A embed URL for the welcome page
