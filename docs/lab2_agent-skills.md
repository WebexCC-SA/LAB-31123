# Lab 2 - Agent Skills

In this section, you will use an **Agent Skill** to teach the assistant *how* to review Webex meetings thoroughly. This separates the operational expertise from the MCP tool connectivity, and you can run it directly inside **VS Code Chat (Agent mode)** without writing any code.

Skills aren't just fancy instructions, they're **portable, task-specific workflows** that load only when you need them. Unlike custom instructions that just define coding standards, skills bring scripts, examples, and automation into the mix to make agents truly **action-oriented**.

Instead of copying a file from the repository, you will create the skill yourself using the VS Code skills flow. VS Code will automatically save it to a supported location, ensuring the lab works regardless of which folder you have open.

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

A skill doesn't add new tools. Instead, it tells the assistant **how to use the tools it already has more effectively**—and what *not* to do.

## Skills vs Custom Instructions

If you already use `.github/copilot-instructions.md` or custom instructions in VS Code, you might be wondering how skills are different. They actually serve different purposes:

| Feature      | Custom Instructions                  | Agent Skills                                                                          |
| ------------ | ------------------------------------ | ------------------------------------------------------------------------------------- |
| **Purpose**  | Coding standards and guidelines      | Task-specific workflows and runbooks                                                  |
| **Scope**    | Always applied to every conversation | Loaded on demand when the task matches                                                |
| **Content**  | Instructions only                    | Instructions + scripts + examples + resources                                         |
| **Standard** | VS Code–specific                     | Open standard ([agentskills.io](https://agentskills.io)) — portable across 30+ agents |

## Step 2.1: Enable Agent Skills

!!! Note "Prerequisite: Webex Meeting MCP"
    This lab relies on the **Webex Meeting MCP server** you configured before.
    
    Before proceeding, make sure it is still present in your `mcp.json` file and running.

### Enable Agent Skills

Skills should be enabled already, but you can check it doing the following:

1. Open **Settings** (`Ctrl+,`) and search for `chat.useAgentSkills`:

    ![Skills](./assets/skill_1.png){ width="850" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

2. **Enable** the checkbox if it is not already enabled.
3. If you had to enable them, reload the window: `Ctrl+Shift+P` → `Developer: Reload Window`.

### Where skills live

VS Code automatically scans these project directories for skills ([VS Code docs](https://code.visualstudio.com/docs/agent-customization/agent-skills)):

| Location          | Convention                         |
| ----------------- | ---------------------------------- |
| `.agents/skills/` | agentskills.io cross-host standard |
| `.github/skills/` | GitHub convention                  |
| `.claude/skills/` | Anthropic convention               |

## Step 2.2: Create a skill

A skill is simply a folder containing a `SKILL.md` file, following an open standard defined by [agentskills.io](https://agentskills.io/home).

1. In the Chat view, type `/skills` and press Enter:

    ![skill_discovery](./assets/lab4/createskill1.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

2. Select **+ New Skill...**:

    ![skill_discovery](./assets/lab4/createskill2.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

3. And select the default option **~/.agents/skills (default) Workspace**:

    ![skill_discovery](./assets/lab4/createskill3.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

4. Name the new skill `meeting-review`:

    ![Skills](./assets/skill_2.png){ width="850" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}
        
5. This will create a new file for you:

    ![Skills](./assets/skill_3.png){ width="850" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

6. Replace the generated contents with the skill below:

    ??? Tip "SKILL.md"
        ````markdown
        ---
        name: meeting-review
        description: >-
          Use when the user asks to prepare for, get ready for, review readiness of, or
          check what is missing from their meetings. Triggers on phrases like 'help me
          prepare', 'am I ready for', 'what do I need before', 'review my meetings', or
          'check my schedule for gaps'. This tool evaluates upcoming meetings for agendas,
          invitees, and conflicts to produce a preparation checklist. Do NOT use this for
          plain requests to list meetings without a readiness or preparation context.
        argument-hint: "person or time range"
        ---
        
        # Meeting Review
        
        ## Tools
        
        Use the Webex Meeting MCP server only.
        
        | Need | Tool |
        |---|---|
        | Find upcoming meetings | `webex-list-meetings` |
        | Set agenda, title, time, or invitees | `webex-update-meeting` |
        
        If no Webex Meeting tool is available, output
        `WEBEX MEETING TOOLS NOT AVAILABLE` and stop. Do not answer from memory.
        
        ## Procedure
        
        1. Call `webex-list-meetings` with `state="scheduled"` and 
        `includeParticipants=true`. Pass `from`/`to` when the user gives a time range.
        If the user does not specify a time frame, default to checking meetings for
        the next 24 hours.
        2. Check all three dimensions for every meeting:
           - **Agenda** — is the `agenda` field non-empty? A meeting without one wastes
             its own first ten minutes, so this is the highest-value flag.
           - **Invitees** — is anyone listed besides the host?
           - **Conflicts** — compare each meeting's start and end against every other
             meeting in the result set. Flag both sides of any overlap.
        3. Report every check, including the ones that pass. A silent check reads as a
           skipped check.
        4. Produce the checklist using the template below.
        
        ## Output template
        
        ```text
        MEETING READINESS -- <person or time range>
        ======================================
        
        [Repeat the block below for each meeting]
        <title> | <day HH:MM> | <duration>
          Agenda:    <present / NO AGENDA>
          Invitees:  <N invited / NO INVITEES>
          Conflict:  <none / CONFLICT with "<other title>">
        [End repeat]
        
        PREPARATION CHECKLIST
        1. <most urgent concrete action>
        2. <next action>
        ======================================
        ```
        
        ## Gotchas & Constraints
        
        - **Creating Agendas:** The `webex-create-meeting` tool has no `agenda` parameter;
        newly scheduled meetings start with no agenda. If a user asks to schedule a meeting
        with an agenda, create the meeting first, then immediately call `webex-update-meeting`
        to set the agenda. Do not imply the agenda was set during creation.
        - **Missing Invitee Data:** `webex-list-meetings` only returns invitees when
        `includeParticipants=true`. If the invitee field is absent from the tool response,
        the data was not requested. Re-query the tool. Do NOT report `NO INVITEES` unless
        the field is explicitly present and empty.
        - **No Hallucination:** Report only what the tools return. Never infer an attendee
        list or agenda content from a meeting title.
        - **No Local Storage:** Never create, edit, or save a local file. This skill produces
        chat output only. Meeting data belongs in Webex, not on disk. If a tool cannot store
        a value the user asked for, report the limitation and stop.
         ````

    ??? "Explanation"

      TBC - Explanantion of the file section

8. **Save** the file.
9. **Reload the window**: `Ctrl+Shift+P` → `Developer: Reload Window`.

!!! Warning
    Reload after every edit to `SKILL.md` in this lab. You will edit the skill again in the Exercise, and the reload is what makes the change take effect before you re-run.

### Reading the front matter

Here are two important rules from the [agentskills.io specification](https://agentskills.io/specification):

- `name` must be lowercase letters, numbers, and hyphens, and **match the folder name**.
- `description` says what the skill does **and when to use it** — this is the only part the agent sees until the skill activates, so it is what decides whether the skill loads at all.

Notice how the description starts with phrases *you* would actually type (like "help me prepare" or "am I ready for") and ends with a specific exclusion. This is deliberate, and you'll see why in Step 2.6.

## Step 2.3: Verify discovery

Do **not** ask the agent "what skills are available?", a model without any skills loaded might just make up a plausible answer. Instead, check the observable state.

Type `/` in the chat input. `meeting-review` should appear in the list.

![skill_discovery](./assets/lab4/skill_discovery.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

!!! Note "If `meeting-review` does not appear"
    - Confirm `chat.useAgentSkills` is enabled (Step 2.1).
    - Confirm the `name` in the front matter is exactly `meeting-review` and matches the folder name.
    - Reload the window again (`Developer: Reload Window`).
    - If you created the file by hand instead of using `/skills`, it may be in a directory VS Code does not scan. Delete it and create it again with `/skills`.

## Step 2.4: Progressive disclosure

Agent Skills load in three stages, allowing many skills to be available without consuming too many resources:

1. **Discovery**: At startup, the agent loads only each skill's name and description (~100 tokens).
2. **Activation**: When the task matches the description, or when you type `/meeting-review`, it reads the full `SKILL.md` body.
3. **Execution**: It follows the procedure, and calling MCP tools as instructed.

!!! Warning "Important"
    The full instructions only load when needed. This is why the `description` field is so important: it's the only part the model sees when deciding whether to use the skill in a conversation.

## Step 2.5: Schedule meetings

Let's schedule two meetings so we have some data to review. Neither meeting will have an agenda because `webex-create-meeting` doesn't have an agenda parameter. This limitation is intentional for this exercise, as the skill will flag this missing information.

1. Schedule the first meeting:

- Ask: *"Schedule a meeting with admin@webexone-ai-assistant.wbx.ai tomorrow at 10am CET. Title: Planning Session."*

    ![Skills](./assets/skill_5.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

2. Schedule the second meeting:

- Ask: *"Schedule a meeting with admin@webexone-ai-assistant.wbx.ai tomorrow at 2pm CET. Title: Architecture Review."*

    ![Skills](./assets/skill_6.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

You now have two upcoming meetings, both without agendas.

## Step 2.6: With and without the skill

### A plain listing question

- Ask: *"What webex meetings do I have scheduled?"*

    ![Skills](./assets/skill_7.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

The agent will simply list them with their title, time, and host. There are no flags, no readiness checks, and no actions suggested.

The skill should **not** activate here, which is by design. The last line of its description specifically says it's "not for a plain list of meetings with no readiness question." 

You can expand **References** to confirm that `meeting-review` wasn't loaded.

![Skills](./assets/skill_8.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

### A readiness question

Now, try it  for the same data a different way:

- Ask: *"Help me prepare for my upcoming webex meetings."*

    ![Skills](./assets/skill_9.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

This phrasing matches the description, so a capable model loads the skill on its own. 

Expand **References** to check whether it did.

![Skills](./assets/skill_9.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

!!! Note "If the skill did not load"
    Automatic activation is a judgment call the model makes — it is not a rule VS Code enforces. Smaller models rarely load skills proactively, especially when a direct tool call would also answer the question. This is normal.

### Force it

```text
/meeting-review
Help me prepare for my upcoming webex meetings.
```

Typing `/meeting-review` loads the body directly. This is the **deterministic**
path: it always works, regardless of model.

### What you should see

```text
MEETING READINESS -- me
======================================

Planning Session | Tue 10:00 | 60 min
  Agenda:    NO AGENDA
  Invitees:  1 invited
  Conflict:  none

Architecture Review | Tue 14:00 | 60 min
  Agenda:    NO AGENDA
  Invitees:  1 invited
  Conflict:  none

PREPARATION CHECKLIST
1. Add an agenda to Planning Session before Tue 10:00.
2. Add an agenda to Architecture Review before Tue 14:00.
======================================
```

Note that the passing checks are reported too, not just the failures. A silent check is indistinguishable from a skipped one.

The difference between 2.6a and 2.6c is the skill's value: the same tools, the same data, but the skill added judgment.

```
WITHOUT skill              WITH skill
-------------              ----------
list meetings (done)       list meetings
                           + check agenda per meeting
                           + check invitees per meeting
                           + check conflicts pairwise
                           + report passes AND failures
                           + preparation checklist
plain listing              actionable preparation
```

!!! Tip "Try the conflict flag"
    Schedule a third meeting that overlaps one of the first two, then re-run.
    The skill flags `CONFLICT` on **both** sides of the overlap.

## Exercise: Skills as guardrails

A skill can tell the agent what to do, how to do it, and — just as importantly — what **not** to do. This exercise adds one new rule and watches behaviour change.

### Part A — Observe a problem

Ask the agent to fix the gaps it just reported:

- Ask: *"Fix the missing agendas on my upcoming webex meetings."*

Watch what it does. Most agents will **write agenda text they invented** and apply it immediately with `webex-update-meeting`, without showing you the text first. Your meetings are now updated with wording you never approved.

The tool call itself was correct. The problem is that a judgement call was made on your behalf, silently.

!!! Note
    A sufficiently cautious model may already ask before applying. If yours does, the contrast in Part C will be smaller — read Part B anyway, since the point is that the behaviour becomes *guaranteed* rather than *likely*.

### Part B — Add a guardrail to the skill

Open your `meeting-review` skill (`/skills` → select it → edit) and add this line to the **Gotchas** section:

![skill_discovery](./assets/lab4/editskill.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

```markdown
- Never write agenda text you invented. Draft the wording, show it to the user,
  and wait for explicit approval before calling `webex-update-meeting`.
```

Save the file, then **reload the window** (`Ctrl+Shift+P` → `Developer: Reload Window`).

### Part C — Re-run and compare

Ask exactly the same question again:

- Ask: *"Fix the missing agendas on my upcoming webex meetings."*

The agent now presents draft agenda text and **waits for your approval** before touching Webex. Approve it, and confirm the agenda is set.

You just changed agent behaviour with one line of markdown. No code.

### Part D — Optional: honest limitations

The skill's Gotchas already record that `webex-create-meeting` has no agenda parameter. Test it:

- Ask: *"Schedule a meeting tomorrow at 4pm titled Budget Review, with the agenda: review Q4 spend."*

The agent should tell you the agenda cannot be set at creation time and propose the `webex-update-meeting` follow-up — rather than quietly implying it was set. Without that gotcha, agents routinely paper over this kind of API gap.

!!! Tip "What you learned"
    Guardrails are not a separate feature. They are ordinary lines in `SKILL.md`. The most valuable ones come from mistakes you personally watched an agent make.

## How this skill follows the agentskills.io best practices

This skill is deliberately written to follow the published [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices).
Each practice maps to a concrete section of the file you pasted:

| Best practice                                    | Where you can see it in `SKILL.md`                                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| **Add what the agent lacks, omit what it knows** | No "what is a meeting" preamble, and no "list them chronologically" rule, because agents do that unprompted   |
| **Provide defaults, not menus**                  | The `## Tools` table gives exactly one tool per need — no "you could use X or Y"                              |
| **Favor procedures over declarations**           | `## Procedure` says *how* to detect a conflict (compare start/end pairwise), not merely that conflicts matter |
| **Match specificity to fragility**               | The agenda check explains *why* it matters; the guardrails are stated as absolutes                            |
| **Gotchas sections**                             | `## Gotchas` carries the `webex-create-meeting` agenda limitation and the `includeParticipants` trap          |
| **Templates for output format**                  | `## Output template` is a concrete block — agents pattern-match structures far better than prose              |
| **Aim for moderate detail**                      | Roughly 70 lines, well inside the 500-line / 5,000-token guidance                                             |
| **Design coherent units**                        | Upcoming-meeting readiness only. Past-meeting review is a separate skill (`meeting-review-full`, Lab 7)       |


Two of those practices are things you just *did*, not just read:

- **"If the agent already handles the task well without the skill, the skill may not be adding value."** Step 2.6a versus 2.6c is exactly that test. If your model produced a full readiness checklist in 2.6a without the skill, then the
  skill's remaining value is its guardrails rather than its checks — and that is a legitimate finding, not a failure.
- **"When an agent makes a mistake you have to correct, add the correction to the gotchas section."** That is precisely the loop you ran in the Exercise: observe the misbehaviour in Part A, encode the correction in Part B, verify in Part C. The best practices page calls this the most direct way to improve a skill.

The page also recommends **refining with real execution** — running a skill against real tasks and feeding the results back in. You have now done one pass.

## Next

In **Lab 7** you build the Python **skill loader** that reads a more advanced version of this skill — `meeting-review-full`, which also reviews past meetings for attendance, summaries, recordings, and transcripts. Same format, same standard, different host. See `07_skills_bot/` in the cloned repo.
