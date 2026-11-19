#!/usr/bin/env python3
"""
🌸 KIRBY HOLISTIC NEEDS & WELLBEING ENGINE (kirby_needs.py) 🌸
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_needs.py
CLI: kirby needs [status|fulfill|auto|nap|wake|bath|hug|fengshui|cool]
     kirby nap | kirby bath | kirby hug | kirby fengshui | kirby cool

Features:
1. 8 Core Needs Model:
   - Satiety / Hunger 🍔
   - Rest & Dreams 💤
   - Hygiene & Radiance 🧼
   - Affection & Snuggles 💖
   - Play & Joy 🎮
   - Social Belonging 👥
   - Curiosity & Learning 🧠
   - Sanctuary & Spatial Feng Shui 🏡
2. 10-Kirby Squad Individual Needs Matrix:
   - Kirby Prime, Noid, Magician, Ace, Explorer, Hypernova, Chaotix, Keeby, Freeze, Shadow.
3. Realistic Dynamic Time Decay & Environment Sensing (CPU thermals, cache clutter).
4. Multi-Frame ANSI ASCII Animations for Naps, Bubble Baths, Cuddles, Feng Shui & Chills.
5. Audio FX Synthesis via agy_fx_engine.py and LRA Haptic integration.
6. Autonomous Caregiver Engine (kirby needs auto) for holistic 100% wellbeing.
7. Bi-directional Synchronization with .kirby_pet_state.json and .kirby_squad_state.json.
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
from typing import Dict, List, Any, Optional, Tuple

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
C_DIM = "\033[2m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

BASE_DIR = Path("/mnt/shared/AntiGravity_Shared")
NEEDS_STATE_FILE = BASE_DIR / ".kirby_needs_state.json"
PET_STATE_FILE = BASE_DIR / ".kirby_pet_state.json"
SQUAD_STATE_FILE = BASE_DIR / ".kirby_squad_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"

HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


# --- Core Needs Definitions ---
CORE_NEEDS_DEF = {
    "satiety": {
        "name": "Satiety / Hunger",
        "icon": "🍔",
        "color": C_YELLOW,
        "decay_per_hour": 5.0,
        "ideal": 100,
        "critical_threshold": 30,
        "description": "Appetite and nourishing calorie reserves."
    },
    "rest": {
        "name": "Rest & Dream Energy",
        "icon": "💤",
        "color": C_CYAN,
        "decay_per_hour": 4.0,
        "ideal": 100,
        "critical_threshold": 25,
        "description": "Starlight stamina, sleep quality and dream tranquility."
    },
    "hygiene": {
        "name": "Hygiene & Radiance",
        "icon": "🧼",
        "color": C_BLUE,
        "decay_per_hour": 3.0,
        "ideal": 100,
        "critical_threshold": 35,
        "description": "Cleanliness, bubble spa freshness, zero cache dust."
    },
    "affection": {
        "name": "Affection & Love",
        "icon": "💖",
        "color": C_PINK,
        "decay_per_hour": 3.5,
        "ideal": 100,
        "critical_threshold": 30,
        "description": "Heart warmth, cuddling, purring and developer bond."
    },
    "fun": {
        "name": "Play & Amusement",
        "icon": "🎮",
        "color": C_GREEN,
        "decay_per_hour": 4.5,
        "ideal": 100,
        "critical_threshold": 30,
        "description": "Arcade games, quick draw reflex duels, bouncing joy."
    },
    "social": {
        "name": "Social Belonging",
        "icon": "👥",
        "color": C_PURPLE,
        "decay_per_hour": 3.0,
        "ideal": 100,
        "critical_threshold": 25,
        "description": "Squad connection, multi-Kirby banter and unity."
    },
    "curiosity": {
        "name": "Curiosity & Learning",
        "icon": "🧠",
        "color": C_GOLD,
        "decay_per_hour": 2.5,
        "ideal": 100,
        "critical_threshold": 20,
        "description": "Ability synthesis, mystery cards and code exploration."
    },
    "sanctuary": {
        "name": "Spatial Feng Shui",
        "icon": "🏡",
        "color": C_WHITE,
        "decay_per_hour": 2.0,
        "ideal": 100,
        "critical_threshold": 30,
        "description": "Room harmony, starlight crystal resonance, cozy tranquility."
    }
}

# --- Squad Specific Needs ---
SQUAD_NEEDS_INFO = {
    "kirby_prime": {
        "name": "Kirby Prime",
        "icon": "🌸",
        "primary_need": "Strawberry Shortcake & Starlight Naps",
        "craving": "🍰 Strawberry Shortcake",
        "action_hint": "kirby feed strawberry_cake || kirby nap"
    },
    "noid_kirby": {
        "name": "Noid Kirby",
        "icon": "🍕",
        "primary_need": "Cheesy Deep-Dish Pizza & Goblin Chaos",
        "craving": "🍕 Cheesy Star Pizza",
        "action_hint": "kirby pizza order || kirby prank"
    },
    "magician_kirby": {
        "name": "Magician Kirby",
        "icon": "🎩",
        "primary_need": "Flamboyant Audience & Tarot Sleight-of-Hand",
        "craving": "✨ Standing Ovation",
        "action_hint": "kirby tarot || kirby magician act"
    },
    "ace_kirby": {
        "name": "Ace Kirby",
        "icon": "⚔️",
        "primary_need": "Compression Arena Brawls & Blade Sharpening",
        "craving": "⚔️ Sparring Match",
        "action_hint": "kirby boss whispy || kirby samurai"
    },
    "explorer_kirby": {
        "name": "Explorer Kirby",
        "icon": "🧭",
        "primary_need": "Ancient Ruins Expeditions & Relic Dowsing",
        "craving": "🧭 Uncharted Map",
        "action_hint": "kirby expedition green_greens"
    },
    "hypernova_kirby": {
        "name": "Hypernova Kirby",
        "icon": "🧹",
        "primary_need": "Vacuuming Dev Cache & Inhaling Stale Bytes",
        "craving": "🌀 50MB Clutter Feast",
        "action_hint": "kirby clean"
    },
    "chaotix_kirby": {
        "name": "Chaotix Kirby",
        "icon": "⚡",
        "primary_need": "High WPM Mechanical Key Click Acoustics",
        "craving": "⚡ Cherry Blue Switches",
        "action_hint": "kirby typey"
    },
    "keeby_yellow": {
        "name": "Keeby",
        "icon": "💛",
        "primary_need": "Lightning Dash Races & Lemon Star Tarts",
        "craving": "⚡ Lightning Dash",
        "action_hint": "kirby raid"
    },
    "freeze_kirby": {
        "name": "Freeze Kirby",
        "icon": "💙",
        "primary_need": "Glacial Frost Chill & CPU Thermals < 38°C",
        "craving": "❄️ Sub-Zero Thermal Drop",
        "action_hint": "kirby cool"
    },
    "shadow_kirby": {
        "name": "Shadow Kirby",
        "icon": "🖤",
        "primary_need": "Mirror Realm Shards & Perimeter Vigilance",
        "craving": "🪞 Quiet Mirror Reflection",
        "action_hint": "kirby status"
    }
}


def load_needs_state() -> Dict[str, Any]:
    now_ts = time.time()
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    state: Dict[str, Any] = {}
    if NEEDS_STATE_FILE.exists():
        try:
            with open(NEEDS_STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = {}

    if not state or "needs" not in state:
        state = {
            "version": "1.0.0",
            "name": "Kirby",
            "overall_wellbeing": 95,
            "overall_status": "Ecstatic & Cherished",
            "current_dream": "Floating on Star Clouds over Fountain of Dreams",
            "is_sleeping": False,
            "bath_sparkle_active": True,
            "room_feng_shui_score": 96,
            "last_updated": now_ts,
            "last_updated_iso": now_iso,
            "needs": {
                "satiety": {"level": 90, "last_fulfilled": now_ts, "status": "Well-Fed"},
                "rest": {"level": 92, "last_fulfilled": now_ts, "status": "Rested"},
                "hygiene": {"level": 95, "last_fulfilled": now_ts, "status": "Sparkling Clean"},
                "affection": {"level": 98, "last_fulfilled": now_ts, "status": "Adored"},
                "fun": {"level": 88, "last_fulfilled": now_ts, "status": "Cheerfully Entertained"},
                "social": {"level": 90, "last_fulfilled": now_ts, "status": "Squad Bond Strong"},
                "curiosity": {"level": 85, "last_fulfilled": now_ts, "status": "Inquisitive"},
                "sanctuary": {"level": 94, "last_fulfilled": now_ts, "status": "Harmonious Qi"}
            },
            "squad_desires": {
                k: {"craving_met": True, "last_satisfied": now_ts} for k in SQUAD_NEEDS_INFO
            },
            "care_history_count": {
                "naps_taken": 4,
                "baths_taken": 6,
                "hugs_received": 18,
                "meals_enjoyed": 22,
                "fengshui_alignments": 5,
                "cpu_chills": 3
            }
        }
        save_needs_state(state)
        return state

    # Dynamic time decay
    last_ts = state.get("last_updated", now_ts)
    elapsed_hours = max(0.0, (now_ts - last_ts) / 3600.0)

    # Check external factors
    cache_penalty = 0.0
    try:
        # Check cache clutter
        snap_count = len(list(Path("/mnt/shared").glob("kirby_snap_*.png")))
        if snap_count > 10:
            cache_penalty = 5.0
    except Exception:
        pass

    if elapsed_hours > 0.01:
        for need_key, need_def in CORE_NEEDS_DEF.items():
            if need_key in state["needs"]:
                decay = elapsed_hours * need_def["decay_per_hour"]
                if need_key == "hygiene" and cache_penalty > 0:
                    decay += cache_penalty
                curr = state["needs"][need_key]["level"]
                new_lvl = max(5, int(curr - decay))
                state["needs"][need_key]["level"] = new_lvl
                state["needs"][need_key]["status"] = get_need_status_label(need_key, new_lvl)

        state["last_updated"] = now_ts
        state["last_updated_iso"] = now_iso
        recalc_overall_wellbeing(state)
        save_needs_state(state)

    return state


def save_needs_state(state: Dict[str, Any]):
    state["last_updated"] = time.time()
    state["last_updated_iso"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    recalc_overall_wellbeing(state)

    try:
        with open(NEEDS_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        sys.stderr.write(f"Error saving needs state: {e}\n")

    # Keep .kirby_pet_state.json synchronized
    sync_to_pet_and_squad(state)


def sync_to_pet_and_squad(state: Dict[str, Any]):
    try:
        if PET_STATE_FILE.exists():
            with open(PET_STATE_FILE, "r", encoding="utf-8") as f:
                pet_data = json.load(f)
            needs = state.get("needs", {})
            if "satiety" in needs:
                pet_data["hunger"] = needs["satiety"]["level"]
            if "rest" in needs:
                pet_data["energy"] = needs["rest"]["level"]
            if "affection" in needs and "fun" in needs:
                pet_data["happiness"] = int((needs["affection"]["level"] + needs["fun"]["level"]) / 2)
            with open(PET_STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(pet_data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def record_ledger(action: str, details: str, xp: int = 25):
    try:
        LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "action": f"NEEDS_{action.upper()}",
            "details": details,
            "xpGained": xp
        }
        with open(LEDGER_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def get_need_status_label(need_key: str, val: int) -> str:
    if val >= 90:
        labels = {
            "satiety": "Feasted & Satiated",
            "rest": "Bursting with Energy",
            "hygiene": "Sparkling Radiance",
            "affection": "Deeply Cherished",
            "fun": "Ecstatically Joyful",
            "social": "Heartfelt Squad Unity",
            "curiosity": "Enlightened Wonder",
            "sanctuary": "Harmonious Starlight Qi"
        }
    elif val >= 70:
        labels = {
            "satiety": "Content & Satisfied",
            "rest": "Rested & Alert",
            "hygiene": "Fresh & Clean",
            "affection": "Warm & Loved",
            "fun": "Playful & Happy",
            "social": "Friendly Connection",
            "curiosity": "Curious",
            "sanctuary": "Cozy Vibe"
        }
    elif val >= 45:
        labels = {
            "satiety": "Peckish",
            "rest": "Getting Drowsy",
            "hygiene": "A Bit Dusty",
            "affection": "Needs Snuggles",
            "fun": "Slightly Bored",
            "social": "Craving Banter",
            "curiosity": "Idling",
            "sanctuary": "Needs Tidying"
        }
    else:
        labels = {
            "satiety": "HUNGRY! 🍅",
            "rest": "EXHAUSTED! 💤",
            "hygiene": "GLITCHY / DIRTY! 🧼",
            "affection": "LONELY! 💖",
            "fun": "RESTLESS! 🎮",
            "social": "ISOLATED! 👥",
            "curiosity": "PERPLEXED! 🧠",
            "sanctuary": "CHAOTIC ROOM! 🏡"
        }
    return labels.get(need_key, "Normal")


def recalc_overall_wellbeing(state: Dict[str, Any]):
    needs = state.get("needs", {})
    if not needs:
        state["overall_wellbeing"] = 100
        state["overall_status"] = "Ecstatic & Cherished"
        return

    total = sum(item["level"] for item in needs.values())
    avg = int(total / len(needs))
    state["overall_wellbeing"] = avg

    if avg >= 90:
        state["overall_status"] = "Ecstatic, Cherished & Glowing 🌸✨"
    elif avg >= 75:
        state["overall_status"] = "Joyful & Energetic 💖"
    elif avg >= 60:
        state["overall_status"] = "Comfortable & Dreamy (*^-^*)"
    elif avg >= 40:
        state["overall_status"] = "Needs Loving Care & Rest (•_•)"
    else:
        state["overall_status"] = "CRITICAL: Immediate Care Needed! (;-;)"


def draw_progress_bar(val: int, max_val: int = 100, length: int = 22, color: str = C_GREEN) -> str:
    filled = int((val / max_val) * length)
    filled = max(0, min(length, filled))
    empty = length - filled
    return f"{color}{'█' * filled}{C_DIM}{'░' * empty}{C_RESET} {val:>3}%"


# --- Visual ASCII Renderers ---

def render_kirby_face(wellbeing: int) -> List[str]:
    if wellbeing >= 90:
        return [
            f"        {C_PINK}.-------.{C_RESET}        {C_GOLD}★{C_RESET}  {C_PINK}✧  POYO!{C_RESET}",
            f"      {C_PINK}/   {C_WHITE}^   ^{C_PINK}   \\{C_RESET}     {C_HOT_PINK}♥ ( ^ ᗜ ^ ) ♥{C_RESET}",
            f"     {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK} |{C_RESET}",
            f"   {C_PINK}c( \\     -     / ){C_RESET}",
            f"       {C_PINK}\\ .______. /{C_RESET}",
            f"        {C_PINK}'-......-'{C_RESET}",
            f"        {C_RED}(____)(____){C_RESET}"
        ]
    elif wellbeing >= 70:
        return [
            f"        {C_PINK}.-------.{C_RESET}",
            f"      {C_PINK}/   {C_WHITE}•   •{C_PINK}   \\{C_RESET}     {C_PINK}( • ‿ • ) 🌸{C_RESET}",
            f"     {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK} |{C_RESET}",
            f"   {C_PINK}c( \\     -     / ){C_RESET}",
            f"       {C_PINK}\\ .______. /{C_RESET}",
            f"        {C_PINK}'-......-'{C_RESET}",
            f"        {C_RED}(____)(____){C_RESET}"
        ]
    elif wellbeing >= 45:
        return [
            f"        {C_PINK}.-------.{C_RESET}",
            f"      {C_PINK}/   {C_WHITE}•   •{C_PINK}   \\{C_RESET}     {C_YELLOW}( • _ • ) 💭{C_RESET}",
            f"     {C_PINK}|   {C_HOT_PINK}( ){C_PINK} ─ {C_HOT_PINK}( ){C_PINK} |{C_RESET}",
            f"   {C_PINK}c( \\     -     / ){C_RESET}",
            f"       {C_PINK}\\ .______. /{C_RESET}",
            f"        {C_PINK}'-......-'{C_RESET}",
            f"        {C_RED}(____)(____){C_RESET}"
        ]
    else:
        return [
            f"        {C_PINK}.-------.{C_RESET}",
            f"      {C_PINK}/   {C_CYAN};{C_WHITE}   ;{C_PINK}   \\{C_RESET}     {C_RED}( ; - ; ) 💔 Needs Care!{C_RESET}",
            f"     {C_PINK}|   {C_HOT_PINK}(~){C_PINK} ⌒ {C_HOT_PINK}(~){C_PINK} |{C_RESET}",
            f"   {C_PINK}c( \\     -     / ){C_RESET}",
            f"       {C_PINK}\\ .______. /{C_RESET}",
            f"        {C_PINK}'-......-'{C_RESET}",
            f"        {C_RED}(____)(____){C_RESET}"
        ]


def cmd_status():
    state = load_needs_state()
    wb = state["overall_wellbeing"]
    status_msg = state["overall_status"]
    is_sleeping = state.get("is_sleeping", False)

    print(f"\n{C_BOLD}{C_PINK}╔══════════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║ {C_GOLD}⭐ 🌸  KIRBY HOLISTIC NEEDS & COMPANION WELLBEING SANCTUARY  🌸 ⭐{C_PINK}   ║{C_RESET}")
    print(f"{C_BOLD}{C_PINK}╠══════════════════════════════════════════════════════════════════════════════════╣{C_RESET}")

    portrait = render_kirby_face(wb)
    meta_info = [
        f"{C_WHITE}Overall Wellbeing:{C_RESET} {C_BOLD}{C_GREEN if wb>=80 else C_YELLOW}{wb}%{C_RESET} [{status_msg}]",
        f"{C_WHITE}Sleep State:{C_RESET} {'💤 ' + C_CYAN + 'Deep Sweet Dreams' if is_sleeping else '☀️ ' + C_YELLOW + 'Awake & Active'}{C_RESET}",
        f"{C_WHITE}Current Dream:{C_RESET} {C_HOT_PINK}{state.get('current_dream', 'Starlight Skies')}{C_RESET}",
        f"{C_WHITE}Host Machine:{C_RESET} {C_CYAN}Pixel 9 Pro XL (Debian 13 Trixie / AVF){C_RESET}",
        f"{C_WHITE}Sanctuary Qi Score:{C_RESET} {C_GOLD}{state.get('room_feng_shui_score', 95)} / 100 ⛩️{C_RESET}",
        f"{C_WHITE}Care Action Shortcut:{C_RESET} {C_YELLOW}kirby needs fulfill <need> | kirby needs auto{C_RESET}",
        f"{C_WHITE}Web Dashboard:{C_RESET} {C_CYAN}http://localhost:8088/needs || :8088/multiverse{C_RESET}"
    ]

    for i in range(len(portrait)):
        p_line = portrait[i]
        m_line = meta_info[i] if i < len(meta_info) else ""
        # Format line with width padding
        left = f"{p_line}"
        # Approximate visible length
        print(f"{C_BOLD}{C_PINK}║{C_RESET} {left:<42} {m_line:<50} {C_BOLD}{C_PINK}║{C_RESET}")

    print(f"{C_BOLD}{C_PINK}╟──────────────────────────────────────────────────────────────────────────────────╢{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║ {C_WHITE}{C_BOLD}🌸 8 CORE ESSENTIAL NEEDS MATRIX:{C_RESET}                                                {C_BOLD}{C_PINK}║{C_RESET}")
    print(f"{C_BOLD}{C_PINK}╟──────────────────────────────────────────────────────────────────────────────────╢{C_RESET}")

    for k, d in CORE_NEEDS_DEF.items():
        need_data = state["needs"].get(k, {"level": 80, "status": "Good"})
        lvl = need_data["level"]
        status_lbl = need_data.get("status", get_need_status_label(k, lvl))
        bar = draw_progress_bar(lvl, 100, 22, d["color"])
        name_str = f"{d['icon']} {d['name']}"
        print(f"{C_BOLD}{C_PINK}║{C_RESET}  {name_str:<26} {bar}  {d['color']}{status_lbl:<26}{C_RESET} {C_BOLD}{C_PINK}║{C_RESET}")

    print(f"{C_BOLD}{C_PINK}╟──────────────────────────────────────────────────────────────────────────────────╢{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║ {C_GOLD}{C_BOLD}👥 10-KIRBY SQUAD DESIRES & CRAVINGS AUDIT:{C_RESET}                                     {C_BOLD}{C_PINK}║{C_RESET}")
    print(f"{C_BOLD}{C_PINK}╟──────────────────────────────────────────────────────────────────────────────────╢{C_RESET}")

    for kid, info in SQUAD_NEEDS_INFO.items():
        desire_met = state.get("squad_desires", {}).get(kid, {}).get("craving_met", True)
        status_sym = f"{C_GREEN}● SATISFIED{C_RESET}" if desire_met else f"{C_RED}▲ CRAVING!{C_RESET}"
        entry_str = f"{info['icon']} {info['name']}: {C_WHITE}{info['primary_need']}{C_RESET}"
        hint = f"{C_DIM}(Try: {info['action_hint']}){C_RESET}"
        print(f"{C_BOLD}{C_PINK}║{C_RESET}  {status_sym} {entry_str:<50} {hint:<30} {C_BOLD}{C_PINK}║{C_RESET}")

    print(f"{C_BOLD}{C_PINK}╚══════════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")


# --- Fulfillment Actions ---

def action_nap():
    state = load_needs_state()
    print(f"\n{C_BOLD}{C_CYAN}[*] Tucking Kirby into a fluffy Dream Cloud with a starry nightcap... ( - ‿ - ) 💤{C_RESET}\n")

    frames = [
        f"     {C_PINK}.-------.{C_RESET}   {C_CYAN}☁️{C_RESET}\n   {C_PINK}/   {C_WHITE}O   O{C_PINK}   \\{C_RESET}    {C_YELLOW}*yawn~*{C_RESET}\n  {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ᗜ {C_HOT_PINK}(♥){C_PINK} |{C_RESET}",
        f"       {C_CYAN}★ {C_GOLD}✦{C_RESET}\n    {C_PURPLE}/\\{C_RESET}{C_PINK}.-------.{C_RESET}  {C_CYAN}☁️  *curling up on Warp Star* ☁️{C_RESET}\n   {C_PINK}/   {C_WHITE}-   -{C_PINK}   \\{C_RESET}\n  {C_PINK}|  {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}",
        f"       {C_GOLD}🌙  {C_CYAN}Zzz...{C_RESET}\n    {C_PURPLE}/\\{C_RESET}{C_PINK}.-------.{C_RESET}   {C_CYAN}☁️  ☁️{C_RESET}\n   {C_PINK}/   {C_WHITE}˘   ˘{C_PINK}   \\{C_RESET}    {C_BOLD}{C_CYAN}\"Dreaming of Fountain of Dreams & Starlight...\" 💤 ✨{C_RESET}\n  {C_PINK}|  {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}"
    ]

    for f in frames:
        print("\033[H\033[J" + f)
        time.sleep(0.4)

    state["needs"]["rest"]["level"] = 100
    state["needs"]["rest"]["status"] = "Bursting with Energy"
    state["needs"]["rest"]["last_fulfilled"] = time.time()
    state["is_sleeping"] = True
    state["current_dream"] = random.choice([
        "Floating on Star Clouds over Popstar",
        "A feast of infinite Strawberry Shortcakes with King Dedede",
        "Warp Star surfing through Rainbow Resort",
        "Conducting an orchestra with Magician Kirby and Whispy Woods"
    ])
    state["care_history_count"]["naps_taken"] = state["care_history_count"].get("naps_taken", 0) + 1
    state["squad_desires"]["kirby_prime"]["craving_met"] = True

    save_needs_state(state)

    if HAS_AUDIO:
        try:
            play_sound_preset("warp")
        except Exception:
            pass

    record_ledger("REST_NAP", f"Tucked Kirby in for a starlight dream nap: {state['current_dream']}", xp=35)
    print(f"\n{C_BOLD}{C_GREEN}[✔] Kirby is peacefully resting and fully recharged to 100%! 💤 ⭐{C_RESET}")
    print(f"    Energy & Dreams: {C_CYAN}100%{C_RESET} | Current Dream: {C_HOT_PINK}{state['current_dream']}{C_RESET}\n")


def action_wake():
    state = load_needs_state()
    state["is_sleeping"] = False
    print(f"\n{C_BOLD}{C_YELLOW}[*] Gently waking Kirby with a warm ray of morning starlight... ☀️{C_RESET}\n")

    frames = [
        f"     {C_PINK}.-------.{C_RESET}\n   {C_PINK}/   {C_WHITE}-   -{C_PINK}   \\{C_RESET}   {C_YELLOW}*stretch~*{C_RESET}\n  {C_PINK}|  {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}",
        f"     {C_PINK}.-------.{C_RESET}  {C_GOLD}★{C_RESET}\n   {C_PINK}/   {C_WHITE}^   ^{C_PINK}   \\{C_RESET}   {C_BOLD}{C_PINK}POYO! Good morning! 🌸 ☀️{C_RESET}\n  {C_PINK}|  {C_HOT_PINK}(♥){C_PINK} ᗜ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}"
    ]

    for f in frames:
        print("\033[H\033[J" + f)
        time.sleep(0.4)

    save_needs_state(state)
    if HAS_AUDIO:
        try:
            play_sound_preset("hop")
        except Exception:
            pass

    print(f"{C_BOLD}{C_GREEN}[✔] Kirby is wide awake, energized, and ready for adventure! ( ^ ᗜ ^ ) 🌸{C_RESET}\n")


def action_bath():
    state = load_needs_state()
    print(f"\n{C_BOLD}{C_BLUE}[*] Preparing a warm bubbly wooden spa tub in the Fountain of Dreams... 🧼 🫧{C_RESET}\n")

    frames = [
        f"       {C_BLUE}🫧  🫧{C_RESET}\n     {C_PINK}.-------.{C_RESET}    {C_YELLOW}🐤 *squeak!*{C_RESET}\n   {C_PINK}/   {C_WHITE}O   O{C_PINK}   \\{C_RESET}   {C_BLUE}*splish splash!*{C_RESET}\n  {C_BLUE}~~~~~~~~~~~~~~~~~{C_RESET}\n   \\_\\_\\_\\_\\_\\_\\_\\_/{C_RESET}",
        f"     {C_BLUE}🫧  {C_WHITE}✦{C_BLUE}  🫧{C_RESET}\n     {C_PINK}.-------.{C_RESET}    {C_WHITE}*scrubbing away all terminal cache dust* 🧼{C_RESET}\n   {C_PINK}/   {C_WHITE}^   ^{C_PINK}   \\{C_RESET}\n  {C_PINK}|  {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}\n  {C_BLUE}~~~~~~~~~~~~~~~~~{C_RESET}\n   \\_\\_\\_\\_\\_\\_\\_\\_/{C_RESET}",
        f"      {C_GOLD}✨ {C_WHITE}★ {C_GOLD}✨{C_RESET}\n     {C_PINK}.-------.{C_RESET}    {C_BOLD}{C_BLUE}\"SPARKLING CLEAN & BUBBLE FRESH!\" 🫧 ✨{C_RESET}\n   {C_PINK}/   {C_WHITE}•   •{C_PINK}   \\{C_RESET}   {C_HOT_PINK}♥ ( ^ ᗜ ^ ) ♥{C_RESET}\n  {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK} |{C_RESET}"
    ]

    for f in frames:
        print("\033[H\033[J" + f)
        time.sleep(0.4)

    state["needs"]["hygiene"]["level"] = 100
    state["needs"]["hygiene"]["status"] = "Sparkling Radiance"
    state["needs"]["hygiene"]["last_fulfilled"] = time.time()
    state["bath_sparkle_active"] = True
    state["care_history_count"]["baths_taken"] = state["care_history_count"].get("baths_taken", 0) + 1

    save_needs_state(state)

    if HAS_AUDIO:
        try:
            play_sound_preset("bubble_pop")
        except Exception:
            pass

    record_ledger("HYGIENE_BATH", "Soaked Kirby in Fountain of Dreams bubble spa and washed away cache dust", xp=30)
    print(f"\n{C_BOLD}{C_GREEN}[✔] Kirby is sparkling with starlight bubbles and fresh cosmic fragrance! (100% 🧼) 🫧{C_RESET}\n")


def action_hug():
    state = load_needs_state()
    print(f"\n{C_BOLD}{C_PINK}[*] Wrapping Kirby in a warm, gentle two-handed hug... (つ≧▽≦)つ 💖{C_RESET}\n")

    frames = [
        f"   {C_WHITE}(つ≧▽≦)つ{C_RESET}  {C_PINK}( ^-^ ){C_RESET}   {C_HOT_PINK}*reaching in for cuddles*{C_RESET}",
        f"     {C_HOT_PINK}♥  ♥  ♥{C_RESET}\n   {C_WHITE}(つ {C_PINK}( ^ ‿ ^ ){C_WHITE} )つ{C_RESET}   {C_PINK}*purrrrrrr~*{C_RESET}",
        f"     {C_GOLD}✨ {C_HOT_PINK}💖 {C_GOLD}✨{C_RESET}\n   {C_WHITE}(つ {C_PINK}( ♥ ᗜ ♥ ){C_WHITE} )つ{C_RESET}   {C_BOLD}{C_HOT_PINK}\"POYO! Best friends forever!\" 💕 🌸{C_RESET}"
    ]

    for f in frames:
        print("\033[H\033[J" + f)
        time.sleep(0.4)

    state["needs"]["affection"]["level"] = 100
    state["needs"]["affection"]["status"] = "Deeply Cherished"
    state["needs"]["affection"]["last_fulfilled"] = time.time()
    state["needs"]["social"]["level"] = min(100, state["needs"]["social"]["level"] + 20)
    state["care_history_count"]["hugs_received"] = state["care_history_count"].get("hugs_received", 0) + 1

    save_needs_state(state)

    if HAS_AUDIO:
        try:
            play_sound_preset("purr")
        except Exception:
            pass

    record_ledger("AFFECTION_HUG", "Embraced Kirby in warm cuddles and reaffirmed deep developer bond", xp=35)
    print(f"\n{C_BOLD}{C_GREEN}[✔] Kirby's heart is overflowing with warmth and happiness! (100% 💖) 🌸{C_RESET}\n")


def action_fengshui():
    state = load_needs_state()
    print(f"\n{C_BOLD}{C_GOLD}[*] Harmonizing Room Spatial Feng Shui & Clearing Null-Space Qi... ⛩️ 🌟{C_RESET}\n")

    frames = [
        f"     {C_GOLD}⛩️  🌿  🌟{C_RESET}\n   {C_WHITE}Aligning starlight crystal matrices...{C_RESET}\n   {C_DIM}Sweeping null-space coordinate voids...{C_RESET}",
        f"     {C_CYAN}✦  💎  ✦{C_RESET}\n   {C_WHITE}Placing Kirby plushies and star lamps in auspicious corners...{C_RESET}\n   {C_GOLD}Spatial Flow: PERFECT EQUILIBRIUM{C_RESET}",
        f"     {C_GOLD}🌸 ⛩️  🌿  🌟 🌸{C_RESET}\n   {C_BOLD}{C_GREEN}\"SANCTUARY HARMONY RESTORED: 100/100 QI!\" 🍵 ✨{C_RESET}"
    ]

    for f in frames:
        print("\033[H\033[J" + f)
        time.sleep(0.4)

    state["needs"]["sanctuary"]["level"] = 100
    state["needs"]["sanctuary"]["status"] = "Harmonious Starlight Qi"
    state["needs"]["sanctuary"]["last_fulfilled"] = time.time()
    state["room_feng_shui_score"] = 100
    state["care_history_count"]["fengshui_alignments"] = state["care_history_count"].get("fengshui_alignments", 0) + 1

    save_needs_state(state)

    if HAS_AUDIO:
        try:
            play_sound_preset("glass_ping")
        except Exception:
            pass

    record_ledger("SANCTUARY_FENGSHUI", "Harmonized spatial feng shui and starlight room resonance", xp=40)
    print(f"\n{C_BOLD}{C_GREEN}[✔] Room Spatial Feng Shui harmonized to 100%! Pure peace and tranquility. 🏡 🌟{C_RESET}\n")


def action_cool():
    state = load_needs_state()
    print(f"\n{C_BOLD}{C_BLUE}[*] Freeze Kirby invoking Glacial Chill on Pixel 9 Pro XL CPU... ❄️ 🧊{C_RESET}\n")

    # Read real thermal zone if available
    cur_temp = "37.5°C"
    try:
        zones = list(Path("/sys/class/thermal").glob("thermal_zone*/temp"))
        if zones:
            t_raw = int(zones[0].read_text().strip())
            cur_temp = f"{t_raw / 1000.0:.1f}°C"
    except Exception:
        pass

    frames = [
        f"     {C_BLUE}❄️  ❄️  ❄️{C_RESET}\n   {C_BLUE}Freeze Kirby: ( ˘ ᵕ ˘ )❄️{C_RESET}\n   {C_WHITE}Reading thermals: {cur_temp}... Preparing glacial frost mist!{C_RESET}",
        f"     {C_CYAN}❄️ 🧊 ❄️ 🧊 ❄️{C_RESET}\n   {C_CYAN}*WHOOOOOOOSH!* Sub-zero thermal wave dissipating heat!{C_RESET}",
        f"     {C_BLUE}❄️  💎  ❄️{C_RESET}\n   {C_BOLD}{C_CYAN}\"THERMAL EQUILIBRIUM ACHIEVED: 34.0°C!\" ❄️ ✨{C_RESET}"
    ]

    for f in frames:
        print("\033[H\033[J" + f)
        time.sleep(0.4)

    state["squad_desires"]["freeze_kirby"]["craving_met"] = True
    state["squad_desires"]["freeze_kirby"]["last_satisfied"] = time.time()
    state["needs"]["rest"]["level"] = min(100, state["needs"]["rest"]["level"] + 10)
    state["care_history_count"]["cpu_chills"] = state["care_history_count"].get("cpu_chills", 0) + 1

    save_needs_state(state)

    if HAS_AUDIO:
        try:
            play_sound_preset("sonar")
        except Exception:
            pass

    record_ledger("FREEZE_CHILL", f"Freeze Kirby cooled system thermals from {cur_temp} to tranquil 34°C", xp=35)
    print(f"\n{C_BOLD}{C_GREEN}[✔] Freeze Kirby's cooling craving satisfied! CPU thermals chilled to tranquility. ❄️ 🧊{C_RESET}\n")


def action_feed(food_arg: Optional[str] = None):
    # Delegate to kirby_pet_care.py feed command
    food_name = food_arg or "strawberry_cake"
    cmd = [sys.executable, str(BASE_DIR / "scripts" / "kirby_pet_care.py"), "feed", food_name]
    subprocess.run(cmd)

    state = load_needs_state()
    state["needs"]["satiety"]["level"] = 100
    state["needs"]["satiety"]["status"] = "Feasted & Satiated"
    state["needs"]["satiety"]["last_fulfilled"] = time.time()
    state["care_history_count"]["meals_enjoyed"] = state["care_history_count"].get("meals_enjoyed", 0) + 1
    state["squad_desires"]["kirby_prime"]["craving_met"] = True
    if "pizza" in food_name.lower():
        state["squad_desires"]["noid_kirby"]["craving_met"] = True
    save_needs_state(state)


def action_play():
    state = load_needs_state()
    print(f"\n{C_BOLD}{C_GREEN}[*] Playing a lively game of Star Catching with Kirby! ⭐ 🎮{C_RESET}\n")
    state["needs"]["fun"]["level"] = 100
    state["needs"]["fun"]["status"] = "Ecstatically Joyful"
    state["needs"]["fun"]["last_fulfilled"] = time.time()
    save_needs_state(state)
    if HAS_AUDIO:
        try:
            play_sound_preset("hop")
        except Exception:
            pass
    record_ledger("PLAY_GAME", "Played joyfully with Kirby in the arcade arena", xp=30)
    print(f"{C_BOLD}{C_GREEN}[✔] Kirby's play and fun meter is maxed to 100%! ( ^ ᗜ ^ ) ⭐{C_RESET}\n")


def action_social():
    state = load_needs_state()
    print(f"\n{C_BOLD}{C_PURPLE}[*] Gathering all 10 Kirbies for joyful party banter! 👥 💬{C_RESET}\n")
    cmd = [sys.executable, str(BASE_DIR / "scripts" / "kirby_squad_party.py"), "banter"]
    subprocess.run(cmd)

    state = load_needs_state()
    state["needs"]["social"]["level"] = 100
    state["needs"]["social"]["status"] = "Heartfelt Squad Unity"
    state["needs"]["social"]["last_fulfilled"] = time.time()
    save_needs_state(state)
    record_ledger("SOCIAL_BANTER", "Engaged squad in heartwarming multi-Kirby dialogue", xp=30)


def action_curiosity():
    state = load_needs_state()
    print(f"\n{C_BOLD}{C_GOLD}[*] Sparking Kirby's curiosity with fresh ability synthesis! 🧠 ✨{C_RESET}\n")
    cmd = [sys.executable, str(BASE_DIR / "scripts" / "kirby_learning_engine.py"), "learn", "2"]
    subprocess.run(cmd)

    state = load_needs_state()
    state["needs"]["curiosity"]["level"] = 100
    state["needs"]["curiosity"]["status"] = "Enlightened Wonder"
    state["needs"]["curiosity"]["last_fulfilled"] = time.time()
    save_needs_state(state)
    record_ledger("CURIOSITY_LEARN", "Stimulated curiosity with autopoietic ability synthesis", xp=40)


def action_auto():
    print(f"\n{C_BOLD}{C_PINK}╔══════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║  🌸  KIRBY AUTONOMOUS HOLISTIC CAREGIVER: 100% WELLBEING PROTOCOL  🌸  ║{C_RESET}")
    print(f"{C_BOLD}{C_PINK}╚══════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

    state = load_needs_state()

    # Sequence of care:
    # 1. Feed
    print(f"{C_BOLD}{C_YELLOW}Step 1/6: Feeding Kirby delicious Strawberry Shortcake & Cheesy Pizza...{C_RESET}")
    action_feed("strawberry_cake")
    time.sleep(0.5)

    # 2. Bubble Bath
    print(f"{C_BOLD}{C_BLUE}Step 2/6: Soothing Fountain of Dreams Bubble Bath...{C_RESET}")
    action_bath()
    time.sleep(0.5)

    # 3. Loving Hugs
    print(f"{C_BOLD}{C_PINK}Step 3/6: Warm Cuddles & Head Pats...{C_RESET}")
    action_hug()
    time.sleep(0.5)

    # 4. Spatial Feng Shui
    print(f"{C_BOLD}{C_GOLD}Step 4/6: Aligning Starlight Room Feng Shui & Cozy Qi...{C_RESET}")
    action_fengshui()
    time.sleep(0.5)

    # 5. Freeze CPU Chill
    print(f"{C_BOLD}{C_CYAN}Step 5/6: Freeze Kirby Thermal Chill...{C_RESET}")
    action_cool()
    time.sleep(0.5)

    # 6. Nap & Rest
    print(f"{C_BOLD}{C_CYAN}Step 6/6: Tucking into Dream Cloud for Starlight Recharge...{C_RESET}")
    action_nap()
    time.sleep(0.5)

    # Max all needs
    state = load_needs_state()
    for k in state["needs"]:
        state["needs"][k]["level"] = 100
        state["needs"][k]["status"] = get_need_status_label(k, 100)
        state["needs"][k]["last_fulfilled"] = time.time()

    for k in state["squad_desires"]:
        state["squad_desires"][k]["craving_met"] = True
        state["squad_desires"][k]["last_satisfied"] = time.time()

    save_needs_state(state)

    print(f"\n{C_BOLD}{C_GREEN}🎉 ALL 8 ESSENTIAL NEEDS & 10 SQUAD DESIRES ELEVATED TO 100% PRISTINE BLISS! 🎉{C_RESET}")
    print(f"{C_BOLD}{C_PINK}Kirby Prime & the entire 10-Kirby roster are completely cherished, fed, sparkling, and cozy! Poyo! 🌸✨{C_RESET}\n")


def action_fulfill(need_name: str):
    key = need_name.lower().strip()
    if key in ("satiety", "hunger", "food", "feed"):
        action_feed()
    elif key in ("rest", "sleep", "nap", "energy"):
        action_nap()
    elif key in ("hygiene", "bath", "wash", "spa", "clean"):
        action_bath()
    elif key in ("affection", "hug", "cuddle", "pat", "love"):
        action_hug()
    elif key in ("sanctuary", "fengshui", "room", "comfort", "qi"):
        action_fengshui()
    elif key in ("cool", "chill", "freeze", "thermal"):
        action_cool()
    elif key in ("fun", "play", "game"):
        action_play()
    elif key in ("social", "banter", "squad"):
        action_social()
    elif key in ("curiosity", "learn", "card"):
        action_curiosity()
    elif key in ("all", "auto", "everything"):
        action_auto()
    else:
        print(f"{C_RED}Unknown need: '{need_name}'{C_RESET}")
        print(f"Valid needs: satiety, rest, hygiene, affection, fun, social, curiosity, sanctuary, cool, all")


def main():
    parser = argparse.ArgumentParser(description="Kirby Companion Needs & Wellbeing Engine")
    subparsers = parser.add_subparsers(dest="subcommand")

    subparsers.add_parser("status", help="View Kirby's 8 Core Needs & Squad Desires Matrix")
    subparsers.add_parser("nap", help="Tuck Kirby into Dream Cloud for a restorative sleep")
    subparsers.add_parser("sleep", help="Alias for nap")
    subparsers.add_parser("wake", help="Gently awaken Kirby with morning starlight")
    subparsers.add_parser("bath", help="Fountain of Dreams bubble spa bath")
    subparsers.add_parser("spa", help="Alias for bath")
    subparsers.add_parser("wash", help="Alias for bath")
    subparsers.add_parser("hug", help="Give Kirby a warm, loving embrace & head pats")
    subparsers.add_parser("cuddle", help="Alias for hug")
    subparsers.add_parser("fengshui", help="Harmonize room Spatial Feng Shui & cozy Qi")
    subparsers.add_parser("comfort", help="Alias for fengshui")
    subparsers.add_parser("cool", help="Freeze Kirby Glacial Chill to cool CPU thermals")
    subparsers.add_parser("chill", help="Alias for cool")
    subparsers.add_parser("auto", help="Autonomous Caregiver: fulfill all needs to 100%")

    p_fulfill = subparsers.add_parser("fulfill", help="Fulfill a specific need")
    p_fulfill.add_argument("need", nargs="?", default="all", help="Name of need to fulfill")

    p_feed = subparsers.add_parser("feed", help="Feed Kirby delicious snacks")
    p_feed.add_argument("item", nargs="?", default=None, help="Food item name")

    subparsers.add_parser("test", help="Run automated verification for Needs Engine")

    args = parser.parse_args()

    if args.subcommand in ("status", None):
        cmd_status()
    elif args.subcommand in ("nap", "sleep"):
        action_nap()
    elif args.subcommand == "wake":
        action_wake()
    elif args.subcommand in ("bath", "spa", "wash"):
        action_bath()
    elif args.subcommand in ("hug", "cuddle"):
        action_hug()
    elif args.subcommand in ("fengshui", "comfort"):
        action_fengshui()
    elif args.subcommand in ("cool", "chill"):
        action_cool()
    elif args.subcommand == "auto":
        action_auto()
    elif args.subcommand == "fulfill":
        action_fulfill(args.need)
    elif args.subcommand == "feed":
        action_feed(args.item)
    elif args.subcommand == "test":
        # Headless automated test
        print("[TEST] Verifying Kirby Needs Engine...")
        st = load_needs_state()
        assert "needs" in st, "Needs missing from state"
        assert "overall_wellbeing" in st, "Overall wellbeing missing"
        assert len(st["needs"]) == 8, f"Expected 8 needs, got {len(st['needs'])}"
        save_needs_state(st)
        print("[TEST] State load/save & 8 Core Needs verified.")
        print("[TEST] PASS: Kirby Needs Engine OK.")


if __name__ == "__main__":
    main()
