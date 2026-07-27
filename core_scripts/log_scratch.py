import os
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime, timedelta

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

def parse_session_file(scratch_file: Path):
    """Parses the scratch file to find the date and entries."""
    date_str = None
    entries = []
    
    # Regex to match [HH:MM] at start of line
    entry_pattern = re.compile(r'^\[(\d{2}:\d{2})\]')
    
    with open(scratch_file, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line.startswith("- Date:"):
                date_str = line.split(":", 1)[1].strip()
            
            match = entry_pattern.match(line)
            if match:
                entries.append(match.group(1))
                
    return date_str, entries

def main():
    parser = argparse.ArgumentParser(description="Adds an entry to the active session log in SESSION_SCRATCH.md")
    parser.add_argument("message", help="Message to annotate (E.g. 'Phase 1 finished')")
    args = parser.parse_args()

    core_path = get_core_path()
    scratch_file = core_path / "SESSION_SCRATCH.md"

    if not scratch_file.exists():
        print(f"[ERROR] No active session. File not found: {scratch_file}")
        sys.exit(1)

    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    entry = f"[{current_time}] {args.message}\n"

    # Append the new entry
    with open(scratch_file, "a", encoding="utf-8-sig") as f:
        f.write(entry)

    print(f"[OK] Annotation added to SESSION_SCRATCH.md: {entry.strip()}")
    
    # Checkpoint validation
    try:
        date_str, entries = parse_session_file(scratch_file)
        
        trigger = False
        reasons = []
        
        if len(entries) > 4:
            trigger = True
            reasons.append(f"more than 4 milestones recorded ({len(entries)})")
            
        if date_str and len(entries) > 0:
            first_time_str = entries[0]
            try:
                first_dt = datetime.strptime(f"{date_str} {first_time_str}", "%Y-%m-%d %H:%M")
                if (now - first_dt) > timedelta(hours=2):
                    trigger = True
                    reasons.append(f"more than 2 hours since session start ({first_time_str})")
            except ValueError:
                pass # Ignore if date format is unexpected
                
        if trigger:
            print(f"\n⚠️ WARNING FOR AGENT: Limit reached ({' and '.join(reasons)}).")
            print("You MUST propose a Checkpoint (close ritual) to the user in your next response.")
            
    except Exception:
        pass # Silently fail validation so the main append still succeeds

if __name__ == "__main__":
    main()
