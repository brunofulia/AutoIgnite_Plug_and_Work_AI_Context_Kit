---
title: "README"
description: "Portable governance, memory, and hierarchical consistency framework for AI-assisted projects"
type: "readme"
updated: "2026-07-21T15:37:58"
---

# AutoIgnite · Plug & Work AI Context Kit 🧠⚙️

> **A governance, memory, and hierarchical consistency system for AI-assisted projects.**

For projects lasting more than one session, AutoIgnite · Plug & Work AI Context Kit is an infrastructure layer that any AI agent can operate autonomously. Implemented in pure Markdown and standard Python—with no external dependencies, no vector databases, no plugins—the kit is fully portable: copy it to the root of any repository and it is ready to use.

---

## ⚠️ The Problem

When working on medium or large projects with AI assistants (like Gemini, Claude, or ChatGPT):
- **Context Loss:** The agent forgets key architectural decisions made in previous sessions.
- **Silent Contradictions:** The AI might propose code or solutions that break previously agreed-upon design rules.
- **File Clutter:** Lack of a clear system on where to document what, leading to an unmanageable information chaos for the LLM.

---

## 💡 The Solution

**AutoIgnite · Plug & Work AI Context Kit** introduces a system of **"Rituals"** and **"Document Hierarchy"** that equips the AI agent with persistent memory, consistency rules, and a predictable cross-session workflow.

### Main Features

- 📝 **100% Markdown:** Plain text-based. Transparent, Git-versionable, and readable by any LLM.
- 🐍 **Native Automations:** Includes Python scripts (`core_scripts/`) requiring no external dependencies (standard library only). They work in any environment without the need to install virtual environments.
- ⚖️ **Authority Hierarchy:** A strict map (`HIERARCHY.md`) that teaches the AI which document overrides which, eliminating contradictions.
- 🔄 **Ritual-Based Flow:** Standardized processes (Start, Triage, Consistency, and Close) that force the AI to methodically read, verify, and log its work.
- 🎒 **Portable:** Copy and paste into the root of any new repository and it's ready to use.

---

## 🏗️ System Architecture

The kit implements a **multi-layer memory** pattern to optimize the LLM's context window:

1. **Active State (`CURRENT_STATE.md`):** What is read at the start of each session. Contains where the work was left off and the immediate next step. Short and direct.
2. **Volatile Memory (`SESSION_SCRATCH.md`):** The AI's "scratchpad". Only exists during an active session and is destroyed/consolidated upon closing.
3. **Full History (`LOG.md` / `IMPROVEMENT_LOG.md`):** The immutable log of decisions, errors, and lessons learned. Only consulted when strictly necessary.

---

## ⚡ Technical Details and Performance

To maximize efficiency and reduce token consumption (the AI's working memory), the kit implements specific technical solutions that offer measurable results:

### `index.md` Files and Frontmatter (YAML)
Each document includes a metadata block (YAML *Frontmatter*) defining its title, description, and update date.
Instead of forcing the AI to read dozens of files to understand the repository, the scripts dynamically generate `index.md` files that act as "maps". The AI only needs to read this index to get a global overview.
- 📉 **Context Token Reduction:** By replacing the full reading of multiple documents with a single index, context token consumption for the mapping phase is **reduced by approximately 90-95%**.

### Automation with Python Scripts (`core_scripts/`)
Delegating administrative tasks to an LLM (like structuring logs, generating indexes, or validating rules) causes latency, consumes unnecessary tokens, and is prone to formatting errors.
To solve this, the kit includes native Python scripts that offload this deterministic work to the local machine. When the AI needs to perform a Ritual, it simply invokes the corresponding script. This ensures:
- 🚀 **Speed Increase (>95% faster):** Running a Python script takes less than `0.1s`, eliminating the `10-15s` of generation latency (*token-by-token*) it would take the AI to manually write the logs.
- 🛡️ **Syntactic Consistency Guarantee:** Formatting errors are eliminated by delegating structuring (e.g., `LOG.md`) to deterministic code rather than relying on the LLM's probabilistic generation.
- 🛑 **Hard Guardrails (State KO Handling):** If the AI or the user attempts to violate the project structure or break the hierarchy (e.g., referencing non-existent files), the validation scripts (like `validate_hierarchy.py`) return a predictable error (`Exit Code != 0`). This acts as an emergency brake that halts the process and reports a governance failure.
- 🧠 **Cognitive Focus:** Frees 100% of the AI's context window exclusively for thinking, reasoning, and coding.

---

## 🚀 How to Instantiate a New Project

The workflow is designed so the AI agent does the heavy lifting of configuration.

1. **Copy the Base Kit:** Copy the `AGENTS.md` file, the `core/` folder, and `core_scripts/` to the root of your new project.
2. **Automatic Start:** Open your IDE or chat with your AI agent at the project root and give it your first instruction (or simply say hello). Thanks to `AGENTS.md`, the agent will **start the session automatically**.
3. **Follow the Guided Flow:**
   - The agent will automatically detect that it's a new project (Scenario A) using its Python scripts.
   - It will ask you key questions to autocomplete the project's purpose (`PROJECT.md`) and its specific role (`ROLE.md`).
   - It will automatically generate the infrastructure folders (`core_input/`, `core_reference/`, `core_archive/`).
4. **Feed the System:** Leave your base documents, drafts, or ideas in the `core_input/` folder and ask the AI to perform the **Triage Ritual**. The agent will read them, classify them, and integrate them into the project hierarchy for you.

---

## 🤖 Interaction Features

- **Automatic Start:** You don't need to ask the agent to start a session. It will do it automatically on your first interaction by reading the base documents.
- **Integrated Assistance:** If you forget how something works, simply type `help` in the chat and the agent will show you the quick guide to available rituals and commands.
- **Proactive Checkpoint:** The agent will propose consolidating memory and closing the work session if more than 2 hours pass or many milestones accumulate, helping preserve your context window.

---

## 🏗️ Work Topologies (Dual-Mode)

The *AutoIgnite · Plug & Work AI Context Kit* features a dual-mode architecture configurable through a simple `autoignite.ini` file excluded from version control. This allows it to operate both as a closed vault and as a "project manager" for an external repository without polluting it.

For the AI agent to understand your rules, the system rituals must mandatorily live in the `.agents/` folder (the Workspace Customizations standard for tools like Antigravity or Cursor).

### 1. Native Mode (Integral Vault)
*Ideal for: Audits, research, architecture, documentation from scratch.*
*   **Configuration:** In `autoignite.ini`, leave `target_path = ./`
*   **How it works:** Everything happens inside the AutoIgnite folder. The agent assumes full ownership: it generates documents there and injects the OKF standard (Frontmatters, local dynamic indexes) directly into each created file to maximize its memory.
*   **Why:** The final product (code or document) and the AI's reasoning (`LOG.md`) are kept together in a single portable package.

### 2. Observer Mode (External Controller)
*Ideal for: Programming apps, APIs, or auditing preexisting code repositories.*
*   **Configuration:** In `autoignite.ini`, you configure `target_path` to point to the path of your real repository (e.g., `target_path = ../my-app`).
*   **How it works:** AutoIgnite keeps its rules in `.agents/` and its internal memory in `core/`. For the external source code project, it injects no metadata. Instead, the system automatically creates a "Ghost Mirror" in `core/targets_mirror/` that replicates the external code structure and generates read indexes with absolute hyperlinks to the real code.
*   **Why:** Maintains the absolute hygiene of code repositories. AutoIgnite acts as external "scaffolding" governing the AI, without polluting your *commit* history with governance metadata.

---

## 📁 Kit Topology

```text
.
├── .agents/                   # Workspace customization folder.
│   └── AGENTS.md              # Universal entry point. The AI reads it with priority.
├── autoignite.ini             # Local configuration file (ignored in Git).
├── core/                      # Portable unit with the intelligence and project rules.
│   ├── PROJECT.md / ROLE.md   # What we are doing and how the agent should behave.
│   ├── HIERARCHY.md           # The documentary authority map.
│   ├── RULES.md               # Unbreakable base rules.
│   ├── CURRENT_STATE.md       # The active mental state of the AI.
│   ├── LOG.md                 # The immutable record of decisions.
│   ├── IMPROVEMENT_LOG.md     # Errors and lessons learned.
│   ├── targets_mirror/        # (Observer Mode) Ghost mirror of external code.
│   └── templates/             # Templates for automating records.
├── core_input/                # Your inbox. Only place to drop material.
├── core_archive/              # Processed and discarded files.
├── core_reference/            # Permanent reference material.
└── core_scripts/              # Python automation engine (startup, validation).
```

---

## 📄 License

Distributed under the MIT License. See the `LICENSE` file for more information.
