import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from config_utils import get_core_path, get_target_path, is_mirror_mode

INFRA_FOLDERS = ["core_input", "core_archive", "core_reference", "output"]

def ensure_infrastructure_exists():
    created_any = False
    for folder in INFRA_FOLDERS:
        p = Path(folder)
        if not p.exists():
            p.mkdir(exist_ok=True)
            print(f"[INFO] Infrastructure folder created: {folder}/")
            created_any = True
            
    if created_any:
        try:
            subprocess.run([sys.executable, "core_scripts/generate_index.py", "--recursive"], check=True, capture_output=True)
            print("[INFO] Indexes generated for new folders.")
        except Exception as e:
            print(f"[WARNING] Could not generate automatic indexes: {e}")

def main():
    parser = argparse.ArgumentParser(description="Instantiates a new session of the AutoIgnite · Plug & Work AI Context Kit.")
    parser.add_argument("-o", "--objective", default="Start session and continue with pendings according to CURRENT_STATE", help="Main objective of the session")
    args = parser.parse_args()
    
    print("\\n=== start_session.py ===")
    
    ensure_infrastructure_exists()
    
    core_path = get_core_path()
    mirror_mode = is_mirror_mode()
    
    template_path = core_path / "templates" / "session_scratch.md"
    scratch_path = core_path / "SESSION_SCRATCH.md"
    
    if mirror_mode:
        target_path = get_target_path()
        print(f"\n[INFO] Observer Mode (Ghost Mirror) Active")
        print(f"       Target project: {target_path}")
        
        target_name = target_path.resolve().name
        mirror_path = core_path / "targets_mirror" / target_name
        
        if mirror_path.exists() and any(mirror_path.iterdir()):
            print(f"       Navigation map is at {mirror_path}/")
            print("       AGENT INSTRUCTION: DO NOT modify external project files unless explicitly requested by the user.")
        else:
            print(f"       [ALERT] Navigation map at {mirror_path}/ does not exist yet or is empty.")
            print("       AGENT INSTRUCTION: BEFORE doing anything, you must generate the Ghost Mirror by running:")
            print("         1. python core_scripts/generate_index.py --recursive")
            print("         2. python core_scripts/generate_tree.py")
            print("       Once generated, use that map to understand the project. DO NOT modify external project files unless explicitly requested.")
    
    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")
    
    if not scratch_path.exists():
        print("\\n[DETECTED] Scenario A — Normal Start")
        
        if not template_path.exists():
            print(f"[ERROR] Template not found: {template_path}", file=sys.stderr)
            sys.exit(1)
            
        content = template_path.read_text(encoding="utf-8-sig")
        
        content = content.replace('updated: ""', f'updated: "{today_date}"')
        content = content.replace("[agent completes upon creation]", today_date)
        content = content.replace("[agent completes upon creation based on user indication]", args.objective)
        content = content.replace("[A — normal / B — pause / C — recovery]", "A — normal")
        
        entry = f"[{current_time}] Session start in Scenario A.\\n"
        content += entry
        
        scratch_path.write_text(content, encoding="utf-8-sig")
        print(f"[OK] Instantiated {scratch_path}")
        
        try:
            subprocess.run(
                [sys.executable, "core_scripts/append_log.py", "Session start", f"Objective: {args.objective}"],
                check=True
            )
            print(f"[OK] Session start entry injected into LOG.md")
        except subprocess.CalledProcessError as e:
            print(f"[WARNING] Injection into LOG.md failed: {e}")
            
        try:
            subprocess.run([sys.executable, "core_scripts/generate_index.py", "--recursive"], check=True, capture_output=True)
            subprocess.run([sys.executable, "core_scripts/generate_tree.py"], check=True, capture_output=True)
            print(f"[OK] Project tree and initial indexes generated.")
        except Exception as e:
            print(f"[WARNING] Generation of initial project tree failed: {e}")
            
        print("\\nINSTRUCTIONS FOR THE AGENT:")
        print("1. Read the base documents (PROJECT, ROLE, HIERARCHY, CURRENT_STATE, IMPROVEMENT_LOG).")
        print("2. Apply the 'Dual Logic' (Step 7 of the Start Ritual from AGENTS.md):")
        print("   - If the user asked for a specific task in their first message, update the 'Declared objective' line in SESSION_SCRATCH.md and start working.")
        print("   - If they only said hello, give them the summary and ask for their objective.")
        
    else:
        content = scratch_path.read_text(encoding="utf-8-sig").strip()
        if content.endswith("[PAUSA]") or content.endswith("[PAUSE]"):
            print("\\n[DETECTED] Scenario B — Resumption of paused session")
            print("\\nINSTRUCTIONS FOR THE AGENT:")
            print("1. Read the base files and then fully read SESSION_SCRATCH.md.")
            print("2. Summarize for the user where the work left off before the pause and what the next step was.")
        else:
            print("\\n[WARNING] Scenario C — Abrupt cut recovery detected")
            print("\\nINSTRUCTIONS FOR THE AGENT:")
            print("1. Read the base files and SESSION_SCRATCH.md.")
            print("2. Reconstruct what happened during the interrupted session.")
            print("3. Present the reconstruction to the user asking for confirmation before consolidating anything.")

    print("\\nReady.\\n")

if __name__ == "__main__":
    main()
