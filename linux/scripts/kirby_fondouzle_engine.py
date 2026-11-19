#!/usr/bin/env python3
"""
🫕 CHIPPITY-CHOP CHAM CHOWDER BREAD BOWL FONDOUZLE ENGINE (kirby_fondouzle_engine.py) 🍲
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_fondouzle_engine.py
CLI: kirby chowder [status|launch|dip|feast|flow|stream|test]
     kirby fondouzle [status|launch|dip|feast|flow|stream|test]

Features:
1. Sourdough Clam Chowder Bread Bowl Flotilla Simulation:
   - Buoyancy, crispness decay, soup temperature, oyster cracker dispersion, and passenger seating.
2. The Great Fondouzle Contraption:
   - Molten cheese canal (Gruyère, Sharp Cheddar, Emmental blend).
   - Steampunk Archimedes cheese screw, turning paddlewheels, steam pressure, and viscosity control.
3. Progresso Soup Bars Engine:
   - Rich ANSI ASCII progress bars measuring Flotilla Buoyancy, Melt Index, Steam PSI, Satiety, and Mesh Sync.
4. Deep Ecosystem Integration:
   - Restores Kirby Squad Satiety via .kirby_needs_state.json and .kirby_pet_state.json.
   - Records XP and achievements in ledger/kirby_learning_ledger.jsonl.
   - Interacts with Dev Web Portal (:8088/chowder and :8088/fondouzle).
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
C_AMBER = "\033[38;5;214m"
C_BROWN = "\033[38;5;137m"
C_WHITE = "\033[38;5;255m"
C_DIM = "\033[2m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"

BASE_DIR = Path("/mnt/shared/AntiGravity_Shared")
STATE_FILE = BASE_DIR / ".kirby_fondouzle_state.json"
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


DEFAULT_BREAD_BOWLS = [
    {
        "id": "bowl-01",
        "name": "Cape Cod Sourdough Clam Classic",
        "crust_style": "Extra-Crisp San Francisco Sourdough",
        "soup_type": "New England Clam Chowder (Heavy Cream & Ocean Clams)",
        "crispness": 96,
        "chowder_temp_c": 79.4,
        "oyster_crackers": 14,
        "bacon_bits": True,
        "paprika_dust": True,
        "passenger": "Kirby Prime (Chef Hat)",
        "floating_pos_pct": 18,
        "buoyancy": 98.2
    },
    {
        "id": "bowl-02",
        "name": "Applewood Bacon & Roasted Garlic Clam",
        "crust_style": "Cracked Pepper Herb Crust",
        "soup_type": "Smoky Clam & Yukon Gold Potato Potage",
        "crispness": 92,
        "chowder_temp_c": 77.8,
        "oyster_crackers": 20,
        "bacon_bits": True,
        "paprika_dust": False,
        "passenger": "Keeby (Yellow Star Chef)",
        "floating_pos_pct": 42,
        "buoyancy": 95.5
    },
    {
        "id": "bowl-03",
        "name": "Chef Kawasaki Grand Fondouzle Special",
        "crust_style": "Golden Glazed French Boule",
        "soup_type": "Triple-Melt Clam Stew with Thyme & Chives",
        "crispness": 98,
        "chowder_temp_c": 81.0,
        "oyster_crackers": 25,
        "bacon_bits": True,
        "paprika_dust": True,
        "passenger": "Chef Kawasaki & Bandana Dee",
        "floating_pos_pct": 68,
        "buoyancy": 99.1
    },
    {
        "id": "bowl-04",
        "name": "Glacial Chill Minty Sourdough Raft",
        "crust_style": "Frosted Sea Salt Sourdough",
        "soup_type": "Chilled Coastal Chowder with Kelp Crisps",
        "crispness": 88,
        "chowder_temp_c": 64.2,
        "oyster_crackers": 12,
        "bacon_bits": False,
        "paprika_dust": False,
        "passenger": "Freeze Kirby (Snow Crown)",
        "floating_pos_pct": 89,
        "buoyancy": 91.0
    }
]


def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Default initial state
    return {
        "version": "1.0.0",
        "contraption_name": "The Great Fondouzle Hydro-Pneumatic Cheese Canal",
        "status": "OPERATIONAL",
        "last_updated": time.time(),
        "fondue_stream": {
            "cheese_blend": "Aged Gruyère, Sharp Cheddar, Emmental & White Wine",
            "temperature_c": 82.5,
            "viscosity_poise": 14.2,
            "flow_speed_rpm": 38,
            "paddlewheels_active": 4,
            "steam_pressure_psi": 26.4,
            "canal_depth_cm": 22.0,
            "melt_index_pct": 94
        },
        "bread_bowls": list(DEFAULT_BREAD_BOWLS),
        "metrics": {
            "total_chowder_dispatched": 42,
            "total_bread_bowls_floated": 89,
            "total_croutons_dipped": 312,
            "cheese_fountains_flowing": 3
        }
    }


def save_state(state: Dict[str, Any]):
    state["last_updated"] = time.time()
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save fondouzle state: {e}", file=sys.stderr)


def record_ledger(event_type: str, details: str, xp: int = 40):
    try:
        LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "subsystem": "CHAM_CHOWDER_FONDOUZLE",
            "event_type": event_type,
            "details": details,
            "xp_awarded": xp
        }
        with open(LEDGER_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def draw_soup_bar(label: str, val: float, max_val: float = 100.0, length: int = 24, color: str = C_GREEN, unit: str = "%") -> str:
    """Renders a gourmet Progresso Soup Bar."""
    pct = max(0.0, min(100.0, (val / max_val) * 100.0))
    filled = int((pct / 100.0) * length)
    empty = length - filled
    bar_str = f"{color}{'█' * filled}{C_DIM}{'░' * empty}{C_RESET}"
    return f"  {label:<30} [{bar_str}] {color}{val:>5.1f}{unit}{C_RESET}"


def print_contraption_ascii():
    art = f"""
{C_AMBER}    ╭─────────────────────────────────────────────────────────────────────────────────╮
    │  {C_BOLD}{C_GOLD}🫕  THE GREAT FONDOUZLE CONTRAPTION & SOURDOUGH CHOWDER FLOTILLA  🍲{C_RESET}{C_AMBER}          │
    ╰─────────────────────────────────────────────────────────────────────────────────╯{C_RESET}
             {C_YELLOW}╔════════════╗{C_RESET}             {C_AMBER}___.---.___  (Steam Pressure: 26.4 PSI){C_RESET}
             {C_YELLOW}║ GRAND CHEF ║{C_RESET}         {C_CYAN}  (  ~  ~   )  *whistle!!*{C_RESET}
  {C_GOLD}▲ Archimedes{C_RESET}  {C_YELLOW}║  CAULDRON  ║{C_RESET}     {C_AMBER}=====(_________)====={C_RESET}
  {C_GOLD}│ Cheese    {C_RESET}  {C_YELLOW}╚══════╦═════╝{C_RESET}               {C_BROWN}|  |{C_RESET}
  {C_GOLD}│ Screw     {C_RESET}         {C_YELLOW}║{C_RESET}  {C_YELLOW}~~~~~~~~~~~~~~~~~~~~{C_BROWN}|  |{C_RESET}  Paddlewheel: [ 38 RPM ]
  {C_GOLD}│ [ 38 RPM ]{C_RESET}       {C_YELLOW}╭─╨──┴───────────────────┴──╨─╮{C_RESET}        {C_CYAN}___(•ᴗ•)___{C_RESET}
  {C_GOLD}▲           {C_RESET}     {C_YELLOW} (  MOLTEN CHEESE FONDOUZLE CANAL ) {C_RESET}      {C_PINK}( Kirby Prime ){C_RESET}
  {C_AMBER}═════════════════════════════════════════════════════════════════════════════════════{C_RESET}
       {C_BROWN}╭───────╮{C_RESET}              {C_BROWN}╭───────╮{C_RESET}              {C_BROWN}╭───────╮{C_RESET}
      {C_BROWN}│ (🍲)  │{C_RESET}             {C_BROWN}│ (🍲)  │{C_RESET}             {C_BROWN}│ (🍲)  │{C_RESET}
      {C_BROWN}╰───┬───╯{C_RESET}             {C_BROWN}╰───┬───╯{C_RESET}             {C_BROWN}╰───┬───╯{C_RESET}
    {C_AMBER}≈≈≈≈≈≈╪≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈╪≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈╪≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈{C_RESET}
      {C_GOLD}[Cape Cod Classic]{C_RESET}     {C_GOLD}[Applewood Bacon]{C_RESET}     {C_GOLD}[Kawasaki Special]{C_RESET}
    {C_AMBER}≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈{C_RESET}
"""
    print(art)


def action_status(state: Dict[str, Any]):
    print_contraption_ascii()

    fs = state["fondue_stream"]
    bowls = state["bread_bowls"]
    metrics = state["metrics"]

    print(f"{C_BOLD}{C_YELLOW}─── [ 🍲 PROGRESSO SOUP BARS // SYSTEM TELEMETRY ] ───────────────────────────{C_RESET}")
    print(draw_soup_bar("🍲 Chowder Flotilla Buoyancy", sum(b["buoyancy"] for b in bowls) / len(bowls), 100.0, color=C_GREEN))
    print(draw_soup_bar("🥖 Sourdough Crust Crispness", sum(b["crispness"] for b in bowls) / len(bowls), 100.0, color=C_GOLD))
    print(draw_soup_bar("🫕 Fondue Melt & Viscosity", fs["melt_index_pct"], 100.0, color=C_AMBER))
    print(draw_soup_bar("⚙️ Archimedes Screw Flow", fs["flow_speed_rpm"], 50.0, color=C_CYAN, unit=" RPM"))
    print(draw_soup_bar("💨 Steam Boiler Pressure", fs["steam_pressure_psi"], 40.0, color=C_PURPLE, unit=" PSI"))

    # Check Satiety from .kirby_needs_state.json if available
    satiety = 100
    if NEEDS_STATE_FILE.exists():
        try:
            with open(NEEDS_STATE_FILE, "r") as f:
                nd = json.load(f)
                satiety = nd.get("needs", {}).get("satiety", {}).get("level", 100)
        except Exception:
            pass
    print(draw_soup_bar("🍅 Kirby Squad Satiety", satiety, 100.0, color=C_HOT_PINK if satiety >= 75 else C_RED))
    print(draw_soup_bar("📱 HWUI VSync 120Hz Sync", 100.0, 100.0, color=C_GREEN))
    print()

    print(f"{C_BOLD}{C_AMBER}─── [ 🚢 SOURDOUGH BREAD BOWL FLOTILLA IN THE CANAL ] ─────────────────────────{C_RESET}")
    print(f"  {'ID':<8} {'Bread Bowl Name':<34} {'Temp':<9} {'Crisp':<8} {'Passenger':<24} {'Position'}")
    print(f"  {'-'*8} {'-'*34} {'-'*9} {'-'*8} {'-'*24} {'-'*10}")
    for b in bowls:
        pos_str = f"{b['floating_pos_pct']}% downstream"
        print(f"  {C_CYAN}{b['id']:<8}{C_RESET} {C_WHITE}{b['name']:<34}{C_RESET} {C_YELLOW}{b['chowder_temp_c']:>5.1f}°C{C_RESET} {C_GOLD}{b['crispness']:>3}%{C_RESET}   {C_PINK}{b['passenger']:<24}{C_RESET} {C_GREEN}{pos_str}{C_RESET}")
    print()

    print(f"{C_BOLD}{C_CYAN}─── [ 🫕 FONDOUZLE STREAM SPECIFICATIONS ] ────────────────────────────────────{C_RESET}")
    print(f"  • {C_BOLD}Cheese Blend:{C_RESET}      {fs['cheese_blend']}")
    print(f"  • {C_BOLD}Temperature:{C_RESET}       {fs['temperature_c']}°C (Simmering & Viscous)")
    print(f"  • {C_BOLD}Viscosity:{C_RESET}         {fs['viscosity_poise']} Poise (Silkily Dips Bread Bites)")
    print(f"  • {C_BOLD}Total Dispatched:{C_RESET}  {metrics['total_chowder_dispatched']} sourdough bread bowls")
    print(f"  • {C_BOLD}Total Dipped:{C_RESET}      {metrics['total_croutons_dipped']} crunchy sourdough skewers")
    print(f"  • {C_BOLD}Dev Web Portal:{C_RESET}    {C_GREEN}http://localhost:8088/chowder{C_RESET} (or :8088/fondouzle)\n")


def action_launch(variant: Optional[str] = None):
    state = load_state()
    bowls = state["bread_bowls"]

    presets = {
        "classic": ("Cape Cod Sourdough Clam Classic", "Ocean Clams & Fresh Cream", "Kirby Prime"),
        "smoky": ("Applewood Bacon & Roasted Garlic Clam", "Smoky Applewood Bacon & Yukon Potatoes", "Keeby"),
        "kawasaki": ("Chef Kawasaki Triple-Melt Special", "Triple Gruyère Fondue Infused Clam Stew", "Chef Kawasaki"),
        "manhattan": ("Manhattan Saffron Clam Fusion", "Tangy Tomato Clam Stew with Saffron", "Magician Kirby"),
        "garlic": ("Roasted Garlic & Rosemary Sourdough Bowl", "Garlic Butter Glazed Clam Potage", "Bandana Dee")
    }

    choice = variant.lower() if variant and variant.lower() in presets else random.choice(list(presets.keys()))
    name, soup, passenger = presets[choice]

    new_id = f"bowl-{len(bowls)+1:02d}"
    new_bowl = {
        "id": new_id,
        "name": name,
        "crust_style": "Golden Sourdough Hearth Boule",
        "soup_type": soup,
        "crispness": random.randint(95, 100),
        "chowder_temp_c": round(random.uniform(78.5, 83.5), 1),
        "oyster_crackers": random.randint(15, 30),
        "bacon_bits": True,
        "paprika_dust": True,
        "passenger": passenger,
        "floating_pos_pct": 5,
        "buoyancy": round(random.uniform(96.0, 99.8), 1)
    }

    bowls.insert(0, new_bowl)
    state["metrics"]["total_bread_bowls_floated"] += 1
    state["metrics"]["total_chowder_dispatched"] += 1
    save_state(state)

    if HAS_AUDIO:
        try:
            play_sound_preset("kirby")
        except Exception:
            pass

    record_ledger("CHOWDER_LAUNCH", f"Launched {name} into Fondouzle stream with passenger {passenger}", xp=45)

    print(f"\n{C_BOLD}{C_GREEN}🚢 [LAUNCH] Sourdough Bread Bowl Dispatched to Fondouzle!{C_RESET}")
    print(f"  • Bowl ID:     {C_CYAN}{new_id}{C_RESET}")
    print(f"  • Recipe:      {C_GOLD}{name}{C_RESET}")
    print(f"  • Soup:        {soup}")
    print(f"  • Passenger:   {C_PINK}{passenger} (•ᴗ•)و 🍲{C_RESET}")
    print(f"  • Temperature: {new_bowl['chowder_temp_c']}°C (Piping Hot!)")
    print(f"  • Flotilla is now {len(bowls)} bread bowls strong drifting down the cheese river!\n")


def action_dip(count: int = 3):
    state = load_state()
    state["metrics"]["total_croutons_dipped"] += count
    save_state(state)

    if HAS_AUDIO:
        try:
            play_sound_preset("cherry_blue")
        except Exception:
            pass

    record_ledger("FONDOUZLE_DIP", f"Dipped {count} sourdough croutons into the molten cheese stream", xp=25)

    print(f"\n{C_BOLD}{C_YELLOW}🫕 [DIP-O-MATIC] Dipping crunchy sourdough skewers into the Fondouzle!{C_RESET}")
    for i in range(count):
        stretch_len = random.randint(12, 28)
        print(f"  Skewer #{i+1}: Sourdough cube submerged... {C_AMBER}~~~{'='*stretch_len}🧀{C_RESET} Pulls {stretch_len}cm of molten Gruyère!")
        time.sleep(0.2)
    print(f"{C_BOLD}{C_GREEN}[✔] Sourdough crunch meets savory molten cheese perfection! Poyo! 🥖🧀✨{C_RESET}\n")


def action_feast(target: str = "squad"):
    state = load_state()
    # Feed Kirby Prime & the squad
    print(f"\n{C_BOLD}{C_PINK}╔═══════════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_PINK}║ 🍲  GRAND FONDOUZLE CHAM CHOWDER SQUAD FEAST // SOURDOUGH COMMUNION 🫕          ║{C_RESET}")
    print(f"{C_BOLD}{C_PINK}╚═══════════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

    print(f"  {C_GOLD}Chef Kawasaki{C_RESET} rings the golden dinner bell: {C_CYAN}*CLANG! CLANG! CLANG!*{C_RESET}")
    print(f"  The entire 10-Kirby Squad gathers around the fondue canal banks:")
    print(f"  • {C_PINK}Kirby Prime{C_RESET} scoops rich creamy clam chowder with an oversized golden ladle!")
    print(f"  • {C_GOLD}Keeby{C_RESET} breaks off a crispy sourdough crust wing and dunks it in molten Gruyère!")
    print(f"  • {C_BLUE}Bandana Dee{C_RESET} passes piping hot chowder bowls with crunchy oyster crackers to all!")
    print(f"  • {C_CYAN}Freeze Kirby{C_RESET} balances the hot soup with an icy breath of frosty contentment!")

    # Update .kirby_needs_state.json
    if NEEDS_STATE_FILE.exists():
        try:
            with open(NEEDS_STATE_FILE, "r") as f:
                nd = json.load(f)
            nd["needs"]["satiety"]["level"] = 100
            nd["needs"]["satiety"]["status"] = "Feasted on Cham Chowder Bread Bowls! 🍲✨"
            nd["needs"]["satiety"]["last_fulfilled"] = time.time()
            nd["needs"]["affection"]["level"] = min(100, nd["needs"]["affection"]["level"] + 30)
            nd["needs"]["social"]["level"] = 100
            nd["care_history_count"]["meals_enjoyed"] = nd["care_history_count"].get("meals_enjoyed", 0) + 1
            # Recalculate overall
            total = sum(item["level"] for item in nd["needs"].values())
            nd["overall_wellbeing"] = int(total / len(nd["needs"]))
            nd["overall_status"] = "Ecstatic, Cherished & Glowing 🌸✨"
            with open(NEEDS_STATE_FILE, "w") as f:
                json.dump(nd, f, indent=2)
            print(f"\n  {C_GREEN}[✔] .kirby_needs_state.json Satiety boosted to 100%! Overall Wellbeing: {nd['overall_wellbeing']}%{C_RESET}")
        except Exception as e:
            print(f"  Notice: needs update: {e}")

    # Feed via kirby_pet_care.py as well
    try:
        cmd = [sys.executable, str(BASE_DIR / "scripts" / "kirby_pet_care.py"), "feed", "cham_chowder"]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

    if HAS_AUDIO:
        try:
            play_sound_preset("fanfare")
        except Exception:
            pass

    record_ledger("CHOWDER_FEAST", "Grand Sourdough Cham Chowder Bread Bowl Feast enjoyed by entire squad", xp=100)
    print(f"\n{C_BOLD}{C_GOLD}✨ Satiety 100% Satiated! Happiness maxed! The bread bowls have blessed Dream Land! 🍲🥖💖{C_RESET}\n")


def action_stream(cycles: int = 5):
    """Animated stream of floating bread bowls down the fondue canal."""
    print(f"{C_BOLD}{C_CYAN}[STREAM] Starting live Fondouzle Flotilla animation ({cycles} cycles)...{C_RESET}")
    for cycle in range(cycles):
        state = load_state()
        bowls = state["bread_bowls"]
        for b in bowls:
            b["floating_pos_pct"] = (b["floating_pos_pct"] + random.randint(8, 15)) % 100
            # Gentle temperature fluctuation
            b["chowder_temp_c"] = round(max(60.0, b["chowder_temp_c"] - 0.1), 1)
        save_state(state)

        # Clear screen segment and redraw
        sys.stdout.write("\033[H\033[J")
        print_contraption_ascii()
        print(f"  {C_GOLD}Cycle {cycle+1}/{cycles} • Flow Speed: {state['fondue_stream']['flow_speed_rpm']} RPM • Pressure: {state['fondue_stream']['steam_pressure_psi']} PSI{C_RESET}")
        for b in bowls:
            pos_bar = " " * int(b["floating_pos_pct"] / 4) + f"{C_BROWN}(🍲 {b['id']}){C_RESET}"
            print(f"  Canal: {pos_bar:<35} {C_YELLOW}{b['chowder_temp_c']}°C{C_RESET} | {C_PINK}{b['passenger']}{C_RESET}")
        time.sleep(0.6)
    print(f"\n{C_GREEN}[✔] Animation loop completed.{C_RESET}")


def action_test() -> bool:
    print("[TEST] Running automated headless verification of Fondouzle Chowder Engine...")
    st = load_state()
    assert "fondue_stream" in st, "Missing fondue_stream"
    assert "bread_bowls" in st, "Missing bread_bowls"
    assert len(st["bread_bowls"]) > 0, "No bread bowls in flotilla"

    # Test launch
    action_launch("classic")
    st2 = load_state()
    assert len(st2["bread_bowls"]) == len(st["bread_bowls"]) + 1, "Bread bowl launch failed"

    # Test dip
    action_dip(2)

    # Test status
    action_status(st2)

    print(f"{C_BOLD}{C_GREEN}✅ ALL FONDOUZLE CHOWDER ENGINE TESTS PASSED!{C_RESET}")
    return True


def main():
    parser = argparse.ArgumentParser(description="🌸 Kirby Cham Chowder Bread Bowl Fondouzle Engine")
    subparsers = parser.add_subparsers(dest="command", help="Subcommand")

    subparsers.add_parser("status", help="Show contraption status and Progresso Soup Bars")
    
    p_launch = subparsers.add_parser("launch", help="Launch a new bread bowl onto the fondue stream")
    p_launch.add_argument("variant", nargs="?", default="classic", help="Bread bowl recipe variant")

    p_dip = subparsers.add_parser("dip", help="Dip crunchy sourdough croutons into the fondue stream")
    p_dip.add_argument("count", nargs="?", type=int, default=3, help="Number of croutons to dip")

    p_feast = subparsers.add_parser("feast", help="Squad feast on cham chowder bread bowls")
    p_feast.add_argument("target", nargs="?", default="squad", help="Feast target (squad or kirby)")

    p_stream = subparsers.add_parser("stream", help="Live stream animation of floating bread bowls")
    p_stream.add_argument("--cycles", type=int, default=5, help="Number of animation frames")

    subparsers.add_parser("test", help="Headless test verification")
    subparsers.add_parser("json", help="Dump state as JSON")

    args = parser.parse_args()

    if not args.command or args.command == "status":
        action_status(load_state())
    elif args.command == "launch":
        action_launch(args.variant)
    elif args.command == "dip":
        action_dip(args.count)
    elif args.command == "feast":
        action_feast(args.target)
    elif args.command == "stream":
        action_stream(args.cycles)
    elif args.command == "test":
        action_test()
    elif args.command == "json":
        print(json.dumps(load_state(), indent=2))


if __name__ == "__main__":
    main()
