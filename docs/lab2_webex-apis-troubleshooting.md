# Lab 2 - Webex APIs

In this section, you will start exploring Webex REST APIs. You will do a quick review on how to use Bruno, then create a **Service App**. That token is what you will use as soon as you need **admin** access — Control Hub, Calling numbers, audit, reports — because a Personal Access Token does not have those rights.

After that, we will look at the APIs that can be used to manage and troubleshoot an organization — status, audit, compliance, reports, calling, and meetings.

## Step 2.1 - General Webex APIs

In the previous section, we enabled our Agent to use MCP Servers to perform actions on our behalf.

At the end of the day, an MCP server is just a list of tools that our agent can use. Those tools are executing API calls. Now, we will be making those API calls ourselves.

### Webex For Developers

Navigate to:<br />

- [Webex for Developers](https://developer.webex.com/){:target="_blank"}

Use the same Webex credentials provided for the lab. 

!!! Warning "Placeholder: Get Personal Access Token"
    [PLACEHOLDER: Add instructions and screenshots showing how to log into the Developer Portal, click on the profile icon, and copy the Personal Access Token (Developer Token). Explain that this token is valid for 12 hours and is useful for **user-level** Try It calls (for example Messaging). Do not use it for admin / Control Hub APIs — those come next with a Service App.]

https://developer.webex.com/messaging/docs/messaging

### Calling APIs using Bruno

### Calling APIs using Python

!!! Note
    A Personal Access Token acts as **you**. User-level APIs (list *your* rooms, *your* meetings) can work. As soon as you call an **admin** API — numbers, people in the org, audit, licenses — you will get `403 Forbidden` or empty data. That is expected. We fix it with a Service App before we start troubleshooting.

## Step 2.2: Service Apps

A Personal Access Token is fine for a quick test in the portal, but it has two problems for this lab:

1. **Rights:** It is user context. Organizational troubleshooting needs admin scopes (Calling config, people, audit, reports).
2. **Lifetime:** It **expires after 12 hours**. That is not valid for anything that should keep running.

This is where **Service Apps** come in.

### What is a Service App?

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

## Step 2.3: Create the Service App

1. Log into [developer.webex.com](https://developer.webex.com/){:target="_blank"} with the credentials that were provided.
2. In the top right corner of the page, click your avatar and then select [My Webex Apps](https://developer.webex.com/my-apps){:target="_blank"}.
3. Click **Create a New App**.
4. On the ‘Create a New App’ page, find the Service App card and click the ‘Create a Service App’ button.

    ![Service App](./assets/bot_1.png){ width="850" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;" }

5. Enter the following information:

    |        	|                                     	      |
    |-----------------------	|-------------------------------------------------|
    | **App name**       	| WebexOne-***USERNAME***                  |
    | **Icon**       	| Choose one of the available options                     |
    | **Description**       	| Service App for WebexOne                   |
    | **Contact Email**       	| userX@webexone-ai-assistant.wbx.ai |
    | **Scopes** | spark:mcp spark:messages_read spark:messages_write spark:rooms_read spark:rooms_write spark:memberships_read spark:memberships_write spark:webhooks_read spark:webhooks_write spark-admin:telephony_config_read |

    !!! Warning
        These are the scopes for **Webex Messaging MCP** and the **Numbers API**. Scopes depend on which MCP server or API you want to use.
       
        Later in this lab, you would need to update the scopes to:

        `spark:mcp spark:messages_read spark:messages_write spark:rooms_read spark:rooms_write spark:memberships_read spark:memberships_write`

        `spark:webhooks_read spark:webhooks_write ...`
       
        For simplicity, in this lab, you can already select all of them.
       
        IMPORTANT: In a real environment, you should be very careful with the assigned scopes and select the minimum required.

6. Once you have entered the information, your screen should look similar to this:

    ![Service App](./assets/serviceapp_1.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    !!! Warning
        From this page, you need to save the **Client ID** and **Client Secret**:

        ![Service App](./assets/serviceapp_2.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

        Open the `.env` file at the root of your project and copy them into it:

        ```env
        CLIENT_ID=
        CLIENT_SECRET=
        ```

7. In the same page, at the top, in the `Admin Authorization` section, click on **Request admin authorization** and you should see it like:

    ![Service App](./assets/serviceapp_3.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    !!! Note
        If you do not do this step, the app won't be visible for admins to authorize.

### Authorize your Service App in your organization

Once the Service App is created, we will need to authorize it. 

!!! Warning
    This is a task that can only be performed by an admin. Presenters will demo it; the next steps are just for reference.

To authorize a **Service App**, go to **Collaboration Control Hub** -> **Apps** -> **Service Apps** and select **Other service apps**. Select the Service App you want to authorize, and click **Authorize** and **Save**:

![Service App](./assets/serviceapp_4.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

To use the newly created **Service App**, you will need to get an **Access token**. 

### Access Token

After the **Service App** has been authorized, you will be able to generate an **Access token**.

1. Return to **Webex for Developers**, go to **My Webex Apps** and select your **Service App**.
2. In the section **Org Authorizations**, select your Organization from the dropdown. 

    ![Service App](./assets/serviceapp_5.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

3. Enter your **Client Secret** and click **Generate tokens**:

    ![Service App](./assets/serviceapp_6.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

4. Copy your **access token** and your **refresh token** into `.env`:

    ```env
    ACCESS_TOKEN=
    REFRESH_TOKEN=
    ```

!!! Note
    The expiration time for the access token is 14 days, while the refresh token expires in 90 days.

From now on, use this **Service App access token** for API testing in Bruno and for the custom MCP server in the next lab.

## Step 2.4: Using the token to call an API

Now, we will test that the Service App token works by making a standard REST API call using **Bruno** (or Postman). 

To demonstrate Control Hub management capabilities, we will use the **Numbers API** to list the phone numbers configured in the organization. This is a typical administrative task. A Personal Access Token would fail here; the Service App should succeed.

1. Open **Bruno** and create a new `GET` request.
2. Set the URL to: `https://webexapis.com/v1/telephony/config/numbers`
3. Go to the **Headers** tab and add:
   * **Name**: `Authorization`
   * **Value**: `Bearer YOUR_SERVICE_APP_ACCESS_TOKEN` (replace with the token from your `.env` file)
4. Click **Send**.

**Equivalent cURL command:**
```bash
curl -s -H "Authorization: Bearer YOUR_SERVICE_APP_ACCESS_TOKEN" \
  "https://webexapis.com/v1/telephony/config/numbers" | python -m json.tool
```

You should receive a JSON response containing a list of phone numbers in your organization, proving your Service App is successfully authenticating and retrieving organizational data.

## Extra: Refresh your access_token

!!! Note
    This is not required for this lab, but it is important to keep in mind for production environments.

As mentioned earlier, the **access_token** will expire after 14 days, and the **refresh_token** will expire in 90 days. It is crucial to handle these expiration scenarios if you have an app running in production.

!!! Note
    When a refresh token is used to generate a new access token, the refresh token's expiration time is reset.

You can refresh your **access_token** using your **refresh_token**, **client_id**, and **client_secret** by making a POST request to the Webex API. 

To manage the token expiration and refresh, we have provided a `TokenManager` class. This class checks if the token is expired and automatically updates your `.env` file so the new token persists across restarts.

1. Navigate to `02_webex_apis/token_manager.py` and review the code:

    ??? Tip "Python Code"
        ```python
        import os
        import time
        import logging
        import requests
        from dotenv import load_dotenv, set_key
        
        log = logging.getLogger("token-manager")
        
        class TokenManager:
            def __init__(self, env_path=".env"):
                self.env_path = env_path
                load_dotenv(self.env_path)
                
                self.client_id = os.getenv("CLIENT_ID")
                self.client_secret = os.getenv("CLIENT_SECRET")
                self.refresh_token_val = os.getenv("REFRESH_TOKEN")
                self.access_token = os.getenv("ACCESS_TOKEN")
                self.expires_at = 0 
        
            def get_token(self):
                """Returns a valid access token, refreshing it if necessary."""
                # If we have a token and it hasn't expired (with a 60s safety buffer)
                if self.access_token and time.time() < self.expires_at:
                    return self.access_token
                
                # Otherwise, refresh the token
                return self.refresh()
        
            def refresh(self):
                """Forces a token refresh via the Webex API."""
                log.info("Refreshing Service App token...")
                if not all([self.client_id, self.client_secret, self.refresh_token_val]):
                    raise ValueError("Missing CLIENT_ID, CLIENT_SECRET, or REFRESH_TOKEN in environment.")
        
                url = "https://webexapis.com/v1/access_token"
                payload = {
                    'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token_val,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                }
                headers = {
                    'Content-type': 'application/x-www-form-urlencoded'
                }
        
                # This is the raw REST API call to Webex to exchange the refresh token
                response = requests.post(url, headers=headers, data=payload)
                
                if response.status_code == 200:
                    token_data = response.json()
                    self.access_token = token_data['access_token']
                    
                    # Calculate expiration time (subtract 60 seconds for safety buffer)
                    self.expires_at = time.time() + token_data['expires_in'] - 60
                    
                    # If a new refresh token is provided, update it
                    if 'refresh_token' in token_data:
                        self.refresh_token_val = token_data['refresh_token']
                        set_key(self.env_path, "REFRESH_TOKEN", self.refresh_token_val)
        
                    # Update the access token in the .env file for persistence
                    set_key(self.env_path, "ACCESS_TOKEN", self.access_token)
                    
                    log.info("Token refreshed successfully.")
                    return self.access_token
                else:
                    raise Exception(f"Failed to refresh token: {response.status_code} - {response.text}")
        ```

2. Navigate to `02_webex_apis/02_refresh.py` and review the code. This script imports the `TokenManager` to perform the refresh:

    ??? Tip "Python Code"
        ```python
        import logging
        from token_manager import TokenManager
        
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
        
        if __name__ == "__main__":
            print("Testing TokenManager...")
            manager = TokenManager()
            
            # Force a refresh by calling refresh() directly instead of get_token()
            new_token = manager.refresh()
            
            print("\n--- Token Refreshed ---")
            print(f"New Access Token: {new_token[:15]}... (truncated)")
            print("\nYour .env file has been automatically updated!")
        ```

3. Run your code with the following command:

    * `python 02_webex_apis/02_refresh.py`

4. After running the code, you will see that the token was refreshed successfully, and if you check your `.env` file, the `ACCESS_TOKEN` and `REFRESH_TOKEN` values have been updated automatically.

## Step 2.5 - Webex APIs for Troubleshooting

You now have a token with **admin** scopes. Use the Service App `ACCESS_TOKEN` in Bruno for the calls below. The Webex Status API is public and does not need a token.

### Webex Status API

Check platform health before deep-diving into org-specific issues.

Reference: [Webex Status API](https://developer.webex.com/calling/docs/webex-status-api){:target="_blank"}

```bash
curl -s https://status.webex.com/api/v2/status.json | python -m json.tool
```

Typical checks:

- Status summary and component rollup
- Unresolved incidents
- Scheduled maintenance

!!! Note "Screenshot needed"
    Add screenshot of status summary JSON or Control Hub status page alongside API output.

### Audit and compliance

| API area | Use case |
| --- | --- |
| Admin Audit Events | Track configuration changes and admin actions |
| Compliance Events | Monitor messaging and room events as compliance officer |
| Security Audit Events | Review security-related admin activity |

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://webexapis.com/v1/adminAudit/events?max=10" | python -m json.tool
```

### Reports

Generate usage and activity reports for analysis:

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reportTemplateId": "REPLACE_WITH_TEMPLATE_ID"}' \
  https://webexapis.com/v1/reports | python -m json.tool
```

!!! Note
    Report templates and scopes vary by license. Your lab instructor will provide the template IDs available in the lab org. Add the matching scopes to the Service App if you get `403`.

### Calling and meetings troubleshooting

| Scenario | API starting point |
| --- | --- |
| Call quality investigation | Detailed Call History, Meeting Qualities |
| Agent / queue issues | Calling Service Settings, Call Routing APIs |
| Meeting attendance / stats | Meetings, Meeting Participants |

Example — list phone numbers (same call as Step 2.4):

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://webexapis.com/v1/telephony/config/numbers" | python -m json.tool
```

### Troubleshooting guide

Review the official guide for diagnostic workflows:

- [Webex API Troubleshooting Guide](https://developer.webex.com/explore/docs/api/guides/troubleshooting){:target="_blank"}

Suggested lab activities (from session deck):

1. Check general Webex Status
2. Review admin audit events
3. Create a report and download it
4. Review compliance events
5. Retrieve call history and meeting statistics

## Exercises

TBC

---

## Step 2.6: The N × M problem MCP solves

Without a standard protocol, every AI application needs custom glue code for every backend system — creating fragile, exponential integration work.

MCP reduces this to **N + M** connections by providing a universal interface between AI hosts and platform capabilities.

## Step 2.7: When to use Webex APIs vs Webex MCP

| Choose Webex REST APIs when… | Choose Webex MCP when… |
| --- | --- |
| You need full control over every request | You want natural-language access from an AI client |
| Performance and custom business logic matter | You need rapid prototyping across MCP-compatible tools |
| You build enterprise apps with webhooks | You connect IDE or agent frameworks to Webex quickly |
