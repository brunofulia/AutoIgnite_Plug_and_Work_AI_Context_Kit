import os
import sys
from pathlib import Path
import re
from config_utils import get_core_path, get_target_path

def parse_markdown_table_for_paths(text):
    paths = []
    # Search for markdown tables
    lines = text.split("\n")
    in_table = False
    headers = []
    for line in lines:
        line = line.strip()
        if not line:
            in_table = False
            headers = []
            continue
            
        if line.startswith("|") and line.endswith("|"):
            in_table = True
            cols = [col.strip() for col in line.strip("|").split("|")]
            
            # If it is the separator row
            if all(set(col).issubset({'-', ':'}) for col in cols if col):
                continue
                
            # If it is header
            if not headers:
                headers = cols
                continue
            
            # Find the Location column
            try:
                ubicacion_idx = headers.index("Location")
            except ValueError:
                # Try to find a column containing path
                ubicacion_idx = -1
                for i, h in enumerate(headers):
                    if "location" in h.lower() or "path" in h.lower() or "ubicación" in h.lower() or "ubicacion" in h.lower():
                        ubicacion_idx = i
                        break
                        
            if ubicacion_idx != -1 and len(cols) > ubicacion_idx:
                raw_path = cols[ubicacion_idx].strip()
                # Remove markdown backticks if present
                raw_path = raw_path.strip("`")
                if raw_path and raw_path.lower() not in ["no aplica", "n/a", "not applicable"]:
                    paths.append(raw_path)
    return paths

def main():
    print("=== validate_hierarchy.py ===")
    core_path = get_core_path()
    target_path = get_target_path()
    hierarchy_path = core_path / "HIERARCHY.md"
    
    if not hierarchy_path.exists():
        print(f"[ERROR] HIERARCHY.md not found at {hierarchy_path}")
        sys.exit(1)
        
    content = hierarchy_path.read_text(encoding="utf-8-sig")
    paths_to_check = parse_markdown_table_for_paths(content)
    
    if not paths_to_check:
        print("[INFO] No paths found to validate in HIERARCHY.md.")
        sys.exit(0)
        
    print(f"[INFO] Found {len(paths_to_check)} files listed in HIERARCHY.md. Validating existence...")
    
    missing_files = []
    
    # Resolve paths
    hierarchy_dir = hierarchy_path.parent
    project_root = Path(".")
    
    for p in paths_to_check:
        # Attempt 1: Relative to target_path
        candidate_1 = target_path / p
        # Attempt 2: Relative to core/ directory
        candidate_2 = hierarchy_dir / p
        # Attempt 3: Relative to project_root
        candidate_3 = project_root / p
        
        if candidate_1.exists():
            print(f"  [OK] {p} (target)")
        elif candidate_2.exists():
            print(f"  [OK] {p} (core)")
        elif candidate_3.exists():
            print(f"  [OK] {p} (root)")
        else:
            print(f"  [MISSING] {p}")
            missing_files.append(p)
            
    if missing_files:
        print(f"\\n[ERROR] Detected {len(missing_files)} referenced files that do not exist physically:")
        for mf in missing_files:
            print(f"  - {mf}")
        sys.exit(1)
    else:
        print("\\n[OK] All referenced files exist in the system.")
        sys.exit(0)

if __name__ == "__main__":
    main()
