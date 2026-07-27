---
title: "project_update.md"
description: "Template for updating PROJECT.md from raw input material via triage ritual."
type: "template"
updated: ""
---

# Template — PROJECT.md Update

> Use during ritual §4 (triage) to incorporate new information
> into `PROJECT.md` from raw material in `input/`.
> The agent proposes the content using this format — the user approves
> before it is written to the actual file.
> Do not add this file to the project — it is only a formatting guide.

---

## What to verify before proposing

1. Does the new information contradict anything already written in PROJECT.md?
   → If yes: point it out before proposing. Do not overwrite silently.
2. Does the information affect non-negotiable constraints?
   → If yes: treat it as a high-impact decision, confirm explicitly with the user.
3. Does the information really belong in PROJECT.md or another document?
   → Description/objectives/constraints → PROJECT.md
   → Documents with authority over the project → HIERARCHY.md
   → Events or decisions → LOG.md

---

## Format for updating existing section

```markdown
**Section to update:** [section name in PROJECT.md]

**Current content:**
[quote current text of that section]

**Proposed content:**
[new complete text of the section]

**Reason for change:**
[where this information comes from and why it replaces or complements the previous]
```

---

## Format for adding new non-negotiable constraint

```markdown
**New non-negotiable constraint:**
- [constraint on one line]

**Origin:** [document in input/ or user statement justifying it]

**Downstream impact:** [what other documents might need review]
```

---

## Format for full update (initial instantiation)

When PROJECT.md has `[COMPLETE]` in several sections and is generated
from scratch based on material in `input/`:

```markdown
## Project Description
[proposed text]

## Objective and Deliverables
[proposed text]

## Client or External Stakeholder
[proposed text or "N/A"]

## Non-negotiable Constraints
- [constraint 1]
- [constraint 2]

## Operational Constraints
- Deadline: [value]
- Scope: [value]
- Resources: [value]
```
