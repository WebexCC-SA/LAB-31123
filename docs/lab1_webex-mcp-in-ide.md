# Lab 1 - Webex MCP Servers in Your IDE

In this section, you will connect **official Webex MCP servers** to your IDE to execute organizational tasks through natural language.

In this lab our IDE will be **Visual Studio Code**.

As of today, these are the official Webex MCP servers available.

| MCP server | Documentation | Server URL |
| --- | --- | --- |
| **Meetings MCP Server** | [Meetings MCP](https://developer.webex.com/mcp/docs/meetings-mcp-server){:target="_blank"} | `https://mcp.webexapis.com/mcp/webex-meeting` |
| **Messaging MCP Server** | [Messaging MCP](https://developer.webex.com/mcp/docs/messaging-mcp-server){:target="_blank"} | `https://mcp.webexapis.com/mcp/webex-messaging` |
| **Vidcast MCP Server** | [Vidcast MCP](https://developer.webex.com/mcp/docs/vidcast-mcp-server){:target="_blank"} | `https://mcp.webexapis.com/mcp/vidcast` |
| **Webex Suite MCP Server** | [Webex Suite MCP](https://developer.webex.com/mcp/docs/webex-suite-mcp-server){:target="_blank"} | `https://mcp.webexapis.com/mcp/webex-suite` |
| **Workspaces MCP Server (New)** | [Workspaces MCP](https://developer.webex.com/mcp/docs/workspaces-mcp-server){:target="_blank"} | `https://mcp.webexapis.com/mcp/workspaces` |
| **Connect CPaaS MCP Server (New)** | [Connect CPaaS MCP](https://developer.webex.com/mcp/docs/connect-mcp-server){:target="_blank"} | **Regional** — use the URL that matches your Webex Connect tenant (see table below) |
| **Contact Center MCP Server (New)** | [Contact Center MCP](https://developer.webex.com/mcp/docs/contact-center-mcp-server){:target="_blank"} | **Tenant-specific** — sign in on the product page to copy your regional URL |
| **Contact Center Operation MCP Server (New)** | [Contact Center Operation MCP](https://developer.webex.com/mcp/docs/contact-center-operation-mcp-server){:target="_blank"} | **Tenant-specific** — sign in on the product page to copy your server URL |

This list is getting updated, you can use the [Webex MCP Server Overview](https://developer.webex.com/mcp/docs/webex-mcp-server-overview){:target="_blank"} for the latest catalog.

### Prerequisites

You can notice very quickly in the documentation that every official Webex MCP server includes this requirement:

!!! Note
    This MCP server must be enabled by your organization's admin in Webex Control Hub before it can be used. See [Provisioning on Control Hub](https://developer.webex.com/mcp/docs/provisioning-on-control-hub){:target="_blank"} for details.

MCP server are **NOT** enabled by default in your organization, and you need to enable them to allow your users to use them.

!!! Warning "Important"
    These steps have been done previously to this lab, as you all are sharing the same organization, but this is relevant to your organizations. This will be shown by presenters as a demo.

1. If you try to enable MCP for the first time, you will see a message **No allowed MCP servers found**.

    ![Create_token](./assets/token_4.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

2. To enable them, you need to go in **Collaboration Control Hub** -> **Apps** -> **Agentic Apps** and go to **Webex** tab:

    ![Create_token](./assets/controlhub_1.png){ width="1000" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

3. To enable any of them, click "Allowed for all users" and save:

    ![Create_token](./assets/controlhub_2.png){ width="1000" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

4. You are not done yet, if you try to use an MCP server now, you will see a similar error to:

    ```bash
    2026-09-14 12:21:38.230 [warning] [server stderr] [63062] Fatal error: SdkHttpError: Error POSTing to endpoint: {"id":0,"jsonrpc":"2.0","error":{"code":-32003,"message":"You don't have access to this MCP server yet. Ask your administrator to enable it for your account or organization.","data":{"reason":"ACCESS_DENIED"}}}
    2026-09-14 12:21:38.230 [warning] [server stderr]     at StreamableHTTPClientTransport._send (XXXX/.npm/_npx/705d23756ff7dacc/node_modules/mcp-remote/dist/chunk-EFMRUNOV.js:31464:15)
    2026-09-14 12:21:38.230 [warning] [server stderr]     at process.processTicksAndRejections (node:internal/process/task_queues:105:5) {
    2026-09-14 12:21:38.231 [warning] [server stderr]   code: 'CLIENT_HTTP_NOT_IMPLEMENTED',
    2026-09-14 12:21:38.231 [warning] [server stderr]   data: {
    2026-09-14 12:21:38.231 [warning] [server stderr]     status: 403,
    2026-09-14 12:21:38.231 [warning] [server stderr]     statusText: 'Forbidden',
    2026-09-14 12:21:38.231 [warning] [server stderr]     text: `{"id":0,"jsonrpc":"2.0","error":{"code":-32003,"message":"You don't have access to this MCP server yet. Ask your administrator to enable it for your account or organization.","data":{"reason":"ACCESS_DENIED"}}}`
    ```

    You need to allow Tools per MCP server.

6. Go to the MCP server and select the **Tools** tab, and enable the ones you will allow user to use, in this case, all of them will be enabled:

    ![Create_token](./assets/controlhub_3.png){ width="1000" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    After this change, users will be able to use it.

## Step 1.1: Adding an MCP server to VS Code

Now that you have allowed your users to use MCP, now every user will be able to generate a token for each of them.

As an user, the first thing that you will need to do is to get the token to access the MCP servers.

1. Log into [developer.webex.com](https://developer.webex.com/){:target="_blank"} with credentials that were provided.
2. Up on the top right corner of the page, click your avatar and then select [Manage Webex Agentic MCP App token](https://developer.webex.com/agentic-token){:target="_blank"}.
3. Inside "Generate token" click on "Generate now":
   
    ![Create_token](./assets/token_1.png){ width="950" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

4. You need a token per MCP server, in this case we will start using **Webex Messaging**:

    ![Create_token](./assets/token_2.png){ width="500" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

5. You will now see the token:

    ![Create_token](./assets/token_3.png){ width="600" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    !!! Warning
        You need to copy the token now, as you won't be able to see it again later.

        Paste your token instead of **WEBEX_MCP_TOKEN** in **.vscode/mcp.json** and save the file.

    !!! Note
        The file **.vscode/mcp.json** is the file where you are going to define all the MCP servers that your agent will have access to. Open it in your VS Code:

        ```json
        {
         "servers": {
          "webex-messaging": {
           "type": "stdio",
           "command": "npx",
           "args": [
            "-y",
            "mcp-remote",
            "https://mcp.webexapis.com/mcp/webex-messaging",
            "--header",
            "Authorization: Bearer WEBEX_MCP_TOKEN"
           ]
          }
         }
        }
        ```

        Currently you will see that we have already introduce the Webex Messaging MCP. It includes the commands that needs to be run, the URL and the token.

    !!! Note
        Note that this token is only valid for 12 hours.

6. You need to reload VS Code node for MCP to take effect. Open the Command Palette `Ctrl+Shift+P` and select "Developer: Reload Window"

    ![Create_token](./assets/vscode_1.png){ width="750" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

7. Open the Command Palette `Ctrl+Shift+P` again and type "MCP: List Servers"

    ![Create_token](./assets/vscode_2.png){ width="750" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

8. You should see now the newly added MCP server, click on it:

    ![Create_token](./assets/vscode_3.png){ width="750" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

9. And click "Start Server".

    ![Create_token](./assets/vscode_4.png){ width="750" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    !!! Note
    Note that you can see also see now the MCP server attached in the Chat.

    ![Create_token](./assets/vscode_16.png){ width="400" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

10. After that, the Output view should open automatically, if not, choose View -> Output.

    ![Create_token](./assets/vscode_5.png){ width="950" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    You should see that tools were discovered. If you see a message like the following, you have connected to the MCP successfully:
   
    ```bash
    2026-09-13 20:35:36.277 [info] Discovered 20 tools
    ```
    
    Now, you have configured VS Code to connect to the MCP Server.

    These are the 20 tools available in this MCP server:
    
    ![Tools](./assets/tools_2.png){ width="400" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

## Step 1.2: Adding the LLM to VS Code

The MCP server itself it is just a bunch of tools that an agent can call, but you need to add the brain, that will be the LLM. In this lab we will be using OpenAI models,
The Webex MCP server is only the tool layer (list spaces, search messages, etc.). The LLM is the brain that reads your question, chooses tools, and turns results into an answer.

Before we have opened the Chat, but now we will set up the agent.
   
1. Open the Command Palette `Ctrl+Shift+P` and type "Chat: Manage Language Models"

    ![Create_token](./assets/vscode_7.png){ width="650" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

2. Select Add Models..." > OpenAI":

    ![Create_token](./assets/vscode_8.png){ width="1000" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

3. Keep "OpenAI" as Group Name and press Enter

    ![Create_token](./assets/vscode_9.png){ width="550" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

4. And introduce the API Key that was provided to you. You should see it now:

    ![Create_token](./assets/vscode_10.png){ width="1000" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    !!! Note
        GPT-5 Nano is the only model available.

5. To test it, make sure you select the model in the chat, and say "Hello":

    ![Create_token](./assets/vscode_11.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    !!! Note
        Now, the LLM is answering so the answer can vary from what you see in the screenshot as it is not predictable.

7. You can ask the agent to list the tools available:

    ![Create_token](./assets/vscode_13.png){ width="700" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

8. Now, ask to create a space for you. In this case, I will ask the following `Create a Webex Space, with title "WebexOne - Diejimen"`:

    ![Create_token](./assets/vscode_14.png){ width="700" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

9. You will get a confirmation, click on "Allow in this Session", after few seconds, you will get the confirmation:

    ![Create_token](./assets/vscode_15.png){ width="700" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    And you can see it in the Webex App!

    ![Webex](./assets/webex_1.png){ width="800" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

Congrats! Now you have your agent set up in your VS Code and it is connected to the MCP server. Now you will have to integrate the Meetings MCP and be able to schedule a meeting.

## Exercises

In this section you can test your knowledge on what we have seen before. If you need some help, you can check the solution.

### Add Meetings MCP server

In this exercise, you need to add the [Meetings MCP](https://developer.webex.com/mcp/docs/meetings-mcp-server) to VS Code.

??? Solution

    1. To add the new MCP server, you will first need to create a new token.

        ![Create_token](./assets/token_5.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    2. Once you have the token, add the server to the `mcp.json` file:

        ```json
        {
          "servers": {
            "webex-messaging": {
              "type": "stdio",
              "command": "npx",
              "args": [
                "-y",
                "mcp-remote",
                "https://mcp.webexapis.com/mcp/webex-messaging",
                "--header",
                "Authorization: Bearer YTkwNzFiZGItMzFjYi00MjRiLTk0MzctNTE5MmQ5MjM4NTkyZjMxMTQwMTUtYTNh_P0A1_74983fd5-5c18-45cb-bfcd-507005e05b0f"
              ]
            },
            "webex-meeting": {
              "type": "stdio",
              "command": "npx",
              "args": [
                "-y",
                "mcp-remote",
                "https://mcp.webexapis.com/mcp/webex-meeting",
                "--header",
                "Authorization: Bearer NzM2MDk2MWItZTg1YS00MmM5LTg4NTQtYTY1YzZhNWY2YzRiZDgwZTg5ZGYtYTA3_P0A1_74983fd5-5c18-45cb-bfcd-507005e05b0f"
              ]
            }
          }
        }
        ```

    3. Save the file, and start the server. For that open the Command Palette `Ctrl+Shift+P`, and type "MCP: List Servers", select the newly added server and click "Start Server". If it work, you will see that 8 tools have been found in the Output tab:

        ```
        2026-09-14 18:07:02.824 [info] Discovered 8 tools
        ```

        These are the tools available in this MCP server:

        ![Tools](./assets/tools_1.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

### Organize a meeting using your AI Assistant

Once the MCP is added, schedule a meeting together with the admin of the organization "admin@webexone-ai-assistant.wbx.ai" for tomorrow at a time of your choice.

??? Solution

    Using the chat, ask your Assistant to schedule a meeting. In my case, I used the following message:

    * I need to schedule a meeting with user1@webexone-ai-assistant.wbx.ai tomorrow at 6PM CET time.

    It may ask your for confirmation:

    ![Meeting](./assets/meeting_1.png){ width="500" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    Once done, it will provide you with the meeting details:

    ![Meeting](./assets/meeting_2.png){ width="500" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    You can check from your Webex App that the meeting was scheduled:

    ![Meeting](./assets/meeting_3.png){ width="950" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    And confirm the participants:

    ![Meeting](./assets/meeting_4.png){ width="400" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    You can also test now the other functionalities.
