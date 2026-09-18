# Lab 7 - Skills in the AI Assistant

In **Lab 4** you dropped the `meeting-review` skill into VS Code Chat (Agent
mode) and it just worked — zero code. In this lab you build and **own the
mechanism**: a Python **skill loader** that reads the *same* `SKILL.md` file,
wire it into a bot, and then **onboard a second skill**.

Same skill file. Same format. You now control the loader.

All paths below are in the `WebexOne2026` repo you cloned in Getting Started.

### Setup

```bash
cd 07_skills_bot
pip install -r requirements.txt
cp .env.example .env    # then edit .env
```

!!! Note
    Scripts 01 and 02 need **no credentials**. Script 03 needs `OPENAI_API_KEY`.
    Script 04 (the full bot) needs `BOT_TOKEN`, `OPENAI_API_KEY`, and MCP tokens.

## Step 7.1: The SkillLoader class

Before running any script, read the shared foundation they all use.

Open `07_skills_bot/skill_loader.py`:

??? Tip "skill_loader.py"
    ```python
    import yaml
    from pathlib import Path

    class Skill:
        def __init__(self, name, description, instructions):
            self.name = name
            self.description = description
            self.instructions = instructions

    class SkillLoader:
        def __init__(self, skills_dir):
            self.skills_dir = Path(skills_dir)
            self.skills = {}
            self._load_skills()

        def _load_skills(self):
            for skill_path in self.skills_dir.rglob("SKILL.md"):
                parts = skill_path.read_text(encoding="utf-8").split("---", 2)
                if len(parts) >= 3:
                    metadata = yaml.safe_load(parts[1])
                    name = metadata.get("name", skill_path.parent.name)
                    description = metadata.get("description", "")
                    self.skills[name] = Skill(name, description, parts[2].strip())

        def get_skill(self, name):
            return self.skills.get(name)

        def get_all_skills_summary(self):
            return "\n".join(f"- {s.name}: {s.description}" for s in self.skills.values())
    ```

This class does three things:

1. **Discover** — scan a directory for `SKILL.md` files, parse YAML frontmatter
2. **Summarize** — `get_all_skills_summary()` returns one-line-per-skill for the system prompt
3. **Activate** — `get_skill(name).instructions` returns the full body on demand

Every script in this folder imports `SkillLoader` from this file. One class,
one parser, shared everywhere.

## Step 7.2: Discover skills

Run:

```bash
python 01_what_is_a_skill.py
```

This script creates a `SkillLoader`, points it at `skills/`, and prints every
discovered skill's `name` and `description`. You should see at least
`meeting-review` and `troubleshoot-address-books`.

This is the **Discovery** stage — what the agent learns at startup.

## Step 7.3: Progressive disclosure

Run:

```bash
python 02_progressive_disclosure.py
```

It shows the Discovery-stage summary (~100 tokens) alongside the full
Activation-stage body (~700+ tokens), and reports the size ratio.

```
Discovery summary:    ~91 tokens
Full body:           ~736 tokens
Full body is 8x larger.
```

With 10 skills, loading all bodies at startup costs ~7,300 tokens.
Progressive disclosure keeps it at ~900 tokens — loading the full body only
when the agent decides the skill is relevant.

## Step 7.4: The value — with and without

Run:

```bash
python 03_with_and_without_skill.py
```

This imports the Chapter 6 agent (`06_mcp_bot/llm.py` + `06_mcp_bot/mcp_client.py`),
asks the same question twice — skill off, then on — and prints both answers.

```
WITHOUT skill              WITH skill
-------------              ----------
list meetings (done)       list meetings
                           + participants + summary + recording + transcript
                           + triage + prioritized actions
1 scope, 1 call            5 scopes, many calls
```

If `WEBEX_MEETING_MCP_TOKEN` is not set, the example uses a canned dataset so the
A/B still runs.

**Key insight:** the skill uses `SkillLoader.get_skill("meeting-review").instructions`
to inject the runbook into the system prompt. Same class as scripts 01 and 02.

## Step 7.5: The full bot

Run:

```bash
python 04_bot_skills.py
```

This is the capstone: a Webex bot connected to multiple MCP servers (messaging +
meeting + custom), with the `SkillLoader` wired in. It:

1. Discovers skills on startup (`SkillLoader`)
2. Injects the skill summaries into the system prompt (`get_all_skills_summary()`)
3. Gives the LLM a `read_skill_runbook` tool that calls `get_skill(name).instructions`
4. The LLM decides when to load a skill — same progressive disclosure pattern

In Webex, ask your bot:

> *"Review the meetings for user1@webexone-ai-assistant.wbx.ai — check who
> joined, summaries, and recordings, and flag anything missing."*

The LLM sees `meeting-review` in the skill summary, calls `read_skill_runbook`,
reads the full runbook, then follows it.

## Step 7.6: Onboard a second skill

`07_skills_bot/skills/` already includes a second skill:

```text
skills/
    meeting-review/SKILL.md
    troubleshoot-address-books/SKILL.md   <- second skill
```

Restart the bot — it discovers both automatically (the loader scans the
directory). Ask a contact-center question:

> *"An agent says they can't see any contacts in their address book on the
> desktop. Can you investigate?"*

The LLM loads `troubleshoot-address-books` and follows its cross-server runbook.

!!! Note "Prerequisite for troubleshoot-address-books"
    This skill orchestrates the capstone **address-book** and
    **desktop-profile** MCP servers plus the local `check_webex_status`
    tool. Those servers must be connected for the skill to execute its steps.

Adding a skill is just adding a folder — no code change. The loader discovers it.

## Step 7.7: What you built

| # | Script | Concept | SkillLoader method |
| --- | --- | --- | --- |
| — | `skill_loader.py` | The shared class | `__init__`, `_load_skills` |
| 01 | `01_what_is_a_skill.py` | Discovery | `SkillLoader(dir).skills` |
| 02 | `02_progressive_disclosure.py` | 3 stages | `get_all_skills_summary()` + `get_skill().instructions` |
| 03 | `03_with_and_without_skill.py` | Value A/B | `get_skill().instructions` → system prompt |
| 04 | `04_bot_skills.py` | Bot integration | `get_all_skills_summary()` + `read_skill_runbook` tool |

The skill file never changed between Lab 4 and Lab 7. Only the host did:
VS Code Chat there, your Python loader + bot here. **Write the skill once,
run it anywhere.**
