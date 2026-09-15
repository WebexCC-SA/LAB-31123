# Lab 5 - Service apps

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

!!! Note
    This applies to pre-defined Webex MCP Servers.

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

## Step 5.1: Create the Service App

1. Log into [developer.webex.com](https://developer.webex.com/){:target="_blank"} with the credentials that were provided.
2. In the top right corner of the page, click your avatar and then select [My Webex Apps](https://developer.webex.com/my-apps){:target="_blank"}.
3. As you already have a Bot created, select ‘Create a New App’.
4. On the ‘Create a New App’ page, find the Service App card and click the ‘Create a Service App’ button.

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
       For simplicity, in this lab you are going to select all the scopes, but scopes are going to be dependent on which MCP server you want to use.
       In a real environment, you should be very careful with the assigned scopes and select the minimum required.

6. Once you have entered the information, your screen should look similar to this:

    ![Service App](./assets/serviceapp_1.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    !!! Warning
        From this page, you need to save the **Client ID** and **Client Secret**:

        ![Service App](./assets/serviceapp_2.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

        In VS Code, make sure your terminal is in the correct folder:

        * cd ../05_serviceapps
  
        - Copy the example .env file:

            * cp .env.example .env

        - Copy them into `.env`:

            ```env
            CLIENT_ID=
            CLIENT_SECRET=
            ```

### Authorize your Service App in your organization

Once the Service App is created, we will need to authorize it. 

!!! Warning
    This is a task that can only be performed by an admin. Presenters will demo it; the next steps are just for reference.

To authorize a **Service App**, go to **Collaboration Control Hub** -> **Apps** -> **Service Apps** and select **Other service apps**. Select the Service App you want to authorize, and click **Authorize** and **Save**:

![developer4](./assets/developer4.png){ width="950" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

To use the newly created **Service App**, you will need to get an **Access token**. 

### Access Token

Return to **Webex for Developers**, go to **My Webex Apps** and select the newly created **Service App**:

![developer6_!](./assets/developer6_1.png){ width="800" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

In the section **Org Authorizations**, select your Organization from the dropdown. 

!!! Warning "If this section does not appear, refresh the page."

A text box to enter your **Client Secret** will appear. This way, you can generate an **access_token** for this organization:

![developer6](./assets/developer6.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

- Copy them into `.env`:

    ```env
    ACCESS_TOKEN=
    REFRESH_TOKEN=
    ```

!!! Note
    The expiration time for the access token is 14 days, while the refresh token expires in 90 days.

## Step 5.2: Using the token to call an MCP

1. Navigate to `05_serviceapps/01_mcp.py` and review the code:

    ??? Tip "Python Code"
        ```
        import asyncio
        import logging
        import os
        
        from dotenv import load_dotenv
        
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '04_mcp'))
        from mcp_client import McpClient
        
        try:
            import truststore
            truststore.inject_into_ssl()
        except ImportError:
            pass
        
        MESSAGING_MCP_URL = "https://mcp.webexapis.com/mcp/webex-messaging"
        
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
        log = logging.getLogger("mcp-service-app")
        
        load_dotenv()
        
        # We use the token generated from the UI or the refresh script
        SERVICE_APP_TOKEN = os.getenv("ACCESS_TOKEN")
        
        if not SERVICE_APP_TOKEN:
            raise SystemExit("Set ACCESS_TOKEN in your .env file")
        
        async def main():
            log.info("Connecting to Messaging MCP with Service App token...")
        
            client = McpClient(SERVICE_APP_TOKEN, MESSAGING_MCP_URL)
        
            # List tools to prove the token is authorized for spark:mcp
            tools = await client.list_tools()
        
            if not tools:
                log.warning("No tools found or connection failed.")
                return
        
            log.info(f"Success! Found {len(tools)} tool(s) available for the Service App:")
            for tool in tools:
                log.info(f"  - {tool.name}: {tool.description}")
        
        if __name__ == "__main__":
            asyncio.run(main())
        ```

## Extra: Refresh your access_token

!!! Note
    This is not required for this lab, but it is important to keep in mind for production environments.

As mentioned earlier, the **access_token** will expire after 14 days, and the **refresh_token** will expire in 90 days. It is crucial to handle these expiration scenarios if you have an app running in production.

!!! Note
    When a refresh token is used to generate a new access token, the refresh token's expiration time is reset.

You can refresh your **access_token** using your **refresh_token**, **client_id**, and **client_secret** with the following code snippet:

1. Navigate to `05_serviceapps/02_refresh.py` and review the code:

    ??? Tip "Python Code"
        ```
        import os
        from dotenv import load_dotenv
        import requests
        
        # Load environment variables from the .env file.
        load_dotenv()
        
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        refresh_token_val = os.getenv("REFRESH_TOKEN")
        
        if not all([client_id, client_secret, refresh_token_val]):
            raise SystemExit("Please set CLIENT_ID, CLIENT_SECRET, and REFRESH_TOKEN in your .env file")
        
        def refresh_token(client_id, client_secret, refresh_token):
            url = "https://webexapis.com/v1/access_token"
        
            payload = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': client_id,
                'client_secret': client_secret,
            }
        
            headers = {
                'Content-type': 'application/x-www-form-urlencoded'
            }
        
            response = requests.post(url, headers=headers, data=payload)
        
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to refresh token: {response.status_code} - {response.text}")
        
        if __name__ == "__main__":
            print("Refreshing Service App token...")
            token = refresh_token(client_id, client_secret, refresh_token_val)
        
            print("\n--- New Token Details ---")
            print(f"Access Token: {token['access_token']}")
            print(f"Expires in: {token['expires_in']} seconds")
            print(f"Refresh Token: {token['refresh_token']}")
            print(f"Refresh Token Expires in: {token['refresh_token_expires_in']} seconds")
            print(f"Token Type: {token['token_type']}")
        
            print("\nUpdate your .env file with the new ACCESS_TOKEN!")
        ```

2.	Run your code with the following command:

    * python 02_refresh.py

3. After running the code, you will see the following results:

    ![pycharm9](./assets/pycharm9.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    !!! Tip 
        Note that the refresh_token will remain the same.

---

From now on, you will be using the **access token** instead of your personal **Webex MCP token**.
