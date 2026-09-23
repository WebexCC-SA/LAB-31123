# Lab 2 - Webex APIs

In the previous section, we enabled our agent to use MCP servers to perform actions on our behalf. The assistant called Webex for you through the official MCP servers, and each of those servers is just a wrapper around Webex API calls.

In this section you will make those API calls yourself. This matters because the official MCP servers cover only a limited set of APIs, and we want to give our agent more tools and possibilities. That is what we will build in the next labs.

## Step 2.1 - Get a Personal Access Token

During the previous lab, you used an **Agentic MCP App token** to perform actions. That is a special token, scoped to execute actions through the MCP servers, and it only works with the official Webex MCP servers. It will not work for the direct API calls in this lab.

For the simplicity of this hands-on lab, we will use your Personal Access Token (PAT) instead. Because you are an administrator in this sandbox, your PAT automatically inherits all your admin rights. It requires no scope configuration and lasts for 12 hours, which is perfect for a workshop.

1. In [Webex for Developers](https://developer.webex.com/){:target="_blank"}, in the top right corner, click your avatar and select copy the **Bearer** token.

    ![Token](./assets/token_6.png){ width="350" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

2. Open the `.env` file at the root of your project (you copied it from `.env.example` in Getting Started), paste the token and save the file:

    ```env
    ACCESS_TOKEN=
    ```

3. Paste the same token into the `token` variable of your Bruno environment, so your requests can use `Bearer {{token}}` and save.

    ![Token](./assets/token_7.png){ width="950" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

## Step 2.2: Production Architecture (Service Apps & Integrations)

While a Personal Access Token is perfect for a quick lab, it has a major problem for production: **It expires after 12 hours**. That is not valid for a bot that should keep running forever.

That is what **Service Apps** and **OAuth Integrations** are for.

### What is a Service App?

A Service App is a Webex integration for **machine-to-machine** communication.

Unlike a Personal Access Token (which acts on behalf of *you*), a Service App has no user context. It acts as a system or background service. That is the usual choice for administrative tasks and compliance in production.

### Tokens and Scopes

You have already seen how scopes work. When we looked at the [Meetings MCP Server documentation](https://developer.webex.com/mcp/docs/meetings-mcp-server), the MCP token was a wrapper around specific permissions (like `meeting:schedules_read` or `meeting:schedules_write`).

![Scope](./assets/scope_1.png){ width="850" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

Every Webex API requires specific scopes. How you get those scopes depends on the token type:

1. **Personal Access Token (what we are using):** The Developer Token you just copied inherits *all* the scopes your user account has. Since you are an admin, it has admin scopes.
2. **Service Apps (production):** When you create a Service App, you must explicitly define its **scopes** to limit what the machine is allowed to do. If it needs to connect to an official Webex MCP Server, it must include the `spark:mcp` scope, alongside any other API scopes the tools require.

![Scope](./assets/scope_3.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

### User Context vs. Machine Context

A Service App token is still a standard Webex OAuth 2.0 Bearer token, so you can pass it to an MCP server the same way you passed a PAT. However, the APIs do not behave the same:

1. **Personal Access Token (User Context):**
   When you used your token with the `webex-list-meetings` MCP tool, the Webex API knew *who* was asking. It fetched *your* meetings.

2. **Service App Token (Machine Context):**
   A Service App is a faceless machine. If it calls `webex-list-meetings` without specifying a user, the API will likely return an empty list because the machine itself does not have a calendar.

!!! Warning "Analytics and Reports"
    Service Apps work for most administrative tasks. Webex Analytics and Reporting APIs require **user context** — they block Service Apps by design.

    If a production AI assistant needs to pull analytics or reports, it cannot use a Service App. It uses an **OAuth Integration**: the bot sends the user a "Log In" button, the human admin logs in, and the bot receives a user-bound token.

### Service Apps

Because a Service App operates at machine level and can access organization-wide data, a Webex administrator must review the requested scopes and authorize the app in Control Hub before it can generate tokens.

For this lab we skip that process. Everything from here on uses your Personal Access Token.

??? Note "Reference: How to Create and approve a Service App"
    If you ever need a Service App in production, here is how you do it:

    1. Log into [developer.webex.com](https://developer.webex.com/){:target="_blank"}.
    2. In the top right corner of the page, click your avatar and then select [My Webex Apps](https://developer.webex.com/my-apps){:target="_blank"}.
    3. Click **Create a New App**.
    4. On the ‘Create a New App’ page, find the Service App card and click the ‘Create a Service App’ button.

        ![Service App](./assets/bot_1.png){ width="850" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;" }

    5. Enter the necessary information (Name, Icon, Description, Contact Email).
    6. Select the **Scopes** your machine needs. For example, to read phone numbers, you would need `spark-admin:telephony_config_read`.

        ![Service App](./assets/serviceapp_1.png){ style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    7. Once created, you will get a **Client ID** and **Client Secret**.

        ![Service App](./assets/serviceapp_2.png){ style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    8. At the top, in the `Admin Authorization` section, click on **Request admin authorization**.

        ![Service App](./assets/serviceapp_3.png){ width="600" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    9. A Webex Administrator must then go to **Collaboration Control Hub** -> **Apps** -> **Service Apps**, select your app, and click **Authorize**.

        ![Service App](./assets/serviceapp_4.png){ style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    10. Finally, you return to the Developer Portal, select your Org under **Org Authorizations**, enter your Client Secret, and click **Generate tokens** to get your 14-day `access_token` and 90-day `refresh_token`.

        ![Service App](./assets/serviceapp_5.png){ width="800" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}
        ![Service App](./assets/serviceapp_6.png){ width="800" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    **How to Refresh a Service App Token**

    Unlike a Personal Access Token which simply expires, a Service App token can be refreshed using the `refresh_token`. That is just another Webex API call: a form-encoded `POST` to `https://webexapis.com/v1/access_token` with these fields:

    | Field | Value |
    | --- | --- |
    | `grant_type` | `refresh_token` |
    | `client_id` | The Client ID from the Service App |
    | `client_secret` | The Client Secret from the Service App |
    | `refresh_token` | The 90-day refresh token generated above |

    The response returns a new `access_token` and a new `refresh_token`. Store both; the previous refresh token is no longer valid.

    The Developer Portal has the same request, with snippets in the language you need: [Using the Refresh Token](https://developer.webex.com/create/docs/authentication#using-the-refresh-token){:target="_blank"}.

    ??? Tip "Python Code" 
        ```python
        import requests
    
        url = "https://webexapis.com/v1/access_token"
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': 'YOUR_REFRESH_TOKEN',
            'client_id': 'YOUR_CLIENT_ID',
            'client_secret': 'YOUR_CLIENT_SECRET',
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
    
        response = requests.post(url, headers=headers, data=payload)
        print(response.json()) # Contains the new access_token and refresh_token
        ```

## Step 2.3: Calling Webex APIs

Now that we have our token, we can start making API calls. The [Webex Developer Portal](https://developer.webex.com/docs/api/v1/){:target="_blank"} provides documentation and ready-to-use code snippets for all APIs. You can select your preferred language (cURL, Python and Node.js) and copy the code directly.

Every Webex API call has the same anatomy: a method, a URL, and an `Authorization` header carrying your token. Once you have seen that, the tool you use is a matter of what you are trying to do:

| Tool | What we will use it for |
| --- | --- |
| **cURL** | A quick check from the terminal. No setup, and it is what you paste into a ticket so a colleague can reproduce your result. |
| **Bruno** | Exploring an API properly: saved requests, the token in an environment variable, and IDs from one response feeding the next. |
| **Python** | The form an assistant needs. This is the shape your Lab 3 MCP tools take. |

### Calling APIs using cURL

Start with the smallest possible call: who does this token belong to?

!!! Warning
    Replace `YOUR_ACCESS_TOKEN` with the token from your `.env` file.

1. Run the following command from the **VS Code terminal**:

    ```bash
    curl -s -H "Authorization: Bearer YOUR_ACCESS_TOKEN" "https://webexapis.com/v1/people/me" | python -m json.tool
    ```

    The response is your own user record:

    ??? Tip "Full response"
        ```powershell
        (webexone)  % curl -s -H "Authorization: Bearer MzY5NzViMTAtOWM0ZS00ZGIwLTllOWItNGQ4ZGMzYmQ5YzUwNDkzMGNiNTYtYmRj_P0A1_74983fd5-5c18-45cb-bfcd-507005e05b0f" "https://webexapis.com/v1/people/me" | python -m json.tool
        {
            "id": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xOGMyYzQ4OS0yZmVmLTRhMTUtYTRiZC1jYWI3YjY1ZDg0MTY",
            "emails": [
                "pod0@webexone-ai-assistant.wbx.ai"
            ],
            "sipAddresses": [
                {
                    "type": "cloud-calling",
                    "value": "pod0@webexone-ai-assistant-sbx.calls.webex.com",
                    "primary": true
                }
            ],
            "displayName": "Pod 0",
            "nickName": "Pod",
            "firstName": "Pod",
            "lastName": "0",
            "orgId": "Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi83NDk4M2ZkNS01YzE4LTQ1Y2ItYmZjZC01MDcwMDVlMDViMGY",
            "roles": [
                "Y2lzY29zcGFyazovL3VzL1JPTEUvaWRfZnVsbF9hZG1pbg"
            ],
            "licenses": [
                "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkZUTV9mNWZkZTM1Zi00NzA0LTQ2MGEtODEwZi00YzVkMzUyNDFlNjk",
                "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkZTU18xYjcyOGZmOS03ZGU4LTRjYjctOTU0MC0yOTMyMGI1YTQyY2I",
                "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkZNU185ZWNhNzgxNC0zMzEzLTQ2NGYtOTY0Mi0wMjM5ODc1YmM5Zjg",
                "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkZUQ19hMjQ3MzgyOC1hOTgwLTQ3MmYtODE5ZC02YjljY2UwOGU5MmI"
            ],
            "created": "2026-09-23T10:06:45.423Z",
            "lastModified": "2026-09-23T10:08:45.930Z",
            "status": "unknown",
            "invitePending": false,
            "loginEnabled": true,
            "type": "person",
            "siteUrls": [
                "webexone-ai-assistant-sbx.webex.com"
            ]
        }
        ```

    !!! Warning
        If this returns `401`, your token is wrong or expired, and no call will work.
    
    2. Now something only an administrator can ask — what is the organization entitled to?
    
        ```bash
        curl -s -H "Authorization: Bearer YOUR_ACCESS_TOKEN" "https://webexapis.com/v1/licenses" | python -m json.tool
        ```

        ??? Tip "Full response"
            ```powershell
            {
                "items": [
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkVQQ19mZDdjNmNkMC0zZWRhLTRkYTUtOWNmZC0yZjVhNGJhMzZlNDk",
                        "name": "Epic Desktop Connector for Webex Contact Center",
                        "totalUnits": 10,
                        "consumedUnits": 0,
                        "consumedByUsers": 0,
                        "consumedByWorkspaces": 0,
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOk1TX2ZkY2E5ZDBkLTJkZmEtNDM5Yi04MmM4LTUzMDU3MGVjOWY1Yw",
                        "name": "Advanced Messaging",
                        "totalUnits": 100,
                        "consumedUnits": 1,
                        "consumedByUsers": 1,
                        "consumedByWorkspaces": 0,
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOlNGRFNLX2VhMThiNzZmLTE2MzQtNGM5Ny05NWQwLTg0MjFjODBmYzkxYg",
                        "name": "Salesforce Desktop Connector",
                        "totalUnits": 10,
                        "consumedUnits": 0,
                        "consumedByUsers": 0,
                        "consumedByWorkspaces": 0,
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkJDUkxDXzRkNTFkZWMxLTU2MDItNDRmZS04ZTgyLWQ1ZDliZTIzOGY0ZQ",
                        "name": "Webex Calling - Route List Calls",
                        "totalUnits": 10,
                        "consumedUnits": 0,
                        "consumedByUsers": null,
                        "consumedByWorkspaces": null,
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkNKUFBSTV9kOTJmMDcxNi00MzM1LTRjYzEtOWYyOC1iODJiZmVmMTRmMzM",
                        "name": "Contact Center Premium Agent",
                        "totalUnits": 50,
                        "consumedUnits": 3,
                        "consumedByUsers": 3,
                        "consumedByWorkspaces": 0,
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOlNEX2YwOTk5YTY0LTNiMWEtNDUxOS1iYWNjLTg1OGVlN2U1NjczNA",
                        "name": "Webex Room Kit",
                        "totalUnits": 5,
                        "consumedUnits": 0,
                        "consumedByUsers": 0,
                        "consumedByWorkspaces": 0,
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkVFXzRkZDBjMWUwLTdhYWUtNDhjZi1iYTQzLTM2M2MxM2RlNDMwYl93ZWJleG9uZS1haS1hc3Npc3RhbnQtc2J4LndlYmV4LmNvbQ",
                        "name": "Webex Meetings Suite",
                        "totalUnits": 100,
                        "consumedUnits": 3,
                        "consumedByUsers": 3,
                        "consumedByWorkspaces": 0,
                        "siteUrl": "webexone-ai-assistant-sbx.webex.com",
                        "siteType": "Control Hub managed site",
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkJDU1REXzdiNzk3N2QxLTQ2MzQtNDJlZS1iMzIwLWY0NDc4NDFkODdiYg",
                        "name": "Webex Calling - Professional",
                        "totalUnits": 100,
                        "consumedUnits": 3,
                        "consumedByUsers": 2,
                        "consumedByWorkspaces": 1,
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkJDQ0FfMWNhZWYxNjYtMjExMy00NGQ1LWJlMzUtZWNkMDk3OTgwODAx",
                        "name": "Webex Calling - Workspaces",
                        "totalUnits": 100,
                        "consumedUnits": 0,
                        "consumedByUsers": 0,
                        "consumedByWorkspaces": 0,
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkNKUFNURF8xN2Y5YTMwOC03OTgyLTRiNmQtYjVlMC0xZTZiM2MyMjMxNzM",
                        "name": "Contact center Standard Agent",
                        "totalUnits": 50,
                        "consumedUnits": 0,
                        "consumedByUsers": 0,
                        "consumedByWorkspaces": 0,
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOlJUVF9lZWVjNGQ2ZC0wNTFhLTRiMjAtODIzNi0xZDM0YWQyYzU3MzQ",
                        "name": "Real-Time Translations",
                        "totalUnits": 100,
                        "consumedUnits": 3,
                        "consumedByUsers": 3,
                        "consumedByWorkspaces": 0,
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkNGXzQzNWIzZGYxLWI3NDYtNGE2MS04Y2Y5LTc4M2RlOWNjY2ZiZA",
                        "name": "Advanced Space Meetings",
                        "totalUnits": 100,
                        "consumedUnits": 1,
                        "consumedByUsers": 1,
                        "consumedByWorkspaces": 0,
                        "subscriptionId": "trialSub.e57285a3-275b-4547-ae16-69d6371cc2c0"
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkJDSERPX2ZmNTZmMTcwLThlZDAtMzE2OC04YWMwLWRmMWJjNGViMDA4Mw",
                        "name": "Webex Calling - Hot desk only",
                        "totalUnits": 9,
                        "consumedUnits": 0,
                        "consumedByUsers": 0,
                        "consumedByWorkspaces": 0
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkNFXzEyM2UzNTY2LTVlMDYtNGJmMy04NDQ5LTFhYjUxYTFkMWNlMw",
                        "name": "Hybrid - Exchange Calendar",
                        "totalUnits": 44,
                        "consumedUnits": 0,
                        "consumedByUsers": 0,
                        "consumedByWorkspaces": 0
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkNHXzVkYjcwNjYyLWNmYTItNGFjZC04MTRlLTgwYjNiNWVkZjNlZA",
                        "name": "Hybrid - Google Calendar",
                        "totalUnits": 44,
                        "consumedUnits": 0,
                        "consumedByUsers": 0,
                        "consumedByWorkspaces": 0
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkZNU185ZWNhNzgxNC0zMzEzLTQ2NGYtOTY0Mi0wMjM5ODc1YmM5Zjg",
                        "name": "Basic Messaging",
                        "totalUnits": 44,
                        "consumedUnits": 44,
                        "consumedByUsers": 44,
                        "consumedByWorkspaces": 0
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkZTU18xYjcyOGZmOS03ZGU4LTRjYjctOTU0MC0yOTMyMGI1YTQyY2I",
                        "name": "Free screen share",
                        "totalUnits": 44,
                        "consumedUnits": 44,
                        "consumedByUsers": 44,
                        "consumedByWorkspaces": 0
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkZUQ19hMjQ3MzgyOC1hOTgwLTQ3MmYtODE5ZC02YjljY2UwOGU5MmI",
                        "name": "Call on Webex (1:1 call, non-PSTN)",
                        "totalUnits": 44,
                        "consumedUnits": 44,
                        "consumedByUsers": 44,
                        "consumedByWorkspaces": 0
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkZUTV9mNWZkZTM1Zi00NzA0LTQ2MGEtODEwZi00YzVkMzUyNDFlNjk",
                        "name": "Basic Space Meetings",
                        "totalUnits": 44,
                        "consumedUnits": 44,
                        "consumedByUsers": 44,
                        "consumedByWorkspaces": 0
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOkhNXzdjOGMyZGVhLWIwNTUtNDNlNy1hODkyLWNmMmI1MDcyNTAzNg",
                        "name": "Hybrid - Message",
                        "totalUnits": 44,
                        "consumedUnits": 0,
                        "consumedByUsers": 0,
                        "consumedByWorkspaces": 0
                    },
                    {
                        "id": "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvNzQ5ODNmZDUtNWMxOC00NWNiLWJmY2QtNTA3MDA1ZTA1YjBmOlVDUFJFTV9jMzMyOWQzMi0xNmVkLTQxNDUtOTUyNS02M2FjYjRiMzFiMjA",
                        "name": "Unified Communication Manager (UCM)",
                        "totalUnits": 44,
                        "consumedUnits": 0,
                        "consumedByUsers": 0,
                        "consumedByWorkspaces": 0
                    }
                ]
            }
            ```

        Two commands in, and you have already proved both halves of what you need: the token is valid, and it carries admin rights.

### Calling APIs using Bruno

cURL is fine for one-off checks, but it gets painful as soon as you want to keep a call, tweak its parameters, or reuse an ID from a previous response. That is where Bruno comes in.

To demonstrate Control Hub management capabilities, we will use the **Numbers API** to list the phone numbers configured in the organization. This is a typical administrative task.

1. In the `WebexOne` collection you created in Getting Started, add a new `GET` request called `List Numbers`.
2. Set the URL to: `https://webexapis.com/v1/telephony/config/numbers`
3. Go to the **Headers** tab and add:
   * **Name**: `Authorization`
   * **Value**: `Bearer {{token}}` (this reads the token from your Bruno environment)
4. Click **Send**. You should get the phone numbers in the organization, each with its state and location.

Notice what you did not do: you did not paste the token into the request.
!!! Note
    When the token expires in 12 hours, you have to update the environment.

Now add a second request, and use a query parameter to keep the response small:

5. Duplicate the request, rename it `List Locations`, and set the URL to `https://webexapis.com/v1/telephony/config/locations`.
6. Open the **Params** tab and add a query parameter `max` with value `10`, then **Send**.

Finally, chain the two calls. Most troubleshooting work looks like this: one call gives you an ID, and the next call needs it.

7. From the locations response, copy the `id` of one location.
8. Add it to your environment as a variable called `locationId`.
9. Create one more request, `Get Location`, with the URL `https://webexapis.com/v1/telephony/config/locations/{{locationId}}`, and **Send**.

You now have the calling configuration of a single location: its announcement language, its calling line ID, its outbound dialing rules. Notice that this detail was not in the list response — you had to ask for it specifically, with an ID you obtained from an earlier call.

### Calling APIs using Python

Bruno is where you explore an API. Code is how you automate it once you know it works. To close this step, we will list the users in the organization from a Python script.

First, see where this snippet comes from:

1. Open the [List People](https://developer.webex.com/admin/docs/api/v1/people/list-people){:target="_blank"} reference in the Developer Portal.
2. In the code panel on the right, switch the language selector to **Python**. The portal generates a ready-to-run snippet for the endpoint you are reading about, with your own token filled in.

The version below is the same request, reading the token from `.env` instead of hardcoding it:

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("ACCESS_TOKEN")

url = "https://webexapis.com/v1/people"
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers, params={"max": 5})
print(response.json())
```

You should receive a JSON response containing a list of people in your organization.

## Step 2.4 - Webex APIs for Troubleshooting

From here on we work in Bruno, adding each call to your `WebexOne` collection so you can keep the requests and reuse the IDs they return.

Unless a call says otherwise, every request needs the same header:

| Header | Value |
| --- | --- |
| `Authorization` | `Bearer {{token}}` |

!!! Note
    The organization ID has already been set for you, both below and as `WEBEX_ORG_ID` in `.env`: `74983fd5-5c18-45cb-bfcd-507005e05b0f`.

    Add it to your Bruno environment as `orgId` so you can write `{{orgId}}` instead of pasting it.

### Webex Status API

Check platform health before deep-diving into org-specific issues.

Reference: [Webex Status API](https://developer.webex.com/calling/docs/webex-status-api){:target="_blank"}

This is the one exception to the rule above: the Status API is public, so these two requests need **no** `Authorization` header at all.

1. Create a `GET` request called `Webex Status` with the URL `https://status.webex.com/status.json` and **Send**.
2. Create a `GET` request called `Unresolved Incidents` with the URL `https://status.webex.com/unresolved-incidents.json` and **Send**.

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

Admin Audit Events will not accept a bare URL: `orgId`, `from`, and `to` are all mandatory.

1. Create a `GET` request called `Admin Audit Events` with the URL `https://webexapis.com/v1/adminAudit/events`.
2. In the **Params** tab, add:

    | Parameter | Value |
    | --- | --- |
    | `orgId` | `{{orgId}}` |
    | `from` | `2026-09-15T00:00:00.000Z` |
    | `to` | `2026-09-22T23:59:59.000Z` |
    | `max` | `10` |

3. **Send**, then expand one item in the response.

Look closely at where the useful values are: `actionText`, `actorEmail`, and `eventCategory` sit inside each item's `data` object, not at the top level. Remember this when you build the audit tool in Lab 3.

### Reports

Reports are not generated automatically. You create one from a template, then list it.

Org-level templates (`identifier` is `org`) need only `templateId`, `startDate`, and `endDate`. Meetings templates also need `siteList`. Lab accounts are Meetings site admins, so those work if you pass the site URL (`webexone-ai-assistant-sbx.webex.com`).

1. Create a `GET` request called `List Report Templates` with the URL `https://webexapis.com/v1/report/templates` and **Send**. Find *User Activity Summary* in the response and note its `Id` (`115`) and its `identifier` (`org`).
2. Create a `POST` request called `Create Report` with the URL `https://webexapis.com/v1/reports`. Open the **Body** tab, choose **JSON**, and paste:

    ```json
    {
      "templateId": 115,
      "startDate": "2026-09-10",
      "endDate": "2026-09-19"
    }
    ```

3. **Send**. The response returns the new report `Id`.
4. Create a `GET` request called `List Reports` with the URL `https://webexapis.com/v1/reports` and **Send**. Your report appears with a status of `waiting` at first, then `done` once Webex has generated it.

### Calling and meetings troubleshooting

| Scenario | API starting point |
| --- | --- |
| Call quality investigation | Detailed Call History, Meeting Qualities |
| Agent / queue issues | Calling Service Settings, Call Routing APIs |
| Meeting attendance / stats | Meetings, Meeting Participants |

A device that "does not work" is a good example of why one call is rarely enough.

1. Create a `GET` request called `List Devices` with the URL `https://webexapis.com/v1/devices` and **Send**.

If that comes back empty even though a phone exists in Control Hub, the phone has not registered to the cloud yet. Webex Calling devices assigned to a workspace are visible through the calling configuration instead:

2. Create a `GET` request called `List Workspaces` with the URL `https://webexapis.com/v1/workspaces`, add a `max` parameter of `5`, and **Send**. Copy the `id` of a workspace into your environment as `workspaceId`.
3. Create a `GET` request called `Get Workspace Devices` with the URL `https://webexapis.com/v1/telephony/config/workspaces/{{workspaceId}}/devices` and **Send**.

The response shows the device model and its `activationState`. A phone whose activation code has never been redeemed sits in `ACTIVATING`, which explains the empty list in step 1.

!!! Note "Detailed Call History needs more than an admin token"
    The CDR APIs require the dedicated `spark-admin:calling_cdr_read` scope, so they are not reachable with the Personal Access Token used in this lab. In production this is one of the cases where you would use a Service App with that scope explicitly granted.

Meeting Qualities has two constraints worth remembering, because both return a `404` that looks like a bad meeting ID. It lives on a **different host**, and it only accepts the ID of a meeting that already ended (the instance ID with `_I_` in the middle). So you list the ended meetings first:

4. Create a `GET` request called `List Ended Meetings` with the URL `https://webexapis.com/v1/meetings` and these parameters:

    | Parameter | Value |
    | --- | --- |
    | `meetingType` | `meeting` |
    | `state` | `ended` |
    | `max` | `5` |

5. **Send**, then copy the `id` of one meeting into your environment as `meetingId`.
6. Create a `GET` request called `Get Meeting Qualities` with the URL `https://analytics.webexapis.com/v1/meeting/qualities`, add a `meetingId` parameter of `{{meetingId}}`, and **Send**.

You get one entry per participant, with client type, operating system, network type, and join time. That is the data you would use to answer "why was that call bad?".

## Exercises

Build these in Bruno as new requests in your `WebexOne` collection. If you need help, you can check the solution.

1. List people, copy one `id` into your environment as `personId`, then get that person's details. Report the `displayName` and how many licenses they have.

    - [List People](https://developer.webex.com/admin/docs/api/v1/people/list-people){:target="_blank"}
    - [Get Person Details](https://developer.webex.com/admin/docs/api/v1/people/get-person-details){:target="_blank"}

    ??? Solution

        1. Create a `GET` request called `List People` with the URL `https://webexapis.com/v1/people`, add a `max` parameter of `5`, and **Send**. As an administrator you can call this with no filter, a regular user would have to pass `email` or `displayName`.
        2. From the `items` array, copy the `id` of one person into your environment as `personId`.
        3. Create a `GET` request called `Get Person Details` with the URL `https://webexapis.com/v1/people/{{personId}}` and **Send**.

        The list response does not include licenses. The single-person response does, in a `licenses` array. Its length is the answer.

2. List hunt groups, copy a hunt group's `id` and `locationId`, then get the details for that hunt group. Report the hunt group name and how many agents it has.

    - [Read the List of Hunt Groups](https://developer.webex.com/calling/docs/api/v1/features-hunt-group/read-the-list-of-hunt-groups){:target="_blank"}
    - [Get Details for a Hunt Group](https://developer.webex.com/calling/docs/api/v1/features-hunt-group/get-details-for-a-hunt-group){:target="_blank"}

    ??? Solution

        1. Create a `GET` request called `List Hunt Groups` with the URL `https://webexapis.com/v1/telephony/config/huntGroups`, add a `max` parameter of `10`, and **Send**.
        2. From the `huntGroups` array, copy the hunt group `id` and its `locationId` into your environment as `huntGroupId` and `locationId`. This chain needs two identifiers, because the detail endpoint is nested under the location.
        3. Create a `GET` request called `Get Hunt Group` with the URL `https://webexapis.com/v1/telephony/config/locations/{{locationId}}/huntGroups/{{huntGroupId}}` and **Send**.

        The response gives you the hunt group `name`, its number or extension, the `callPolicies` that decide how calls are distributed, and the `agents` array. The length of `agents` is the answer.

        If `huntGroups` is empty, the organization has no hunt group configured. Run the same chain against [call queues](https://developer.webex.com/calling/docs/api/v1/features-call-queue/read-the-list-of-call-queue-or-customer-assist-queues){:target="_blank"} instead, passing `hasCxEssentials=false`.

3. Reuse a `meetingId` from the ended-meetings request you already built, then list the participants of that meeting. Report how many people joined.

    - [List Meetings](https://developer.webex.com/meeting/docs/api/v1/meetings/list-meetings){:target="_blank"}
    - [List Meeting Participants](https://developer.webex.com/meeting/docs/api/v1/meeting-participants/list-meeting-participants){:target="_blank"}

    ??? Solution

        1. Send the `List Ended Meetings` request from Step 2.4 again, with `meetingType=meeting`, `state=ended`, and `max=5`. Copy the `id` of one meeting into your environment as `meetingId`.
        2. Create a `GET` request called `List Meeting Participants` with the URL `https://webexapis.com/v1/meetingParticipants`, add a `meetingId` parameter of `{{meetingId}}`, and **Send**.

        Each entry in `items` is one participant, with their `email`, `displayName`, whether they were the `host`, and their join and leave times. The number of entries is the answer.

        Like Meeting Qualities, this API only accepts a meeting that is in progress or already ended, so a scheduled meeting that never ran will fail here too.

## Step 2.5: From API calls to agent tools

In Bruno you did not answer a troubleshooting question with a single request. You listed locations, copied an `id`, and asked for that location's calling config. You listed ended meetings, then asked for qualities. You listed workspaces, then asked one of them for its devices.

That chain is the real work: one call produces the identifier the next call needs. You were the one concatenating them. Later in the lab, the agent will do that concatenation for you. You will ask a question in natural language, and the model will choose *list locations*, read the ID from the result, and call *get location* on its own. Same APIs, same order, no copy-paste.

That is only possible if the assistant can see those calls as **tools** rather than as URLs you have to type. An MCP server is not a new Webex product. It is the Webex APIs you just called, wrapped: a name, a short description, and an input schema, so the model can discover what exists and chain it.

### The knowledge behind every call

Look back at what you needed to know to complete this lab, none of which was the actual troubleshooting question:

- Which endpoint answers the question, out of hundreds in the portal
- Which parameters are mandatory, such as `orgId`, `from`, and `to` on audit events
- Where the useful values actually live, such as `actionText` nested under `data`
- That reports must be created before they can be listed, and which template IDs exist
- That Meeting Qualities is on a different host and only accepts an ended meeting instance ID

That knowledge is real. If you wanted an LLM to hit `webexapis.com` directly, you would have to teach it every URL, parameter, and quirk above, and re-teach it whenever the API changed. Wrapping each call as an MCP tool moves that knowledge into the tool description, which is why this chapter had to come first: you cannot wrap what you have not seen.

### The N × M problem

Now multiply that. Every AI application that needs Webex has to learn those details. Every other platform an AI application touches has the same kind of details. Wiring **N** applications to **M** systems by hand produces N × M pieces of fragile glue code, each maintained separately.

MCP turns that into **N + M**. Each system is exposed once as an MCP server, and every MCP-capable host speaks the same protocol to reach it.

### APIs vs MCP

| Choose Webex REST APIs when… | Choose Webex MCP when… |
| --- | --- |
| You need full control over every request | You want natural-language access from an AI client |
| Performance and custom business logic matter | You need the assistant to chain calls the way you just did in Bruno |
| You build enterprise apps with webhooks | You connect IDE or agent frameworks to Webex quickly |

These are not competing choices. MCP does not replace the APIs. The HTTP call still happens underneath, with the same token and the same JSON. MCP is how you give an agent **new capabilities** on top of APIs that already exist.

### Why you need your own server

The current official MCP servers explored before wrap messaging, meetings, and workspaces, and more, but they are user-oriented: they act on *a person's* meetings, messages, and rooms. There is no official server for Webex Calling or Control Hub troubleshooting, which is exactly the set of APIs you just called by hand, and that is the organization-level capability we are after.

In the next section will wrap them yourself: the same endpoints, the same token, now exposed as tools. The assistant will then concatenate them the way you concatenated them in Bruno, automatically.

