# Lab 4 - Webex APIs for Troubleshooting

In this section, you will explore Webex REST APIs commonly used to manage and troubleshoot an organization — status, audit, compliance, reports, calling, and meetings.

## Learning Objectives

Upon completion of this section, you will be able to:

- Query the Webex Status API for service health
- Review admin audit and compliance events
- Generate and retrieve operational reports
- Identify APIs useful for call history and meeting statistics

## Step 4.1: Webex Status API

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

## Step 4.2: Audit and compliance

| API area | Use case |
| --- | --- |
| Admin Audit Events | Track configuration changes and admin actions |
| Compliance Events | Monitor messaging and room events as compliance officer |
| Security Audit Events | Review security-related admin activity |

Placeholder request (update path and scopes for lab tenant):

```bash
curl -s -H "Authorization: Bearer $WEBEX_ACCESS_TOKEN" \
  "https://webexapis.com/v1/adminAudit/events?max=10" | python -m json.tool
```

## Step 4.3: Reports

Generate usage and activity reports for analysis:

```bash
curl -s -X POST -H "Authorization: Bearer $WEBEX_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reportTemplateId": "REPLACE_WITH_TEMPLATE_ID"}' \
  https://webexapis.com/v1/reports | python -m json.tool
```

!!! Note
    Report templates and scopes vary by license. Your lab instructor will provide the template IDs available in the lab org.

## Step 4.4: Calling and meetings troubleshooting

| Scenario | API starting point |
| --- | --- |
| Call quality investigation | Detailed Call History, Meeting Qualities |
| Agent / queue issues | Calling Service Settings, Call Routing APIs |
| Meeting attendance / stats | Meetings, Meeting Participants |

Example placeholder — list recent call history:

```python
import os
import requests

TOKEN = os.getenv("WEBEX_ACCESS_TOKEN")
response = requests.get(
    "https://webexapis.com/v1/callHistory",
    headers={"Authorization": f"Bearer {TOKEN}"},
    params={"max": 5},
    timeout=30,
)
response.raise_for_status()
print(response.json())
```

## Step 4.5: Troubleshooting guide

Review the official guide for diagnostic workflows:

- [Webex API Troubleshooting Guide](https://developer.webex.com/explore/docs/api/guides/troubleshooting){:target="_blank"}

Suggested lab activities (from session deck):

1. Check general Webex Status
2. Review admin audit events
3. Create a report and download it
4. Review compliance events
5. Retrieve call history and meeting statistics

## Exercise

Pick one operational scenario (e.g., "agents offline" or "address book sync failure") and list which APIs you would call first and why.

## Content still to define

- Lab-specific report template IDs
- Service App or integration token with admin scopes
- Sample audit event payloads for the exercise
