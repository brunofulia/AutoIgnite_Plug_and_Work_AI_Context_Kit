import os
import sys
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

def main():
    print("\n=== archive_log.py ===")
    
    core_path = get_core_path()
    log_file = core_path / "LOG.md"
    archive_dir = Path("core_archive")
    
    if not log_file.exists():
        print(f"[ERROR] Not found {log_file}")
        sys.exit(1)
        
    if not archive_dir.exists():
        archive_dir.mkdir(exist_ok=True)
        print(f"[INFO] Created folder {archive_dir}/")
        
    with open(log_file, "r", encoding="utf-8-sig") as f:
        content = f.read()
        
    split_marker = "<!-- Entries are added here, newest first -->\n"
    
    if split_marker not in content:
        print("[ERROR] Separation marker not found in LOG.md.")
        print("Make sure the line '<!-- Entries are added here, newest first -->' exists.")
        sys.exit(1)
        
    parts = content.split(split_marker)
    header = parts[0] + split_marker
    body = parts[1]
    
    if not body.strip():
        print("[INFO] LOG.md is already empty. There is nothing to archive.")
        sys.exit(0)
        
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M")
    archive_file = archive_dir / f"log_{timestamp}.md"
    
    # 1. Copy full content to archive file
    with open(archive_file, "w", encoding="utf-8-sig") as f:
        f.write(content)
    print(f"[OK] File securely saved in {archive_file}")
    
    # 2. Purge original file keeping the header
    iso_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    header = re.sub(r'updated:\s*".*?"', f'updated: "{iso_time}"', header, count=1)
    
    with open(log_file, "w", encoding="utf-8-sig") as f:
        f.write(header + "\n")
    print(f"[OK] {log_file} purged successfully.")
    
    # 3. Regenerate indexes
    try:
        subprocess.run([sys.executable, "core_scripts/generate_index.py", "--recursive"], check=True, capture_output=True)
        print("[OK] Indexes regenerated (generate_index.py)")
    except Exception as e:
        print(f"[WARNING] Index regeneration failed: {e}")
        
    try:
        subprocess.run([sys.executable, "core_scripts/generate_tree.py"], check=True, capture_output=True)
        print("[OK] Tree regenerated (generate_tree.py)")
    except Exception as e:
        print(f"[WARNING] Tree regeneration failed: {e}")
        
    print("\n[OK] Archiving completed successfully.\n")

if __name__ == "__main__":
    main()
