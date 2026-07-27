import os
import sys
import argparse
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
                # Parse: core_path: ./core/
                val = line.split(":", 1)[1].strip()
                return Path(val)
    return default_core

def main():
    parser = argparse.ArgumentParser(description="Deterministically appends an entry to LOG.md")
    parser.add_argument("verb", help="Action verb (e.g. Update, Decision)")
    parser.add_argument("message", help="Descriptive message")
    args = parser.parse_args()
    
    core_path = get_core_path()
    log_file = core_path / "LOG.md"
    
    if not log_file.exists():
        print(f"[ERROR] Log file not found: {log_file}")
        sys.exit(1)
        
    # Read the file with utf-8-sig to ignore BOM if it exists
    with open(log_file, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()
        
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    
    marker = "<!-- Entries are added here, newest first -->"
    marker_idx = -1
    for i, line in enumerate(lines):
        if marker in line:
            marker_idx = i
            break
            
    if marker_idx == -1:
        print(f"[ERROR] Marker not found in {log_file}")
        sys.exit(1)
        
    new_entry = f"* **{args.verb}** — {args.message}\n"
    today_header = f"## {today_date}\n"
    
    # Look for the next non-empty line to see if it's today's header
    next_line_idx = -1
    for i in range(marker_idx + 1, len(lines)):
        if lines[i].strip():
            next_line_idx = i
            break
            
    if next_line_idx != -1 and lines[next_line_idx].strip() == today_header.strip():
        # The date already exists, we insert immediately below
        insert_idx = next_line_idx + 1
        # If the next line is a line break, we skip it to maintain format
        if insert_idx < len(lines) and lines[insert_idx].strip() == "":
            insert_idx += 1
            
        lines.insert(insert_idx, new_entry)
        print(f"[OK] Entry added as the most recent item for the day {today_date}.")
    else:
        # Today's block does not exist at the top. We create it.
        # Define where to insert (after the marker's line break, if there is one)
        insert_idx = marker_idx + 1
        if insert_idx < len(lines) and lines[insert_idx].strip() == "":
            insert_idx += 1
            
        lines.insert(insert_idx, today_header)
        lines.insert(insert_idx + 1, "\n")
        lines.insert(insert_idx + 2, new_entry)
        lines.insert(insert_idx + 3, "\n")
        print(f"[OK] New day block {today_date} created and inserted at the top.")
        
    # Write back to the file preserving utf-8-sig
    with open(log_file, "w", encoding="utf-8-sig") as f:
        f.writelines(lines)

if __name__ == "__main__":
    main()
