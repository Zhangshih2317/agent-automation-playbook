#!/usr/bin/env python3
"""
patch_ufo_for_mavis.py
======================
Patches your local UFO repo to use Mavis/MiniMax as the LLM backend.

What it does:
  1. Copies mavis.py into <UFO>/ufo/llm/
  2. Patches <UFO>/ufo/llm/base.py to add "mavis" to the service_map
  3. Backs up any file it modifies (timestamped .bak)

Usage:
  python patch_ufo_for_mavis.py --ufo-dir "C:\\Users\\zhangshih\\Desktop\\AgentAuto\\UFO"

Revert:
  - Restore base.py from the .bak file
  - Delete the copied mavis.py
"""
import argparse, os, shutil, sys, re
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
MAVIS_PY_SRC = os.path.join(HERE, "ufo", "llm", "mavis.py")
BASE_PY_REL = os.path.join("ufo", "llm", "base.py")

def backup(path: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = f"{path}.{ts}.bak"
    shutil.copy2(path, bak)
    return bak

def patch_base_py(ufo_dir: str) -> bool:
    base = os.path.join(ufo_dir, BASE_PY_REL)
    if not os.path.exists(base):
        print(f"  FAIL: not found: {base}")
        return False
    with open(base, "r", encoding="utf-8") as f:
        src = f.read()
    if '"mavis": "MavisService"' in src or "'mavis': 'MavisService'" in src:
        print("  already patched (skipping)")
        return True
    # Insert into service_map dict. Find a stable anchor.
    anchor = '"claude": "ClaudeService",'
    if anchor not in src:
        anchor = '"custom": "CustomService",'
    if anchor not in src:
        print("  FAIL: can't find anchor in service_map")
        return False
    new_entry = '\n            "mavis": "MavisService",  # added by patch_ufo_for_mavis.py'
    patched = src.replace(anchor, anchor + new_entry, 1)
    bak = backup(base)
    with open(base, "w", encoding="utf-8") as f:
        f.write(patched)
    print(f"  patched (backup: {os.path.basename(bak)})")
    return True

def copy_mavis_py(ufo_dir: str) -> bool:
    if not os.path.exists(MAVIS_PY_SRC):
        print(f"  FAIL: source not found: {MAVIS_PY_SRC}")
        return False
    dst = os.path.join(ufo_dir, BASE_PY_REL.replace("base.py", "mavis.py"))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(MAVIS_PY_SRC, dst)
    print(f"  copied -> {dst}")
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ufo-dir", required=True, help="Path to UFO repo root")
    ap.add_argument("--check", action="store_true", help="Only check, don't patch")
    args = ap.parse_args()
    ufo = os.path.abspath(args.ufo_dir)
    print(f"UFO dir: {ufo}")
    if not os.path.isdir(ufo):
        print("not a directory")
        sys.exit(1)
    print("[1/2] Patch ufo/llm/base.py service_map...")
    if not args.check:
        if not patch_base_py(ufo):
            sys.exit(2)
    print("[2/2] Copy mavis.py to ufo/llm/...")
    if not args.check:
        if not copy_mavis_py(ufo):
            sys.exit(3)
    print()
    print("Done. Now configure your agent:")
    print("  Edit config/ufo/agents.yaml:")
    print("    HOST_AGENT:")
    print("      API_TYPE: mavis")
    print("      API_MODEL: minimax")
    print("      API_BASE: http://127.0.0.1:15321/mavis/api/v1")
    print("      API_KEY: ignored")
    print()
    print("To revert: restore the .bak file and delete ufo/llm/mavis.py")

if __name__ == "__main__":
    main()
