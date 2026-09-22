# Lab 2 - Webex APIs

In the previous section, we enabled our agent to use MCP servers to perform actions on our behalf. The assistant called Webex for you through the official MCP servers, and each of those servers is just a wrapper around Webex API calls.

In this section you will make those API calls yourself. This matters because the official MCP servers cover only a limited set of APIs, and we want to give our agent more tools and possibilities. That is what we will build in the next labs.


## Step 2.1 - Get a Personal Access Token

During the previous lab, you used an **Agentic MCP App token** to perform actions. That is a special token, scoped to execute actions through the MCP servers, and it only works with the official Webex MCP servers. It will not work for the direct API calls in this lab.

For the simplicity of this hands-on lab, we will use your Personal Access Token (PAT) instead. Because you are an administrator in this sandbox, your PAT automatically inherits all your admin rights. It requires no scope configuration and lasts for 12 hours, which is perfect for a workshop.

1. In [Webex for Developers](https://developer.webex.com/){:target="_blank"}, in the top right corner, click your avatar and select **Copy Developer Token**.
2. Open the `.env` file at the root of your project (you copied it from `.env.example` in Getting Started) and paste the token:

    ```env
    ACCESS_TOKEN=your_copied_token_here
    ```

3. Paste the same token into the `token` variable of your Bruno environment, so your requests can use `Bearer {{token}}`.

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

### The Catch: User Context vs. Machine Context

A Service App token is still a standard Webex OAuth 2.0 Bearer token, so you can pass it to an MCP server the same way you passed a PAT. However, the APIs do not behave the same:

1. **Personal Access Token (User Context):**
   When you used your token with the `webex-list-meetings` MCP tool, the Webex API knew *who* was asking. It fetched *your* meetings.

2. **Service App Token (Machine Context):**
   A Service App is a faceless machine. If it calls `webex-list-meetings` without specifying a user, the API will likely return an empty list because the machine itself does not have a calendar.

!!! Note "Architectural Gotcha: Analytics and Reports"
    Service Apps work for most administrative tasks. Webex Analytics and Reporting APIs require **user context** — they block Service Apps by design.

    If a production AI assistant needs to pull analytics or reports, it cannot use a Service App. It uses an **OAuth Integration**: the bot sends the user a "Log In" button, the human admin logs in, and the bot receives a user-bound token.

### The Approval Process

Because a Service App operates at machine level and can access organization-wide data, a Webex administrator must review the requested scopes and authorize the app in Control Hub before it can generate tokens.

For this lab we skip that process. Everything from here on uses your Personal Access Token.

??? Note "Reference: How to Create a Service App"
    If you ever need a Service App in production, here is how you do it:

    1. Log into [developer.webex.com](https://developer.webex.com/){:target="_blank"}.
    2. In the top right corner of the page, click your avatar and then select [My Webex Apps](https://developer.webex.com/my-apps){:target="_blank"}.
    3. Click **Create a New App**.
    4. On the ‘Create a New App’ page, find the Service App card and click the ‘Create a Service App’ button.

        ![Service App](./assets/bot_1.png){ width="850" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;" }

    5. Enter the necessary information (Name, Icon, Description, Contact Email).
    6. Select the **Scopes** your machine needs. For example, to read phone numbers, you would need `spark-admin:telephony_config_read`.

        ![Service App](./assets/serviceapp_1.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    7. Once created, you will get a **Client ID** and **Client Secret**.

        ![Service App](./assets/serviceapp_2.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    8. At the top, in the `Admin Authorization` section, click on **Request admin authorization**.

        ![Service App](./assets/serviceapp_3.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    9. A Webex Administrator must then go to **Collaboration Control Hub** -> **Apps** -> **Service Apps**, select your app, and click **Authorize**.

        ![Service App](./assets/serviceapp_4.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    10. Finally, you return to the Developer Portal, select your Org under **Org Authorizations**, enter your Client Secret, and click **Generate tokens** to get your 14-day `access_token` and 90-day `refresh_token`.

        ![Service App](./assets/serviceapp_5.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}
        ![Service App](./assets/serviceapp_6.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    **How to Refresh a Service App Token**

    Unlike a Personal Access Token which simply expires, a Service App token can be refreshed programmatically using the `refresh_token`.

    You can refresh your **access_token** by making a POST request to the Webex API as shown in the following python example:

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

Now that we have our token, we can start making API calls. The [Webex Developer Portal](https://developer.webex.com/docs/api/v1/){:target="_blank"} provides documentation and ready-to-use code snippets for all APIs. You can select your preferred language (cURL, Python, Node.js, etc.) and copy the code directly.

To demonstrate Control Hub management capabilities, we will use the **Numbers API** to list the phone numbers configured in the organization. This is a typical administrative task.

### Calling APIs using Bruno

1. In the `WebexOne` collection you created in Getting Started, add a new `GET` request.
2. Set the URL to: `https://webexapis.com/v1/telephony/config/numbers`
3. Go to the **Headers** tab and add:
   * **Name**: `Authorization`
   * **Value**: `Bearer {{token}}` (this reads the token from your Bruno environment)
4. Click **Send**.

### Calling APIs using cURL

You can find the equivalent cURL command directly in the Developer Portal. It looks like this:

```bash
curl -s -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://webexapis.com/v1/telephony/config/numbers" | python -m json.tool
```

### Calling APIs using Python

Similarly, the portal provides Python snippets using the `requests` library. You can run this in a simple script:

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("ACCESS_TOKEN")

url = "https://webexapis.com/v1/telephony/config/numbers"
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)
print(response.json())
```

You should receive a JSON response containing a list of phone numbers in your organization, proving you are successfully authenticating and retrieving organizational data.

## Step 2.4 - Webex APIs for Troubleshooting

You now have a token with **admin** scopes. Use the `ACCESS_TOKEN` in Bruno for the calls below. The Webex Status API is public and does not need a token.

!!! Note
    The organization ID has already been set for you, both below and as `WEBEX_ORG_ID` in `.env`: `74983fd5-5c18-45cb-bfcd-507005e05b0f`.

### Webex Status API

Check platform health before deep-diving into org-specific issues.

Reference: [Webex Status API](https://developer.webex.com/calling/docs/webex-status-api){:target="_blank"}

```bash
curl -s https://status.webex.com/status.json | python -m json.tool
curl -s https://status.webex.com/unresolved-incidents.json | python -m json.tool
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

Admin Audit Events require `orgId`, `from`, and `to`. The interesting fields (`actionText`, `actorEmail`, `eventCategory`) sit under each item's `data` object, not at the top level.

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  --get "https://webexapis.com/v1/adminAudit/events" \
  --data-urlencode "orgId=74983fd5-5c18-45cb-bfcd-507005e05b0f" \
  --data-urlencode "from=2026-09-15T00:00:00.000Z" \
  --data-urlencode "to=2026-09-22T23:59:59.000Z" \
  --data-urlencode "max=10" | python -m json.tool
```

### Reports

Reports are not generated automatically. You create one from a template, then list it.

Org-level templates (`identifier` is `org`) need only `templateId`, `startDate`, and `endDate`. Meetings templates also need `siteList`. Lab accounts are Meetings site admins, so those work if you pass the site URL (`webexone-ai-assistant-sbx.webex.com`).

List templates:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://webexapis.com/v1/report/templates" | python -m json.tool
```

Create an org-level report (template `115` is *User Activity Summary*):

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"templateId": 115, "startDate": "2026-09-10", "endDate": "2026-09-19"}' \
  https://webexapis.com/v1/reports | python -m json.tool
```

List generated reports:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://webexapis.com/v1/reports" | python -m json.tool
```

### Calling and meetings troubleshooting

| Scenario | API starting point |
| --- | --- |
| Call quality investigation | Detailed Call History, Meeting Qualities |
| Agent / queue issues | Calling Service Settings, Call Routing APIs |
| Meeting attendance / stats | Meetings, Meeting Participants |

Location calling config:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://webexapis.com/v1/telephony/config/locations" | python -m json.tool
```

Meeting Qualities lives on a **different host** and only accepts the ID of a meeting that already ended (the instance ID with `_I_` in the middle). List ended meetings first, then ask for qualities:

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  --get "https://webexapis.com/v1/meetings" \
  --data-urlencode "meetingType=meeting" \
  --data-urlencode "state=ended" \
  --data-urlencode "max=5" | python -m json.tool

curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  --get "https://analytics.webexapis.com/v1/meeting/qualities" \
  --data-urlencode "meetingId=ENDED_MEETING_ID" | python -m json.tool
```

`GET https://webexapis.com/v1/devices` only returns devices that have registered to the cloud. A phone still in `ACTIVATING` state will not appear there.

## Exercises

Run these in Bruno or cURL, using your `ACCESS_TOKEN`:

1. Check general Webex status, including unresolved incidents (no token needed).
2. Review the admin audit events for the last few days, and find an `actionText` value under `data` rather than at the top level of the item.
3. Create a report from an org-level template, then list reports until its status is `done`.
4. List ended meetings, then pull meeting qualities for one of them. Remember the different host.
5. List locations and read the calling configuration of the first one.

## Step 2.5: Why MCP matters, not just APIs

You have now used both routes to the same organization data: in Lab 1 you asked an assistant in natural language, and in this lab you made the calls yourself. It is worth stopping on why the second route is hard to hand to an AI assistant directly.

### What the raw APIs asked of you

Look back at what you needed to know to complete Step 2.4, none of which was about troubleshooting:

- Which endpoint answers the question, out of hundreds in the portal
- Which parameters are mandatory, such as `orgId`, `from`, and `to` on audit events
- Where the useful values actually live, such as `actionText` nested under `data`
- That reports must be created before they can be listed, and which template IDs exist
- That Meeting Qualities is on a different host and only accepts an ended meeting instance ID

That knowledge is real, and it is exactly what an assistant does not have. If you wanted an LLM to make these calls directly, you would have to teach it every URL, parameter, and quirk above, and re-teach it whenever the API changed.

### The N × M problem

Now multiply that. Every AI application that needs Webex has to learn those details. Every other platform an AI application touches has the same kind of details. Wiring **N** applications to **M** systems by hand produces N × M pieces of fragile glue code, each maintained separately.

MCP turns that into **N + M**. Each system is exposed once, through a standard interface, and any MCP-capable host can use it. A tool in MCP carries its own name, description, and input schema, so the model can discover what exists and how to call it instead of being told in advance.

That is the real difference: with a REST API, *you* decide which call to make and when. With MCP, you describe capabilities once and let the model choose. The API call still happens underneath, which is why understanding the APIs in this lab was the prerequisite.

### When to use which

| Choose Webex REST APIs when… | Choose Webex MCP when… |
| --- | --- |
| You need full control over every request | You want natural-language access from an AI client |
| Performance and custom business logic matter | You need rapid prototyping across MCP-compatible tools |
| You build enterprise apps with webhooks | You connect IDE or agent frameworks to Webex quickly |

These are not competing choices. MCP does not replace the APIs, it packages them for a model to use.

### Where this leaves us

The official MCP servers from Lab 1 cover messaging, meetings, workspaces, and more, but there is no official server for Webex Calling or Control Hub troubleshooting, which is exactly the set of APIs you just called by hand.

So in Lab 3 you will wrap them yourself: the same endpoints, the same token, now exposed as tools with descriptions and schemas that an assistant can discover and chain on its own.

