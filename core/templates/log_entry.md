---
title: "log_entry.md"
description: "Template for LOG.md entries. Used in closing ritual and triage."
type: "template"
updated: ""
---

# Template — LOG.md Entry

> Use in ritual §3 (close) to add the session entry to `LOG.md`.
> Also used in ritual §4 (triage) when the processed material
> generates an event or decision to record.
> Newest entries at the top — always add at the beginning of the file,
> below the main header.
> Do not add this file to the project — it is only a formatting guide.

---

## Available entry verbs

| Verb | When to use it |
|---|---|
| `**Session start**` | First entry of a session |
| `**Session close**` | Last entry of a session |
| `**Update**` | Modification of an existing document |
| `**Creation**` | New document created |
| `**Decision**` | Decision made during the session |
| `**Scope decision**` | Agreement with third party on what goes in/out of the project |
| `**Blocked**` | Something that couldn't progress and why |
| `**Resolved**` | Previous problem that was resolved |

---

## Session entry format (close ritual)

```markdown
## YYYY-MM-DD

* **Session start** — Objective: [objective declared at start of session].
* **[Verb]** — [What happened. Affected document if applicable. Key reasoning if not obvious.]
* **[Verb]** — [ditto]
* **Decision** — [What was decided and why. What alternatives were discarded.]
* **Session close** — [State upon closing. Next priority step.]
```

---

## Specific entry format (triage, isolated event)

When an event is recorded outside of a session close — for example,
a scope decision made in the middle of the session:

```markdown
## YYYY-MM-DD

* **[Verb]** — [Event description. Origin (document in input/, user statement, etc.).]
```

If an entry already exists for that date, add the new line inside
the existing section — do not create a second section with the same date.

---

## What must always be recorded in the closure

- What was done (documents created or modified)
- Why the main decisions were made (reasoning, not just the result)
- What alternatives were discarded and why
- What remained unresolved and what information is missing to resolve it
- What is the concrete next step
