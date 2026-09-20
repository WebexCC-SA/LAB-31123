# Lab 4 - Agent Skills

In this section, you will use an **Agent Skill** to encode operational expertise —
*how* to review Webex meetings thoroughly — separately from MCP tool connectivity,
and run it directly inside **VS Code Chat (Agent mode)** with no code.

Skills aren't just fancy instructions — they're **portable, task-specific
workflows** that load only when you need them. Unlike custom instructions, which
define coding standards, skills bring scripts, examples, and automation into the
mix, making agents truly **action-oriented**.

You cloned `WebexOne2026` in Getting Started. For this focused skill test,
open the `.agents` folder as the VS Code workspace. This keeps the repository's
Python code out of the agent's active context so it does not distract from the
skill workflow.

## Skills vs MCP


| Layer            | Responsibility                                    | Example                                                                                   |
| ---------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **MCP server**   | What the assistant *can do* — governed API access | Webex Meeting tools (list meetings, participants, summaries, recordings)                  |
| **Agent Skills** | *How* to use those tools — runbooks and judgment  | "For every meeting, also check participants, summary, recording, transcript, then triage" |


```mermaid
flowchart TB
    Skills[Agent Skill - HOW]
    MCP[Webex Meeting MCP - WHAT]
    Client[VS Code Chat - Agent mode]
    Skills --> Client
    MCP --> Client
    Client --> Webex[Webex Meeting APIs]
```



A skill does not add tools. It tells the assistant to **use the tools it already
has, more thoroughly**.

## Skills vs Custom Instructions

If you already use `.github/copilot-instructions.md` or custom instructions in
VS Code, you may wonder how skills differ. They serve different purposes:


| Feature      | Custom Instructions                  | Agent Skills                                                                          |
| ------------ | ------------------------------------ | ------------------------------------------------------------------------------------- |
| **Purpose**  | Coding standards and guidelines      | Task-specific workflows and runbooks                                                  |
| **Scope**    | Always applied to every conversation | Loaded on demand when the task matches                                                |
| **Content**  | Instructions only                    | Instructions + scripts + examples + resources                                         |
| **Standard** | VS Code–specific                     | Open standard ([agentskills.io](https://agentskills.io)) — portable across 30+ agents |


Use custom instructions for *"always format imports this way."*
Use skills for *"when reviewing meetings, check all five dimensions and triage."*

## Step 4.1: Isolate the skill workspace, configure MCP, and enable Agent Skills

Open `WebexOne2026/.agents/` in VS Code, not the full `WebexOne2026/`
repository. The full repository contains many Python files and bot
implementations useful for Lab 7, but unrelated code can mislead the agent
during this focused skill test.

Because `.vscode/mcp.json` is outside this focused workspace, configure the
Webex Meeting MCP at **user scope**:

1. Open the Command Palette.
2. Run **MCP: Open User Configuration**.
3. Add the Webex Meeting MCP using your lab token.
4. Start the server or reload VS Code.

Never commit a real token to the repository.

Before looking at the skill itself, make sure VS Code can discover it.

1. Open **Settings** (`Ctrl+,`) and search for `chat.useAgentSkills`.
2. **Enable** the checkbox.
  !!! Warning
        This setting must be enabled or skills will not load. If you skip this step,
        nothing else in this lab will work.
3. Reload the window: `Ctrl+Shift+P` → `Developer: Reload Window`.
4. Open **Chat** (`Ctrl+Shift+P` → `Chat: Open Chat (Agent)`).
5. **Verify discovery** — ask the agent:
  ```text
    What skills are available?
  ```

    The agent should list `meeting-review` with its description. If it does,
    skills are working and you can proceed.
    !!! Note
        If `meeting-review` does not appear:
  ```
    - Confirm `chat.useAgentSkills` is enabled (step 2)
    - Confirm the skill exists in the cloned repo at
      `.agents/skills/meeting-review/SKILL.md` (it appears as
      `skills/meeting-review/SKILL.md` from the focused `.agents` workspace)
    - Reload the window again (`Developer: Reload Window`)
  ```

VS Code automatically scans these project directories for skills
([VS Code docs](https://code.visualstudio.com/docs/agent-customization/agent-skills)):


| Location          | Convention                         |
| ----------------- | ---------------------------------- |
| `.agents/skills/` | agentskills.io cross-host standard |
| `.github/skills/` | GitHub convention                  |
| `.claude/skills/` | Anthropic convention               |


The cloned repo places the skill in `.agents/skills/` — the most portable
option. **No settings file is needed** for auto-discovery.

### Other prerequisites


| Requirement                 | How to set up                                                            |
| --------------------------- | ------------------------------------------------------------------------ |
| VS Code **>= 1.108**        | `Help > About`                                                           |
| OpenAI model configured     | Lab 1 Step 1.2 — `Chat: Manage Language Models` → OpenAI → enter API key |
| Webex Meeting MCP connected | Lab 1 — configure the server in the user MCP configuration |




## Step 4.2: Skill anatomy

A skill is a folder containing a `SKILL.md` file — an open standard defined by
[agentskills.io](https://agentskills.io/home).

In the cloned repository, the skill is at:

```text
.agents/skills/meeting-review/SKILL.md
```

Because the focused VS Code workspace is `.agents/`, the same file appears
inside that workspace as:

```text
skills/meeting-review/SKILL.md
```

Open it and look at the front matter:

```yaml
---
name: meeting-review
description: >-
  Use when a user asks to review or prepare for upcoming meetings.
  Check each meeting for agenda, invitees, and scheduling conflicts.
  Flag anything missing and produce a preparation checklist.
---
```

Two rules from the [agentskills.io specification](https://agentskills.io/specification):

- `name` must be lowercase letters, numbers, and hyphens, and **match the folder name**.
- `description` says what the skill does **and when to use it** — this is what the
  agent reads to decide whether to load the skill.

The body below the front matter is the runbook: check each upcoming meeting for
agenda, invitees, and conflicts; produce a preparation checklist.

## Step 4.3: Progressive disclosure

Agent Skills load in three stages so many skills can be available cheaply:

1. **Discovery** — at startup, the agent loads only each skill's name and
  description (~100 tokens).
2. **Activation** — when a task matches, it reads the full `SKILL.md` body.
3. **Execution** — it follows the steps, calling MCP tools as instructed.

Full instructions load only when needed.

## Step 4.4: Create meeting data

Before testing the skill, create two meetings so there is data to review.
One meeting will have an agenda; the other will not.

1. Open **Chat** (`Ctrl+Shift+P` → `Chat: Open Chat (Agent)`).
2. Ensure the **Webex Meeting MCP** is started.
3. Schedule the first meeting (with an agenda):

```text
Schedule a meeting with admin@webexone-ai-assistant.wbx.ai for tomorrow
at 10am. Title: "Planning Session". Agenda: review project milestones
and assign action items.
```

4. Schedule the second meeting (without an agenda):

```text
Schedule a meeting with admin@webexone-ai-assistant.wbx.ai for tomorrow
at 2pm. Title: "Architecture Review".
```

You now have two upcoming meetings — one with an agenda, one without. The
skill will flag the difference.

## Step 4.5: Run the skill

1. Invoke the skill explicitly:

```text
/meeting-review
```

Then ask:

```text
Help me prepare for my upcoming meetings. Check if agendas are set
and flag anything I should prepare.
```

Expected behavior:

- The agent activates `meeting-review`.
- It checks each upcoming meeting for agenda, invitees, and conflicts.
- It flags `NO AGENDA` on the Architecture Review.
- It produces a preparation checklist.

```text
UPCOMING — Planning Session | tomorrow 10:00
  Agenda: review project milestones and assign action items
  --> Ready.

UPCOMING — Architecture Review | tomorrow 14:00
  Agenda: NO AGENDA
  --> Add an agenda before the meeting.

PREPARATION CHECKLIST
1. Add an agenda to Architecture Review.
```

## Step 4.6: See the difference

To feel the value, compare:

- **Without the skill** (temporarily rename the `.agents/skills/meeting-review/`
  folder and reload): the agent lists meetings and stops — title, time, done.
- **With the skill**: the agent checks agenda readiness for each meeting and
  produces a preparation checklist with concrete actions.

```
WITHOUT skill              WITH skill
-------------              ----------
list meetings (done)       list meetings
                           + check agenda per meeting
                           + flag NO AGENDA
                           + preparation checklist
plain listing              actionable preparation
```

Same tools, same data — the skill supplies the judgment.

## Exercise

1. **Fix it** — add an agenda to the Architecture Review meeting:

    ```text
    Update the Architecture Review meeting. Add this agenda:
    review API design, security model, and deployment plan.
    ```

2. **Re-run the skill** — invoke `/meeting-review` again and confirm the
   `NO AGENDA` flag is gone. The skill now shows both meetings as ready.

3. **Edit the skill** — open `.agents/skills/meeting-review/SKILL.md` and add
   one rule (for example: "flag any meeting with only one invitee as
   *needs more participants*"). Save the file.

4. **Re-run** the scenario in Chat and confirm your new rule is applied — no
   code change required, just the edited `SKILL.md`.

## Next

In **Lab 7** you build the Python **skill loader** that reads a more advanced
version of this skill — one that also reviews past meetings for attendance,
summaries, recordings, and transcripts. See `07_skills_bot/` in the cloned repo.