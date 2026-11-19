#!/usr/bin/env python3
"""
🌀 KIRBY HYPERNOVA SYSTEM CLEANER & DISK INHALER (kirby_cleaner.py) 🌀
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_cleaner.py
CLI: kirby clean [--dry-run] [--auto] | kirby inhale

Features:
- Hypernova Inhale cleans development clutter and cache files:
  - Python bytecode cache (__pycache__, *.pyc)
  - Ephemeral screen snaps (/mnt/shared/temp_snap.png, old snaps)
  - Stale temp scratch files and cache remnants
- Displays dramatic ASCII Hypernova Inhale vortex animation.
- Reclaims megabytes of storage across the 3 Dev Environments.
- Awards Kirby digestion XP and Star Coins for every cleaned file.
================================================================================
"""

import os
import sys
import time
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Any

C_PINK = "\033[38;5;205m"
C_HOT_PINK = "\033[38;5;218m"
C_CYAN = "\033[38;5;81m"
C_YELLOW = "\033[38;5;220m"
C_GOLD = "\033[38;5;226m"
C_GREEN = "\033[38;5;120m"
C_PURPLE = "\033[38;5;141m"
C_RED = "\033[38;5;196m"
C_WHITE = "\033[38;5;255m"
C_DIM = "\033[2m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

BASE_DIR = Path("/mnt/shared/AntiGravity_Shared")
PET_STATE_FILE = BASE_DIR / ".kirby_pet_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"

HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


def scan_clutter() -> List[Dict[str, Any]]:
    clutter = []

    # 1. Scan for __pycache__ and *.pyc in /mnt/shared/AntiGravity_Shared and ~/dev
    scan_roots = [
        Path("/mnt/shared/AntiGravity_Shared"),
        Path("/home/droid/.agents"),
        Path("/tmp")
    ]

    for root in scan_roots:
        if not root.exists():
            continue
        try:
            for p in root.rglob("__pycache__"):
                if p.is_dir():
                    size = sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
                    clutter.append({
                        "path": str(p),
                        "type": "PYCACHE_DIR",
                        "size": size,
                        "desc": f"Python bytecode cache ({len(list(p.glob('*')))} files)"
                    })
        except Exception:
            pass

    # 2. Scan for temp snaps
    temp_snap = Path("/mnt/shared/temp_snap.png")
    if temp_snap.exists():
        clutter.append({
            "path": str(temp_snap),
            "type": "TEMP_SCREENSHOT",
            "size": temp_snap.stat().st_size,
            "desc": "Temporary display screenshot capture"
        })

    return clutter


def format_size(bytes_num: int) -> str:
    if bytes_num < 1024:
        return f"{bytes_num} B"
    elif bytes_num < 1024 * 1024:
        return f"{bytes_num / 1024:.1f} KB"
    else:
        return f"{bytes_num / (1024 * 1024):.2f} MB"


def award_pet_loot(coins: int, xp: int):
    if not PET_STATE_FILE.exists():
        return
    try:
        import json
        with open(PET_STATE_FILE, "r", encoding="utf-8") as f:
            pet = json.load(f)
        pet["starCoins"] = pet.get("starCoins", 0) + coins
        pet["bondXp"] = pet.get("bondXp", 0) + xp
        while pet["bondXp"] >= pet.get("bondXpNext", 500):
            pet["bondLevel"] = pet.get("bondLevel", 1) + 1
            pet["bondXp"] -= pet["bondXpNext"]
            pet["bondXpNext"] = int(pet["bondXpNext"] * 1.35)
            pet["starCoins"] += 50
        with open(PET_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(pet, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def run_clean(dry_run: bool = False):
    print(f"\n{C_BOLD}{C_PINK}╔══════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║ {C_YELLOW}🌀  KIRBY HYPERNOVA SYSTEM SWEEPER & CACHE INHALER  🌀{C_PINK}             ║{C_RESET}")
    print(f"{C_BOLD}{C_PINK}╠══════════════════════════════════════════════════════════════════════╣{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║{C_RESET} Scanning development mesh for pycache, temp snaps, and clutter...")
    print(f"{C_BOLD}{C_PINK}╚══════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

    items = scan_clutter()

    if not items:
        print(f"{C_BOLD}{C_GREEN}[✔] Clean tranquility! No stale caches or temp clutter found! Poyo! 🌸✨{C_RESET}\n")
        return

    total_bytes = sum(i["size"] for i in items)
    print(f"{'TYPE':<18} {'SIZE':<12} {'PATH'}")
    print(f"{'─'*18} {'─'*12} {'─'*45}")
    for item in items[:15]:
        print(f"{C_CYAN}{item['type']:<18}{C_YELLOW}{format_size(item['size']):<12}{C_WHITE}{item['path']}{C_RESET}")
    if len(items) > 15:
        print(f"{C_DIM}... and {len(items) - 15} more items.{C_RESET}")
    print(f"\nTotal Clutter Identified: {C_BOLD}{C_GOLD}{format_size(total_bytes)}{C_RESET} across {len(items)} entries.\n")

    if dry_run:
        print(f"{C_YELLOW}[!] Dry-run mode enabled: No files were deleted.{C_RESET}\n")
        return

    # Hypernova Inhale Animation!
    print(f"{C_BOLD}{C_PINK}[*] Kirby inhales deeply! Activating HYPERNOVA VORTEX...{C_RESET}")
    time.sleep(0.4)

    frames = [
        f"         {C_PINK}.-------.{C_RESET}\n       {C_PINK}/   {C_WHITE}O   O{C_PINK}   \\{C_RESET}   {C_CYAN}彡 彡 彡 *gasp!*{C_RESET}\n      {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ᗜ {C_HOT_PINK}(♥){C_PINK} |{C_RESET}",
        f"         {C_PINK}.-------.{C_RESET}   {C_CYAN}彡 彡 彡 彡 彡 彡 彡{C_RESET}\n       {C_PINK}/  {C_WHITE}⭕   0   ⭕{C_PINK} \\{C_CYAN}====== HYPERNOVA INHALE =====>>{C_RESET}\n      {C_PINK}|   {C_HOT_PINK}(♥){C_PINK}   {C_HOT_PINK}(♥){C_PINK} |{C_CYAN}   彡 彡 彡 彡 彡 彡 彡{C_RESET}",
        f"         {C_PINK}.-------.{C_RESET}  {C_YELLOW}★ {C_GOLD}*GULP!*{C_RESET}\n       {C_PINK}/   {C_WHITE}^   ^{C_PINK}   \\{C_RESET}\n      {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK} |{C_RESET}  {C_BOLD}{C_GREEN}SPIT OUT STAR SHARDS! POYO! ✨ 🌸{C_RESET}"
    ]

    for f in frames:
        print("\033[H\033[J" + f)
        time.sleep(0.5)

    if HAS_AUDIO:
        try:
            play_sound_preset("kirby")
        except Exception:
            pass

    # Perform cleaning
    cleaned_count = 0
    reclaimed_bytes = 0
    for item in items:
        p = Path(item["path"])
        try:
            if p.is_dir():
                shutil.rmtree(p)
            elif p.is_file():
                p.unlink()
            cleaned_count += 1
            reclaimed_bytes += item["size"]
        except Exception:
            pass

    coins_reward = max(20, cleaned_count * 5)
    xp_reward = max(30, cleaned_count * 8)
    award_pet_loot(coins_reward, xp_reward)

    print(f"\n{C_BOLD}{C_GREEN}[✔] HYPERNOVA INHALE COMPLETE!{C_RESET}")
    print(f"    Entries Inhaled: {C_WHITE}{cleaned_count}{C_RESET}")
    print(f"    Storage Reclaimed: {C_BOLD}{C_GOLD}{format_size(reclaimed_bytes)}{C_RESET}")
    print(f"    Digestion Rewards: {C_GOLD}+{coins_reward} Star Coins 🪙{C_RESET} | {C_PURPLE}+{xp_reward} Bond XP{C_RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Kirby Hypernova System Sweeper")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Scan without deleting")
    args = parser.parse_args()

    run_clean(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
