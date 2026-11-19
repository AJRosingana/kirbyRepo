#!/usr/bin/env python3
"""
🗺️ KIRBY DREAM LAND EXPEDITIONS & DEV QUEST ENGINE (kirby_expeditions.py) 🗺️
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_expeditions.py
CLI: kirby quest [region] [--auto] | kirby explore | kirby expedition

Features:
- Procedural expeditions across 6 iconic Dream Land and Pixel Mesh realms:
  1. Green Greens (Whispy Woods' lush arboreal orchard)
  2. Bubbly Clouds (Kracko's floating starlight cloud kingdom)
  3. Magma Mountain (Volcanic caverns & lava rivers)
  4. Cyber Dream Net (Debian AVF VM, Termux bridges, VirtIO-FS fabric)
  5. Battleship Halberd (Meta Knight's legendary skyship)
  6. Fountain of Dreams (Sacred rainbow waters & Star Rod shrine)
- Dynamic node encounters: Enemy Inhale, Ability Puzzles, Treasure Chests,
  Warp Star Portals, and Boss Gateways.
- Interactive mode and autonomous AI expedition mode (--auto).
- Star Coin, Treat, and Artifact loot persistent tracking.
================================================================================
"""

import os
import sys
import time
import json
import random
import select
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

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
QUEST_STATE_FILE = BASE_DIR / ".kirby_quest_progress.json"
PET_STATE_FILE = BASE_DIR / ".kirby_pet_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"

HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


REGIONS = {
    "green_greens": {
        "id": "green_greens",
        "name": "Green Greens",
        "icon": "🌳",
        "title": "Verdant Orchard of Whispy Woods",
        "desc": "Lush rolling green hills, apple trees, and peaceful meadows.",
        "guardian": "Whispy Woods",
        "enemies": ["Waddle Dee", "Poppy Bros. Jr.", "Sir Kibble", "Bronto Burt"],
        "lootMultiplier": 1.0,
        "bg_color": C_GREEN
    },
    "bubbly_clouds": {
        "id": "bubbly_clouds",
        "name": "Bubbly Clouds",
        "icon": "☁️",
        "title": "Starlight Sky Realm of Kracko",
        "desc": "Fluffy levitating marshmallow clouds and crackling thunder skies.",
        "guardian": "Kracko",
        "enemies": ["Waddle Doo", "Sparky", "Flapper", "Scarfy"],
        "lootMultiplier": 1.25,
        "bg_color": C_CYAN
    },
    "magma_mountain": {
        "id": "magma_mountain",
        "name": "Magma Mountain",
        "icon": "🌋",
        "title": "Molten Volcanic Caverns",
        "desc": "Subterranean magma flumes, obsidian pillars, and searing heat waves.",
        "guardian": "Fire Lion",
        "enemies": ["Flamer", "Bobo", "Rocky", "Grizzo"],
        "lootMultiplier": 1.4,
        "bg_color": C_RED
    },
    "cyber_mesh": {
        "id": "cyber_mesh",
        "name": "Cyber Dream Net",
        "icon": "🌐",
        "title": "Pixel 9 Pro XL VirtIO-FS Digital Core",
        "desc": "Debian Linux AVF VM, Termux socket bridge, and fast virtiofs threads.",
        "guardian": "Kernel Memory Anomaly",
        "enemies": ["Packet Glitch", "Null Pointer Gremlin", "Zombie Process", "Bit-Flip Bug"],
        "lootMultiplier": 1.5,
        "bg_color": C_PURPLE
    },
    "halberd": {
        "id": "halberd",
        "name": "Battleship Halberd",
        "icon": "🚢",
        "title": "Meta Knight's Flying Dreadnought",
        "desc": "Iron skyship hulls, deck cannons, and the twin-wing observation deck.",
        "guardian": "Meta Knight",
        "enemies": ["Meta-Axe Knight", "Meta-Mace Knight", "Javelin Knight", "Heavy Lobster"],
        "lootMultiplier": 1.75,
        "bg_color": C_YELLOW
    },
    "fountain_of_dreams": {
        "id": "fountain_of_dreams",
        "name": "Fountain of Dreams",
        "icon": "⛲",
        "title": "Sacred Star Rod Sanctuary",
        "desc": "Crystalline rainbow cascades where all good dreams in the universe originate.",
        "guardian": "Nightmare Wizard",
        "enemies": ["Star Phantom", "Dream Mirage", "Cosmic Jester", "Nebula Shade"],
        "lootMultiplier": 2.0,
        "bg_color": C_GOLD
    }
}


def load_quest_state() -> Dict[str, Any]:
    if QUEST_STATE_FILE.exists():
        try:
            with open(QUEST_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    state = {
        "totalExpeditions": 0,
        "completedExpeditions": 0,
        "totalStarCoinsFound": 0,
        "totalChestsOpened": 0,
        "guardiansDefeated": [],
        "artifactsDiscovered": [],
        "unlockedRegions": ["green_greens", "bubbly_clouds", "magma_mountain", "cyber_mesh", "halberd", "fountain_of_dreams"],
        "lastExpedition": None
    }
    save_quest_state(state)
    return state


def save_quest_state(state: Dict[str, Any]):
    state["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(QUEST_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def award_pet_loot(coins: int, xp: int, treats: int = 0):
    if not PET_STATE_FILE.exists():
        return
    try:
        with open(PET_STATE_FILE, "r", encoding="utf-8") as f:
            pet = json.load(f)
        pet["starCoins"] = pet.get("starCoins", 0) + coins
        pet["bondXp"] = pet.get("bondXp", 0) + xp
        if treats > 0:
            pet["totalTreatsEaten"] = pet.get("totalTreatsEaten", 0) + treats
        # Check level up
        while pet["bondXp"] >= pet.get("bondXpNext", 500):
            pet["bondLevel"] = pet.get("bondLevel", 1) + 1
            pet["bondXp"] -= pet["bondXpNext"]
            pet["bondXpNext"] = int(pet["bondXpNext"] * 1.35)
            pet["starCoins"] += 50
        with open(PET_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(pet, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def record_ledger(action: str, details: str, xp: int = 0):
    try:
        LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "action": f"QUEST_{action.upper()}",
            "details": details,
            "xpGained": xp
        }
        with open(LEDGER_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def run_expedition(region_key: str, auto_mode: bool = False):
    region_key = region_key.lower().strip().replace("-", "_").replace(" ", "_")
    if region_key not in REGIONS:
        matched = [k for k in REGIONS if region_key in k]
        if matched:
            region_key = matched[0]
        else:
            region_key = "green_greens"

    reg = REGIONS[region_key]
    state = load_quest_state()
    state["totalExpeditions"] += 1

    print(f"\n{C_BOLD}{C_PINK}╔══════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║ {C_YELLOW}⭐ 🌸  DREAM LAND EXPEDITION: {reg['name'].upper()} {reg['icon']}  🌸 ⭐{C_PINK} ║{C_RESET}")
    print(f"{C_BOLD}{C_PINK}╠══════════════════════════════════════════════════════════════════════╣{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║{C_RESET} {reg['bg_color']}{reg['title']}{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║{C_RESET} {C_DIM}{reg['desc']}{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║{C_RESET} Guardian: {C_BOLD}{C_RED}{reg['guardian']}{C_RESET} | Loot Multiplier: {C_GOLD}{reg['lootMultiplier']}x{C_RESET}")
    print(f"{C_BOLD}{C_PINK}╚══════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

    if HAS_AUDIO:
        try:
            play_sound_preset("warp")
        except Exception:
            pass

    time.sleep(0.6)

    # Generate 4 procedural nodes
    nodes = ["ENEMY", "PUZZLE", "CHEST", "GUARDIAN"]
    coins_gained = 0
    xp_gained = 0
    chests_opened = 0
    kirby_hp = 100

    for idx, node_type in enumerate(nodes, 1):
        print(f"{C_BOLD}{C_CYAN}─── [Node {idx}/4] ───{C_RESET}")

        if node_type == "ENEMY":
            enemy = random.choice(reg["enemies"])
            print(f"  {C_YELLOW}⚠️  A wild {C_BOLD}{enemy}{C_RESET}{C_YELLOW} leaps from the shadows!{C_RESET}")
            if auto_mode:
                action = random.choice(["INHALE", "STRIKE"])
                print(f"  {C_PINK}[Auto-Pilot]{C_RESET} Kirby chose: {C_BOLD}{action}!{C_RESET}")
            else:
                print(f"  {C_WHITE}What should Kirby do? [1] Hypernova Inhale  [2] Sword Strike  [3] Star Dash{C_RESET}")
                # Simple prompt with default
                time.sleep(0.4)
                action = "INHALE"

            if action in ("INHALE", "1"):
                print(f"  {C_PINK}( ⭕ 0 ⭕ ) 彡 彡 彡 *VORTEX INHALE!*{C_RESET}")
                print(f"  {C_GREEN}[✔] Inhaled {enemy}! Absorbed combat experience! (+40 XP){C_RESET}")
                xp_gained += 40
            else:
                print(f"  {C_CYAN}⚔️ Kirby delivered a radiant starlight slash! (+50 XP){C_RESET}")
                xp_gained += 50

            if HAS_AUDIO:
                try:
                    play_sound_preset("kirby")
                except Exception:
                    pass

        elif node_type == "PUZZLE":
            puzzles = [
                ("Starlight Barrier Block", "Ultra Hammer", 30),
                ("Dark Abyssal Chasm", "Light-Bulb Luminescence", 35),
                ("Frozen Crystal Waterfall", "Inferno Fire", 40),
                ("High VirtIO-FS Latency Wall", "Mesh Bridge Harmonizer", 45)
            ]
            pname, req, coin_rew = random.choice(puzzles)
            print(f"  {C_PURPLE}🧩 Environmental Challenge: {C_BOLD}{pname}{C_RESET}")
            print(f"  {C_WHITE}Kirby activates copy ability synergy: {C_YELLOW}{req}{C_RESET}!")
            print(f"  {C_GREEN}[✔] Solved effortlessly! Barrier shattered! (+{coin_rew} Star Coins){C_RESET}")
            coins_gained += int(coin_rew * reg["lootMultiplier"])
            xp_gained += 35

        elif node_type == "CHEST":
            chest_coins = random.randint(30, 80)
            chests_opened += 1
            print(f"  {C_GOLD}📦 Gleaming Ancient Treasure Chest discovered! *CREEEAK*{C_RESET}")
            print(f"  {C_GOLD}✨ Found: {chest_coins} Star Coins 🪙 and a delicious Maxi Tomato 🍅!{C_RESET}")
            coins_gained += int(chest_coins * reg["lootMultiplier"])
            xp_gained += 50
            if HAS_AUDIO:
                try:
                    play_sound_preset("glass_ping")
                except Exception:
                    pass

        elif node_type == "GUARDIAN":
            guardian = reg["guardian"]
            print(f"  {C_BOLD}{C_RED}👑 REGION GUARDIAN: {guardian.upper()} STANDS BEFORE YOU!{C_RESET}")
            time.sleep(0.5)
            print(f"  {C_PINK}(•̀ᴗ•́)و 🌸 Kirby brandishes his Ultra Star Blade!{C_RESET}")
            time.sleep(0.4)
            print(f"  {C_YELLOW}⚡ CLASH! Cosmic shockwaves illuminate the realm!{C_RESET}")
            time.sleep(0.4)
            print(f"  {C_BOLD}{C_GREEN}✨ CRITICAL FINISHER! {guardian} defeated with honor! Poyo! 🎉{C_RESET}")
            boss_coins = int(random.randint(60, 120) * reg["lootMultiplier"])
            coins_gained += boss_coins
            xp_gained += 120
            if guardian not in state.get("guardiansDefeated", []):
                state.setdefault("guardiansDefeated", []).append(guardian)

            if HAS_AUDIO:
                try:
                    play_sound_preset("fanfare")
                except Exception:
                    pass

        print()
        time.sleep(0.3)

    # Finalize expedition
    state["completedExpeditions"] += 1
    state["totalStarCoinsFound"] += coins_gained
    state["totalChestsOpened"] += chests_opened
    state["lastExpedition"] = {
        "region": reg["name"],
        "coins": coins_gained,
        "xp": xp_gained,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    save_quest_state(state)
    award_pet_loot(coins=coins_gained, xp=xp_gained, treats=1)
    record_ledger("EXPEDITION_COMPLETE", f"Explored {reg['name']}, cleared {reg['guardian']}", xp=xp_gained)

    print(f"{C_BOLD}{C_GREEN}══════════════════════════════════════════════════════════════════════{C_RESET}")
    print(f"{C_BOLD}{C_GREEN}🌸 EXPEDITION VICTORIOUS! {reg['name'].upper()} CONQUERED! 🌸{C_RESET}")
    print(f"  Total Star Coins Reaped: {C_GOLD}+{coins_gained} 🪙{C_RESET}")
    print(f"  Total Experience Earned: {C_PURPLE}+{xp_gained} XP{C_RESET}")
    print(f"  Total Expeditions Cleared: {C_WHITE}{state['completedExpeditions']}{C_RESET}")
    print(f"{C_BOLD}{C_GREEN}══════════════════════════════════════════════════════════════════════{C_RESET}\n")


def cmd_list_regions():
    print(f"\n{C_BOLD}{C_PINK}🗺️  DREAM LAND EXPEDITION DESTINATIONS  🗺️{C_RESET}")
    print(f"{'REGION KEY':<22} {'REALM NAME':<24} {'GUARDIAN':<22} {'LOOT'}")
    print(f"{'─'*22} {'─'*24} {'─'*22} {'─'*6}")
    for k, v in REGIONS.items():
        print(f"{C_CYAN}{k:<22}{C_WHITE}{v['icon']} {v['name']:<22}{C_RED}{v['guardian']:<22}{C_GOLD}{v['lootMultiplier']}x{C_RESET}")
    print(f"\n{C_YELLOW}To embark on a quest:{C_RESET} {C_CYAN}kirby quest <region_key>{C_RESET} or {C_CYAN}kirby quest --auto{C_RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Kirby Dream Land Expeditions Engine")
    parser.add_argument("region", nargs="?", default=None, help="Region to explore")
    parser.add_argument("--auto", "-a", action="store_true", help="Run expedition in AI auto-pilot mode")
    parser.add_argument("--list", "-l", action="store_true", help="List available regions")

    args = parser.parse_args()

    if args.list:
        cmd_list_regions()
        return

    chosen_region = args.region or random.choice(list(REGIONS.keys()))
    run_expedition(chosen_region, auto_mode=args.auto)


if __name__ == "__main__":
    main()
