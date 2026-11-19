#!/usr/bin/env python3
"""
🎩 MAGICIAN KIRBY & TAC SLEIGHT-OF-HAND ENGINE (kirby_magician_tac.py) 🎩
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_magician_tac.py
CLI: kirby magician [trick|act|tarot|play] [--test]

Features:
- Fulfills the Magician Kirby & Tac Cursor Sleight-of-Hand Paradigm.
- 4-Act Zero-LLM Cinematic Screenplay Director:
    Act I:   The Setup (Magician bow, Tac sneaking in the shadows)
    Act II:  The Misdirection (Decoy cursor swap, star wand wave)
    Act III: The Prestige (Hotspot Catapult & Tarot Card pull)
    Act IV:  Resolution ("✨ Presto Chango! ✨", star shower, XP ledger)
- Tarot Card Pulls from the Magician Top Hat:
    * THE_STAR (Poyo Cosmic Transcendence)
    * THE_MAGICIAN (Infinite Possibilities & Sleight)
    * THE_CHARIOT (Warp Star Kinetic Acceleration)
    * THE_FOOL (Noid Gremlin Chaos & Pizza Luck)
    * THE_HERMIT (Freeze Kirby Cold Thermal Contemplation)
    * THE_WHEEL (Autopoietic Learning Evolution)
- Visual ANSI Flourishes & agy_fx_engine audio presets.
- Persistent ledger updates to /mnt/shared/AntiGravity_Shared/ledger/kirby_learning_ledger.jsonl.
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
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"
SQUAD_STATE_FILE = BASE_DIR / ".kirby_squad_state.json"

HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


TAROT_DECK = [
    {
        "card": "THE_STAR",
        "num": "XVII",
        "name": "The Star (Poyo Transcendence)",
        "icon": "⭐",
        "aspect": "Hope, Radiance, Cosmic Inspiration",
        "fortune": "A brilliant constellation aligns above your workspace. Your code flows with zero friction."
    },
    {
        "card": "THE_MAGICIAN",
        "num": "I",
        "name": "The Magician (Sleight of Hand)",
        "icon": "🎩",
        "aspect": "Willpower, Mastery, Creative Alchemy",
        "fortune": "What seemed impossible transforms before your eyes. The decoy yields to pure creation."
    },
    {
        "card": "THE_CHARIOT",
        "num": "VII",
        "name": "The Chariot (Warp Star Velocity)",
        "icon": "🚀",
        "aspect": "Momentum, Hyper-Focus, Conquering Obstacles",
        "fortune": "Accelerate across the mesh. Deployments hit production with blazing speed."
    },
    {
        "card": "THE_FOOL",
        "num": "0",
        "name": "The Fool (Noid Gremlin Mischief)",
        "icon": "🍕",
        "aspect": "Wildcard Chaos, Beginner's Mind, Pizza Fortune",
        "fortune": "Expect the unexpected! A rogue prank uncovers a hidden insight."
    },
    {
        "card": "THE_HERMIT",
        "num": "IX",
        "name": "The Hermit (Freeze Kirby Solitude)",
        "icon": "❄️",
        "aspect": "Inner Wisdom, Cool Thermals, Deep Reflection",
        "fortune": "Silence the chatter. A quiet moment of refactoring cools the architecture."
    },
    {
        "card": "THE_WHEEL",
        "num": "X",
        "name": "The Wheel of Fortune (Autopoiesis)",
        "icon": "🎡",
        "aspect": "Cycles, Evolutionary Upgrades, Destiny",
        "fortune": "The mesh turns in your favor. XP multipliers double across all Kirbies."
    }
]


def log_ledger_magic(action: str, card_info: Dict[str, Any]):
    LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": time.time(),
        "date_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "actor": "magician_kirby",
        "action": action,
        "payload": card_info
    }
    with open(LEDGER_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def perform_screenplay(test: bool = False):
    print(f"\n{C_PURPLE}{C_BOLD}🎩 ═══════════════════════════════════════════════════════════════════════ 🎩{C_RESET}")
    print(f"{C_PURPLE}{C_BOLD}     ✨ MAGICIAN KIRBY & TAC: 4-ACT SLEIGHT-OF-HAND SCREENPLAY ✨{C_RESET}")
    print(f"{C_CYAN}       Starring: Magician Kirby, Tac the Thief & The Operator Pointer{C_RESET}")
    print(f"{C_PURPLE}{C_BOLD}🎩 ═══════════════════════════════════════════════════════════════════════ 🎩{C_RESET}\n")

    acts = [
        ("Act I: The Setup", [
            ("🎩 Magician Kirby", "Tips top hat and bows gracefully to the terminal audience.", 0.6),
            ("🐱 Tac the Cat", "Creeps along the bottom status bar, eyes gleaming like emeralds.", 0.6),
            ("🎩 Magician Kirby", "\"Ladies and gentlemen of the Pixel 9 Pro XL... keep your eyes on the cursor!\"", 0.5)
        ]),
        ("Act II: The Misdirection", [
            ("🎩 Magician Kirby", "Flourishes star wand with a dazzling shower of chromatic sparks! 🪄✨", 0.6),
            ("🐱 Tac the Cat", "SWIPE! Swaps the real pointer with a stationary decoy cursor!", 0.7),
            ("🎩 Magician Kirby", "\"Nothing in this sleeve... nothing behind this terminal prompt!\"", 0.5)
        ]),
        ("Act III: The Prestige", [
            ("🎩 Magician Kirby", "Reaches deep into the velvet top hat and extracts a glowing Tarot card!", 0.7),
            ("🐱 Tac the Cat", "Catapults the operator's focus into the hot productive input zone!", 0.6),
            ("⭐ Starlight Spark", "The cursor returns, glowing with ethereal celestial fire!", 0.5)
        ]),
        ("Act IV: Resolution", [
            ("🎩 Magician Kirby", "\"✨ PRESTO CHANGO! ✨ Everything restored better than before!\"", 0.6),
            ("🐱 Tac the Cat", "Disappears in a puff of lavender smoke with a pouch of Star Coins!", 0.5),
            ("🌸 Choir of Kirbies", "POYO! ( ^-^ )人( ✿◕‿◕)人( ʘ ͜ʖ ʘ ) 🎉", 0.4)
        ])
    ]

    for act_title, beats in acts:
        print(f"{C_GOLD}{C_BOLD}═══ [ {act_title} ] ═══{C_RESET}")
        for actor, line, delay in beats:
            if not test:
                time.sleep(delay)
            print(f"  {C_CYAN}{actor:<18}{C_RESET}: {C_WHITE}{line}{C_RESET}")
        print()

    if HAS_AUDIO:
        play_sound_preset("warp")

    drawn = random.choice(TAROT_DECK)
    print(f"{C_PURPLE}{C_BOLD}🔮 THE PRESTIGE REVELATION:「 {drawn['name']} 」{C_RESET}")
    print(f"  {C_GOLD}Arcana Num{C_RESET} : {drawn['num']}")
    print(f"  {C_CYAN}Aspect    {C_RESET} : {drawn['aspect']}")
    print(f"  {C_GREEN}Fortune   {C_RESET} : \"{drawn['fortune']}\"\n")

    log_ledger_magic("PERFORM_SCREENPLAY", drawn)
    print(f"{C_GREEN}[✔] Magic Prestige recorded to Evolutionary Learning Ledger! 🌸{C_RESET}\n")


def draw_tarot():
    drawn = random.choice(TAROT_DECK)
    print(f"\n{C_PURPLE}{C_BOLD}🎩 MAGICIAN TOP HAT TAROT PULL 🎩{C_RESET}")
    print(f"{C_DIM}─────────────────────────────────────────────────────────────────{C_RESET}")
    print(f"  {drawn['icon']} {C_GOLD}{C_BOLD}{drawn['name']} ({drawn['num']}){C_RESET}")
    print(f"  Domain : {C_CYAN}{drawn['aspect']}{C_RESET}")
    print(f"  Oracular Vision: {C_WHITE}\"{drawn['fortune']}\"{C_RESET}")
    print(f"{C_DIM}─────────────────────────────────────────────────────────────────{C_RESET}\n")

    if HAS_AUDIO:
        play_sound_preset("kirby")

    log_ledger_magic("DRAW_TAROT", drawn)


def main():
    parser = argparse.ArgumentParser(description="Magician Kirby & Tac Sleight-of-Hand Engine")
    subparsers = parser.add_subparsers(dest="command", help="Magician commands")

    subparsers.add_parser("act", help="Perform 4-Act Cinematic Screenplay")
    subparsers.add_parser("trick", help="Perform 4-Act Cinematic Screenplay")
    subparsers.add_parser("tarot", help="Draw a Tarot Card from the Magician Top Hat")
    subparsers.add_parser("test", help="Headless test verification")

    args = parser.parse_args()

    if args.command in ("act", "trick") or not args.command:
        perform_screenplay()
    elif args.command == "tarot":
        draw_tarot()
    elif args.command == "test":
        print("[*] Running Magician Kirby & Tac test verification...")
        assert len(TAROT_DECK) >= 6, "Tarot deck must have at least 6 cards"
        perform_screenplay(test=True)
        print("[✔] Magician Kirby & Tac Engine: 100% OPERATIONAL & VERIFIED!")


if __name__ == "__main__":
    main()
