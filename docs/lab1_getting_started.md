# Getting Started

Welcome to **LAB-31123: Troubleshoot and Manage Your Organization with an AI Assistant**. This section prepares your lab workstation, credentials, and development environment.

## Tools used in this lab

- **Webex Client** — interact with your bot and verify assistant responses
- **Visual Studio Code** — edit code, configure MCP servers, and run the lab assistant from the terminal
- **OpenAI API** — LLM for the bot and agent (key provided by your instructor; **not** GitHub Copilot)
- **Webex for Developers** — create bots, WCIT tokens, and review API documentation
- **Python 3.10+** — run bot, OpenAI, and MCP client samples

## Webex lab credentials

Use the credentials provided by your lab instructor:

| Item | Value |
| --- | --- |
| Username | `podX@cb127.dc-02.com` (replace X with your pod number) |
| Password | Provided in the lab handout |

## OpenAI API key (instructor-provided)

Each participant receives an **OpenAI API key** for this session. Use it only for lab exercises on your assigned workstation.

1. Copy the key from the handout or pod instructions (do not share it in Webex spaces or email).
2. Add it to your local `.env` file (see below).
3. Use the **model name** your instructor specifies (the lab code defaults to `gpt-5-nano` unless changed in `.env`).

```env
OPENAI_API_KEY=sk-your-lab-key-here
OPENAI_MODEL=gpt-5-nano
```

!!! Note
    Never commit `.env` to git. If a key is exposed, tell your instructor immediately so it can be rotated.

## Clone the lab repository

1. Open **Visual Studio Code** on your lab workstation.
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

4. Copy the environment template and fill in your values:

    ```bash
    cp .env.example .env
    ```

    ```env
    BOT_TOKEN=
    WEBEX_WCIT_TOKEN=
    OPENAI_API_KEY=
    OPENAI_MODEL=gpt-5-nano
    WEBEX_ORG_ID=
    ```

## Prepare for Webex MCP (Lab 3)

You will register hosted Webex MCP servers in VS Code in **Lab 3 — Webex MCP Servers in Visual Studio Code**.

This lab **does not use GitHub Copilot**. You will:

- Configure MCP servers in VS Code (`.vscode/mcp.json` or user `mcp.json`)
- Run the **OpenAI-powered Python assistant** from the VS Code terminal (starting in Lab 5)

Before the event, confirm with your instructor that required MCP servers are **enabled in Control Hub** ([provisioning guide](https://developer.webex.com/mcp/docs/provisioning-on-control-hub){:target="_blank"}).

Generate a **WCIT** on **[Webex Agentic Token](https://developer.webex.com/agentic-token){:target="_blank"}** when you reach Lab 3, or use **OAuth Integration** if your instructor directs you to that path (recommended when you are not using a Copilot-style MCP chat UI).

## Create your lab Webex space

1. In Webex Client, create a space named **[Your Name] - AI Assistant Lab**.
2. Save the space ID — you will use it when testing the bot integration in Lab 5.

## Lab flow

| Section | Focus |
| --- | --- |
| Lab 1 | AI assistants, agents, and session architecture |
| Lab 2 | MCP host, client, server, tools, resources, and prompts |
| Lab 3 | Connect and validate Webex MCP servers in VS Code |
| Lab 4 | Webex APIs for status, audit, reports, and troubleshooting |
| Lab 5 | Webex Bot + OpenAI + MCP integration |
| Lab 6 | Agent Skills for operational runbooks |
| Lab 7 | Build a custom MCP server with Webex API tools |
| Lab 8 | Capstone — investigate and resolve an org issue end-to-end |

## Content still to define

- Final lab code repository URL and branch
- Pod-specific credential table and OpenAI model name for the event
- Slido / Q&A embed URL for the welcome page
