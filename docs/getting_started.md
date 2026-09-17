# Getting Started

Welcome to **LAB-31123: Troubleshoot and Manage Your Organization with an AI Assistant**. This section prepares your lab workstation, credentials, and development environment.

## Join the conversation!

Scan the QR code to be added to the Webex space for Q&A and more.

![Webex](./assets/webex_space.png){ width="300" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

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
| Username | `userX@webexone-ai-assistant.wbx.ai` (replace X with your pod number) |
| Password | Provided in the lab handout |

## Webex Client

To begin, you'll log into your dedicated Webex lab account. This will allow you to see the results of your exercises and interact with your assistant.

1. **Open the Webex Client:** Launch the Webex Desktop App on your lab workstation.
2. **Enter Lab Credentials:** When prompted, enter the **Webex email address and password** provided to you.

!!! Note
    You can also log in at [Webex](https://web.webex.com/){:target="_blank"} 

## Visual Studio

Visual Studio Code will be used for Python-based bot development, service app configuration, and the agentic app and MCP server exercises.

1. Open Visual Studio Code from the desktop:

   ![vsc_logo](./assets/docx-image-004.png){ width="150" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

### Clone the lab repository

2. Go to the **Source Control** tab and click **Clone Repository**:

    ![vsc_clone](./assets/docx-image-005.png){ width="500" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

3. Type the following URL:

    - https://github.com/diegomjimenez/WebexOne2026.git

    ![vsc_repo](./assets/github_1.png){ width="600" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

4. Select a directory to save the project.
5. Click on **Yes, I trust the authors** if a pop-up appears.

### Virtual Environment

1. From the top bar, click on Terminal > New terminal.
2. Create a virtual environment and install dependencies:

    ```bash
    python -m venv .venv
    .\webexone2026\Scripts\activate.ps1
    pip install -r requirements.txt
    ```
    
3. Copy the environment template and fill in your values:

    ```bash
    cp .env.example .env
    ```

### Chat

1. Open the Command Palette (`Ctrl+Shift+P`) and type "Chat: Open Chat (Agent)".

    ![Create_token](./assets/vscode_6.png){ width="600" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    The Chat should open on the side:

    ![Create_token](./assets/vscode_16.png){ width="400" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

### Bruno / Postman
