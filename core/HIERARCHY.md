---
title: "HIERARCHY.md"
description: "Authority map between project documents. Defines what governs what."
type: "governance"
updated: ""
---

# HIERARCHY.md

> This file defines which document has authority over which in this project.
> It is the most important piece of the kit for maintaining consistency over time.
>
> It can be generated with assistance from `input/` via ritual §4 (triage)
> or completed directly via ritual §5.

---

## How to read this file

**Authority** means: if two documents contradict each other, the one with higher
authority (lower number) prevails. The one with lower authority must be updated
to align, not the other way around.

**Authority ≠ creation order.**
A document can be written weeks after others already exist as
drafts, and still be the one with the highest authority. The number in this hierarchy
reflects a deliberate decision about what governs what — not the chronological order
in which they were written.

> Concrete example: in a consulting project, the Intervention Strategy
> might be written last (when the problem is well understood) but it governs
> the Work Plan, Deliverables, and any operational document.
> If the Work Plan was written first, it doesn't give it more authority.

---

## Authority Hierarchy

> Complete with the actual project documents.
> Level 1 = maximum authority. Numbering without gaps.
> Add or remove rows depending on the project.

| Level | Document | Location | Description |
|---|---|---|---|
| 1 | PROJECT.md | `core/PROJECT.md` | Description, objectives, and non-negotiable constraints of the project |
| 2 | ROLE.md | `core/ROLE.md` | Agent behavior in this project |
| [COMPLETE] | [COMPLETE] | [COMPLETE] | [COMPLETE] |

> **Note:** PROJECT.md and ROLE.md always occupy the first levels.
> Project-specific documents (specifications, plans, deliverables)
> are added starting from level 3.

---

## Read-only Inputs

External documents the agent can consult but **never edit**.
They have no assigned authority level — they are a source of information, not rules.

| Document | Location | Origin |
|---|---|---|
| N/A | | |

> If there are no external inputs, delete the example rows and write "N/A".

---

## Documents Outside Hierarchy

Documents that exist in the project but **must not be cited as authority**.
Typically: historical background, previous versions, generic reference materials
that pre-exist the specific project.

| Document | Exclusion Reason |
|---|---|
| N/A | |

> If there are no excluded documents, write "N/A".

---

## Sibling Documents

Pairs of documents developed in parallel that must remain
mutually consistent, without either deriving its content from the other.

| Document A | Document B | Relationship |
|---|---|---|
| N/A | | |

> Ritual §2 (consistency) especially applies to these pairs:
> editing one forces checking the other.
> If there are no sibling documents, write "N/A".
