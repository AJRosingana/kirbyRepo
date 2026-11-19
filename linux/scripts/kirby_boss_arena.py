#!/usr/bin/env python3
"""
⚔️ KIRBY DREAM LAND BOSS ARENA & COLOSSEUM (kirby_boss_arena.py) ⚔️
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_boss_arena.py
CLI: kirby boss [boss_name] [--auto] | kirby duel | kirby brawl

Features:
- Turn-based / tactical boss colosseum pitting Kirby against 5 iconic bosses:
  1. Whispy Woods (Apple Drops, Gale Breath, Root Spikes)
  2. King Dedede (Hammer Pound, Royal Inhale, Super Jump)
  3. Meta Knight (Mach Tornado, Sword Beam, Knight's Thrust)
  4. Kracko (Thunderbolt Barrage, Rainstorm, Waddle Doo Summon)
  5. Marx Cosmic Jester (Black Hole, Cutter Wings, Cosmic Laser)
- Copy Ability selection: Ultra Sword, Inferno Fire, Plasma Spark, Mega Hammer, Mecha Overdrive.
- Visual ANSI HP health meters, combat logs, sound effects, and LRA haptics.
- Persistent victory trophies saved to /mnt/shared/AntiGravity_Shared/.kirby_boss_trophies.json.
================================================================================
"""

import os
import sys
import time
import json
import random
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
TROPHY_FILE = BASE_DIR / ".kirby_boss_trophies.json"
PET_STATE_FILE = BASE_DIR / ".kirby_pet_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"

HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


BOSSES = {
    "whispy": {
        "id": "whispy",
        "name": "Whispy Woods",
        "title": "Ancient Forest Patriarch",
        "icon": "🌳",
        "maxHp": 400,
        "rewardCoins": 150,
        "rewardXp": 200,
        "attacks": [
            ("Apple Bomb Drop", 25, "Drops ripe explosive apples from overhead branches!"),
            ("Gale Breath Gust", 20, "Blows mighty wind gusts pushing Kirby back!"),
            ("Root Spike Tremor", 35, "Spikes erupt from the soil beneath Kirby!")
        ]
    },
    "dedede": {
        "id": "dedede",
        "name": "King Dedede",
        "title": "Self-Proclaimed King of Dream Land",
        "icon": "👑",
        "maxHp": 650,
        "rewardCoins": 250,
        "rewardXp": 350,
        "attacks": [
            ("Super Hammer Slam", 45, "Swings his massive wooden mallet with earthquake force!"),
            ("Royal Inhale Battle", 30, "Opens mouth in a competing royal suction vortex!"),
            ("Super Dedede Belly Flop", 50, "Leaps 50 feet into the air and crashes downward!")
        ]
    },
    "meta_knight": {
        "id": "meta_knight",
        "name": "Meta Knight",
        "title": "Master of the Galaxia Sword",
        "icon": "⚔️",
        "maxHp": 800,
        "rewardCoins": 350,
        "rewardXp": 500,
        "attacks": [
            ("Mach Tornado", 50, "Spins into a sonic tornado slashing with the Galaxia blade!"),
            ("Sword Beam Shockwave", 40, "Unleashes razor-sharp glowing crescent energy arcs!"),
            ("Knightly Piercing Thrust", 45, "Lunges across the arena with lightning rapier speed!")
        ]
    },
    "kracko": {
        "id": "kracko",
        "name": "Kracko",
        "title": "One-Eyed Thunder Lord",
        "icon": "⚡",
        "maxHp": 750,
        "rewardCoins": 300,
        "rewardXp": 450,
        "attacks": [
            ("Thunderbolt Lightning Strike", 45, "Channels 50,000 volts of plasma directly down!"),
            ("Rainstorm Drench", 30, "Summons torrential storm rain chilling the arena!"),
            ("Waddle Doo Beam Dropper", 40, "Drops beam-firing minions across the floor!")
        ]
    },
    "marx": {
        "id": "marx",
        "name": "Marx",
        "title": "Cosmic Jester of Chaos",
        "icon": "🃏",
        "maxHp": 1000,
        "rewardCoins": 500,
        "rewardXp": 750,
        "attacks": [
            ("Black Hole Gravity Well", 65, "Opens an abyssal cosmic rift pulling all reality inward!"),
            ("Razor Cutter Wings", 45, "Fires four pairs of crescent energy blades!"),
            ("Cosmic Particle Laser", 60, "Fires a massive blinding beam tearing through space!")
        ]
    }
}

ABILITIES = {
    "sword": {
        "name": "Ultra Sword",
        "icon": "🗡️",
        "attackName": "Starlight Cleave",
        "baseDamage": 55,
        "specName": "Ultra Spin Slash",
        "specDamage": 110,
        "sound": "laser"
    },
    "fire": {
        "name": "Inferno Fire",
        "icon": "🔥",
        "attackName": "Flamethrower Breath",
        "baseDamage": 50,
        "specName": "Meteor Flame Dash",
        "specDamage": 105,
        "sound": "fire"
    },
    "spark": {
        "name": "Plasma Spark",
        "icon": "⚡",
        "attackName": "Electric Shock",
        "baseDamage": 45,
        "specName": "Gigavolt Lightning Dome",
        "specDamage": 120,
        "sound": "laser"
    },
    "hammer": {
        "name": "Mega Hammer",
        "icon": "🔨",
        "attackName": "Giant Mallet Pound",
        "baseDamage": 65,
        "specName": "Volcano Hammer Cataclysm",
        "specDamage": 130,
        "sound": "hammer"
    },
    "mecha": {
        "name": "Mecha Overdrive",
        "icon": "🤖",
        "attackName": "Twin Arm Blasters",
        "baseDamage": 50,
        "specName": "Hyper Jet Cannon",
        "specDamage": 115,
        "sound": "laser"
    }
}


def load_trophies() -> Dict[str, Any]:
    if TROPHY_FILE.exists():
        try:
            with open(TROPHY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    state = {
        "totalVictories": 0,
        "defeatedBosses": {},
        "currentArenaRank": "Bronze Brawler",
        "trophies": []
    }
    save_trophies(state)
    return state


def save_trophies(data: Dict[str, Any]):
    data["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(TROPHY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def award_pet_loot(coins: int, xp: int):
    if not PET_STATE_FILE.exists():
        return
    try:
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


def draw_hp_bar(cur: int, max_hp: int, length: int = 24, fill_col: str = C_GREEN) -> str:
    cur = max(0, cur)
    pct = cur / max_hp
    filled = int(pct * length)
    empty = length - filled
    return f"{fill_col}{'█' * filled}{C_DIM}{'░' * empty}{C_RESET} {cur:>4}/{max_hp}"


def run_boss_fight(boss_key: str, ability_key: str = "sword", auto_mode: bool = False):
    boss_key = boss_key.lower().strip().replace("-", "_").replace(" ", "_")
    if boss_key not in BOSSES:
        matched = [k for k in BOSSES if boss_key in k]
        boss_key = matched[0] if matched else "whispy"

    boss = BOSSES[boss_key]
    ab = ABILITIES.get(ability_key, ABILITIES["sword"])

    kirby_max_hp = 200
    kirby_hp = kirby_max_hp
    kirby_sp = 50
    boss_hp = boss["maxHp"]
    tomatoes_left = 2

    print(f"\n{C_BOLD}{C_RED}╔══════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_RED}║ ⚔️  DREAM LAND BOSS COLOSSEUM: {boss['name'].upper()} {boss['icon']}  ⚔️ ║{C_RESET}")
    print(f"{C_BOLD}{C_RED}╠══════════════════════════════════════════════════════════════════════╣{C_RESET}")
    print(f"{C_BOLD}{C_RED}║{C_RESET} Opponent: {C_BOLD}{C_YELLOW}{boss['name']}{C_RESET} ({boss['title']})")
    print(f"{C_BOLD}{C_RED}║{C_RESET} Equipped Ability: {C_CYAN}{ab['icon']} {ab['name']}{C_RESET} | Kirby HP: {C_GREEN}200{C_RESET} | SP: {C_PURPLE}50{C_RESET}")
    print(f"{C_BOLD}{C_RED}╚══════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

    if HAS_AUDIO:
        try:
            play_sound_preset("laser")
        except Exception:
            pass

    time.sleep(0.8)
    turn = 1

    while kirby_hp > 0 and boss_hp > 0:
        print(f"{C_BOLD}{C_CYAN}─── [Round {turn}] ───{C_RESET}")
        print(f"  {C_PINK}Kirby:{C_RESET} {draw_hp_bar(kirby_hp, kirby_max_hp, 20, C_PINK)}  |  {C_PURPLE}SP:{C_RESET} {kirby_sp}/100  |  {C_RED}Tomatoes:{C_RESET} {tomatoes_left}")
        print(f"  {C_RED}{boss['name']}:{C_RESET} {draw_hp_bar(boss_hp, boss['maxHp'], 20, C_RED)}\n")

        # Player Action
        if auto_mode:
            if kirby_hp < 70 and tomatoes_left > 0:
                act = "3"
            elif kirby_sp >= 25:
                act = "2"
            else:
                act = "1"
        else:
            time.sleep(0.4)
            act = "2" if kirby_sp >= 25 else "1"

        if act == "3" and tomatoes_left > 0:
            # Eat Maxi Tomato
            tomatoes_left -= 1
            heal = 80
            kirby_hp = min(kirby_max_hp, kirby_hp + heal)
            print(f"  {C_BOLD}{C_GREEN}🍅 Kirby ate a Maxi Tomato! Restored +{heal} HP! Poyo!{C_RESET}")
            if HAS_AUDIO:
                try:
                    play_sound_preset("kirby")
                except Exception:
                    pass
        elif act == "2" and kirby_sp >= 25:
            # Special Move
            kirby_sp -= 25
            crit = random.choice([1.0, 1.25, 1.5])
            dmg = int(ab["specDamage"] * crit)
            boss_hp -= dmg
            crit_text = f" {C_BOLD}{C_YELLOW}★ CRITICAL HIT! ★{C_RESET}" if crit > 1.0 else ""
            print(f"  {C_BOLD}{C_CYAN}✨ SPECIAL MOVE: {ab['specName']}!!{crit_text}{C_RESET}")
            print(f"  {C_YELLOW}💥 Starlight energy blasts {boss['name']} for {C_BOLD}{dmg} damage!{C_RESET}")
            if HAS_AUDIO:
                try:
                    play_sound_preset(ab["sound"])
                except Exception:
                    pass
        else:
            # Basic Attack
            dmg = int(ab["baseDamage"] * random.uniform(0.9, 1.2))
            boss_hp -= dmg
            kirby_sp = min(100, kirby_sp + 15)
            print(f"  {C_BOLD}{C_WHITE}⚔️ {ab['name']} strikes with {ab['attackName']}!{C_RESET}")
            print(f"  {C_YELLOW}💥 Delivered {C_BOLD}{dmg} damage! (+15 SP){C_RESET}")
            if HAS_AUDIO:
                try:
                    play_sound_preset("hop")
                except Exception:
                    pass

        # Check Boss Defeat
        if boss_hp <= 0:
            break

        time.sleep(0.5)

        # Boss Counter-Attack
        b_att, b_dmg, b_desc = random.choice(boss["attacks"])
        actual_dmg = int(b_dmg * random.uniform(0.85, 1.15))
        # Chance for Kirby to dodge
        if random.random() < 0.20:
            print(f"  {C_BOLD}{C_YELLOW}🛡️ {boss['name']} used {b_att}! But Kirby backflipped and DODGED! Poyo!{C_RESET}\n")
        else:
            kirby_hp -= actual_dmg
            print(f"  {C_BOLD}{C_RED}⚠️ {boss['name']} unleashes {b_att}!{C_RESET}")
            print(f"     {C_DIM}{b_desc}{C_RESET}")
            print(f"     {C_RED}💥 Kirby took {actual_dmg} damage!{C_RESET}\n")

        turn += 1
        time.sleep(0.4)

    # Resolution
    trophies = load_trophies()
    if boss_hp <= 0:
        print(f"\n{C_BOLD}{C_GREEN}══════════════════════════════════════════════════════════════════════{C_RESET}")
        print(f"{C_BOLD}{C_GREEN}🎉 VICTORY! {boss['name'].upper()} WAS DEFEATED! 🌸 POYO! 🎉{C_RESET}")
        print(f"  Star Coins Awarded: {C_GOLD}+{boss['rewardCoins']} 🪙{C_RESET}")
        print(f"  Colosseum Experience: {C_PURPLE}+{boss['rewardXp']} XP{C_RESET}")
        print(f"{C_BOLD}{C_GREEN}══════════════════════════════════════════════════════════════════════{C_RESET}\n")

        trophies["totalVictories"] += 1
        trophies["defeatedBosses"][boss["name"]] = trophies["defeatedBosses"].get(boss["name"], 0) + 1
        t_name = f"{boss['name']} Colosseum Gold Trophy"
        if t_name not in trophies["trophies"]:
            trophies["trophies"].append(t_name)
            print(f"  {C_BOLD}{C_GOLD}🏆 NEW TROPHY UNLOCKED: {t_name}! 🏆{C_RESET}\n")

        save_trophies(trophies)
        award_pet_loot(boss["rewardCoins"], boss["rewardXp"])

        if HAS_AUDIO:
            try:
                play_sound_preset("fanfare")
            except Exception:
                pass
    else:
        print(f"\n{C_BOLD}{C_RED}💀 DEFEAT! Kirby retreated to Dream Land to rest and snack! 🌸{C_RESET}\n")


def cmd_list_bosses():
    print(f"\n{C_BOLD}{C_RED}👑  DREAM LAND BOSS COLOSSEUM ROSTER  👑{C_RESET}")
    print(f"{'BOSS KEY':<16} {'NAME':<20} {'HP':<8} {'REWARD':<14} {'TITLE'}")
    print(f"{'─'*16} {'─'*20} {'─'*8} {'─'*14} {'─'*25}")
    for k, v in BOSSES.items():
        print(f"{C_CYAN}{k:<16}{C_WHITE}{v['icon']} {v['name']:<18}{C_RED}{v['maxHp']:<8}{C_GOLD}{v['rewardCoins']} 🪙{C_RESET}     {C_DIM}{v['title']}{C_RESET}")
    print(f"\n{C_YELLOW}Usage:{C_RESET} {C_CYAN}kirby boss <boss_key>{C_RESET} or {C_CYAN}kirby boss <boss_key> --auto{C_RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Kirby Boss Colosseum Engine")
    parser.add_argument("boss", nargs="?", default=None, help="Boss key to fight")
    parser.add_argument("--ability", "-a", default="sword", help="Starting copy ability (sword|fire|spark|hammer|mecha)")
    parser.add_argument("--auto", action="store_true", help="Run in auto-battle mode")
    parser.add_argument("--list", "-l", action="store_true", help="List available bosses")

    args = parser.parse_args()

    if args.list:
        cmd_list_bosses()
        return

    boss_target = args.boss or random.choice(list(BOSSES.keys()))
    run_boss_fight(boss_target, ability_key=args.ability, auto_mode=args.auto)


if __name__ == "__main__":
    main()
