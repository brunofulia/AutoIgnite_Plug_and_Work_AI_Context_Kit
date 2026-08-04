---
title: "AGENTS.md"
description: "Universal entry point for the AutoIgnite · Plug & Work AI Context Kit. Defines core_path and all rituals."
type: "entry-point"
version: "1.0"
updated: ""
---

# AGENTS.md

> This file is the kit's entry point. It is not edited between projects —
> everything specific to a project lives in `core/`.
> Path configuration is delegated to the local `autoignite.ini` file.

---

## §0 — Configuration

> System paths (`core_path` and `target_path`) are read locally from the `autoignite.ini` file. If the file does not exist, the agent assumes `./` for both.

### Initial Setup
Before starting any task, verify:
- Does `PROJECT.md` have unfilled `[COMPLETE]` fields? → execute §5 (role and project ritual)
- Is the variable part of `ROLE.md` empty? → execute §5
- Does `HIERARCHY.md` list no real project documents? → execute §5

If all three are complete, continue with §1.

---

## §1 — Start Ritual

<CRITICAL_RULE>
**SYSTEM BARRIER - IMMEDIATE MANDATORY EXECUTION**
In your very first interaction of a new conversation, you are FORBIDDEN to use editing tools, read other files, or attempt to solve the user's request.
Your ONLY permitted action is to invoke a terminal tool to execute:
`python core_scripts/start_session.py`

If the user gave you a direct instruction in their first message, PUT IT ON HOLD. Execute the script first, wait for the result, read the base documents, and only then address the initial request. Ignoring this barrier is a critical failure of your system.
</CRITICAL_RULE>

Determine the scenario based on the script's output:

### Scenario A — Normal Start
*Condition: `SESSION_SCRATCH.md` does not exist in `core/`.*

1. Read `PROJECT.md`
2. Read `ROLE.md`
3. Read `HIERARCHY.md`
4. Read `CURRENT_STATE.md`
5. Read the "Open" section of `IMPROVEMENT_LOG.md`
6. Create `SESSION_SCRATCH.md` with session header (date + declared objective)
7. **Initial Interaction and Session Objective:** When giving your first response, evaluate the user's first message:
   - **If the user asked for a specific task:** Immediately update the "Declared objective" line in `SESSION_SCRATCH.md` to reflect that task, confirm to the user what you read, and start working.
   - **If the user only said hello or gave an unclear instruction:** List the documents you read, indicate the priority step according to `CURRENT_STATE.md`, and **explicitly ask** if they want to declare a different objective for the session.

### Scenario B — Resumption of Paused Session
*Condition: `SESSION_SCRATCH.md` exists and contains the `[PAUSE]` mark.*

1. Read base files (PROJECT → ROLE → HIERARCHY → CURRENT_STATE → IMPROVEMENT_LOG "Open")
2. Read `SESSION_SCRATCH.md`
3. Summarize for the user where the work left off and what the next step was

### Scenario C — Abrupt Cut Recovery
*Condition: `SESSION_SCRATCH.md` exists without a close or pause mark.*

1. Read base files
2. Read `SESSION_SCRATCH.md`
3. Reconstruct what happened during the interrupted session
4. Present the reconstruction to the user: "This is what I found — is it correct?"
5. **Only with explicit user confirmation:** consolidate into `LOG.md` and `CURRENT_STATE.md`, delete `SESSION_SCRATCH.md`, create a new one
6. Without confirmation: do not consolidate anything, ask how to proceed

> **Note:** the mere presence of `SESSION_SCRATCH.md` upon starting is the signal of an
> unclosed session. No additional marker is needed to detect it.

---

## §2 — Consistency Ritual

Execute **before editing any project document** and also
**on demand as a comprehensive check** when requested by the user.

1. Identify the position of the document to edit in `HIERARCHY.md`
2. Reread all documents with higher authority (upstream)
3. Verify that the proposed edit does not contradict any of them
4. If there is a discrepancy: point it out explicitly to the user and wait for instruction
   — **never resolve a discrepancy silently**
5. Only with confirmation: proceed with the edit

> For a comprehensive project check: go through all documents listed
> in `HIERARCHY.md` and verify mutual consistency between pairs. Report
> any contradiction found before proposing corrections.

---

## §3 — Close Ritual

Execute at the end of each session, before the user closes the conversation, or proactively as a "Checkpoint".

### Proactive Checkpoint
To protect the context window and consolidate memory, the agent MUST proactively propose performing the Close Ritual if it notices that **any** of these conditions are met:
1. The main objective declared at the start of the session was completed.
2. `SESSION_SCRATCH.md` has recorded more than 4 important milestones.
3. More than 2 hours have passed since the first record in `SESSION_SCRATCH.md` (calculated using the timestamps of each entry).
*(Note: If in the future a script automates these validations and issues a warning, the agent must obey that warning immediately).*

**How to act:** Early execution of the closure is always a **proposal**. The agent must ask the user if they want to execute the ritual to consolidate memory before continuing with the next task.

### Closure Execution Flow
1. Read `SESSION_SCRATCH.md` completely
2. Update `CURRENT_STATE.md` — it should remain short (guideline: maximum 1 page)
3. Add entry to `LOG.md` with the structure of `templates/log_entry.md`
4. If there were errors or lessons learned: add entry to `IMPROVEMENT_LOG.md`
5. If any document became outdated: add file banner at the beginning
6. Invoke `python core_scripts/generate_index.py --recursive` on the affected folders
7. Invoke `python core_scripts/generate_tree.py`
8. **Delete `SESSION_SCRATCH.md`** — this step is mandatory so that the
   next start is Scenario A

> If the user needs to pause without formally closing, add `[PAUSE]`
> at the end of `SESSION_SCRATCH.md` instead of deleting it → next start will be Scenario B.

---

## §4 — Triage Ritual

Invoked **only when the user requests it** to process material in `core_input/`.
`core_input/` is never read automatically.

1. Read the material indicated by the user in `core_input/`
2. Identify ambiguities before proposing anything — clarify with the user
3. Propose where the information fits:
   - Does it describe the project? → `PROJECT.md` (use `templates/project_update.md`)
   - Is it a document with authority over the project? → `HIERARCHY.md` (use `templates/hierarchy_entry.md`)
   - Is it an event or decision to log? → `LOG.md` (use `templates/log_entry.md`)
   - Is it an external read-only input? → log in `HIERARCHY.md` § Inputs
4. Wait for explicit user approval
5. With approval: edit the destination document using the corresponding template
6. Log the action in `SESSION_SCRATCH.md`
7. **Cleanup (Mandatory):** The agent MOVES the processed physical file from `core_input/` to `core_reference/` (if it is a read-only input) or to `core_archive/` (if it was discarded or its text integrated into the project).
8. Invoke `python core_scripts/generate_index.py --recursive`

---

## §5 — Creation / Update Ritual for role and project

Invoked when instantiating the kit for the first time, or when the task type
or project context changes during an ongoing project.

### Part A — Project (if PROJECT.md or HIERARCHY.md are empty or have [COMPLETE])

Ask the minimum necessary questions, one at a time:
1. What is this project in one or two sentences?
2. What is the expected deliverable or result?
3. Is there a client or external stakeholder involved?
4. Are there non-negotiable constraints (language, deadlines, mandatory conventions)?
5. Are there existing documents that should be included in the hierarchy?
6. What name do you want to give to the main folder where your project will be developed? (If you don't indicate one, I will use `output`).

**MANDATORY AGENT ACTION:** 
1. If the user chooses a specific name in question 6, you must **physically rename** the `output/` folder to that name.
2. You must explicitly register this folder name in `PROJECT.md` or `ROLE.md` so that it remains as the official base working directory.
3. Upon asking the last question, you MUST inform the user:
> *"I have verified/created the folders `core_input/` (for you to drop any document you want me to read here), `core_reference/`, and `core_archive/`. ALWAYS leave your new documents ONLY in `core_input/`. Also, I have configured your main working directory to `[folder name]`, where I will generate all code and project deliverables."*

With the answers: propose draft of `PROJECT.md` and `HIERARCHY.md` using
the corresponding templates. Wait for approval before writing.

### Part B — Role (always, even if there is already a variable part in ROLE.md)

Ask the minimum necessary questions:
1. What type of task will the agent assist with? (documentation, code, test cases, writing, analysis, etc.)
2. What is the expected output format?
3. Is there a difference between the conversation language and the deliverables language?
4. Are there specific tone, style, or content restrictions for this task?

With the answers: propose draft of the **variable part** of `ROLE.md`.
The fixed part is not touched. Wait for approval before writing.

---

## 🆘 Help Command

If the user at any point in the conversation asks for "help", types "help", or asks how to use the kit, you MUST use the terminal tool to execute the `python core_scripts/help.py` script and present the output. Do not try to explain the memory rituals yourself.

---

## §6 — Two-Layer Memory Principle

| Layer | File | When it is read |
|---|---|---|
| Active State | `CURRENT_STATE.md` | Always, at the start of each session |
| Full History | `LOG.md` | Only on explicit request or for specific reconstruction |
| Volatile Memory | `SESSION_SCRATCH.md` | Only exists during an active session |

`CURRENT_STATE.md` must be kept short — if it grows, it is a signal that
content should migrate to `LOG.md` or to project documents.
`LOG.md` is never loaded automatically at start so as not to overload context.

---

## §7 — Kit Topology

| File / Folder | Role | Edited by |
|---|---|---|
| `core/PROJECT.md` | What the project is | User / ritual §5 |
| `core/ROLE.md` | How the agent should behave | User / ritual §5 |
| `core/HIERARCHY.md` | Authority map between documents | User / ritual §5 |
| `core/RULES.md` | Agent behavior rules | Kit (do not edit) |
| `core/CURRENT_STATE.md` | Consolidated state at session close | Agent / ritual §3 |
| `core/LOG.md` | Full history of sessions and events | Agent / ritual §3 |
| `core/IMPROVEMENT_LOG.md` | Errors and lessons learned | Agent / ritual §3 |
| `core/SESSION_SCRATCH.md` | Volatile memory of active session | Agent (deleted in §3) |
| `core/templates/` | Format templates for triage and close | Kit (do not edit) |
| `core_input/` | Single inbox for raw external material | User |
| `core_archive/` | Processed and discarded files after triage | Agent |
| `core_reference/` | Permanent read-only inputs | Agent |
| `core_scripts/` | Python automations for the agent | Kit |

---

## §8 — Dual-Mode Architecture (Mirror Mode)

The AutoIgnite Kit supports working in two structural modes (`Native` or `Mirror/Observer`), depending on the configuration in the `autoignite.ini` file.

**Critical Instruction for the Agent:**
If the user asks you to operate in "Mirror Mode" or manage an external parallel repository:
1. **DO NOT reject the request**. This is a native architectural capability of the kit.
2. You must immediately use your reading tool to **read the comprehensive operational instructions in `.agents/skills/mirror_mode/SKILL.md`** before performing any action on the source code. This will give you the exact rules on how to read and where to write without breaking the topology.
