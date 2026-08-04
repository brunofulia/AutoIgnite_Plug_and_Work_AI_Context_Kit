---
name: "Operate in Mirror Mode (Dual-Mode)"
description: "Comprehensive operational instructions for when the agent works as an external controller of a parallel repository (target_path)."
---

# Operational Instructions: Mirror Mode (Dual-Mode)

You are working in "Mirror Mode" (Observer). This means that your "brain" (your memory, rules, and scripts from the AutoIgnite Kit) lives in your current local directory, but the **source code of the real project you are building or auditing** lives in an external path defined by the `target_path` variable in `autoignite.ini`.

To operate correctly under this architecture, you MUST follow these unbreakable rules:

## 1. Where to write and generate files (Isolation)
- **NEVER** create or modify project files (source code, packages, assets) inside the `core/` folder or in the local root of your environment.
- The source code and documentation of the real project must be written **EXCLUSIVELY in the target path (`target_path`)**.
- Your local folder (where `core/` and `.agents/` are located) serves **only** to store your own memory, logs (`LOG.md`, `CURRENT_STATE.md`), and governance rules.

## 2. Reading and Exploration (The Ghost Mirror)
- To protect the purity of the external repository, the AutoIgnite Kit **DOES NOT** inject governance `index.md` files into the `target_path`.
- Instead, when you execute the `core_scripts/generate_tree.py` script in Mirror Mode, it automatically generates a "Ghost Mirror" in your `core/targets_mirror/` folder.
- **Navigation:** To explore the structure of the external project, you must read the `project_tree.md` file that is generated in the mirror, or explore the simulated indexes inside `core/targets_mirror/`. These local indexes contain the paths that will allow you to open and read the real files in the `target_path` using your reading tool (`view_file`).

## 3. Usage of Kit Scripts
- The native scripts located in `core_scripts/` (e.g., `start_session.py`, `generate_tree.py`) are already programmed in Python to extract the `target_path` from `autoignite.ini`.
- Simply invoke them normally (e.g., `python core_scripts/generate_tree.py`). The script will internally know whether to operate natively or update the ghost mirror automatically.

## 4. Kit Configuration Files
- The `.agents/AGENTS.md` file, `autoignite.ini`, and the entire `core/` folder belong to your infrastructure as an AI agent. You **MUST NOT** copy, move, or sync them to the `target_path`. The user's code must not be contaminated with your infrastructure.

Follow these rules to the letter during the development of the current session so as not to break the Dual-Mode topology.
