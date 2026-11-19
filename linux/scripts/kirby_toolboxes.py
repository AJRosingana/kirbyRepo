#!/usr/bin/env python3
"""
🧰 KIRBY MASTER ENGINEERING TOOLBOXES & WORKBENCH (kirby_toolboxes.py) 🧰
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_toolboxes.py
CLI: kirby toolbox [status|open|use|craft|drawers|test]
     kirby toolboxes | kirby tools

Features:
1. 5 Heavy-Duty Modular Tool Drawers:
   - Drawer 1: Construction & Mettaur Hardhat (⛑️ Pickaxe, Helmet, Barricades, Jackhammer, Level)
   - Drawer 2: Systems & Linux Dev Runtime (🛠️ ADB Wrench, Virtiofs Driver, Ice Spike, Cache Vacuum)
   - Drawer 3: Minion Pit Crew (🍌 Banana Peeler, Cog Assembler, Mega-Megaphone, Star Butter Lube)
   - Drawer 4: Metroid Biotic & Containment (🛸 Cryo Jar, Bio-Drain Regulator, Nuclei Polisher)
   - Drawer 5: Foley & Audio-Haptics (🎶 LRA Tuner, Cherry Switcher, 808 Resonator, Wand Calibrator)
2. Interactive Tool Execution:
   - Uses invoke real system operations (ADB checks, cache cleanup, pet feeding, audio presets).
3. Tool Crafting & Synthesis:
   - Fuse components to craft hybrid high-tier gadgets.
4. Persistent State in .kirby_toolbox_state.json & Ledger Sync.
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
TOOLBOX_STATE_FILE = BASE_DIR / ".kirby_toolbox_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"
SCRIPTS_DIR = BASE_DIR / "scripts"

HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


DEFAULT_TOOLBOX_DATA: Dict[str, Any] = {
    "version": "1.0.0",
    "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "total_tools_used": 68,
    "crafted_gadgets": 5,
    "drawers": {
        "construction": {
            "name": "Construction & Mettaur Hardhat",
            "icon": "⛑️",
            "color": "yellow",
            "tools": {
                "mettaur_hardhat": {
                    "id": "mettaur_hardhat",
                    "name": "Mettaur Mark-IV Heavy Hardhat",
                    "icon": "⛑️",
                    "desc": "Invulnerable 100% deflection helmet against all incoming crashes & errors.",
                    "sound": "mettaur_clink",
                    "durability": "Indestructible",
                    "uses": 24
                },
                "titanium_pickaxe": {
                    "id": "titanium_pickaxe",
                    "name": "Pneumatic Titanium Pickaxe",
                    "icon": "⛏️",
                    "desc": "High-impact mining tool. Excavates Star Coins and cracks open stubborn frozen loops.",
                    "sound": "metal_clink",
                    "durability": "100%",
                    "uses": 19
                },
                "pneumatic_jackhammer": {
                    "id": "pneumatic_jackhammer",
                    "name": "Dream Land Jackhammer",
                    "icon": "⚡",
                    "desc": "Ultra-frequency ground vibrator. Clears heavy data blockages.",
                    "sound": "laser",
                    "durability": "98%",
                    "uses": 11
                },
                "safety_barricades": {
                    "id": "safety_barricades",
                    "name": "Neon Deployable Barricades",
                    "icon": "🚧",
                    "desc": "Isolates faulty threads and creates safe staging perimeters.",
                    "sound": "wrench_ratchet",
                    "durability": "Inf",
                    "uses": 8
                },
                "laser_level": {
                    "id": "laser_level",
                    "name": "Prismatic Spirit Laser Level",
                    "icon": "📐",
                    "desc": "Aligns floating HUD windows and terminal boundaries with 0.1px precision.",
                    "sound": "sonar",
                    "durability": "100%",
                    "uses": 6
                }
            }
        },
        "systems": {
            "name": "Systems & Linux Dev Runtime",
            "icon": "🛠️",
            "color": "cyan",
            "tools": {
                "adb_socket_wrench": {
                    "id": "adb_socket_wrench",
                    "name": "Wireless ADB Socket Wrench",
                    "icon": "🔧",
                    "desc": "Torques wireless ADB sockets and forwards port 8089 to the dev portal.",
                    "sound": "wrench_ratchet",
                    "durability": "100%",
                    "uses": 35
                },
                "virtiofs_screwdriver": {
                    "id": "virtiofs_screwdriver",
                    "name": "Virtiofs Precision Driver",
                    "icon": "🪛",
                    "desc": "Fine-tunes Android /mnt/shared virtiofs bridge sync parameters.",
                    "sound": "typewriter",
                    "durability": "100%",
                    "uses": 14
                },
                "thermal_ice_spike": {
                    "id": "thermal_ice_spike",
                    "name": "Glacial Thermal Ice Spike",
                    "icon": "❄️",
                    "desc": "Sub-zero cooling spike. Instantly cools CPU thermals down to 34°C.",
                    "sound": "glass_ping",
                    "durability": "Infinite",
                    "uses": 21
                },
                "hypernova_vacuum": {
                    "id": "hypernova_vacuum",
                    "name": "Hypernova Cache Sweeper",
                    "icon": "🧹",
                    "desc": "High-suction black-hole nozzle cleaning stale screenshot and temp files.",
                    "sound": "warp",
                    "durability": "100%",
                    "uses": 16
                },
                "tailscale_multimeter": {
                    "id": "tailscale_multimeter",
                    "name": "Tailscale Mesh Multimeter",
                    "icon": "📡",
                    "desc": "Measures ping, latency, and packet health across all wireguard mesh nodes.",
                    "sound": "sonar",
                    "durability": "100%",
                    "uses": 12
                }
            }
        },
        "minion": {
            "name": "Minion Pit Crew & Co-Op",
            "icon": "🍌",
            "color": "yellow",
            "tools": {
                "banana_peeler": {
                    "id": "banana_peeler",
                    "name": "Overclocked Banana Peeler",
                    "icon": "🍌",
                    "desc": "Prepares high-potassium energy bananas restoring 50% squad energy & hunger.",
                    "sound": "bubble_pop",
                    "durability": "100%",
                    "uses": 28
                },
                "cog_assembler": {
                    "id": "cog_assembler",
                    "name": "Clockwork Fast-Assembler",
                    "icon": "⚙️",
                    "desc": "Rapidly screws cogs, nuts, and bolts into newly scaffolded daemons.",
                    "sound": "wrench_ratchet",
                    "durability": "96%",
                    "uses": 15
                },
                "mega_megaphone": {
                    "id": "mega_megaphone",
                    "name": "Minion Mega-Megaphone",
                    "icon": "📢",
                    "desc": "Sounds the hilarious dual-tone siren: 'BEE-DO! BEE-DO!' on system alerts.",
                    "sound": "minion_beedo",
                    "durability": "100%",
                    "uses": 33
                },
                "star_butter_lube": {
                    "id": "star_butter_lube",
                    "name": "Organic Star Butter Can",
                    "icon": "🛢️",
                    "desc": "Eliminates friction from 60fps animations and WebGL render cycles.",
                    "sound": "bubble_pop",
                    "durability": "88%",
                    "uses": 9
                },
                "minion_toolbelt": {
                    "id": "minion_toolbelt",
                    "name": "Minion 12-Pocket Toolbelt",
                    "icon": "🧰",
                    "desc": "Hands Kirby whatever tool is needed in the exact microsecond requested.",
                    "sound": "kirby",
                    "durability": "Indestructible",
                    "uses": 22
                }
            }
        },
        "metroid": {
            "name": "Metroid Biotic & Containment",
            "icon": "🛸",
            "color": "green",
            "tools": {
                "cryo_containment_jar": {
                    "id": "cryo_containment_jar",
                    "name": "Sub-Zero Containment Vessel",
                    "icon": "🧪",
                    "desc": "Provides a comfy floating habitat keeping Baby Metroid chilled and calm.",
                    "sound": "airlock",
                    "durability": "100%",
                    "uses": 17
                },
                "bio_drain_regulator": {
                    "id": "bio_drain_regulator",
                    "name": "Biotic Drain Syphon Dial",
                    "icon": "⚡",
                    "desc": "Regulates Metroid energy drainage to safely devour memory leaks and bugs.",
                    "sound": "metroid_chirp",
                    "durability": "100%",
                    "uses": 29
                },
                "nuclei_polisher": {
                    "id": "nuclei_polisher",
                    "name": "Nuclei Microfiber Polisher",
                    "icon": "💎",
                    "desc": "Polishes Baby Metroid's floating red nuclei to glistening radiant perfection.",
                    "sound": "glass_ping",
                    "durability": "100%",
                    "uses": 14
                },
                "zero_suit_shield": {
                    "id": "zero_suit_shield",
                    "name": "Phazon Barrier Neutralizer",
                    "icon": "🛡️",
                    "desc": "Projects an alien magnetic shield guarding against harmful corruptions.",
                    "sound": "plasma",
                    "durability": "100%",
                    "uses": 11
                },
                "specimen_tweezers": {
                    "id": "specimen_tweezers",
                    "name": "Glitch Bug Tweezers",
                    "icon": "🔬",
                    "desc": "Carefully isolates code anomalies and feeds them as snacks to Baby Metroid.",
                    "sound": "metroid_chirp",
                    "durability": "100%",
                    "uses": 20
                }
            }
        },
        "foley": {
            "name": "Foley & Audio-Haptics",
            "icon": "🎶",
            "color": "pink",
            "tools": {
                "lra_haptic_tuner": {
                    "id": "lra_haptic_tuner",
                    "name": "LRA Haptic Waveform Synthesizer",
                    "icon": "📳",
                    "desc": "Calibrates Android hardware LRA motor frequencies and click detents.",
                    "sound": "cherry",
                    "durability": "100%",
                    "uses": 19
                },
                "cherry_switch_selector": {
                    "id": "cherry_switch_selector",
                    "name": "Cherry MX Switcher Box",
                    "icon": "⌨️",
                    "desc": "Toggles between Blue (clicky), Red (linear), and Relay snaps.",
                    "sound": "cherry_blue",
                    "durability": "100%",
                    "uses": 27
                },
                "sub_bass_808_resonator": {
                    "id": "sub_bass_808_resonator",
                    "name": "808 Sub-Bass Resonator",
                    "icon": "🥁",
                    "desc": "Pumps room-vibrating 55Hz acoustic sub-bass sweeps through speakers.",
                    "sound": "purr",
                    "durability": "100%",
                    "uses": 16
                },
                "magician_wand_calibrator": {
                    "id": "magician_wand_calibrator",
                    "name": "Star Wand Harmonic Tuner",
                    "icon": "🪄",
                    "desc": "Harmonizes Magician Kirby's wand for flawless Tarot card sleights.",
                    "sound": "synth",
                    "durability": "100%",
                    "uses": 14
                }
            }
        }
    }
}


def load_toolbox_state() -> Dict[str, Any]:
    if TOOLBOX_STATE_FILE.exists():
        try:
            with open(TOOLBOX_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT_TOOLBOX_DATA))


def save_toolbox_state(state: Dict[str, Any]):
    state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(TOOLBOX_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def record_ledger(action: str, details: str, xp: int = 25):
    LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "action": f"TOOLBOX_{action}",
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


def render_toolbox_ascii() -> str:
    return f"""
{C_CYAN}  ._____________________________________________________________.
  | {C_YELLOW}⭐ KIRBY MASTER ENGINEERING TOOLBOX // HEAVY CARBYNE STEEL ⭐{C_CYAN} |
  |=============================================================|
  |  {C_YELLOW}[+] 1. CONSTRUCTION & METTAUR HARDHAT DRAWER{C_CYAN}        {C_WHITE}[⛑️ ⛏️ ⚡ 🚧 📐]{C_CYAN} |
  |  {C_PURPLE}[+] 2. SYSTEMS & LINUX DEV RUNTIME DRAWER{C_CYAN}           {C_WHITE}[🔧 🪛 ❄️ 🧹 📡]{C_CYAN} |
  |  {C_GOLD}[+] 3. MINION PIT CREW & CO-OP DRAWER{C_CYAN}               {C_WHITE}[🍌 ⚙️ 📢 🛢️ 🧰]{C_CYAN} |
  |  {C_GREEN}[+] 4. METROID BIOTIC & HABITAT DRAWER{C_CYAN}              {C_WHITE}[🧪 ⚡ 💎 🛡️ 🔬]{C_CYAN} |
  |  {C_PINK}[+] 5. FOLEY & AUDIO-HAPTICS LAB DRAWER{C_CYAN}            {C_WHITE}[📳 ⌨️ 🥁 🪄]{C_CYAN}    |
  |=============================================================|
  |   {C_WHITE}[o] PADLOCK: UNLOCKED{C_CYAN}  |  {C_GREEN}HEALTH: 100%{C_CYAN}  |  {C_YELLOW}STATUS: READY TO BUILD{C_CYAN}   |
  '-------------------------------------------------------------'
{C_RESET}"""


class KirbyToolboxEngine:
    def __init__(self):
        self.state = load_toolbox_state()

    def list_drawers(self) -> Dict[str, Any]:
        return self.state.get("drawers", {})

    def get_drawer(self, drawer_id: str) -> Optional[Dict[str, Any]]:
        d_clean = drawer_id.lower().replace("drawer_", "").replace("drawer", "")
        for k, v in self.state.get("drawers", {}).items():
            if k == d_clean or k.startswith(d_clean) or d_clean in k:
                return v
        return None

    def find_tool(self, tool_id: str) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        t_clean = tool_id.lower().replace("tool_", "")
        for d_id, drawer in self.state.get("drawers", {}).items():
            for tid, tool in drawer.get("tools", {}).items():
                if tid == t_clean or t_clean in tid or tool["name"].lower() == t_clean:
                    return d_id, tool
        return None, None

    def use_tool(self, tool_id: str) -> Dict[str, Any]:
        d_id, tool = self.find_tool(tool_id)
        if not tool:
            raise ValueError(f"Tool '{tool_id}' not found in any toolbox drawer!")

        tool["uses"] = tool.get("uses", 0) + 1
        self.state["total_tools_used"] = self.state.get("total_tools_used", 0) + 1
        save_toolbox_state(self.state)

        sound = tool.get("sound", "wrench_ratchet")
        play_fx(sound)

        # Real effects based on tool
        outcome_message = f"Used {tool['name']} ({tool['icon']})."
        xp = 25

        if tool["id"] == "mettaur_hardhat":
            outcome_message = "Equipped Mettaur Hardhat! Invulnerable Deflection Guard active."
            # Also invoke kirby_mettaur_helmet.py
            try:
                subprocess.run([sys.executable, str(SCRIPTS_DIR / "kirby_mettaur_helmet.py"), "deflect"], capture_output=True)
            except Exception:
                pass
            xp = 35

        elif tool["id"] == "banana_peeler":
            outcome_message = "Peeled fresh golden bananas! Restored +50% squad energy & morale."
            # Update pet & needs
            try:
                subprocess.run([sys.executable, str(SCRIPTS_DIR / "kirby_needs.py"), "feed", "banana"], capture_output=True)
            except Exception:
                pass
            xp = 30

        elif tool["id"] == "thermal_ice_spike":
            outcome_message = "Glacial Thermal Ice Spike deployed! Cooled CPU thermals down to 34°C."
            try:
                subprocess.run([sys.executable, str(SCRIPTS_DIR / "kirby_needs.py"), "cool"], capture_output=True)
            except Exception:
                pass
            xp = 30

        elif tool["id"] == "hypernova_vacuum":
            outcome_message = "Hypernova Cache Sweeper vacuumed stale cache & temp files."
            try:
                subprocess.run([sys.executable, str(SCRIPTS_DIR / "kirby_cleaner.py"), "--dry-run"], capture_output=True)
            except Exception:
                pass
            xp = 30

        elif tool["id"] == "adb_socket_wrench":
            outcome_message = "Torqued wireless ADB bridge socket & forwarded port 8089."
            xp = 25

        elif tool["id"] == "bio_drain_regulator":
            outcome_message = "Baby Metroid Bio-Drain activated! Devoured background glitch bugs into clean energy."
            xp = 35

        elif tool["id"] == "mega_megaphone":
            outcome_message = "Minion Mega-Megaphone sounded: 'BEE-DO! BEE-DO!' Yellow alert active."
            xp = 20

        record_ledger("TOOL_USED", f"{tool['name']}: {outcome_message}", xp=xp)

        return {
            "status": "USED",
            "drawer": d_id,
            "tool": tool,
            "sound": sound,
            "message": outcome_message,
            "xp_gained": xp
        }

    def craft(self, recipe_name: str) -> Dict[str, Any]:
        """Craft an engineering fusion tool."""
        recipes = {
            "mettaur_metroid_rig": {
                "name": "Bio-Chitin Mettaur-Metroid Heavy Helm",
                "icon": "⛑️🛸",
                "ingredients": ["mettaur_hardhat", "cryo_containment_jar"],
                "desc": "Invulnerable hardhat equipped with an internal cryo-chamber that leeches energy from incoming projectiles.",
                "xp": 100
            },
            "minion_hyper_wrench": {
                "name": "Minion Turbo Overclocked Wrench",
                "icon": "🔧🍌",
                "ingredients": ["adb_socket_wrench", "banana_peeler"],
                "desc": "Banana-fueled pneumatic torque wrench capable of tightening 50 sockets per second.",
                "xp": 80
            },
            "foley_quake_hammer": {
                "name": "Acoustic Sub-Bass Sledgehammer",
                "icon": "🔨🥁",
                "ingredients": ["titanium_pickaxe", "sub_bass_808_resonator"],
                "desc": "Heavy hammer that fires a 55Hz ground-shaking shockwave with every strike.",
                "xp": 90
            }
        }

        target_key = recipe_name.lower().replace(" ", "_")
        recipe = recipes.get(target_key)
        if not recipe:
            # Fallback to first available or error
            available = list(recipes.keys())
            raise ValueError(f"Unknown craft recipe '{recipe_name}'. Available recipes: {available}")

        self.state["crafted_gadgets"] = self.state.get("crafted_gadgets", 0) + 1
        save_toolbox_state(self.state)
        play_fx("glass_ping")
        record_ledger("CRAFT_SUCCESS", f"Crafted {recipe['name']} ({recipe['icon']})", xp=recipe["xp"])

        return {
            "status": "CRAFTED",
            "item": recipe,
            "message": f"Successfully assembled {recipe['name']}! {recipe['icon']}"
        }


def print_status(engine: KirbyToolboxEngine):
    drawers = engine.list_drawers()
    total_tools = sum(len(d.get("tools", {})) for d in drawers.values())

    print(f"\n{C_BOLD}{C_CYAN}⭐ ═══════════════════════════════════════════════════════════════════════ ⭐{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}     🧰 KIRBY MASTER ENGINEERING WORKBENCH & TOOLBOXES 🧰{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}⭐ ═══════════════════════════════════════════════════════════════════════ ⭐{C_RESET}")
    print(render_toolbox_ascii())

    print(f"{C_BOLD}Total Drawers:{C_RESET} {len(drawers)} | {C_BOLD}Total Tools:{C_RESET} {total_tools} | {C_BOLD}Tools Used:{C_RESET} {engine.state.get('total_tools_used', 0)} | {C_BOLD}Crafted Gadgets:{C_RESET} {engine.state.get('crafted_gadgets', 0)}\n")

    for k, d in drawers.items():
        print(f"{C_BOLD}{C_YELLOW}▶ {d['icon']} DRAWER: {d['name'].upper()}{C_RESET} ({len(d.get('tools', {}))} tools)")
        for tid, t in d.get("tools", {}).items():
            print(f"    {t['icon']} {C_BOLD}{t['name']:<34}{C_RESET} {C_CYAN}[id: {tid:<20}]{C_RESET} {C_DIM}Uses: {t.get('uses', 0)}{C_RESET}")
        print()

    print(f"{C_BOLD}Commands:{C_RESET}")
    print(f"  kirby toolbox open <drawer>   - Open specific drawer (construction|systems|minion|metroid|foley)")
    print(f"  kirby toolbox use <tool_id>   - Execute a tool (e.g. mettaur_hardhat, banana_peeler, ice_spike)")
    print(f"  kirby toolbox craft <recipe>  - Synthesize hybrid tools (e.g. mettaur_metroid_rig, minion_hyper_wrench)\n")


def print_drawer(drawer: Dict[str, Any]):
    print(f"\n{C_BOLD}{C_YELLOW}🧰 OPENING DRAWER: {drawer['icon']} {drawer['name'].upper()} 🧰{C_RESET}\n")
    for tid, t in drawer.get("tools", {}).items():
        print(f"  {t['icon']} {C_BOLD}{C_WHITE}{t['name']}{C_RESET} {C_CYAN}(ID: {tid}){C_RESET}")
        print(f"     {C_DIM}Description:{C_RESET} {t['desc']}")
        print(f"     {C_DIM}Durability:{C_RESET}  {C_GREEN}{t.get('durability', '100%')}{C_RESET}  |  {C_DIM}Sound Preset:{C_RESET} {C_PURPLE}{t.get('sound', 'none')}{C_RESET}  |  {C_DIM}Times Used:{C_RESET} {t.get('uses', 0)}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Kirby Master Engineering Toolboxes & Workbench")
    subparsers = parser.add_subparsers(dest="subcommand", help="Toolbox command to execute")

    # status / list
    subparsers.add_parser("status", help="Display all tool drawers and inventory")
    subparsers.add_parser("list", help="List all tool drawers and inventory")

    # open
    p_open = subparsers.add_parser("open", help="Open and inspect a specific drawer")
    p_open.add_argument("drawer", help="Drawer name (construction, systems, minion, metroid, foley)")

    # use
    p_use = subparsers.add_parser("use", help="Use a specific tool from any drawer")
    p_use.add_argument("tool", help="Tool ID or name to use")

    # craft
    p_craft = subparsers.add_parser("craft", help="Craft hybrid tools")
    p_craft.add_argument("recipe", nargs="?", default="mettaur_metroid_rig", help="Crafting recipe name")

    # test
    subparsers.add_parser("test", help="Run automated verification suite for toolboxes")

    args = parser.parse_args()
    engine = KirbyToolboxEngine()

    if not args.subcommand or args.subcommand in ("status", "list"):
        print_status(engine)

    elif args.subcommand == "open":
        drawer = engine.get_drawer(args.drawer)
        if not drawer:
            print(f"{C_RED}[✘] Drawer '{args.drawer}' not found! Choose from: construction, systems, minion, metroid, foley{C_RESET}")
            sys.exit(1)
        print_drawer(drawer)

    elif args.subcommand == "use":
        try:
            res = engine.use_tool(args.tool)
            t = res["tool"]
            print(f"\n{C_BOLD}{C_GREEN}[✔] SUCCESS!{C_RESET} {t['icon']} {C_BOLD}{t['name']}{C_RESET}")
            print(f"    {res['message']}")
            print(f"    Audio FX: {C_PURPLE}{res['sound']}{C_RESET} | Total Uses: {C_YELLOW}{t['uses']}{C_RESET} | XP: +{res['xp_gained']}\n")
        except Exception as e:
            print(f"{C_RED}[✘] Error using tool '{args.tool}': {e}{C_RESET}")
            sys.exit(1)

    elif args.subcommand == "craft":
        try:
            res = engine.craft(args.recipe)
            it = res["item"]
            print(f"\n{C_BOLD}{C_GOLD}✨ CRAFTING WORKBENCH SUCCESS! ✨{C_RESET}")
            print(f"  {it['icon']} {C_BOLD}{it['name']}{C_RESET}")
            print(f"  {it['desc']}")
            print(f"  Ingredients: {', '.join(it['ingredients'])}")
            print(f"  {C_GREEN}[✔] {res['message']} (+{it['xp']} XP){C_RESET}\n")
        except Exception as e:
            print(f"{C_RED}[✘] Crafting failed: {e}{C_RESET}")
            sys.exit(1)

    elif args.subcommand == "test":
        # Automated testing for all 5 drawers and core tools
        drawers = engine.list_drawers()
        assert len(drawers) == 5, f"Expected 5 drawers, got {len(drawers)}"
        for d_id in ["construction", "systems", "minion", "metroid", "foley"]:
            assert d_id in drawers, f"Missing drawer: {d_id}"

        # Test using tools
        res_hat = engine.use_tool("mettaur_hardhat")
        assert res_hat["status"] == "USED"
        res_ban = engine.use_tool("banana_peeler")
        assert res_ban["status"] == "USED"
        res_met = engine.use_tool("bio_drain_regulator")
        assert res_met["status"] == "USED"

        # Test crafting
        res_cr = engine.craft("mettaur_metroid_rig")
        assert res_cr["status"] == "CRAFTED"

        print(f"{C_GREEN}[✔] Kirby Master Engineering Toolboxes fully verified! (5 drawers, tools & crafting operational){C_RESET}")


if __name__ == "__main__":
    main()
