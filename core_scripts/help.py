import sys

def show_help():
    # Fix for Windows console unicode error
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    help_text = """
=========================================
🧠 AutoIgnite · Plug & Work AI Context Kit - Rituals Quick Guide ⚙️
=========================================

Rituals are standardized processes that maintain project consistency and memory.
The agent is designed to execute them, but you can also explicitly request them.

🔹 §1 Start Ritual
   - Automatically executed at the beginning of each new session.
   - Restores context, reads the hierarchy, and creates the volatile SESSION_SCRATCH.md file.

🔹 §2 Coherence Ritual
   - The agent executes it before modifying key documents.
   - Verifies that changes do not contradict higher authority documents (according to HIERARCHY.md).
   - You can ask for a "comprehensive check" so the agent reviews the whole project.

🔹 §3 Close Ritual
   - Execute it when you finish working for the day or to save a "checkpoint".
   - Consolidates memory into CURRENT_STATE.md and LOG.md, and clears the volatile session.

🔹 §4 Triage Ritual
   - Use it when you drop new raw files into the `core_input/` folder.
   - The agent will read them, classify them, and propose where to integrate them.

🔹 §5 Creation Ritual for role and project
   - Used when creating a new project or to change the agent's behavior.
   - The agent will ask you questions to configure PROJECT.md and ROLE.md.

Automation commands (Local Scripts):
- start_session.py     : Detects the state and starts the session.
- close_session.py     : Closes the session and consolidates memory structurally.
- generate_index.py    : Generates index.md files in all folders (for Lazy Loading).
- generate_tree.py     : Builds the visual file map (project_tree.md).
- validate_hierarchy.py: Checks the integrity of paths in HIERARCHY.md.
- help.py              : Shows this help screen.

Agent Skills (Ask in natural language):
- "Export the kit"     : Generates a clean release version of the kit in .AutoIgnite_Export/
"""
    print(help_text)

if __name__ == "__main__":
    show_help()
