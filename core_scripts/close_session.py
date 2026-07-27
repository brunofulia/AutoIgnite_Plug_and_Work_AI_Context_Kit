import os
import sys
import argparse
import subprocess
import re
from pathlib import Path
from datetime import datetime

def get_core_path() -> Path:
    agents_md = Path("AGENTS.md")
    default_core = Path("core")
    if not agents_md.exists():
        return default_core
    
    with open(agents_md, "r", encoding="utf-8-sig") as f:
        for line in f:
            if line.strip().startswith("core_path:"):
                val = line.split(":", 1)[1].strip()
                return Path(val)
    return default_core

def update_section(content: str, section_title: str, new_text: str) -> str:
    # Searches for the header and replaces everything until the next "---"
    # DOTALL allows .* to cover line breaks
    pattern = re.compile(rf"(## {re.escape(section_title)}\n+)(.*?)(?=\n+---)", re.DOTALL)
    
    if pattern.search(content):
        return pattern.sub(rf"\1{new_text}\n", content)
    return content

def main():
    parser = argparse.ArgumentParser(description="Orchestrates session closure and updates states.")
    parser.add_argument("--done", required=True, help="Text for 'What was done in the last session'")
    parser.add_argument("--next", required=True, dest="next_step", help="Text for 'Next priority step'")
    parser.add_argument("--log-message", required=True, help="Message to add to LOG.md as Session close")
    parser.add_argument("--docs", action="append", default=[], help="Files for the work table (Format: Name|State|Observation)")
    args = parser.parse_args()
    
    core_path = get_core_path()
    scratch_file = core_path / "SESSION_SCRATCH.md"
    current_state_file = core_path / "CURRENT_STATE.md"
    
    if not scratch_file.exists():
        print(f"[ERROR] No active session (cannot find {scratch_file}).")
        sys.exit(1)
        
    print("\n=== close_session.py ===")
    
    # 1. Update CURRENT_STATE.md
    if current_state_file.exists():
        with open(current_state_file, "r", encoding="utf-8-sig") as f:
            content = f.read()
            
        # Update datetime frontmatter
        now = datetime.now()
        iso_time = now.strftime("%Y-%m-%dT%H:%M:%S")
        content = re.sub(r'updated:\s*".*?"', f'updated: "{iso_time}"', content, count=1)
        
        # Update "What was done"
        content = update_section(content, "What was done in the last session", args.done)
        
        # Update "Next step"
        content = update_section(content, "Next priority step", args.next_step)
        
        # Rebuild "Where the work left off" table
        table_lines = [
            "| Document | State | Observations |",
            "|---|---|---|"
        ]
        if args.docs:
            for doc_str in args.docs:
                parts = doc_str.split("|")
                if len(parts) == 3:
                    table_lines.append(f"| {parts[0].strip()} | {parts[1].strip()} | {parts[2].strip()} |")
                else:
                    # Fallback if format is wrong
                    table_lines.append(f"| {doc_str} | modified | |")
        else:
            table_lines.append("| None | | |")
            
        table_text = "\n".join(table_lines)
        content = update_section(content, "Where the work left off", table_text)
        
        with open(current_state_file, "w", encoding="utf-8-sig") as f:
            f.write(content)
        print(f"[OK] Updated {current_state_file}")
    else:
        print(f"[WARNING] Could not find {current_state_file}")

    # 2. Add entry to LOG.md
    try:
        subprocess.run(
            [sys.executable, "core_scripts/append_log.py", "Session close", args.log_message],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] append_log.py failed: {e}")
        sys.exit(1)
        
    # 3. Regenerate Indexes
    try:
        subprocess.run([sys.executable, "core_scripts/generate_index.py", "--recursive"], check=True, capture_output=True)
        print(f"[OK] Indexes regenerated (generate_index.py)")
    except Exception as e:
        print(f"[WARNING] Could not execute generate_index.py: {e}")
        
    try:
        subprocess.run([sys.executable, "core_scripts/generate_tree.py"], check=True, capture_output=True)
        print(f"[OK] Tree regenerated (generate_tree.py)")
    except Exception as e:
        print(f"[WARNING] Could not execute generate_tree.py: {e}")
        
    # 4. Delete SESSION_SCRATCH.md
    try:
        os.remove(scratch_file)
        print(f"[OK] Deleted {scratch_file}")
    except Exception as e:
        print(f"[ERROR] Could not delete {scratch_file}: {e}")
        sys.exit(1)
        
    print("\n[OK] Session closed successfully.\n")

if __name__ == "__main__":
    main()
