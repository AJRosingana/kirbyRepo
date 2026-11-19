#!/usr/bin/env python3
"""
🌸 KIRBY CARETAKER DUO & MUTUAL CAREGIVING ENGINE (kirby_caretakers.py) 🌸
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_caretakers.py
CLI: kirby caretaker [status|round|mutual|feed|tuck|assign]
     kirby caretakers | kirby buddy

Features:
1. Caretaker Duo:
   - Primary Manager & Caretaker: Bandana Waddle Dee 💙 (Clipboard, Spear & Blankets)
   - Secondary Assistant Caretaker: Chef Kawasaki 🍳 (Culinary Wellness & Hearty Stews)
2. Mutual Caregiving Protocol ("They take care of one another"):
   - Caretakers nurture each other (tea, massage, warm stew, rest shifts)
   - Squad buddies step up to care for their companions (Keeby, Prime, Freeze, etc.)
   - Kirbies give appreciation hugs & gifts back to the Caretaker Duo
3. Proactive Care Rounds (kirby caretaker round):
   - Audits all 8 Core Needs & 10 Squad Cravings
   - Dispatches custom care (meals, baths, bedtime tuck-ins, thermal chills)
   - Executes mutual care ritual between Bandana Dee and Chef Kawasaki
4. Real-time Synchronization with .kirby_needs_state.json and .kirby_caretakers_state.json
5. Audio FX & ANSI ASCII illustrated storyboards.
================================================================================
"""

import os
import sys
import time
import json
import random
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

# ANSI Palette
C_PINK = "\033[38;5;205m"
C_HOT_PINK = "\033[38;5;218m"
C_CYAN = "\033[38;5;81m"
C_YELLOW = "\033[38;5;220m"
C_GOLD = "\033[38;5;226m"
C_GREEN = "\033[38;5;120m"
C_PURPLE = "\033[38;5;141m"
C_RED = "\033[38;5;196m"
C_BLUE = "\033[38;5;39m"
C_WHITE = "\033[38;5;255m"
C_ORANGE = "\033[38;5;208m"
C_DIM = "\033[2m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

BASE_DIR = Path("/mnt/shared/AntiGravity_Shared")
CARETAKERS_STATE_FILE = BASE_DIR / ".kirby_caretakers_state.json"
NEEDS_STATE_FILE = BASE_DIR / ".kirby_needs_state.json"
PET_STATE_FILE = BASE_DIR / ".kirby_pet_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"

HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


DEFAULT_CARETAKERS_STATE = {
    "version": "1.0.0",
    "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "caretaker_duo": {
        "bandana_dee": {
            "id": "bandana_dee",
            "name": "Bandana Waddle Dee",
            "title": "Head Caretaker & Needs Operations Manager",
            "icon": "💙",
            "accessory": "Star Bandana & Golden Spear",
            "energy": 94,
            "affection": 98,
            "shift_status": "Active on Duty",
            "quote": "Everyone's pillows are fluffed and starlight blankets tucked! 💙",
            "acts_performed": 38
        },
        "chef_kawasaki": {
            "id": "chef_kawasaki",
            "name": "Chef Kawasaki",
            "title": "Culinary Wellness Assistant & Co-Caretaker",
            "icon": "🍳",
            "accessory": "Toque Blanche Hat, Frying Pan & Ladle",
            "energy": 91,
            "affection": 96,
            "shift_status": "Cooking Fresh Treats",
            "quote": "Hot Maxi-Tomato stew and strawberry tarts hot off the stove! 🍳✨",
            "acts_performed": 44
        }
    },
    "mutual_care_stats": {
        "mutual_harmony_level": 98,
        "duo_care_exchanges": 24,
        "squad_buddy_acts": 31,
        "last_mutual_ritual": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "last_round_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    },
    "recent_care_log": [
        {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "actor": "Chef Kawasaki", "recipient": "Bandana Dee", "act": "Served hot tomato ramen to recharge Dee after morning room sweep"},
        {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "actor": "Bandana Dee", "recipient": "Chef Kawasaki", "act": "Massaged Kawasaki's cooking shoulders and poured chamomile tea"},
        {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "actor": "Kirby Prime", "recipient": "Caretaker Duo", "act": "Gave huge squishy gratitude hug to both caretakers (Poyo!)"}
    ]
}


def load_caretakers_state() -> Dict[str, Any]:
    if CARETAKERS_STATE_FILE.exists():
        try:
            with open(CARETAKERS_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    state = json.loads(json.dumps(DEFAULT_CARETAKERS_STATE))
    save_caretakers_state(state)
    return state


def save_caretakers_state(state: Dict[str, Any]):
    state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        with open(CARETAKERS_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        sys.stderr.write(f"Error saving caretakers state: {e}\n")


def record_ledger(action: str, details: str, xp: int = 30):
    try:
        LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "action": f"CARETAKER_{action.upper()}",
            "details": details,
            "xpGained": xp
        }
        with open(LEDGER_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def draw_bar(val: int, max_val: int = 100, length: int = 16, color: str = C_GREEN) -> str:
    filled = int((val / max_val) * length)
    filled = max(0, min(length, filled))
    empty = length - filled
    return f"{color}{'█' * filled}{C_DIM}{'░' * empty}{C_RESET} {val:>3}%"


# --- Visual ASCII Portraits ---

def render_bandana_dee_portrait() -> List[str]:
    return [
        f"       {C_BLUE}.---'~~~'---.{C_RESET}       {C_GOLD}★{C_RESET} {C_BLUE}Star Bandana{C_RESET}",
        f"      {C_BLUE}/  ★ ========= \\{C_RESET}",
        f"     {C_ORANGE}|   {C_WHITE}(•)     (•){C_ORANGE}  |{C_RESET}     {C_BOLD}{C_BLUE}Bandana Waddle Dee{C_RESET}",
        f"     {C_ORANGE}|     {C_WHITE}( • ‿ • ){C_ORANGE}  |{C_RESET}     {C_CYAN}[Head Caretaker & Needs Manager]{C_RESET}",
        f"      {C_ORANGE}\\   .-------.  /{C_RESET}      {C_GOLD}Equipped: Clipboard & Starlight Spear{C_RESET}",
        f"       {C_ORANGE}'-'         '-'{C_RESET}",
        f"       {C_YELLOW}(____)   (____){C_RESET}"
    ]


def render_chef_kawasaki_portrait() -> List[str]:
    return [
        f"         {C_WHITE}.======.{C_RESET}",
        f"         {C_WHITE}| CHEF |{C_RESET}         {C_YELLOW}🍳 Culinary Wellness Assistant{C_RESET}",
        f"        {C_WHITE}.========.{C_RESET}",
        f"       {C_ORANGE}/  {C_WHITE}^    ^   {C_ORANGE}\\{C_RESET}      {C_BOLD}{C_YELLOW}Chef Kawasaki{C_RESET}",
        f"      {C_ORANGE}|  {C_WHITE}(•)  ‿ (•){C_ORANGE} |{C_RESET}      {C_PINK}[Second Co-Caretaker & Chef]{C_RESET}",
        f"      {C_ORANGE}|   \\ {C_RED}=={C_ORANGE} /    |{C_RESET}      {C_GOLD}Equipped: Iron Skillet & Honey Ladle{C_RESET}",
        f"       {C_ORANGE}\\  '----'   /{C_RESET}",
        f"        {C_RED}(____)(____){C_RESET}"
    ]


def cmd_status():
    st = load_caretakers_state()
    dee = st["caretaker_duo"]["bandana_dee"]
    chef = st["caretaker_duo"]["chef_kawasaki"]
    mutual = st["mutual_care_stats"]

    print(f"\n{C_BOLD}{C_CYAN}╔══════════════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║ {C_GOLD}⭐ 💙 🍳  KIRBY CARETAKER DUO & MUTUAL CAREGIVING HEADQUARTERS  🍳 💙 ⭐{C_CYAN}    ║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}╠══════════════════════════════════════════════════════════════════════════════════════╣{C_RESET}")

    # Bandana Dee Info
    p_dee = render_bandana_dee_portrait()
    print(f"{C_BOLD}{C_CYAN}║ {C_WHITE}{C_BOLD}1. PRIMARY CARETAKER & NEEDS MANAGER:{C_RESET}                                              {C_BOLD}{C_CYAN}║{C_RESET}")
    for line in p_dee:
        print(f"{C_BOLD}{C_CYAN}║{C_RESET}  {line:<86} {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║{C_RESET}     Energy: {draw_bar(dee['energy'], 100, 18, C_CYAN)}  Affection: {draw_bar(dee['affection'], 100, 18, C_PINK)}  Duty Acts: {C_BOLD}{dee['acts_performed']}{C_RESET} {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║{C_RESET}     {C_DIM}Status: {dee['shift_status']} • \"{dee['quote']}\"{C_RESET} {C_BOLD}{C_CYAN}║{C_RESET}")

    print(f"{C_BOLD}{C_CYAN}╟──────────────────────────────────────────────────────────────────────────────────────╢{C_RESET}")

    # Chef Kawasaki Info
    p_chef = render_chef_kawasaki_portrait()
    print(f"{C_BOLD}{C_CYAN}║ {C_WHITE}{C_BOLD}2. SECONDARY ASSISTANT CARETAKER (THE HELPER):{C_RESET}                                      {C_BOLD}{C_CYAN}║{C_RESET}")
    for line in p_chef:
        print(f"{C_BOLD}{C_CYAN}║{C_RESET}  {line:<86} {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║{C_RESET}     Energy: {draw_bar(chef['energy'], 100, 18, C_YELLOW)}  Affection: {draw_bar(chef['affection'], 100, 18, C_PINK)}  Meals Served: {C_BOLD}{chef['acts_performed']}{C_RESET} {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║{C_RESET}     {C_DIM}Status: {chef['shift_status']} • \"{chef['quote']}\"{C_RESET} {C_BOLD}{C_CYAN}║{C_RESET}")

    print(f"{C_BOLD}{C_CYAN}╟──────────────────────────────────────────────────────────────────────────────────────╢{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║ {C_GOLD}{C_BOLD}💞 MUTUAL CAREGIVING PROTOCOL (\"THEY TAKE CARE OF ONE ANOTHER\"):{C_RESET}                    {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}╟──────────────────────────────────────────────────────────────────────────────────────╢{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║{C_RESET}  Mutual Caregiver Harmony: {draw_bar(mutual['mutual_harmony_level'], 100, 24, C_GREEN)}   Duo Exchanges: {C_BOLD}{mutual['duo_care_exchanges']}{C_RESET} | Buddy Acts: {C_BOLD}{mutual['squad_buddy_acts']}{C_RESET}  {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║{C_RESET}  {C_DIM}Rule: When one caretaker is tired, the second steps in; they nurture each other & the squad.{C_RESET}  {C_BOLD}{C_CYAN}║{C_RESET}")

    print(f"{C_BOLD}{C_CYAN}╟──────────────────────────────────────────────────────────────────────────────────────╢{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║ {C_PINK}{C_BOLD}📜 RECENT ACTS OF MUTUAL & SQUAD COMPANION CARE:{C_RESET}                                       {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}╟──────────────────────────────────────────────────────────────────────────────────────╢{C_RESET}")

    for log in st.get("recent_care_log", [])[-4:]:
        actor = f"{C_BOLD}{log.get('actor')}{C_RESET}"
        recipient = f"{C_PINK}{log.get('recipient')}{C_RESET}"
        act = f"{C_WHITE}{log.get('act')}{C_RESET}"
        print(f"{C_BOLD}{C_CYAN}║{C_RESET}  • {actor} -> {recipient}: {act:<50} {C_BOLD}{C_CYAN}║{C_RESET}")

    print(f"{C_BOLD}{C_CYAN}╚══════════════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")


def action_round():
    """Performs a comprehensive Caretaker Duo care round."""
    st = load_caretakers_state()
    print(f"\n{C_BOLD}{C_CYAN}╔══════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║  ⭐ 💙 🍳  CARETAKER DUO DISPATCH: FULL SQUAD WELLNESS ROUND  🍳 💙 ⭐  ║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}╚══════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

    # Step 1: Bandana Dee Audits Needs
    print(f"{C_BOLD}{C_BLUE}[1/4] Bandana Waddle Dee reviewing Sanctuary Clipboard & Needs Matrix... 📋 💙{C_RESET}")
    time.sleep(0.4)
    print(f"      Bandana Dee: \"Checking on all 10 Kirbies... Prime needs shortcake, Freeze Kirby wants thermals chilled!\"")

    # Step 2: Chef Kawasaki Prepares Meals
    print(f"\n{C_BOLD}{C_YELLOW}[2/4] Chef Kawasaki firing up the dream stoves & baking fresh treats... 🍳 🥞{C_RESET}")
    frames_cooking = [
        f"        {C_WHITE}.======.{C_RESET}\n        {C_WHITE}| CHEF |{C_RESET}\n       {C_WHITE}.========.{C_RESET}\n      {C_ORANGE}/  {C_WHITE}O    O   {C_ORANGE}\\{C_RESET}   🍳 {C_YELLOW}*FLIP! Pan-tossing golden star pancakes!*{C_RESET}\n     {C_ORANGE}|  {C_WHITE}(•)  ‿ (•){C_ORANGE} |{C_RESET}",
        f"        {C_WHITE}.======.{C_RESET}\n        {C_WHITE}| CHEF |{C_RESET}\n       {C_WHITE}.========.{C_RESET}\n      {C_ORANGE}/  {C_WHITE}^    ^   {C_ORANGE}\\{C_RESET}   🍰 🍅 🍕 {C_BOLD}{C_GREEN}\"Hot Maxi-Tomato stew & Shortcake ready!\" 🍲 ✨{C_RESET}\n     {C_ORANGE}|  {C_WHITE}(•)  ▽ (•){C_ORANGE} |{C_RESET}"
    ]
    for f in frames_cooking:
        print("\033[H\033[J" + f)
        time.sleep(0.4)

    # Step 3: Fulfill in kirby_needs
    try:
        sys.path.insert(0, str(BASE_DIR / "scripts"))
        import kirby_needs
        kirby_needs.action_feed("strawberry_cake")
        kirby_needs.action_bath()
        kirby_needs.action_fengshui()
    except Exception as e:
        pass

    # Step 4: Mutual Care between Caretaker 1 and Caretaker 2
    action_mutual(skip_header=True)

    # Update state
    st["caretaker_duo"]["bandana_dee"]["acts_performed"] += 1
    st["caretaker_duo"]["chef_kawasaki"]["acts_performed"] += 1
    st["mutual_care_stats"]["last_round_time"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    save_caretakers_state(st)

    record_ledger("CARETAKER_ROUND", "Bandana Dee and Chef Kawasaki completed full proactive squad wellness round", xp=50)
    print(f"\n{C_BOLD}{C_GREEN}[✔] Proactive Caretaker Round Complete! All Kirbies nurtured, fed, and cozy! Poyo! 🌸✨{C_RESET}\n")


def action_mutual(skip_header: bool = False):
    """Executes the Mutual Caregiving Protocol: Caretaker 1 and Caretaker 2 take care of one another."""
    st = load_caretakers_state()

    if not skip_header:
        print(f"\n{C_BOLD}{C_PINK}╔══════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_BOLD}{C_PINK}║  💞  MUTUAL CAREGIVING PROTOCOL: CARETAKERS CARING FOR ONE ANOTHER  💞  ║{C_RESET}")
        print(f"{C_BOLD}{C_PINK}╚══════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

    print(f"{C_BOLD}{C_YELLOW}[*] Step A: Chef Kawasaki serves warm honey stew to Bandana Dee... 🍲 💙{C_RESET}")
    print(f"    Kawasaki: {C_YELLOW}\"Dee, you've been running around with that clipboard all morning! Sit down, here is a steaming bowl of tomato dumpling ramen!\"{C_RESET}")
    time.sleep(0.4)

    print(f"\n{C_BOLD}{C_BLUE}[*] Step B: Bandana Dee tends to Chef Kawasaki's tired cooking arms... 🍵 💆{C_RESET}")
    print(f"    Bandana Dee: {C_BLUE}\"Thank you, Chef! You've been flipping pancakes for 4 hours! Let me pour you calming chamomile tea and massage your shoulders.\"{C_RESET}")
    time.sleep(0.4)

    print(f"\n{C_BOLD}{C_HOT_PINK}[*] Step C: Kirby Prime & Keeby join in for a warm trio gratitude hug! (つ≧▽≦)つ 💖{C_RESET}")
    print(f"    Kirby Prime: {C_HOT_PINK}\"POYO! Best caretakers in all of Popstar! We love you both!\" 💕 🌸{C_RESET}\n")

    # Animation
    frames_mutual = [
        f"      {C_BLUE}💙 Bandana Dee{C_RESET}             {C_YELLOW}🍳 Chef Kawasaki{C_RESET}\n    ( • ‿ • ) 🍵             ( ^ ‿ ^ ) 🍲\n            {C_WHITE}*sharing tea and warm bowls of soup*{C_RESET}",
        f"                 {C_HOT_PINK}♥  ♥  ♥{C_RESET}\n       {C_WHITE}(つ {C_BLUE}( • ‿ • ) {C_PINK}( ^ ᗜ ^ ) {C_YELLOW}( ^ ‿ ^ ){C_WHITE} )つ{C_RESET}\n       {C_BOLD}{C_HOT_PINK}✨ \"MUTUAL CARE HARMONY: 100% BLISS!\" ✨{C_RESET}"
    ]

    for f in frames_mutual:
        print("\033[H\033[J" + f)
        time.sleep(0.4)

    # Update mutual stats
    st["caretaker_duo"]["bandana_dee"]["energy"] = 100
    st["caretaker_duo"]["bandana_dee"]["affection"] = 100
    st["caretaker_duo"]["chef_kawasaki"]["energy"] = 100
    st["caretaker_duo"]["chef_kawasaki"]["affection"] = 100
    st["mutual_care_stats"]["mutual_harmony_level"] = 100
    st["mutual_care_stats"]["duo_care_exchanges"] += 1
    st["mutual_care_stats"]["squad_buddy_acts"] += 1
    st["mutual_care_stats"]["last_mutual_ritual"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    st["recent_care_log"].append({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "actor": "Bandana Dee & Chef Kawasaki",
        "recipient": "Each Other & Kirby Prime",
        "act": "Executed mutual care ritual: shared hot stew, chamomile tea & trio gratitude hugs"
    })
    # Keep last 10 logs
    st["recent_care_log"] = st["recent_care_log"][-10:]
    save_caretakers_state(st)

    if HAS_AUDIO:
        try:
            play_sound_preset("purr")
        except Exception:
            pass

    record_ledger("MUTUAL_CARE", "Bandana Dee, Chef Kawasaki, and Kirby executed mutual caregiving ritual", xp=45)
    print(f"\n{C_BOLD}{C_GREEN}[✔] Mutual Care Ritual complete! Bandana Dee and Chef Kawasaki are 100% recharged & harmonized! 💞 ✨{C_RESET}\n")


def action_tuck(kirby_name: Optional[str] = None):
    """Bandana Dee tucks a Kirby in with starry blankets."""
    target = kirby_name or "Kirby Prime"
    print(f"\n{C_BOLD}{C_BLUE}[*] Bandana Waddle Dee bringing out fluffy starlight blankets for {target}... 💙 🛌{C_RESET}")
    time.sleep(0.3)
    try:
        sys.path.insert(0, str(BASE_DIR / "scripts"))
        import kirby_needs
        kirby_needs.action_nap()
    except Exception:
        pass

    st = load_caretakers_state()
    st["caretaker_duo"]["bandana_dee"]["acts_performed"] += 1
    st["recent_care_log"].append({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "actor": "Bandana Dee",
        "recipient": target,
        "act": f"Tucked {target} into Dream Cloud with warm starlight fleece blanket"
    })
    save_caretakers_state(st)
    print(f"{C_BOLD}{C_GREEN}[✔] Bandana Dee tucked {target} in warmly. Sweet dreams! 💤 ⭐{C_RESET}\n")


def action_cook(dish_name: Optional[str] = None):
    """Chef Kawasaki cooks a gourmet vitality dish."""
    dish = dish_name or "Maxi-Tomato Dumpling Ramen"
    print(f"\n{C_BOLD}{C_YELLOW}[*] Chef Kawasaki cooking gourmet {dish} with fresh herbs... 🍳 🍲{C_RESET}")
    time.sleep(0.4)
    try:
        sys.path.insert(0, str(BASE_DIR / "scripts"))
        import kirby_needs
        kirby_needs.action_feed("maxi_tomato")
    except Exception:
        pass

    st = load_caretakers_state()
    st["caretaker_duo"]["chef_kawasaki"]["acts_performed"] += 1
    st["recent_care_log"].append({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "actor": "Chef Kawasaki",
        "recipient": "Squad & Bandana Dee",
        "act": f"Cooked and served fresh {dish}"
    })
    save_caretakers_state(st)
    record_ledger("CARETAKER_COOK", f"Chef Kawasaki cooked {dish} for squad", xp=35)
    print(f"{C_BOLD}{C_GREEN}[✔] Chef Kawasaki served delicious {dish}! Vitality restored. 🍲 ✨{C_RESET}\n")


def action_care_for_one_another():
    """Grand Showcase of the entire squad and Caretaker Duo taking care of one another."""
    st = load_caretakers_state()

    print(f"\n{C_BOLD}{C_PINK}╔══════════════════════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║  💖 🌸 💙  THE SQUAD & CARETAKER DUO TAKING CARE OF ONE ANOTHER: POPSTAR SANCTUARY  💙 🌸 💖  ║{C_RESET}")
    print(f"{C_BOLD}{C_PINK}╚══════════════════════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

    moments = [
        (
            f"{C_BLUE}Bandana Waddle Dee{C_RESET} & {C_YELLOW}Chef Kawasaki{C_RESET}",
            "Kawasaki brings hot tomato ramen to Dee; Dee wraps a warm fleece scarf around Kawasaki's shoulders and rubs his tired cooking arms!",
            "\"Drink this warm tea, Chef! You've cooked all day!\" 🍵人🍲 \"And eat this fresh ramen, Dee! You've kept everyone safe!\""
        ),
        (
            f"{C_PINK}Kirby Prime{C_RESET} & {C_GOLD}Keeby{C_RESET}",
            "Kirby Prime splits a giant Strawberry Shortcake in two; Keeby shares his golden cosmic star candies!",
            "\"Half for Keeby, half for Prime! Poyo!\" 🍰人⭐ \"Warp speed siblings sticking together!\""
        ),
        (
            f"{C_CYAN}Freeze Kirby{C_RESET} & {C_GREEN}Chaotix Kirby{C_RESET}",
            "Freeze Kirby breathes gentle cooling glacial frost over Chaotix's smoking mechanical switches; Chaotix gifts Freeze Kirby a soothing ambient star lamp.",
            "\"Rest your fingers, Chaotix. Thermals 34°C.\" ❄️人⚡ \"Thanks, chill bro! Pure kinetic harmony!\""
        ),
        (
            f"{C_RED}Ace Kirby ( ಠ ʖ̯ ಠ ){C_RESET} & {C_WHITE}Shadow Kirby{C_RESET}",
            "Ace Kirby polishes Shadow's mirror shield; Shadow Kirby quietly offers Ace a whetstone and takes over the midnight watch so Ace can sleep.",
            "\"Keep the perimeter tight, Shadow.\" ⚔️人🪞 \"...Sleep well, Ace. The mirror world guards your dreams.\""
        ),
        (
            f"{C_PURPLE}Magician Kirby{C_RESET} & {C_GOLD}Explorer Kirby{C_RESET} & {C_CYAN}Hypernova Kirby{C_RESET} & {C_YELLOW}Noid Kirby{C_RESET}",
            "Noid Kirby shares his secret cheesy pizza crust; Hypernova vacuums all crumbs; Magician pulls a golden compass for Explorer's next quest!",
            "\"Fine, take the cheese crust!\" 🍕人🌀 \"Gulp! Crumb-free sanctuary!\" 🎩人🧭 \"Presto! New horizon charted!\""
        )
    ]

    for pair, desc, dialogue in moments:
        print(f"{C_BOLD}✨ Care Pair: {pair}{C_RESET}")
        print(f"   {C_WHITE}{desc}{C_RESET}")
        print(f"   {C_HOT_PINK}{dialogue}{C_RESET}\n")
        time.sleep(0.3)

    # Grand finale ASCII
    frames = [
        f"                 {C_HOT_PINK}♥  ♥  ♥  ♥  ♥{C_RESET}\n   {C_WHITE}(つ {C_BLUE}( • ‿ • ) {C_PINK}( ^ ᗜ ^ ) {C_YELLOW}( ʘ ͜ʖ ʘ ) {C_GOLD}( ^ ᗜ ^ ) {C_RED}( ಠ ʖ̯ ಠ ) {C_CYAN}( ˘ ᵕ ˘ ){C_WHITE} )つ{C_RESET}\n     {C_BOLD}{C_GOLD}🌟 \"EVERYONE TAKING CARE OF ONE ANOTHER: 100% UNCONDITIONAL LOVE!\" 🌟{C_RESET}"
    ]
    for f in frames:
        print(f)

    # Max stats
    st["caretaker_duo"]["bandana_dee"]["energy"] = 100
    st["caretaker_duo"]["bandana_dee"]["affection"] = 100
    st["caretaker_duo"]["chef_kawasaki"]["energy"] = 100
    st["caretaker_duo"]["chef_kawasaki"]["affection"] = 100
    st["mutual_care_stats"]["mutual_harmony_level"] = 100
    st["mutual_care_stats"]["duo_care_exchanges"] += 2
    st["mutual_care_stats"]["squad_buddy_acts"] += 5
    st["recent_care_log"].append({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "actor": "Entire Squad & Caretaker Duo",
        "recipient": "One Another",
        "act": "Executed full circle of care: all 10 Kirbies & Caretaker Duo nurtured one another!"
    })
    save_caretakers_state(st)

    try:
        sys.path.insert(0, str(BASE_DIR / "scripts"))
        import kirby_needs
        st_needs = kirby_needs.load_needs_state()
        for k in st_needs["needs"]:
            st_needs["needs"][k]["level"] = 100
            st_needs["needs"][k]["status"] = kirby_needs.get_need_status_label(k, 100)
        for k in st_needs["squad_desires"]:
            st_needs["squad_desires"][k]["craving_met"] = True
        kirby_needs.save_needs_state(st_needs)
    except Exception:
        pass

    if HAS_AUDIO:
        try:
            play_sound_preset("purr")
        except Exception:
            pass

    record_ledger("ONE_ANOTHER", "All Kirbies and Caretakers took care of one another in full harmony", xp=60)
    print(f"\n{C_BOLD}{C_GREEN}[✔] The entire family has taken care of one another! Every heart is full, peaceful, and warm! Poyo! 🌸✨{C_RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Kirby Caretaker Duo & Mutual Caregiving Engine")
    subparsers = parser.add_subparsers(dest="subcommand")

    subparsers.add_parser("status", help="Display Caretaker Duo & Mutual Care status")
    subparsers.add_parser("round", help="Dispatch full Caretaker Duo proactive wellness round")
    subparsers.add_parser("mutual", help="Execute Mutual Caregiving ritual (Caretakers care for each other)")
    subparsers.add_parser("buddy", help="Alias for mutual")
    subparsers.add_parser("oneanother", help="The squad and Caretaker Duo take care of one another")
    subparsers.add_parser("care", help="Alias for oneanother")

    p_tuck = subparsers.add_parser("tuck", help="Bandana Dee tucks Kirby into bed")
    p_tuck.add_argument("target", nargs="?", default="Kirby Prime", help="Name of Kirby")

    p_cook = subparsers.add_parser("cook", help="Chef Kawasaki bakes or cooks a meal")
    p_cook.add_argument("dish", nargs="?", default="Maxi-Tomato Stew", help="Dish name")

    subparsers.add_parser("test", help="Headless test verification")

    args = parser.parse_args()

    if args.subcommand in ("status", None):
        cmd_status()
    elif args.subcommand == "round":
        action_round()
    elif args.subcommand in ("mutual", "buddy"):
        action_mutual()
    elif args.subcommand in ("oneanother", "care"):
        action_care_for_one_another()
    elif args.subcommand == "tuck":
        action_tuck(args.target)
    elif args.subcommand == "cook":
        action_cook(args.dish)
    elif args.subcommand == "test":
        print("[TEST] Verifying Caretaker Duo & Mutual Care Engine...")
        st = load_caretakers_state()
        assert "caretaker_duo" in st, "Caretaker duo missing from state"
        assert "bandana_dee" in st["caretaker_duo"], "Bandana Dee missing"
        assert "chef_kawasaki" in st["caretaker_duo"], "Chef Kawasaki missing"
        assert "mutual_care_stats" in st, "Mutual care stats missing"
        save_caretakers_state(st)
        print("[TEST] PASS: Caretaker Duo Engine OK.")


if __name__ == "__main__":
    main()
