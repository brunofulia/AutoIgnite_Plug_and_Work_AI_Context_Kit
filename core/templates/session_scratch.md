---
title: "SESSION_SCRATCH.md"
description: "Volatile session memory. Created at session start, deleted at close."
type: "volatile"
updated: ""
---

# SESSION_SCRATCH.md

> **Volatile File** — created at the start of each session and deleted at close.
> Its presence indicates that there is an active session or that the previous
> session was not closed properly (crash, abrupt cut).
>
> The agent logs important changes here during the session —
> not every micro-action, but at natural breaking points:
> upon completing a sub-objective, before an irreversible action,
> when changing tasks.
>
> Upon closing: the content of this file is used as input to
> update CURRENT_STATE.md and add the entry to LOG.md.
> Then this file is deleted.
>
> To pause without formally closing: add `[PAUSE]` at the end
> of this file instead of deleting it.

---

## Session

- Date: [agent completes upon creation]
- Declared objective: [agent completes upon creation based on user indication]
- Start scenario: [A — normal / B — pause / C — recovery]

---

## Session Log

<!-- The agent adds entries here during the session -->
<!-- Format: [HH:MM] Relevant action or decision -->
