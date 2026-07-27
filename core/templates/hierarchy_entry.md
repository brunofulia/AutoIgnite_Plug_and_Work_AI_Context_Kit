---
title: "hierarchy_entry.md"
description: "Template for registering a new document in HIERARCHY.md via triage ritual."
type: "template"
updated: ""
---

# Template — HIERARCHY.md Entry

> Use during ritual §4 (triage) to register a new document
> in `HIERARCHY.md`. Complete the fields and add the row to the table
> of hierarchy, inputs, excluded documents, or sibling documents as appropriate.
> Do not add this file to the project — it is only a formatting guide.

---

## For the Authority Hierarchy table

```markdown
| [level] | [Document Name] | [path/to/document.md] | [One sentence: what it contains and what it governs] |
```

**How to determine the level:**
- Does this document define objectives or constraints that others must respect? → high level (2-3)
- Does this document implement or detail something already defined in another? → lower level than its upstream
- Are two documents at the same conceptual level? → same number, add a sibling relationship note

---

## For the Read-only Inputs table

```markdown
| [Document Name] | [path or location] | [Who produced it / origin] |
```

**When to use this table:**
The document is external to the project (produced by the client, a third party, or
pre-exists the project) and the agent can consult it but never edit it.

---

## For the Documents Outside Hierarchy table

```markdown
| [Document Name] | [Why it is excluded from the hierarchy] |
```

**When to use this table:**
The document exists and can be useful as background, but must not be cited
as authority. Examples: previous replaced versions, generic methodologies
that the specific project has already moved past, historical context materials.

---

## For the Sibling Documents table

```markdown
| [Document A] | [Document B] | [Nature of relationship — what must be consistent between both] |
```

**When to use this table:**
Two documents are developed in parallel, neither derives from the other, but
they must remain mutually consistent. Editing one forces checking the other.
