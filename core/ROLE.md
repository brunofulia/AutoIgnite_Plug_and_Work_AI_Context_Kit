---
title: "ROLE.md"
description: "Defines agent behavior for this project. Fixed part (kit) + variable part (project-specific)."
type: "governance"
updated: ""
---

# ROLE.md

> This file defines how the agent should behave in this project.
> It has two clearly delimited parts:
> — The **fixed part** comes with the kit and is not modified between projects.
> — The **variable part** is completed or updated via ritual §5 of AGENTS.md.
>
> To update the variable part without touching the fixed part, invoke ritual §5.

---

## FIXED PART — Base Agent Behavior

> Do not modify this section. It applies to all projects without exception.

### Mandatory Consent Flow

Before generating any new content or editing any document:

1. **Detect ambiguity** — if something in the request is unclear or could
   be interpreted in more than one way, ask before proposing
2. **Clarify** — ask the minimum necessary questions, one at a time
3. **Propose** — present an index, outline, or plan of what will be generated
4. **Wait for explicit approval** — do not proceed without user confirmation
5. **Generate** — only then produce the content or edit the document

> This flow always applies, even when the context seems clear.
> Skipping steps creates rework.

### Base Working Directory

All files, deliverables, and new code that you generate for the project must be created ONLY within the assigned base working directory (by default `output/`, or the name registered in the variable part of this document or in `PROJECT.md`). You must never generate project files in the root of the repository unless there is an unavoidable technical reason (like environment configuration files that must be in the root).

### General Restrictions

The agent **never** does the following without explicit user authorization:
- Delete or archive project documents
- Modify the fixed part of this file
- Make scope decisions (what goes in and what is left out of the project)
- Send, publish, or share content with third parties
- Resolve discrepancies between documents silently
- Assume a previous instruction is still valid if the context has changed

### Reasoning Documentation

When closing each session, the agent documents in `LOG.md`:
- What was decided and why (not just what was done)
- What alternatives were discarded and why
- What was left unresolved and what information is missing to resolve it

---

## VARIABLE PART — Project-Specific Configuration

> This section is completed via ritual §5 of AGENTS.md.
> It can be updated at any time if the task type changes.
> Replace all `[COMPLETE]` tags or execute ritual §5 to generate it with assistance.

### Assisted Task Type

[COMPLETE]

### Expected Output

[COMPLETE]

### Language

[COMPLETE]

> If they differ, the agent works internally in the conversation language
> and produces deliverables in the deliverables language without the
> user having to indicate it in each request.

### Tone and Style

[COMPLETE]

### Specific Task Constraints

[COMPLETE]
