# Lab 5 - Service apps (Extra)

So far in this lab, we have been using a Personal Access Token to authenticate our bot and MCP clients. While this is great for rapid prototyping and local development, **Personal Access Tokens expire after 12 hours**. 

If we want our AI assistant to run 24/7 and perform organizational troubleshooting, we need a production-ready authentication method. This is where **Service Apps** come in.

## What is a Service App?

A Service App is a type of Webex integration designed for **machine-to-machine** communication. 

Unlike a Personal Access Token (which acts on behalf of *you*, the user), a Service App has no user context. It acts as a system or background service. This makes it the perfect choice for administrative tasks, compliance, and **organizational troubleshooting**.

### Scopes: MCP vs. Service Apps

You have already seen how scopes work. When we looked at the [Meetings MCP Server documentation](https://developer.webex.com/mcp/docs/meetings-mcp-server), we saw that the MCP token acts as a wrapper around specific permissions (like `meeting:schedules_read` or `meeting:schedules_write`). 

![Scope](./assets/scope_1.png){ width="850" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

Service Apps use this exact same concept. When you create a Service App, you must define its **scopes** to strictly limit what the machine is allowed to do. To allow the Service App to connect to an MCP Server, it must include the `spark:mcp` scope, alongside any other API scopes the tools require.

![Scope](./assets/scope_3.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

### The Catch: User Context vs. Machine Context

Because a Service App token is just a standard Webex OAuth 2.0 Bearer token, you can pass it to an MCP Server exactly like you did with your Personal Access Token. However, there is an important difference in how the APIs behave:

1. **Personal Access Token (User Context):** 
   When you used your personal token with the `webex-list-meetings` MCP tool, the Webex API knew exactly *who* was asking. It automatically fetched *your* meetings.

2. **Service App Token (Machine Context):**
   A Service App is a faceless machine. If it calls `webex-list-meetings` without specifying a user, the API will likely return an empty list because the machine itself doesn't have a calendar. 

Since our final goal is **organizational troubleshooting**, we *want* machine-level access. Troubleshooting tools—like looking up organization-wide call diagnostics, checking user provisioning status, or pulling admin logs—are designed for admins. They don't rely on a "me" context; they look at the organization as a whole. 

### The Approval Process: Global vs. Local

Because a Service App operates at a machine level and can access organization-wide data, it requires strict security oversight. 

* **MCP Servers:** As you saw earlier, MCP servers (like the Webex Meetings MCP) are **global** services provided by Cisco or partners. An admin simply toggles them "on" for the organization in Control Hub.
* **Service Apps:** Service Apps are **local** to your organization's development. Because you are building a custom application, a Webex Administrator must explicitly review the requested scopes and authorize your specific Service App before it can generate any tokens.

---

## Step 5.1: Create the Service App

1. Log into [developer.webex.com](https://developer.webex.com/){:target="_blank"} with credentials that were provided.
2. Up on the top right corner of the page, click your avatar and then select [My Webex Apps](https://developer.webex.com/my-apps){:target="_blank"}.
3. As you already have a Bot created, select ‘Create a New App’.
4. In `Create a New App’ page, find the Service App card and click the ‘Create a Service App’ button.

    ![Service Ap](assets/bot_1.png){ width="850" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;" }

5. Enter the following information:

    |        	|                                     	      |
    |-----------------------	|-------------------------------------------------|
    | **App name**       	| WebexOne-***USERNAME***                  |
    | **Icon**       	| Choose one of the available options                     |
    | **Description**       	| Service App for WebexOne                   |
    | **Contact Email**       	| userX@webexone-ai-assistant.wbx.ai |
    | **Scopes** | XXX |

!!! Warning
    For simplicity, in this lab you are going to select all the scopes, but scopes are going to be dependant on which MCP server do you want to use.
    In real enviroment you should be very careful with the scopes assigned and you must select the less possible.

6. Once you have entered the information, your screen should look similar to this:

    ![Service App](./assets/serviceapp_1.png){ width="700" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    !!! Warning
        From this page, copy and save the **Client ID** and **Client Secret**:

        ![Service App](./assets/serviceapp_2.png){ width="700" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}
    
        In VS Code, make sure that in your terminal you are in the right folder:

            * cd ../05_serviceapps
  
        - Copy the example .venv file:

            * cp .env.example .env

        - Copy the them into `.env`:

            ```env
            CLIENT_ID=
            CLIENT_SECRET=
            ```

### Authorize your Service App in your organization

Once the Service App is created, we will need to authorize it. 

!!! Warning
    This is a task that can only be performed by an admin.

Navigate to **Management > Apps > Service Apps** select the Service App you created, and click **Authorize** and **Save**:<br/>

![developer4](./assets/developer4.png){ width="950" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

To use the newly created **Service App**, you will need to get an **Access token**. 

### Access Token

Return to **Webex for Developers**, go to **My Webex Apps** and select the newly created **Service App**:

![developer6_!](./assets/developer6_1.png){ width="800" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

In the section **Org Authorizations**, select your Organization from the dropdown. 

!!! Warning "If this section does not appear, refresh the page."

A text box to enter your **Client Secret** will appear. This way, you can generate an **access_token** for this organization:

![developer6](./assets/developer6.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

!!! Warning
    Now you can save those values in your .env file. You must have already all the needed variables:

    ![env](./assets/env.png){ width="500" style="display: block; border: 1px solid lightgray; border-radius: 8px;"}

!!! Note
    The expiration time for the access token is 14 days, while the refresh token expires in 90 days.



## Step 5.2: Using the token to call an MCP


