#!/usr/bin/env python3
"""
🌸 KIRBY UNIFIED BUDDY COMPANION SYSTEM (kirby_buddies.py) 🌸
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_buddies.py
CLI: kirby buddy [status|list|summon|play|feed|banter|assist|test]
     kirby minion [status|banana|wrench|cheer|beedo|dance]
     kirby metroid [status|drain|freeze|chirp|shield]

Features:
1. Iconic Buddy Companions:
   - 🍌 Minion Buddy (Bob / Kevin): Pit Crew Chief, Overalls & Goggles, Wrench & Banana
   - 🛸 Metroid Buddy (The Baby): Biotic Glitch Devourer, Floating Translucent Dome, Red Nuclei
   - ⛑️ Mettaur Buddy (Foreman Metty): Hardhat Safety Officer, Titanium Pickaxe
   - Plus Caretaker Duo: Bandana Dee 💙 & Chef Kawasaki 🍳
2. Interactive Mechanics:
   - Minion Banana Boost (+50% energy), Wrench Repair, Wacky Minion Dance, "BEE-DO" Alarm
   - Metroid Glitch Bio-Drain, Cryo Freezing Shield (-40°C), Sonar Chirp, Biotic Barrier
   - Mettaur Safety Audit & Pickaxe Quarrying
3. Cross-Buddy Banter:
   - Heartwarming, comical conversations between Minion, Metroid, Mettaur, and Kirby.
4. Persistent State in .kirby_buddies_state.json & Ledger Sync.
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
BUDDIES_STATE_FILE = BASE_DIR / ".kirby_buddies_state.json"
NEEDS_STATE_FILE = BASE_DIR / ".kirby_needs_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"
SCRIPTS_DIR = BASE_DIR / "scripts"

HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


DEFAULT_BUDDIES_DATA: Dict[str, Any] = {
    "version": "1.0.0",
    "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "active_buddies": ["minion_buddy", "metroid_buddy", "mettaur_buddy"],
    "buddies": {
        "minion_buddy": {
            "id": "minion_buddy",
            "name": "Bob the Minion",
            "nickname": "Minion Buddy",
            "title": "Pit Crew Chief & Morale Booster",
            "icon": "🍌",
            "species": "Minion",
            "outfit": "Denim Overalls, Steampunk Goggles, Safety Boots",
            "held_item": "Overclocked Socket Wrench & Ripe Banana",
            "energy": 98,
            "affection": 96,
            "bananas_stashed": 48,
            "repairs_completed": 31,
            "high_fives_given": 54,
            "dialogues": [
                "BEE-DO! BEE-DO! All systems running smooth, boss! 🍌",
                "Bello! Me bring yummy banana for Kirby! Poyo!",
                "Wrench is calibrated! Any loose bolts on port 8088?",
                "Banana-ba-na-na! High five, Kirby buddy! ⭐"
            ]
        },
        "metroid_buddy": {
            "id": "metroid_buddy",
            "name": "The Baby Metroid",
            "nickname": "Metroid Buddy",
            "title": "Biotic Glitch Devourer & Floating Guardian",
            "icon": "🛸",
            "species": "Baby Metroid (Dream Land 3 Variant)",
            "outfit": "Translucent Bioluminescent Jelly Dome",
            "held_item": "Floating Twin Mandibles & 3 Pulsing Nuclei",
            "energy": 95,
            "affection": 99,
            "nuclei_clarity": 100,
            "glitches_devoured": 42,
            "cryo_temp_c": -45.0,
            "dialogues": [
                "Skreeeee! *happy alien chirp* (Chirps affectionately at Kirby) 🛸✨",
                "*gentle floating hum* Devouring stray memory leaks from background daemons...",
                "*nuzzles Kirby's rosy cheek with squishy gelatinous dome*",
                "Skree-poyo! Biotic thermal cryo-shield deployed! ❄️"
            ]
        },
        "mettaur_buddy": {
            "id": "mettaur_buddy",
            "name": "Foreman Metty",
            "nickname": "Mettaur Buddy",
            "title": "Heavy Construction Foreman & Safety Inspector",
            "icon": "⛑️",
            "species": "Mettaur (Hardhat)",
            "outfit": "Yellow Mark-IV Hardhat, Safety Vest",
            "held_item": "Titanium Pickaxe & Blueprint Board",
            "energy": 92,
            "affection": 91,
            "safety_rating": 100,
            "star_coins_mined": 220,
            "blueprints_approved": 18,
            "dialogues": [
                "Safety first! Helmets buckled and chin straps tightened! ⛑️",
                "Quarried 20 fresh Star Coins from the storage partition!",
                "All scaffolds meet 5-star Dream Land construction codes!",
                "Whenever trouble strikes: DUCK and DEFLECT! TING! ✨"
            ]
        }
    }
}


def load_buddies_state() -> Dict[str, Any]:
    if BUDDIES_STATE_FILE.exists():
        try:
            with open(BUDDIES_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT_BUDDIES_DATA))


def save_buddies_state(state: Dict[str, Any]):
    state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(BUDDIES_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def record_ledger(action: str, details: str, xp: int = 30):
    LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "action": f"BUDDY_{action}",
        "details": details,
        "xpGained": xp
    }
    with open(LEDGER_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def play_fx(sound_name: str):
    if HAS_AUDIO:
        try:
            play_sound_preset(sound_name)
        except Exception:
            pass


def render_minion_buddy_ascii() -> str:
    return f"""
{C_YELLOW}              .--------.
           .-'   {C_WHITE}(o)(o){C_YELLOW}   '-.        {C_GOLD}🍌 "Bello!"{C_YELLOW}
          /    {C_DARK_GRAY}[======]{C_YELLOW}     \\
         |       {C_RED}\\__/       {C_YELLOW}|      {C_CYAN}🔧 *CLINK*{C_YELLOW}
         |                  |
         |    {C_BLUE}.--------.{C_YELLOW}    |
         |   {C_BLUE}/   {C_WHITE}(G){C_BLUE}   \\{C_YELLOW}   |    {C_WHITE}BOB THE MINION BUDDY{C_YELLOW}
         |  {C_BLUE}|   OVER-  |{C_YELLOW}  |    {C_DIM}Pit Crew Chief & Morale Booster{C_YELLOW}
         '--{C_BLUE}|   ALLS   |{C_YELLOW}--'
            {C_BLUE}'----------'{C_YELLOW}
            {C_DARK_GRAY}(____)(____){C_RESET}
"""


def render_metroid_buddy_ascii() -> str:
    return f"""
{C_GREEN}              .----------------.
           .-'   {C_RED}(●)      (●){C_GREEN}   '-.       {C_CYAN}🛸 "Skreeeee!"{C_GREEN}
         .'      {C_CYAN}~~~      ~~~{C_GREEN}      '.
        /     {C_RED}*  (●)  *{C_GREEN}             \\    {C_HOT_PINK}✨ BIOTIC PULSE ✨{C_GREEN}
       |     {C_CYAN}3 PULSING NUCLEI{C_GREEN}        |
       |     {C_GREEN}TRANSLUCENT JELLY{C_GREEN}       |   {C_WHITE}THE BABY METROID{C_GREEN}
        \\_         {C_WHITE}\\  /{C_GREEN}            _/   {C_DIM}Glitch Devourer & Guardian{C_GREEN}
          '--.     {C_WHITE}\\/{C_GREEN}         .--'
              {C_WHITE}/\\        /\\{C_RESET}
"""


def render_buddies_trio_ascii() -> str:
    return f"""
{C_PINK}   ⭐ KIRBY & HIS BEST BUDDIES: MINION BOB, BABY METROID & FOREMAN METTY ⭐{C_RESET}

{C_GREEN}         [METROID]               {C_YELLOW}[METTAUR HELM]            {C_GOLD}[MINION BUDDY]{C_RESET}
{C_GREEN}        .--------.              {C_YELLOW}.------------.            {C_YELLOW}.--------.{C_RESET}
{C_GREEN}      .-' {C_RED}(●)  (●){C_GREEN} '-.          {C_YELLOW}.-' {C_WHITE}[+] SAFETY{C_YELLOW} '-.        {C_YELLOW}.-' {C_WHITE}(o)(o){C_YELLOW} '-.{C_RESET}
{C_GREEN}     /   {C_CYAN}~~ {C_RED}(●){C_CYAN} ~~{C_GREEN}   \\        {C_YELLOW}/   {C_WHITE}/--------\\{C_YELLOW}   \\      {C_YELLOW}/   {C_DARK_GRAY}[======]{C_YELLOW}   \\{C_RESET}
{C_GREEN}     |  {C_CYAN}BIOTIC JELLY{C_GREEN}  |       {C_YELLOW}|==={C_WHITE}(  MARK-IV ){C_YELLOW}===|     {C_YELLOW}|     {C_RED}\\__/{C_YELLOW}     |{C_RESET}
{C_GREEN}      \\_   {C_WHITE}\\/{C_GREEN}      _/        {C_YELLOW}'----------------'     {C_YELLOW}|   {C_BLUE}.------.{C_YELLOW}   |{C_RESET}
{C_GREEN}        {C_WHITE}/\\    /\\{C_RESET}                   {C_PINK}.----------.{C_RESET}          {C_YELLOW}|  {C_BLUE}| {C_WHITE}(G)  {C_BLUE}|{C_YELLOW}  |{C_RESET}
                                {C_PINK}/   {C_WHITE}●    ●{C_PINK}   \\{C_RESET}         {C_BLUE}'----------'{C_RESET}
      {C_CYAN}🛸 "Skree-poyo!"{C_RESET}       {C_HOT_PINK}(> (    {C_HOT_PINK}♥    ♥{C_PINK}   ) <) {C_GOLD}🍌 "Bello Kirby!"{C_RESET}
                                {C_PINK}\\     {C_RED}▽{C_PINK}    /{C_RESET}
                               {C_RED}.'---.  .---'.{C_RESET}
                              {C_RED}(_____) (_____){C_RESET}
"""


class KirbyBuddiesEngine:
    def __init__(self):
        self.state = load_buddies_state()

    def list_buddies(self) -> Dict[str, Any]:
        return self.state.get("buddies", {})

    def get_buddy(self, buddy_id: str) -> Optional[Dict[str, Any]]:
        clean_id = buddy_id.lower().replace("buddy_", "").replace("buddy", "")
        for k, b in self.state.get("buddies", {}).items():
            if k == clean_id or clean_id in k or b["nickname"].lower() == clean_id:
                return b
        return None

    def minion_banana(self) -> Dict[str, Any]:
        b = self.state["buddies"]["minion_buddy"]
        b["bananas_stashed"] += 1
        b["affection"] = min(100, b["affection"] + 2)
        save_buddies_state(self.state)
        play_fx("bubble_pop")

        # Feed squad & update needs
        try:
            subprocess.run([sys.executable, str(SCRIPTS_DIR / "kirby_needs.py"), "feed", "banana"], capture_output=True)
        except Exception:
            pass

        record_ledger("MINION_BANANA", "Minion Buddy handed Kirby a sweet golden energy banana! (+50% Energy)", xp=35)
        return {
            "status": "BANANA_BOOST",
            "buddy": b["name"],
            "bananas_total": b["bananas_stashed"],
            "speech": "Bello! Banana for Kirby! Yummy poyo! 🍌✨",
            "effect": "+50% Energy & Satiety restored to Kirby!"
        }

    def minion_repair(self) -> Dict[str, Any]:
        b = self.state["buddies"]["minion_buddy"]
        b["repairs_completed"] += 1
        save_buddies_state(self.state)
        play_fx("wrench_ratchet")
        record_ledger("MINION_REPAIR", "Minion Buddy torqued ADB sockets and tuned daemon ports", xp=30)
        return {
            "status": "REPAIRED",
            "buddy": b["name"],
            "repairs_total": b["repairs_completed"],
            "speech": "All bolts tightened on port 8088! Everything shipshape, boss! 🔧",
            "effect": "Subsystem connections verified and tuned."
        }

    def minion_beedo(self) -> Dict[str, Any]:
        play_fx("minion_beedo")
        record_ledger("MINION_BEEDO", "Minion Buddy sounded the iconic BEE-DO alarm siren!", xp=25)
        return {
            "status": "ALARM_SOUNDED",
            "siren": "BEE-DO! BEE-DO!",
            "speech": "🚨 BEE-DO! BEE-DO! Minion hazard squad standing by! 🚨"
        }

    def minion_dance(self) -> Dict[str, Any]:
        b = self.state["buddies"]["minion_buddy"]
        b["high_fives_given"] += 1
        save_buddies_state(self.state)
        play_fx("kirby")
        record_ledger("MINION_DANCE", "Minion Buddy & Kirby performed a cheerful synchronized shuffle dance!", xp=35)
        return {
            "status": "DANCED",
            "speech": "Ta-da! Dance party with Kirby! High five! ⭐🍌",
            "high_fives": b["high_fives_given"]
        }

    def metroid_drain(self) -> Dict[str, Any]:
        b = self.state["buddies"]["metroid_buddy"]
        b["glitches_devoured"] += 1
        b["nuclei_clarity"] = min(100, b["nuclei_clarity"] + 1)
        save_buddies_state(self.state)
        play_fx("metroid_chirp")
        record_ledger("METROID_DRAIN", f"Baby Metroid devoured memory glitch bugs! Total: {b['glitches_devoured']}", xp=40)
        return {
            "status": "GLITCH_DRAINED",
            "buddy": b["name"],
            "glitches_eaten": b["glitches_devoured"],
            "nuclei_clarity": b["nuclei_clarity"],
            "speech": "Skreeee! *alien purr* Devoured residual memory bugs into pure starlight! 🛸✨",
            "effect": "Cleaned memory leaks and boosted nuclei luminescence."
        }

    def metroid_freeze(self) -> Dict[str, Any]:
        b = self.state["buddies"]["metroid_buddy"]
        b["cryo_temp_c"] = round(random.uniform(-40.0, -60.0), 1)
        save_buddies_state(self.state)
        play_fx("glass_ping")

        # Invoke needs cooling
        try:
            subprocess.run([sys.executable, str(SCRIPTS_DIR / "kirby_needs.py"), "cool"], capture_output=True)
        except Exception:
            pass

        record_ledger("METROID_FREEZE", f"Baby Metroid emitted sub-zero cryo wave ({b['cryo_temp_c']}°C), cooling CPU", xp=35)
        return {
            "status": "CRYO_CHILLED",
            "temp": b["cryo_temp_c"],
            "speech": "Chirp-chirp! Sub-zero cryo membrane cooled device thermals to 34°C! ❄️",
            "effect": "CPU thermals cooled to serene ice levels."
        }

    def metroid_sonar(self) -> Dict[str, Any]:
        play_fx("sonar")
        found_coins = random.randint(10, 30)
        record_ledger("METROID_SONAR", f"Baby Metroid ultrasonic sonar located +{found_coins} hidden Star Coins", xp=30)
        return {
            "status": "SONAR_PULSE",
            "coins_found": found_coins,
            "speech": "Skree-chirp! Ultrasonic sonar uncovered hidden star treasure! 🪙💎"
        }

    def metroid_shield(self) -> Dict[str, Any]:
        play_fx("plasma")
        record_ledger("METROID_SHIELD", "Baby Metroid deployed zero-suit biotic barrier around Kirby", xp=35)
        return {
            "status": "SHIELDED",
            "speech": "Skreeeee! Translucent biotic bubble barrier protects Kirby from all damage! 🛡️✨"
        }

    def banter(self) -> List[Dict[str, str]]:
        dialogues_pool = [
            [
                ("Minion Bob", "🍌", "Bello! Me offer Baby Metroid nice yellow banana! Want some?"),
                ("The Baby", "🛸", "Skreeeee? *sniffs banana with curiosity, floats on top of it, and hums happily*"),
                ("Foreman Metty", "⛑️", "Careful with that fruit! Is it OSHA approved? Helmet inspections first!"),
                ("Kirby Prime", "🌸", "Poyo! *eats the banana in one gulp, hugs everyone tightly*")
            ],
            [
                ("Foreman Metty", "⛑️", "Today's construction objective: reinforce the dev web portal on port 8088!"),
                ("Minion Bob", "🍌", "Me got the socket wrench! Tighten, tighten! BEE-DO BEE-DO!"),
                ("The Baby", "🛸", "Skree-chirp! *devours loose glitch fragments floating in the scaffolding*"),
                ("Kirby Prime", "🌸", "Poyo builder! Safety hardhat equipped! TING! ✨")
            ],
            [
                ("The Baby", "🛸", "*nuzzles Minion Bob's goggles gently with soft squishy dome* Skreeee~"),
                ("Minion Bob", "🍌", "Hehehe! Ticklish! Baby Metroid is super soft like marshmallow!"),
                ("Bandana Dee", "💙", "Awww, look at them! I fluffed a cloud pillow for all of us to cuddle on!"),
                ("Chef Kawasaki", "🍳", "Hot Maxi-Tomato soup is served! Extra star noodles for the buddies!")
            ]
        ]
        chosen = random.choice(dialogues_pool)
        play_fx("kirby")
        record_ledger("BUDDY_BANTER", f"Buddy banter played between {', '.join([c[0] for c in chosen])}", xp=25)
        return [{"speaker": s[0], "icon": s[1], "text": s[2]} for s in chosen]


def print_status(engine: KirbyBuddiesEngine):
    buddies = engine.list_buddies()

    print(f"\n{C_BOLD}{C_PINK}⭐ ═══════════════════════════════════════════════════════════════════════ ⭐{C_RESET}")
    print(f"{C_BOLD}{C_PINK}     🌸 KIRBY & BEST BUDDIES COMPANION DECK (PIXEL 9 PRO XL) 🌸{C_RESET}")
    print(f"{C_BOLD}{C_PINK}⭐ ═══════════════════════════════════════════════════════════════════════ ⭐{C_RESET}")
    print(render_buddies_trio_ascii())

    for k, b in buddies.items():
        print(f"{C_BOLD}{C_YELLOW}▶ {b['icon']} {b['name'].upper()} ({b['nickname']}){C_RESET}")
        print(f"    {C_CYAN}Title:{C_RESET}       {b['title']}")
        print(f"    {C_WHITE}Gear:{C_RESET}        {b.get('held_item', 'None')} | {C_DIM}Outfit: {b.get('outfit', 'Standard')}{C_RESET}")
        print(f"    {C_GREEN}Energy:{C_RESET}      {b.get('energy', 95)}%  |  {C_HOT_PINK}Affection:{C_RESET} {b.get('affection', 95)}%")
        if k == "minion_buddy":
            print(f"    {C_GOLD}Stats:{C_RESET}       {b.get('bananas_stashed', 0)} Bananas 🍌 | {b.get('repairs_completed', 0)} Repairs 🔧 | {b.get('high_fives_given', 0)} High-Fives ⭐")
        elif k == "metroid_buddy":
            print(f"    {C_GREEN}Stats:{C_RESET}       {b.get('glitches_devoured', 0)} Glitches Devoured 👾 | {b.get('nuclei_clarity', 100)}% Nuclei Clarity 💎 | {b.get('cryo_temp_c', -45)}°C Cryo ❄️")
        elif k == "mettaur_buddy":
            print(f"    {C_YELLOW}Stats:{C_RESET}       {b.get('safety_rating', 100)}% Safety Score ⛑️ | {b.get('star_coins_mined', 0)} Star Coins Quarried 🪙")
        print(f"    {C_PURPLE}Quote:{C_RESET}       \"{random.choice(b['dialogues'])}\"")
        print()

    print(f"{C_BOLD}Direct Commands:{C_RESET}")
    print(f"  kirby buddy banter            - Listen to delightful cross-buddy chatter")
    print(f"  kirby minion banana           - Feed Kirby an energy-packed golden banana")
    print(f"  kirby minion repair           - Wrench repair on mesh services & ports")
    print(f"  kirby minion beedo            - Sound the hilarious BEE-DO alarm siren")
    print(f"  kirby minion dance            - Joyful synchronized minion shuffle dance")
    print(f"  kirby metroid drain           - Devour memory leaks & bug anomalies")
    print(f"  kirby metroid freeze          - Sub-zero cryo wave cooling CPU thermals")
    print(f"  kirby metroid sonar           - Ultrasonic pulse uncovering secret Star Coins")
    print(f"  kirby metroid shield          - Surrounds Kirby with translucent biotic bubble\n")


def main():
    parser = argparse.ArgumentParser(description="Kirby Unified Buddy Engine")
    subparsers = parser.add_subparsers(dest="subcommand", help="Buddy command to execute")

    # status / list
    subparsers.add_parser("status", help="Display all buddies status and ASCII artwork")
    subparsers.add_parser("list", help="List all buddy companions")

    # banter
    subparsers.add_parser("banter", help="Trigger lively conversation between Kirby and buddies")

    # minion shortcuts
    p_minion = subparsers.add_parser("minion", help="Minion buddy actions")
    p_minion.add_argument("action", nargs="?", default="status", choices=["status", "banana", "repair", "wrench", "beedo", "alarm", "dance", "cheer"])

    # metroid shortcuts
    p_metroid = subparsers.add_parser("metroid", help="Metroid buddy actions")
    p_metroid.add_argument("action", nargs="?", default="status", choices=["status", "drain", "freeze", "cool", "sonar", "chirp", "shield"])

    # test
    subparsers.add_parser("test", help="Run automated test suite for buddy systems")

    args = parser.parse_args()
    engine = KirbyBuddiesEngine()

    if not args.subcommand or args.subcommand in ("status", "list"):
        print_status(engine)

    elif args.subcommand == "banter":
        lines = engine.banter()
        print(f"\n{C_BOLD}{C_PINK}💬 ═══════════════════════════════════════════════════════════════════ 💬{C_RESET}")
        print(f"{C_BOLD}{C_PINK}     🌸 KIRBY & BUDDIES LIVE CONVERSATION STREAM 🌸{C_RESET}")
        print(f"{C_BOLD}{C_PINK}💬 ═══════════════════════════════════════════════════════════════════ 💬{C_RESET}\n")
        for line in lines:
            print(f"  {line['icon']} {C_BOLD}{line['speaker']:<16}{C_RESET}: {C_WHITE}\"{line['text']}\"{C_RESET}")
            time.sleep(0.12)
        print()

    elif args.subcommand == "minion":
        act = args.action
        if act == "status":
            print(render_minion_buddy_ascii())
            b = engine.state["buddies"]["minion_buddy"]
            print(f"{C_BOLD}{C_YELLOW}🍌 {b['name']} ({b['nickname']}){C_RESET} - {b['title']}")
            print(f"   Bananas: {b['bananas_stashed']} | Repairs: {b['repairs_completed']} | High-Fives: {b['high_fives_given']}")
            print(f"   Dialogue: \"{random.choice(b['dialogues'])}\"\n")
        elif act == "banana":
            res = engine.minion_banana()
            print(f"\n{C_BOLD}{C_GOLD}🍌 MINION POTASSIUM BOOST! 🍌{C_RESET}")
            print(f"  {C_GREEN}[✔] {res['speech']}{C_RESET}")
            print(f"  {res['effect']} (Total Stashed: {res['bananas_total']})\n")
        elif act in ("repair", "wrench"):
            res = engine.minion_repair()
            print(f"\n{C_BOLD}{C_CYAN}🔧 MINION PIT CREW WRENCH REPAIR! 🔧{C_RESET}")
            print(f"  {C_GREEN}[✔] {res['speech']}{C_RESET}")
            print(f"  {res['effect']} (Total Repairs: {res['repairs_total']})\n")
        elif act in ("beedo", "alarm"):
            res = engine.minion_beedo()
            print(f"\n{C_BOLD}{C_RED}🚨 {res['siren']} 🚨{C_RESET}")
            print(f"  {res['speech']}\n")
        elif act in ("dance", "cheer"):
            res = engine.minion_dance()
            print(f"\n{C_BOLD}{C_YELLOW}💃 MINION SHUFFLE & KIRBY HIGH-FIVE! 💃{C_RESET}")
            print(f"  {C_GREEN}[✔] {res['speech']}{C_RESET}")
            print(f"  High-Fives Exchanged: {res['high_fives']} ⭐\n")

    elif args.subcommand == "metroid":
        act = args.action
        if act == "status":
            print(render_metroid_buddy_ascii())
            b = engine.state["buddies"]["metroid_buddy"]
            print(f"{C_BOLD}{C_GREEN}🛸 {b['name']} ({b['nickname']}){C_RESET} - {b['title']}")
            print(f"   Glitches Devoured: {b['glitches_devoured']} | Nuclei Clarity: {b['nuclei_clarity']}% | Cryo: {b['cryo_temp_c']}°C")
            print(f"   Dialogue: \"{random.choice(b['dialogues'])}\"\n")
        elif act == "drain":
            res = engine.metroid_drain()
            print(f"\n{C_BOLD}{C_GREEN}👾 BIOTIC GLITCH DEVOURER! 👾{C_RESET}")
            print(f"  {C_GREEN}[✔] {res['speech']}{C_RESET}")
            print(f"  {res['effect']} (Glitches Eaten: {res['glitches_eaten']}, Clarity: {res['nuclei_clarity']}%)\n")
        elif act in ("freeze", "cool"):
            res = engine.metroid_freeze()
            print(f"\n{C_BOLD}{C_CYAN}❄️ METROID SUB-ZERO CRYO MEMBRANE! ❄️{C_RESET}")
            print(f"  {C_GREEN}[✔] {res['speech']}{C_RESET}")
            print(f"  Cryo temperature: {res['temp']}°C | CPU thermals cooled to serene ice levels.\n")
        elif act in ("sonar", "chirp"):
            res = engine.metroid_sonar()
            print(f"\n{C_BOLD}{C_GOLD}📡 ULTRASONIC ALIEN SONAR PULSE! 📡{C_RESET}")
            print(f"  {C_GREEN}[✔] {res['speech']}{C_RESET}")
            print(f"  Uncovered: +{res['coins_found']} Star Coins! 🪙\n")
        elif act == "shield":
            res = engine.metroid_shield()
            print(f"\n{C_BOLD}{C_GREEN}🛡️ BIOTIC BUBBLE BARRIER ACTIVE! 🛡️{C_RESET}")
            print(f"  {C_GREEN}[✔] {res['speech']}\n")

    elif args.subcommand == "test":
        # Verification suite for buddies
        buddies = engine.list_buddies()
        assert "minion_buddy" in buddies
        assert "metroid_buddy" in buddies
        assert "mettaur_buddy" in buddies

        # Test minion
        res_ban = engine.minion_banana()
        assert res_ban["status"] == "BANANA_BOOST"
        res_rep = engine.minion_repair()
        assert res_rep["status"] == "REPAIRED"
        res_bee = engine.minion_beedo()
        assert res_bee["status"] == "ALARM_SOUNDED"

        # Test metroid
        res_drn = engine.metroid_drain()
        assert res_drn["status"] == "GLITCH_DRAINED"
        res_frz = engine.metroid_freeze()
        assert res_frz["status"] == "CRYO_CHILLED"
        res_snr = engine.metroid_sonar()
        assert res_snr["status"] == "SONAR_PULSE"

        # Test banter
        banter_res = engine.banter()
        assert len(banter_res) >= 3

        print(f"{C_GREEN}[✔] Kirby Unified Buddy Companion Engine fully verified! (Minion, Metroid, Mettaur operational){C_RESET}")


if __name__ == "__main__":
    main()
