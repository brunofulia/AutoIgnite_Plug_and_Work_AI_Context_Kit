import os
import sys
import argparse
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

def parse_table(lines, header_idx):
    row_idx = header_idx + 2
    rows = []
    while row_idx < len(lines):
        line = lines[row_idx].strip()
        if not line.startswith("|"):
            break
        cols = [c.strip() for c in line.strip("|").split("|")]
        rows.append({"line_idx": row_idx, "cols": cols, "text": lines[row_idx]})
        row_idx += 1
    return row_idx, rows

def update_abiertas_ids(lines, start_idx, end_idx):
    current_id = 1
    for i in range(start_idx, end_idx):
        line = lines[i].strip()
        if line.startswith("|") and "—" not in line.split("|")[1]:
            parts = line.split("|")
            parts[1] = f" {current_id} "
            lines[i] = "|".join(parts) + "\n"
            current_id += 1

def main():
    parser = argparse.ArgumentParser(description="Manages IMPROVEMENT_LOG.md")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand open
    parser_open = subparsers.add_parser("open", help="Adds a problem to the Open table")
    parser_open.add_argument("where", help="Where it was detected")
    parser_open.add_argument("problem", help="Description of the problem")
    parser_open.add_argument("--status", default="Pending", help="Initial state")

    # Subcommand resolve
    parser_resolve = subparsers.add_parser("resolve", help="Moves a problem from Open to Resolved")
    parser_resolve.add_argument("id", type=int, help="ID in the Open table")
    parser_resolve.add_argument("correction", help="What was done to correct it")
    parser_resolve.add_argument("lesson", help="Reusable lesson learned")

    args = parser.parse_args()

    core_path = get_core_path()
    log_file = core_path / "IMPROVEMENT_LOG.md"

    if not log_file.exists():
        print(f"[ERROR] File not found: {log_file}")
        sys.exit(1)

    with open(log_file, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    # Search for section headers
    abiertas_hdr_idx = -1
    resueltas_hdr_idx = -1
    
    for i, line in enumerate(lines):
        if line.strip() == "## Open":
            abiertas_hdr_idx = i
        elif line.strip() == "## Resolved":
            resueltas_hdr_idx = i

    if abiertas_hdr_idx == -1 or resueltas_hdr_idx == -1:
        print("[ERROR] Unrecognizable file format. Section headers missing.")
        sys.exit(1)

    # Search for start of Open table
    abiertas_table_idx = -1
    for i in range(abiertas_hdr_idx, resueltas_hdr_idx):
        if lines[i].strip().startswith("| # | Detected |"):
            abiertas_table_idx = i
            break

    if abiertas_table_idx == -1:
        print("[ERROR] Open table not found.")
        sys.exit(1)

    # Search for start of Resolved table
    resueltas_table_idx = -1
    for i in range(resueltas_hdr_idx, len(lines)):
        if lines[i].strip().startswith("| # | Detected | Resolved |"):
            resueltas_table_idx = i
            break

    if resueltas_table_idx == -1:
        print("[ERROR] Resolved table not found.")
        sys.exit(1)

    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")

    abiertas_end, abiertas_rows = parse_table(lines, abiertas_table_idx)
    resueltas_end, resueltas_rows = parse_table(lines, resueltas_table_idx)

    dummy_abiertas = len(abiertas_rows) == 1 and "—" in abiertas_rows[0]["cols"][0]
    dummy_resueltas = len(resueltas_rows) == 1 and "—" in resueltas_rows[0]["cols"][0]

    if args.command == "open":
        next_id = 1
        if not dummy_abiertas and abiertas_rows:
            last_id = int(abiertas_rows[-1]["cols"][0])
            next_id = last_id + 1
            
        new_row = f"| {next_id} | {today_date} | {args.where} | {args.problem} | {args.status} |\n"
        
        if dummy_abiertas:
            lines[abiertas_rows[0]["line_idx"]] = new_row
        else:
            lines.insert(abiertas_end, new_row)
            
        print(f"[OK] Added item #{next_id} to Open table.")

    elif args.command == "resolve":
        if dummy_abiertas:
            print("[ERROR] The Open table is empty.")
            sys.exit(1)
            
        target_row = None
        for r in abiertas_rows:
            if r["cols"][0] == str(args.id):
                target_row = r
                break
                
        if not target_row:
            print(f"[ERROR] ID {args.id} not found in the Open table.")
            sys.exit(1)
            
        # Extract data: Detected, Where, Problem
        detectado = target_row["cols"][1]
        donde = target_row["cols"][2]
        problema = target_row["cols"][3]
        
        # Delete row from open
        del lines[target_row["line_idx"]]
        
        # Recalculate indexes because we removed a line
        resueltas_table_idx -= 1
        resueltas_end -= 1
        
        # Renumber Open table
        update_abiertas_ids(lines, abiertas_table_idx + 2, abiertas_end - 1)
        
        # If the open table is empty, insert dummy
        if abiertas_end - 1 == abiertas_table_idx + 2:
            lines.insert(abiertas_table_idx + 2, "| — | — | — | — | — |\n")
            resueltas_table_idx += 1
            resueltas_end += 1
            
        # Refresh resolved parsing
        resueltas_end, resueltas_rows = parse_table(lines, resueltas_table_idx)
        dummy_resueltas = len(resueltas_rows) == 1 and "—" in resueltas_rows[0]["cols"][0]
        
        next_res_id = 1
        if not dummy_resueltas and resueltas_rows:
            last_res_id = int(resueltas_rows[-1]["cols"][0])
            next_res_id = last_res_id + 1
            
        prob_desc = f"[{donde}] {problema}"
        new_res_row = f"| {next_res_id} | {detectado} | {today_date} | {prob_desc} | {args.correction} | {args.lesson} |\n"
        
        if dummy_resueltas:
            lines[resueltas_rows[0]["line_idx"]] = new_res_row
        else:
            lines.insert(resueltas_end, new_res_row)
            
        print(f"[OK] Item moved to Resolved table with ID #{next_res_id}.")

    with open(log_file, "w", encoding="utf-8-sig") as f:
        f.writelines(lines)

if __name__ == "__main__":
    main()
