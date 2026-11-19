#!/usr/bin/env python3
"""
⛑️ KIRBY METTAUR CONSTRUCTION HELMET ENGINE (kirby_mettaur_helmet.py) ⛑️
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_mettaur_helmet.py
CLI: kirby helmet [status|equip|unequip|deflect|crouch|pickaxe|quake|build|test]
     kirby hardhat | kirby mettaur

Features:
1. Iconic Mega Man Mettaur (Met / Hardhat) Copy Ability & Gear for Kirby:
   - Yellow safety construction helmet with white cross emblem (+)
   - Heavy titanium shell with 100% deflection rating
2. Tactical Mechanics:
   - Deflect / Crouch Guard: Kirby completely ducks underneath the hardhat!
     All attacks, exceptions, and anomalies bounce off with a high-Q "TING!" clink.
   - Pickaxe Mining Strike: High-impact pneumatic pickaxe swings break bedrock,
     excavate Star Coins, and dissolve blocking threads.
   - Ground Quake Shockwave: Slams helmet into ground, generating 3-way spread shockwaves.
   - Construction Builder: Deploys heavy safety barricades, girder scaffolding, and workbenches.
3. Persistent State in .kirby_mettaur_state.json.
4. Full ANSI ASCII Visualizations & Procedural Audio FX integration.
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
METTAUR_STATE_FILE = BASE_DIR / ".kirby_mettaur_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"

HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


DEFAULT_METTAUR_STATE: Dict[str, Any] = {
    "version": "1.0.0",
    "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "equipped": True,
    "stance": "STANDBY",  # STANDBY | CROUCH_DEFLECT | MINING | BUILDING
    "helmet_stats": {
        "model": "Mettaur Mark-IV Heavy Hardhat",
        "material": "Hardened Carbyne-Titanium Alloy",
        "armor_rating": 100,
        "deflection_count": 42,
        "mining_depth_meters": 128.5,
        "star_coins_quarried": 340,
        "scaffolds_erected": 14,
        "safety_certification": "OSHA Dream Land Gold Star ★★★★★"
    },
    "current_gear": {
        "helmet_color": "Safety Canary Yellow",
        "emblem": "White Cross (+)",
        "pickaxe": "Reinforced Diamond-Tipped Pneumatic Pickaxe",
        "visor_status": "Anti-Glare HUD Active",
        "earmuffs": "Acoustic Noise-Cancelling Sound Dampeners"
    }
}


def load_mettaur_state() -> Dict[str, Any]:
    if METTAUR_STATE_FILE.exists():
        try:
            with open(METTAUR_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT_METTAUR_STATE))


def save_mettaur_state(state: Dict[str, Any]):
    state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(METTAUR_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def record_ledger(action: str, details: str, xp: int = 25):
    LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "action": f"METTAUR_HELMET_{action}",
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


def render_mettaur_kirby_ascii(stance: str = "STANDBY") -> str:
    if stance == "CROUCH_DEFLECT":
        # Completely turtled under the hardhat, cute eyes peeking through bottom gap, TING! sparks!
        return f"""
{C_YELLOW}              .--------------------.
           .-'       {C_WHITE}[+] SAFETY{C_YELLOW}       '-.
         .'      {C_WHITE}__________________{C_YELLOW}      '.
        /      {C_WHITE}/                  \\{C_YELLOW}       \\
       |======{C_WHITE}(  METTAUR MARK-IV  ){C_YELLOW}======|  {C_CYAN}✨ *TING!* ✨{C_YELLOW}
       |===================================|  {C_WHITE}💥 DEFLECT!{C_YELLOW}
        \\_                               _/
          '--{C_PINK}( {C_WHITE}●       ●{C_PINK} ){C_YELLOW}----------------'
              {C_RED}(___)     (___){C_RESET}
"""
    elif stance == "MINING":
        # Kirby swinging the pickaxe with sparks
        return f"""
{C_YELLOW}               .------------------.
            .-'      {C_WHITE}[+] SAFETY{C_YELLOW}    '-.      {C_CYAN}⛏️ *CLANG!*{C_YELLOW}
          .'     {C_WHITE}__________________{C_YELLOW}  '.     {C_WHITE}_____{C_YELLOW}
         /     {C_WHITE}/                  \\{C_YELLOW}   \\   {C_WHITE}/  |  \\{C_YELLOW}
        |====={C_WHITE}(  METTAUR HARDHAT   ){C_YELLOW}====| {C_WHITE}/___|___\\{C_YELLOW}
         '------------------------------'      {C_YELLOW}| |{C_YELLOW}
                 {C_PINK}.------------.{C_YELLOW}                | |
               {C_PINK}/   {C_WHITE}●      ●{C_PINK}   \\               | |
          {C_HOT_PINK}(> {C_PINK}(    {C_HOT_PINK}♥      ♥{C_PINK}     ) {C_YELLOW}===O========' '{C_RESET}
              {C_PINK}\\     {C_RED}▽{C_PINK}      /       {C_GOLD}*QUARRY SHARD!* 💎{C_RESET}
             {C_RED}.'---.    .---'.{C_RESET}
            {C_RED}(______)  (______){C_RESET}
"""
    else:  # STANDBY
        # Kirby standing proudly wearing the oversized yellow Mettaur helmet
        return f"""
{C_YELLOW}               .------------------.
            .-'      {C_WHITE}[+] SAFETY{C_YELLOW}    '-.
          .'     {C_WHITE}__________________{C_YELLOW}  '.
         /     {C_WHITE}/                  \\{C_YELLOW}   \\
        |====={C_WHITE}(  METTAUR HARDHAT   ){C_YELLOW}====|
        |================================|
         '------------------------------'
                 {C_PINK}.------------.{C_RESET}
               {C_PINK}/   {C_WHITE}●      ●{C_PINK}   \\{C_RESET}
          {C_HOT_PINK}(> {C_PINK}(    {C_HOT_PINK}♥      ♥{C_PINK}     ) <){C_RESET}
              {C_PINK}\\     {C_RED}▽{C_PINK}      /{C_RESET}       {C_YELLOW}⛑️ "Poyo Builder!" ✨{C_RESET}
             {C_RED}.'---.    .---'.{C_RESET}
            {C_RED}(______)  (______){C_RESET}
"""


class KirbyMettaurEngine:
    def __init__(self):
        self.state = load_mettaur_state()

    def equip(self) -> Dict[str, Any]:
        self.state["equipped"] = True
        self.state["stance"] = "STANDBY"
        save_mettaur_state(self.state)
        play_fx("mettaur_clink")
        record_ledger("EQUIPPED", "Equipped Mettaur Mark-IV Heavy Hardhat")
        return {"status": "EQUIPPED", "state": self.state}

    def unequip(self) -> Dict[str, Any]:
        self.state["equipped"] = False
        self.state["stance"] = "STANDBY"
        save_mettaur_state(self.state)
        play_fx("hop")
        record_ledger("UNEQUIPPED", "Stowed Mettaur Hardhat in Master Toolbox")
        return {"status": "UNEQUIPPED", "state": self.state}

    def deflect(self) -> Dict[str, Any]:
        self.state["equipped"] = True
        self.state["stance"] = "CROUCH_DEFLECT"
        self.state["helmet_stats"]["deflection_count"] += 1
        save_mettaur_state(self.state)
        play_fx("mettaur_clink")
        record_ledger("DEFLECT_GUARD", f"Turtled under hardhat! Total deflections: {self.state['helmet_stats']['deflection_count']}", xp=35)
        return {
            "status": "DEFLECTED",
            "count": self.state["helmet_stats"]["deflection_count"],
            "sound": "mettaur_clink",
            "message": "TING! Invulnerable Mettaur Guard deflected all incoming anomalies!"
        }

    def pickaxe(self) -> Dict[str, Any]:
        self.state["equipped"] = True
        self.state["stance"] = "MINING"
        coins = random.randint(15, 45)
        depth = round(random.uniform(0.5, 3.2), 1)
        self.state["helmet_stats"]["star_coins_quarried"] += coins
        self.state["helmet_stats"]["mining_depth_meters"] += depth
        save_mettaur_state(self.state)
        play_fx("metal_clink")
        record_ledger("PICKAXE_MINING", f"Mined +{coins} Star Coins at depth +{depth}m", xp=30)
        return {
            "status": "MINED",
            "coins_found": coins,
            "total_coins": self.state["helmet_stats"]["star_coins_quarried"],
            "depth_gained": depth,
            "total_depth": self.state["helmet_stats"]["mining_depth_meters"]
        }

    def quake(self) -> Dict[str, Any]:
        self.state["equipped"] = True
        self.state["stance"] = "MINING"
        save_mettaur_state(self.state)
        play_fx("laser")
        record_ledger("GROUND_QUAKE", "Discharged 3-way Mettaur Shockwave Wavefront", xp=40)
        return {
            "status": "QUAKE_FIRED",
            "pellets": 3,
            "spread_deg": 45,
            "damage": 85,
            "message": "BOOM! Ground shockwave cleared out obstacles and glitch blocks!"
        }

    def build(self) -> Dict[str, Any]:
        self.state["equipped"] = True
        self.state["stance"] = "BUILDING"
        self.state["helmet_stats"]["scaffolds_erected"] += 1
        save_mettaur_state(self.state)
        play_fx("wrench_ratchet")
        record_ledger("SCAFFOLD_BUILT", f"Erected Heavy Girder Scaffolding #{self.state['helmet_stats']['scaffolds_erected']}", xp=30)
        return {
            "status": "BUILT",
            "total_scaffolds": self.state["helmet_stats"]["scaffolds_erected"],
            "structures": ["Neon Safety Cones", "Heavy Girder Scaffolding", "Terminal HUD Workbench"]
        }


def print_status(engine: KirbyMettaurEngine):
    st = engine.state
    stats = st["helmet_stats"]
    gear = st["current_gear"]
    eq_badge = f"{C_GREEN}● EQUIPPED & ACTIVE{C_RESET}" if st["equipped"] else f"{C_DIM}○ STOWED IN TOOLBOX{C_RESET}"

    print(f"\n{C_BOLD}{C_YELLOW}⛑️ ═══════════════════════════════════════════════════════════════════════ ⛑️{C_RESET}")
    print(f"{C_BOLD}{C_YELLOW}     ✨ KIRBY METTAUR CONSTRUCTION HELMET & HARDHAT ENGINE ✨{C_RESET}")
    print(f"{C_BOLD}{C_YELLOW}⛑️ ═══════════════════════════════════════════════════════════════════════ ⛑️{C_RESET}")
    print(render_mettaur_kirby_ascii(st.get("stance", "STANDBY")))

    print(f"{C_BOLD}{C_CYAN}▶ Hardware Status:{C_RESET} {eq_badge}  |  {C_PURPLE}Stance:{C_RESET} {C_BOLD}{st.get('stance', 'STANDBY')}{C_RESET}")
    print(f"{C_BOLD}{C_WHITE}  Model:{C_RESET}           {stats['model']}")
    print(f"{C_BOLD}{C_WHITE}  Material:{C_RESET}        {stats['material']} ({gear['helmet_color']})")
    print(f"{C_BOLD}{C_WHITE}  Armor Deflection:{C_RESET} {C_GREEN}{stats['armor_rating']}% Invulnerable Guard{C_RESET}")
    print(f"{C_BOLD}{C_WHITE}  Total Deflects:{C_RESET}  {C_YELLOW}{stats['deflection_count']} attacks reflected (TING!){C_RESET}")
    print(f"{C_BOLD}{C_WHITE}  Pickaxe Mining:{C_RESET}  {C_GOLD}{stats['star_coins_quarried']} Star Coins{C_RESET} quarried ({stats['mining_depth_meters']}m deep)")
    print(f"{C_BOLD}{C_WHITE}  Structures Built:{C_RESET} {C_CYAN}{stats['scaffolds_erected']} Scaffolds & Barricades erected{C_RESET}")
    print(f"{C_BOLD}{C_WHITE}  Safety Compliant:{C_RESET} {C_GOLD}{stats['safety_certification']}{C_RESET}")
    print(f"\n{C_BOLD}Commands:{C_RESET}")
    print(f"  kirby helmet equip     - Put on Mettaur Construction Helmet")
    print(f"  kirby helmet deflect   - Crouch invulnerably under hardhat (TING!)")
    print(f"  kirby helmet pickaxe   - Swing pneumatic pickaxe to quarry Star Coins")
    print(f"  kirby helmet quake     - Slam ground for 3-way shockwave attack")
    print(f"  kirby helmet build     - Deploy construction barricades & scaffolding")
    print(f"  kirby helmet unequip   - Stow helmet back into Master Toolbox\n")


def main():
    parser = argparse.ArgumentParser(description="Kirby Mettaur Construction Helmet Engine")
    parser.add_argument("action", nargs="?", default="status",
                        choices=["status", "equip", "on", "unequip", "off", "deflect", "crouch", "guard", "pickaxe", "mine", "quake", "slam", "build", "test"],
                        help="Action to perform with Mettaur Helmet")
    args = parser.parse_args()
    engine = KirbyMettaurEngine()

    if args.action == "status":
        print_status(engine)

    elif args.action in ("equip", "on"):
        res = engine.equip()
        print(f"\n{C_GREEN}[✔] Mettaur Construction Helmet EQUIPPED!{C_RESET}")
        print(f"{C_YELLOW}    \"Poyo! Safety first! Ready to build and deflect!\" ⛑️✨{C_RESET}")
        print(render_mettaur_kirby_ascii("STANDBY"))

    elif args.action in ("unequip", "off"):
        res = engine.unequip()
        print(f"\n{C_YELLOW}[✔] Mettaur Construction Helmet stowed in Master Toolbox.{C_RESET}\n")

    elif args.action in ("deflect", "crouch", "guard"):
        res = engine.deflect()
        print(f"\n{C_BOLD}{C_CYAN}✨ *TING!* ✨ METTAUR HARDHAT DEFLECTION GUARD!{C_RESET}")
        print(render_mettaur_kirby_ascii("CROUCH_DEFLECT"))
        print(f"{C_GREEN}[✔] {res['message']}{C_RESET}")
        print(f"    Deflection count: {C_BOLD}{res['count']}{C_RESET} | Audio: {C_YELLOW}{res['sound']}{C_RESET}\n")

    elif args.action in ("pickaxe", "mine"):
        res = engine.pickaxe()
        print(f"\n{C_BOLD}{C_GOLD}⛏️ *CLANG!* TITANIUM PICKAXE QUARRY STRIKE!{C_RESET}")
        print(render_mettaur_kirby_ascii("MINING"))
        print(f"{C_GREEN}[✔] Mined +{res['coins_found']} Star Coins! (Total: {res['total_coins']} 🪙){C_RESET}")
        print(f"    Shaft excavated: +{res['depth_gained']}m (Current Depth: {res['total_depth']}m)\n")

    elif args.action in ("quake", "slam"):
        res = engine.quake()
        print(f"\n{C_BOLD}{C_RED}💥 METTAUR 3-WAY GROUND SHOCKWAVE SLAM!{C_RESET}")
        print(f"{C_GREEN}[✔] {res['message']}{C_RESET}")
        print(f"    Spread: {res['spread_deg']}° | Pellets: {res['pellets']} | Kinetic Power: {res['damage']} AP\n")

    elif args.action == "build":
        res = engine.build()
        print(f"\n{C_BOLD}{C_CYAN}🏗️ DEPLOYING HEAVY CONSTRUCTION SCAFFOLDING...{C_RESET}")
        print(f"{C_GREEN}[✔] Scaffolding erected! Total active sites: {res['total_scaffolds']}{C_RESET}")
        print(f"    Structures: {', '.join(res['structures'])}\n")

    elif args.action == "test":
        # Verification routine for automated test suite
        res_eq = engine.equip()
        assert res_eq["status"] == "EQUIPPED"
        res_def = engine.deflect()
        assert res_def["status"] == "DEFLECTED"
        res_pick = engine.pickaxe()
        assert res_pick["status"] == "MINED"
        res_q = engine.quake()
        assert res_q["status"] == "QUAKE_FIRED"
        res_b = engine.build()
        assert res_b["status"] == "BUILT"
        print(f"{C_GREEN}[✔] Kirby Mettaur Construction Helmet Engine fully verified! (5/5 checks passed){C_RESET}")


if __name__ == "__main__":
    main()
