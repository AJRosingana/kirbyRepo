#!/usr/bin/env python3
"""
🌸 KIRBY TAMAGOTCHI & PET CARE SIMULATOR (kirby_pet_care.py) 🌸
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_pet_care.py
CLI: kirby pet | kirby feed <item> | kirby mood | kirby equip <ability>

Features:
- Real-time pet care simulation for Kirby on Pixel 9 Pro XL.
- Hunger, Happiness, Energy, Bond Level, and Mood state tracking.
- Gourmet snack pantry (Maxi Tomato, Strawberry Cake, Star Candy, etc.).
- Animated ASCII eating, petting, and joy reactions.
- Audio synthesis via agy_fx_engine.py and LRA haptic dispatch.
- Persistent state saved to /mnt/shared/AntiGravity_Shared/.kirby_pet_state.json.
================================================================================
"""

import os
import sys
import time
import json
import random
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Colors
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
STATE_FILE = BASE_DIR / ".kirby_pet_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"

HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


FOOD_PANTRY = {
    "maxi_tomato": {
        "name": "Maxi Tomato",
        "icon": "🍅",
        "hunger": 40,
        "happiness": 25,
        "energy": 35,
        "xp": 50,
        "sound": "kirby",
        "desc": "The legendary M-stamped tomato of Dream Land! Fully restores vitality!",
        "speech": "MAXI TOMATO!! Maximum vitality restored! Poyo! 🍅✨"
    },
    "strawberry_cake": {
        "name": "Strawberry Shortcake",
        "icon": "🍰",
        "hunger": 30,
        "happiness": 50,
        "energy": 20,
        "xp": 60,
        "sound": "kirby",
        "desc": "Kirby's all-time favorite dessert with fluffy cream and a ruby strawberry.",
        "speech": "STRAWBERRY SHORTCAKE! Absolute dessert heaven! 🍰💖"
    },
    "star_candy": {
        "name": "Star Candy",
        "icon": "⭐",
        "hunger": 15,
        "happiness": 35,
        "energy": 45,
        "xp": 75,
        "sound": "glass_ping",
        "desc": "Crystalline starlight confection crackling with cosmic mana.",
        "speech": "Star Candy crackle! Sparkling with cosmic stardust! ⭐✨"
    },
    "invincible_candy": {
        "name": "Invincible Candy",
        "icon": "🍭",
        "hunger": 20,
        "happiness": 50,
        "energy": 60,
        "xp": 100,
        "sound": "fanfare",
        "desc": "Spins with flashing rainbow aura! Grants temporary speed overdrive!",
        "speech": "INVINCIBLE CANDY! Rainbow speed surge engaged! 🍭🌈⚡"
    },
    "hot_curry": {
        "name": "Super Hot Curry",
        "icon": "🍛",
        "hunger": 45,
        "happiness": 30,
        "energy": 40,
        "xp": 65,
        "sound": "fire",
        "desc": "Spicy volcanic curry that makes Kirby breathe fiery plumes of joy!",
        "speech": "SPICY VOLCANIC CURRY! Breathing fire plumes! 🍛🔥"
    },
    "coffee": {
        "name": "Dream Land Espresso",
        "icon": "☕",
        "hunger": 10,
        "happiness": 20,
        "energy": 55,
        "xp": 40,
        "sound": "relay_snap",
        "desc": "Steaming roasted coffee mug giving a prompt boost of developer energy.",
        "speech": "Espresso roast! Fully charged and bug-free! ☕⚡"
    },
    "apple": {
        "name": "Whispy Apple",
        "icon": "🍎",
        "hunger": 25,
        "happiness": 20,
        "energy": 15,
        "xp": 30,
        "sound": "hop",
        "desc": "Crisp red apple freshly fallen from Whispy Woods' branches.",
        "speech": "Sweet crunchy Whispy apple! Delicious! 🍎🍃"
    },
    "melon": {
        "name": "Emerald Melon",
        "icon": "🍈",
        "hunger": 30,
        "happiness": 25,
        "energy": 20,
        "xp": 35,
        "sound": "hop",
        "desc": "Juicy sweet melon slice refreshing on warm Pixel days.",
        "speech": "Cool refreshing emerald melon! 🍈💦"
    },
    "pizza": {
        "name": "Cheesy Star Pizza",
        "icon": "🍕",
        "hunger": 50,
        "happiness": 40,
        "energy": 30,
        "xp": 55,
        "sound": "cherry_blue",
        "desc": "Wood-fired pizza topped with star cheese and savory herbs.",
        "speech": "Cheesy star pizza slice! Yum yum poyo! 🍕🧀"
    },
    "cham_chowder": {
        "name": "Cham Chowder Bread Bowl",
        "icon": "🍲",
        "hunger": 65,
        "happiness": 65,
        "energy": 55,
        "xp": 125,
        "sound": "kirby",
        "desc": "Piping hot New England clam chowder in a scooped sourdough bread bowl floating on molten fondue!",
        "speech": "CHAM CHOWDER BREAD BOWL!! Creamy savory perfection flowting in fondouzle glory! 🍲✨🥖"
    },
    "fondouzle_bread_bowl": {
        "name": "Fondouzle Chowder Bread Bowl Flotilla",
        "icon": "🫕",
        "hunger": 85,
        "happiness": 90,
        "energy": 75,
        "xp": 175,
        "sound": "fanfare",
        "desc": "Grand sourdough chowder bowl drifting down the Archimedes molten cheese fondouzle stream!",
        "speech": "THE FONDOUZLE FLOTILLA!! Melted cheese canals and chowder bread bowls! Poyo supreme! 🫕⭐🚢"
    }
}



def load_pet_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
                return state
        except Exception:
            pass

    # Default state
    state = {
        "name": "Kirby",
        "hunger": 75,
        "happiness": 85,
        "energy": 90,
        "bondLevel": 5,
        "bondXp": 320,
        "bondXpNext": 500,
        "starCoins": 120,
        "totalTreatsEaten": 14,
        "totalPetsReceived": 28,
        "currentAbility": "Ultra Sword",
        "currentMood": "Ecstatic",
        "favoriteFood": "Strawberry Shortcake",
        "lastFed": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "lastPet": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    save_pet_state(state)
    return state


def save_pet_state(state: Dict[str, Any]):
    state["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def record_ledger(action: str, details: str, xp: int = 0):
    try:
        LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "action": f"PET_{action.upper()}",
            "details": details,
            "xpGained": xp
        }
        with open(LEDGER_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def draw_bar(val: int, max_val: int = 100, length: int = 20, fill_color: str = C_GREEN) -> str:
    filled = int((val / max_val) * length)
    filled = max(0, min(length, filled))
    empty = length - filled
    return f"{fill_color}{'█' * filled}{C_DIM}{'░' * empty}{C_RESET} {val:>3}/{max_val}"


def recalculate_mood(state: Dict[str, Any]) -> str:
    h = state.get("hunger", 50)
    hap = state.get("happiness", 50)
    e = state.get("energy", 50)

    if h < 25:
        return "Starving"
    elif e < 25:
        return "Exhausted"
    elif hap < 30:
        return "Lonely"
    elif h >= 80 and hap >= 80 and e >= 80:
        return "Ecstatic"
    elif e >= 80:
        return "Energetic"
    elif hap >= 70:
        return "Playful"
    elif h >= 70:
        return "Content"
    else:
        return "Dreamy"


def cmd_mood():
    state = load_pet_state()
    state["currentMood"] = recalculate_mood(state)
    save_pet_state(state)

    mood = state["currentMood"]
    name = state["name"]
    level = state["bondLevel"]
    xp = state["bondXp"]
    xp_next = state["bondXpNext"]
    coins = state.get("starCoins", 0)
    ability = state.get("currentAbility", "None")

    print(f"\n{C_BOLD}{C_PINK}╔══════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║ {C_YELLOW}⭐ 🌸  KIRBY COMPANION PET STATUS & DEV COMPENDIUM HUD  🌸 ⭐{C_PINK}  ║{C_RESET}")
    print(f"{C_BOLD}{C_PINK}╠══════════════════════════════════════════════════════════════════════╣{C_RESET}")

    portrait = [
        f"        {C_PINK}.-------.{C_RESET}        {C_WHITE}Name:{C_RESET} {C_BOLD}{C_PINK}{name}{C_RESET}  {C_DIM}|{C_RESET}  {C_YELLOW}Bond Level:{C_RESET} {C_BOLD}Lv.{level}{C_RESET}",
        f"      {C_PINK}/   {C_WHITE}•   •{C_PINK}   \\{C_RESET}      {C_WHITE}Mood:{C_RESET} {C_BOLD}{C_HOT_PINK}{mood} 💖{C_RESET}  {C_DIM}|{C_RESET}  {C_GOLD}Star Coins:{C_RESET} {C_BOLD}{coins} 🪙{C_RESET}",
        f"     {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK} |{C_RESET}     {C_WHITE}Ability:{C_RESET} {C_CYAN}{ability} ✨{C_RESET}",
        f"   {C_PINK}c( \\     -     / ){C_RESET}   {C_WHITE}Favorite:{C_RESET} {C_HOT_PINK}{state.get('favoriteFood')}{C_RESET}",
        f"       {C_PINK}\\ .______. /{C_RESET}",
        f"        {C_PINK}'-......-'{C_RESET}",
        f"        {C_RED}(____)(____){C_RESET}",
    ]

    for line in portrait:
        # Pad lines to fit inside border
        print(f"{C_BOLD}{C_PINK}║{C_RESET} {line:<80} {C_BOLD}{C_PINK}║{C_RESET}")

    print(f"{C_BOLD}{C_PINK}╟──────────────────────────────────────────────────────────────────────╢{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║{C_RESET}  {C_WHITE}Hunger / Satiety:{C_RESET}  {draw_bar(state['hunger'], 100, 24, C_YELLOW)}  {C_DIM}Treats Eaten: {state.get('totalTreatsEaten', 0)}{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║{C_RESET}  {C_WHITE}Happiness Meter: {C_RESET}  {draw_bar(state['happiness'], 100, 24, C_PINK)}  {C_DIM}Pets Received: {state.get('totalPetsReceived', 0)}{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║{C_RESET}  {C_WHITE}Energy Reserve:  {C_RESET}  {draw_bar(state['energy'], 100, 24, C_CYAN)}  {C_DIM}Host: Pixel 9 Pro XL{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║{C_RESET}  {C_WHITE}Bond Progress:   {C_RESET}  {draw_bar(xp, xp_next, 24, C_PURPLE)}  {C_DIM}Next Lv: {xp_next - xp} XP{C_RESET}")
    print(f"{C_BOLD}{C_PINK}╚══════════════════════════════════════════════════════════════════════╝{C_RESET}\n")


def cmd_pet():
    state = load_pet_state()
    print(f"\n{C_BOLD}{C_PINK}[*] Gently reaching out to pet Kirby... (*^ ‿ ^*){C_RESET}")
    time.sleep(0.3)

    frames = [
        f"     {C_PINK}.-------.{C_RESET}\n   {C_PINK}/   {C_WHITE}•   •{C_PINK}   \\{C_RESET}\n  {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK} |{C_RESET}  {C_WHITE}*pat pat*{C_RESET}",
        f"     {C_PINK}.-------.{C_RESET}\n   {C_PINK}/   {C_WHITE}>   <{C_PINK}   \\{C_RESET}\n  {C_PINK}|  {C_HOT_PINK}(♥){C_PINK} ▿ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}  {C_HOT_PINK}*purr purr~*{C_RESET}",
        f"     {C_PINK}.-------.{C_RESET}  {C_YELLOW}★ {C_WHITE}✦{C_RESET}\n   {C_PINK}/   {C_WHITE}^   ^{C_PINK}   \\{C_RESET}\n  {C_PINK}|  {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}  {C_BOLD}{C_PINK}POYO! 💖 💕 ✨{C_RESET}"
    ]

    for frame in frames:
        print("\033[H\033[J" + frame)
        time.sleep(0.4)

    state["happiness"] = min(100, state.get("happiness", 50) + 15)
    state["energy"] = min(100, state.get("energy", 50) + 5)
    state["totalPetsReceived"] = state.get("totalPetsReceived", 0) + 1
    state["bondXp"] = state.get("bondXp", 0) + 25

    # Check level up
    level_up = False
    if state["bondXp"] >= state["bondXpNext"]:
        state["bondLevel"] += 1
        state["bondXp"] -= state["bondXpNext"]
        state["bondXpNext"] = int(state["bondXpNext"] * 1.35)
        state["starCoins"] = state.get("starCoins", 0) + 50
        level_up = True

    state["currentMood"] = recalculate_mood(state)
    state["lastPet"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    save_pet_state(state)

    if HAS_AUDIO:
        try:
            play_sound_preset("hop")
        except Exception:
            pass

    record_ledger("PET_KIRBY", "Pet Kirby and gave head pats", xp=25)

    print(f"\n{C_BOLD}{C_GREEN}[✔] Kirby is glowing with warmth and happiness! (Poyo! 🌸){C_RESET}")
    print(f"    Happiness: {C_PINK}+{15}{C_RESET} | Bond XP: {C_PURPLE}+{25}{C_RESET}")
    if level_up:
        print(f"    {C_BOLD}{C_YELLOW}🎉 BOND LEVEL UP! Kirby reached Bond Level {state['bondLevel']}! (+50 Star Coins 🪙){C_RESET}")
    print()


def cmd_feed(food_arg: Optional[str] = None):
    if not food_arg:
        print(f"\n{C_BOLD}{C_PINK}🍽️  DREAM LAND GOURMET PANTRY  🍽️{C_RESET}")
        print(f"{'ITEM KEY':<20} {'NAME':<24} {'EFFECTS':<32} {'DESCRIPTION'}")
        print(f"{'─'*20} {'─'*24} {'─'*32} {'─'*25}")
        for k, v in FOOD_PANTRY.items():
            eff = f"Hunger +{v['hunger']} | Happy +{v['happiness']}"
            print(f"{C_CYAN}{k:<20}{C_WHITE}{v['icon']} {v['name']:<22}{C_YELLOW}{eff:<32}{C_DIM}{v['desc'][:25]}...{C_RESET}")
        print(f"\n{C_YELLOW}Usage: kirby feed <food_key>{C_RESET}  (e.g., {C_CYAN}kirby feed strawberry_cake{C_RESET})\n")
        return

    key = food_arg.lower().strip().replace("-", "_").replace(" ", "_")
    if key not in FOOD_PANTRY:
        # Match prefix or substring
        matched = [k for k in FOOD_PANTRY if key in k]
        if matched:
            key = matched[0]
        else:
            print(f"{C_RED}Error:{C_RESET} Unknown food item '{food_arg}'. Run 'kirby feed' to see the pantry!")
            return

    item = FOOD_PANTRY[key]
    state = load_pet_state()

    print(f"\n{C_BOLD}{C_PINK}[*] Offering delicious {item['icon']} {item['name']} to Kirby...{C_RESET}\n")

    # Animated eating
    frames = [
        f"     {C_PINK}.-------.{C_RESET}\n   {C_PINK}/   {C_WHITE}O   O{C_PINK}   \\{C_RESET}    {item['icon']} {C_WHITE}*gasps with joy!*{C_RESET}\n  {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ᗜ {C_HOT_PINK}(♥){C_PINK} |{C_RESET}",
        f"     {C_PINK}.-------.{C_RESET}\n   {C_PINK}/   {C_WHITE}>   <{C_PINK}   \\{C_RESET}   {C_YELLOW}*NOM NOM NOM!*{C_RESET}\n  {C_PINK}|  {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}   {C_WHITE}*gulp!*{C_RESET}",
        f"     {C_PINK}.-------.{C_RESET}  {C_YELLOW}★ {C_WHITE}✦{C_RESET}\n   {C_PINK}/   {C_WHITE}^   ^{C_PINK}   \\{C_RESET}\n  {C_PINK}|  {C_HOT_PINK}(♥){C_PINK} ▽ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}  {C_BOLD}{C_PINK}\"{item['speech']}\"{C_RESET}"
    ]

    for f in frames:
        print("\033[H\033[J" + f)
        time.sleep(0.4)

    state["hunger"] = min(100, state.get("hunger", 50) + item["hunger"])
    state["happiness"] = min(100, state.get("happiness", 50) + item["happiness"])
    state["energy"] = min(100, state.get("energy", 50) + item["energy"])
    state["totalTreatsEaten"] = state.get("totalTreatsEaten", 0) + 1
    state["bondXp"] = state.get("bondXp", 0) + item["xp"]

    level_up = False
    if state["bondXp"] >= state["bondXpNext"]:
        state["bondLevel"] += 1
        state["bondXp"] -= state["bondXpNext"]
        state["bondXpNext"] = int(state["bondXpNext"] * 1.35)
        state["starCoins"] = state.get("starCoins", 0) + 50
        level_up = True

    state["currentMood"] = recalculate_mood(state)
    state["lastFed"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    save_pet_state(state)

    if HAS_AUDIO:
        try:
            play_sound_preset(item.get("sound", "kirby"))
        except Exception:
            pass

    record_ledger("FEED_KIRBY", f"Fed Kirby {item['name']}", xp=item["xp"])

    print(f"\n{C_BOLD}{C_GREEN}[✔] Kirby happily devoured the {item['name']}!{C_RESET}")
    print(f"    Hunger: {C_YELLOW}+{item['hunger']}{C_RESET} | Happiness: {C_PINK}+{item['happiness']}{C_RESET} | Energy: {C_CYAN}+{item['energy']}{C_RESET} | Bond XP: {C_PURPLE}+{item['xp']}{C_RESET}")
    if level_up:
        print(f"    {C_BOLD}{C_YELLOW}🎉 BOND LEVEL UP! Kirby reached Bond Level {state['bondLevel']}! (+50 Star Coins 🪙){C_RESET}")
    print()


def cmd_equip(ability: Optional[str] = None):
    state = load_pet_state()
    if not ability:
        print(f"\n{C_CYAN}Current Equipped Ability:{C_RESET} {C_BOLD}{C_YELLOW}{state.get('currentAbility', 'Normal')}{C_RESET}")
        print(f"To equip a new ability: {C_CYAN}kirby equip <ability_name>{C_RESET}")
        return

    state["currentAbility"] = ability.title()
    save_pet_state(state)
    record_ledger("EQUIP_ABILITY", f"Equipped copy ability {ability.title()}")
    print(f"{C_BOLD}{C_GREEN}[✔] Kirby equipped copy ability: {ability.title()}! Poyo! ⚔️✨{C_RESET}")


def main():
    parser = argparse.ArgumentParser(description="Kirby Companion Pet Care Engine")
    subparsers = parser.add_subparsers(dest="subcommand")

    subparsers.add_parser("mood", help="Display Kirby's pet status, mood, and HUD")
    subparsers.add_parser("status", help="Alias for mood")
    subparsers.add_parser("pet", help="Pet Kirby with loving affection")

    p_feed = subparsers.add_parser("feed", help="Feed Kirby delicious Dream Land food")
    p_feed.add_argument("food", nargs="?", default=None, help="Name of food item")

    p_equip = subparsers.add_parser("equip", help="Equip an active copy ability onto Kirby")
    p_equip.add_argument("ability", nargs="?", default=None, help="Ability name")

    args = parser.parse_args()

    if args.subcommand in ("mood", "status") or not args.subcommand:
        cmd_mood()
    elif args.subcommand == "pet":
        cmd_pet()
    elif args.subcommand == "feed":
        cmd_feed(args.food)
    elif args.subcommand == "equip":
        cmd_equip(args.ability)


if __name__ == "__main__":
    main()
