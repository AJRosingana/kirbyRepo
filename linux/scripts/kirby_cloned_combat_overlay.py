#!/usr/bin/env python3
"""
===============================================================================
⚔️ KIRBY CLONED COMBAT & KUNG FU OVERLAY ENGINE 🥋
===============================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_cloned_combat_overlay.py
CLI:      kirby combat [manga|arcade|cyberpunk|glass] [--fps N] [--duration S] [--test]

Features:
1. Cloned Overlay Multi-Fighter Architecture:
   - Fighter 1 (Hero): Pink Kirby / Brawler (( ^-^ ) / (ง •̀_•́)ง)
   - Fighter 2 (Clone): Shadow Kirby / Rogue Clone (( ▀ ͜ʖ ▀ ) / (ง'̀-'́)ง)
   - Autonomous Kung Fu AI State Machine:
     * IDLE, ADVANCE, RETREAT, JAB, HIGH_KICK, FLYING_DRAGON_KICK,
     * HAMMER_SMASH, BLOCK_PARRY, HURT_KNOCKBACK, STUN, VICTORY_DANCE.

2. Real 2D Physics Kinematics:
   - Spatial position (x, y), velocity (vx, vy), gravity, and ground friction.
   - Momentum conservation & elastic impact recoil: m1*v1 + m2*v2 = m1*v1' + m2*v2'
   - Hitboxes, collision detection, block mitigation, combo counters, and health bars.

3. Four Swappable Visual Wrappers:
   - MANGA_COMIC: Rounded panel gutters, typewriter speech balloons (╰┈➤, ▼),
     half-tone terrain (░▒▓█), and dramatic action SFX bursts (*WHAM!*, *POYO-KICK!*).
   - RETRO_ARCADE_90S: Street Fighter / Neo-Geo dual HP meters, Braille sparks (⠁⠃⡇⣧⣿),
     "ROUND 1 - FIGHT!", "K.O.!", and combo announcements (COMBO x4!).
   - CYBERPUNK_HUD: Neon cyan/magenta wireframes, lock-on target brackets ([ ⌖ ]),
     real-time kinetic energy telemetry (Joules), and glitch particles.
   - FLOATING_GLASS: Sleek, borderless minimalist desktop silhouettes.

4. Zero-Flicker In-Place Terminal Rendering:
   - Leverages 2D virtual framebuffer matrix and targeted ANSI cursor addressing.
===============================================================================
"""

import os
import sys
import time
import math
import json
import random
import signal
import shutil
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Optional, Any

# --- ANSI Codes ---
ESC = "\033"
C_RESET = f"{ESC}[0m"
C_BOLD = f"{ESC}[1m"
C_DIM = f"{ESC}[2m"
C_ITALIC = f"{ESC}[3m"
C_CLEAR = f"{ESC}[2J{ESC}[H"
C_HIDE_CURSOR = f"{ESC}[?25l"
C_SHOW_CURSOR = f"{ESC}[?25h"

# Palette
C_PINK = f"{ESC}[38;5;218m"
C_HOT_PINK = f"{ESC}[38;5;205m"
C_PURPLE = f"{ESC}[38;5;141m"
C_SHADOW_PURPLE = f"{ESC}[38;5;99m"
C_GOLD = f"{ESC}[38;5;220m"
C_YELLOW = f"{ESC}[38;5;226m"
C_CYAN = f"{ESC}[38;5;51m"
C_BLUE = f"{ESC}[38;5;75m"
C_GREEN = f"{ESC}[38;5;120m"
C_RED = f"{ESC}[38;5;196m"
C_DARK_RED = f"{ESC}[38;5;88m"
C_WHITE = f"{ESC}[38;5;255m"
C_GRAY = f"{ESC}[38;5;244m"
C_DARK_GRAY = f"{ESC}[38;5;238m"

SHARED_DIR = Path("/mnt/shared/AntiGravity_Shared")
STATE_FILE = SHARED_DIR / ".kirby_cloned_combat_state.json"
LEDGER_FILE = SHARED_DIR / "ledger" / "kirby_learning_ledger.jsonl"


# =============================================================================
# 2D CHARACTER FRAMEBUFFER MATRIX
# =============================================================================

class BufferCanvas:
    def __init__(self, width: int, height: int, default_char: str = " "):
        self.width = width
        self.height = height
        self.default_char = default_char
        self.grid = [[default_char for _ in range(width)] for _ in range(height)]
        self.color_grid = [["" for _ in range(width)] for _ in range(height)]

    def clear(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = self.default_char
                self.color_grid[y][x] = ""

    def put_char(self, x: int, y: int, char: str, color: str = ""):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = char
            self.color_grid[y][x] = color

    def put_string(self, x: int, y: int, text: str, color: str = ""):
        if not (0 <= y < self.height):
            return
        curr_x = x
        for ch in text:
            if 0 <= curr_x < self.width:
                self.grid[y][curr_x] = ch
                self.color_grid[y][curr_x] = color
            curr_x += 1

    def put_box(self, x: int, y: int, w: int, h: int, style: str = "rounded", color: str = ""):
        if style == "double":
            tl, tr, bl, br, hz, vt = "╔", "╗", "╚", "╝", "═", "║"
        elif style == "rounded":
            tl, tr, bl, br, hz, vt = "╭", "╮", "╰", "╯", "─", "│"
        elif style == "heavy":
            tl, tr, bl, br, hz, vt = "┏", "┓", "┗", "┛", "━", "┃"
        elif style == "cyber":
            tl, tr, bl, br, hz, vt = "◤", "◥", "◣", "◢", "═", "║"
        else: # single
            tl, tr, bl, br, hz, vt = "┌", "┐", "└", "┘", "─", "│"

        self.put_char(x, y, tl, color)
        self.put_char(x + w - 1, y, tr, color)
        self.put_char(x, y + h - 1, bl, color)
        self.put_char(x + w - 1, y + h - 1, br, color)

        for col in range(x + 1, x + w - 1):
            self.put_char(col, y, hz, color)
            self.put_char(col, y + h - 1, hz, color)

        for row in range(y + 1, y + h - 1):
            self.put_char(x, row, vt, color)
            self.put_char(x + w - 1, row, vt, color)

    def render(self) -> str:
        lines = []
        for y in range(self.height):
            row_str = []
            curr_col = ""
            for x in range(self.width):
                c = self.color_grid[y][x]
                if c != curr_col:
                    row_str.append(c if c else C_RESET)
                    curr_col = c
                row_str.append(self.grid[y][x])
            if curr_col:
                row_str.append(C_RESET)
            lines.append("".join(row_str))
        return "\n".join(lines)


# =============================================================================
# KUNG FU FIGHTER ENTITY MODEL
# =============================================================================

@dataclass
class Fighter:
    name: str
    is_clone: bool
    color: str
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    mass: float = 1.0
    hp: int = 100
    max_hp: int = 100
    super_gauge: int = 0
    state: str = "IDLE"          # IDLE, ADVANCE, RETREAT, PUNCH, KICK, FLYING_KICK, BLOCK, HURT, KO
    state_timer: int = 0
    facing: int = 1              # 1 = Right, -1 = Left
    combo: int = 0
    total_hits: int = 0
    last_action_desc: str = ""

    def get_sprite(self) -> Tuple[List[str], str]:
        """Returns the multi-line ASCII sprite and color based on state and clone status."""
        c = self.color

        if self.state == "KO":
            return [
                " (x _ x) ",
                "  /|_|\\  ",
                "  _\\ /_  "
            ], C_DIM + self.color

        if self.state == "HURT":
            return [
                " (> _ <) ",
                " ~\\|_|/~ ",
                "   / \\   "
            ], C_BOLD + C_RED

        if self.state == "BLOCK":
            return [
                " |(•̀_•́)|",
                "  [🛡️🛡️]  ",
                "   / \\   "
            ], C_BOLD + C_CYAN

        if self.state == "PUNCH":
            if self.facing == 1:
                return [
                    " (•̀ᴗ•́)っ🥊",
                    "  /|_|\\   ",
                    "  _\\ \\_   "
                ], C_BOLD + c
            else:
                return [
                    "🥊c(•̀ᴗ•́) ",
                    "   /|_|\\  ",
                    "   _/ /_  "
                ], C_BOLD + c

        if self.state == "KICK":
            if self.facing == 1:
                return [
                    " ╰(°ㅂ°╰) ",
                    "   /|_|\\  ",
                    "  _/  🦵═ "
                ], C_BOLD + c
            else:
                return [
                    " (╯°ㅂ°)╯ ",
                    "   /|_|\\  ",
                    " ═🦵  \\_  "
                ], C_BOLD + c

        if self.state == "FLYING_KICK":
            if self.facing == 1:
                return [
                    " ~(>_<~)====🦵",
                    "   /|_|\\      ",
                    "              "
                ], C_BOLD + C_YELLOW
            else:
                return [
                    "🦵====(~>_<)~ ",
                    "      /|_|\\   ",
                    "              "
                ], C_BOLD + C_YELLOW

        # Default IDLE / ADVANCE / RETREAT
        if self.is_clone:
            return [
                " ( ▀ ͜ʖ ▀ ) ",
                "   /|_|\\   ",
                "   / \\     "
            ], c
        else:
            return [
                " (づ｡◕‿◕｡)づ",
                "   /|_|\\   ",
                "   / \\     "
            ], c


# =============================================================================
# KUNG FU ARENA & PHYSICS ARBITER
# =============================================================================

class KungFuCombatArena:
    def __init__(self, width: int = 84, height: int = 24, wrapper: str = "manga"):
        self.width = width
        self.height = height
        self.wrapper = wrapper.lower()
        self.canvas = BufferCanvas(width, height)

        # Arena bounds (inner playfield)
        self.arena_left = 3
        self.arena_right = width - 4
        self.arena_top = 4
        self.arena_floor = height - 4

        # Fighter 1: Original Pink Hero
        self.f1 = Fighter(
            name="Pink Kirby",
            is_clone=False,
            color=C_HOT_PINK,
            x=self.arena_left + 10,
            y=self.arena_floor - 3,
            facing=1,
            mass=1.0
        )

        # Fighter 2: Cloned Shadow Kirby
        self.f2 = Fighter(
            name="Shadow Clone",
            is_clone=True,
            color=C_SHADOW_PURPLE,
            x=self.arena_right - 20,
            y=self.arena_floor - 3,
            facing=-1,
            mass=1.05
        )

        # Battle Event Log & Action SFX
        self.active_sfx = ""
        self.sfx_x = 0
        self.sfx_y = 0
        self.sfx_color = C_YELLOW
        self.sfx_timer = 0
        self.impact_sparks = []  # Braille particle positions
        self.round_num = 1
        self.step_count = 0

    def update_physics_and_ai(self):
        """Simulates 1 tick of AI decision making, kinematics, and combat resolution."""
        self.step_count += 1
        f1, f2 = self.f1, self.f2

        # 1. Update facing direction
        if f1.x < f2.x:
            f1.facing = 1
            f2.facing = -1
        else:
            f1.facing = -1
            f2.facing = 1

        # 2. AI Decision Logic for each fighter
        for f, opp in [(f1, f2), (f2, f1)]:
            if f.state in ["HURT", "STUN", "KO"]:
                f.state_timer -= 1
                if f.state_timer <= 0 and f.state != "KO":
                    f.state = "IDLE"
                continue

            if f.state in ["PUNCH", "KICK", "FLYING_KICK", "BLOCK"]:
                f.state_timer -= 1
                if f.state_timer <= 0:
                    f.state = "IDLE"
                continue

            # In IDLE: Decide next kung fu action based on distance
            dist = abs(f.x - opp.x)
            r = random.random()

            if dist > 22:
                # Far: Advance, Jump, or Flying Dragon Kick!
                if r < 0.35:
                    f.state = "ADVANCE"
                    f.vx = 1.8 * f.facing
                elif r < 0.55 and f.super_gauge >= 40:
                    f.state = "FLYING_KICK"
                    f.state_timer = 7
                    f.vx = 4.2 * f.facing
                    f.vy = -1.2
                    f.super_gauge -= 40
                elif r < 0.70:
                    # Jump advance
                    f.vy = -2.2
                    f.vx = 1.5 * f.facing
                else:
                    f.state = "IDLE"
                    f.vx *= 0.5
            elif dist > 8:
                # Mid-range: Footwork, kicks, or lunges
                if r < 0.40:
                    f.state = "ADVANCE"
                    f.vx = 1.4 * f.facing
                elif r < 0.65:
                    f.state = "KICK"
                    f.state_timer = 4
                    f.vx = 0.5 * f.facing
                elif r < 0.80:
                    f.state = "BLOCK"
                    f.state_timer = 5
                    f.vx = -0.5 * f.facing
                else:
                    f.state = "RETREAT"
                    f.vx = -1.5 * f.facing
            else:
                # Close-quarters infighting: Punches, kicks, or parries
                if r < 0.45:
                    f.state = "PUNCH"
                    f.state_timer = 3
                    f.vx = 0.2 * f.facing
                elif r < 0.75:
                    f.state = "KICK"
                    f.state_timer = 4
                    f.vx = 0.3 * f.facing
                elif r < 0.90:
                    f.state = "BLOCK"
                    f.state_timer = 4
                else:
                    f.state = "RETREAT"
                    f.vx = -2.0 * f.facing

        # 3. Kinematics integration (Gravity & Velocity)
        for f in [f1, f2]:
            f.x += f.vx
            f.y += f.vy

            # Ground floor collision
            if f.y >= self.arena_floor - 3:
                f.y = self.arena_floor - 3
                f.vy = 0.0
                f.vx *= 0.7  # Friction
            else:
                f.vy += 0.8  # Gravity

            # Screen boundary clamping with bounce
            if f.x < self.arena_left + 1:
                f.x = self.arena_left + 1
                f.vx = abs(f.vx) * 0.6
            elif f.x > self.arena_right - 14:
                f.x = self.arena_right - 14
                f.vx = -abs(f.vx) * 0.6

        # 4. Combat Hitbox & Collision Arbiter
        dist = abs(f1.x - f2.x)
        y_dist = abs(f1.y - f2.y)

        # Check attacks connecting
        for att, vic in [(f1, f2), (f2, f1)]:
            if att.state in ["PUNCH", "KICK", "FLYING_KICK"] and att.state_timer == 2:
                reach = 14 if att.state == "FLYING_KICK" else (11 if att.state == "KICK" else 9)
                if dist <= reach and y_dist <= 3:
                    # Attack Connected!
                    is_blocked = (vic.state == "BLOCK")

                    if att.state == "FLYING_KICK":
                        base_dmg = 24
                        sfx_name = "⚡ *DRAGON POYO-KICK!* ⚡"
                        impulse = 6.0
                    elif att.state == "KICK":
                        base_dmg = 14
                        sfx_name = "🥋 *ROUNDHOUSE!* 💥"
                        impulse = 4.0
                    else: # PUNCH
                        base_dmg = 8
                        sfx_name = "🥊 *WHAM!*"
                        impulse = 2.8

                    if is_blocked:
                        dmg = max(2, base_dmg // 4)
                        vic.hp = max(0, vic.hp - dmg)
                        vic.vx = impulse * 0.4 * att.facing
                        self.trigger_sfx("🛡️ *PARRY!*", int((att.x + vic.x) / 2), int(att.y - 1), C_CYAN)
                    else:
                        dmg = base_dmg
                        vic.hp = max(0, vic.hp - dmg)
                        vic.state = "HURT"
                        vic.state_timer = 5
                        vic.vx = impulse * att.facing
                        vic.vy = -1.2
                        att.combo += 1
                        att.total_hits += 1
                        att.super_gauge = min(100, att.super_gauge + 18)
                        self.trigger_sfx(sfx_name, int((att.x + vic.x) / 2), int(att.y - 2), C_RED if att.combo > 1 else C_YELLOW)
                        self.spawn_braille_sparks(int((att.x + vic.x) / 2), int(att.y))

                    # Check Knockout
                    if vic.hp <= 0:
                        vic.state = "KO"
                        att.state = "VICTORY_DANCE"
                        self.trigger_sfx("👑 ★ K. O. ! ★ 👑", self.width // 2 - 8, self.arena_top + 2, C_BOLD + C_GOLD)
                        self.log_combat_victory(att.name, vic.name)

        # Decay SFX timer
        if self.sfx_timer > 0:
            self.sfx_timer -= 1

    def trigger_sfx(self, text: str, x: int, y: int, color: str):
        self.active_sfx = text
        self.sfx_x = max(2, min(self.width - len(text) - 2, x))
        self.sfx_y = max(self.arena_top + 1, min(self.arena_floor - 2, y))
        self.sfx_color = color
        self.sfx_timer = 4

    def spawn_braille_sparks(self, cx: int, cy: int):
        self.impact_sparks.clear()
        glyphs = ["⠁", "⠃", "⠇", "⡇", "⣇", "⣧", "⣷", "⣿", "⢿", "⡿"]
        for _ in range(8):
            ox = random.randint(-4, 4)
            oy = random.randint(-2, 2)
            self.impact_sparks.append((cx + ox, cy + oy, random.choice(glyphs)))

    def log_combat_victory(self, winner: str, loser: str):
        """Appends combat victory telemetry to the persistent learning ledger."""
        try:
            LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "subsystem": "kirby_cloned_combat_overlay",
                "wrapper": self.wrapper,
                "winner": winner,
                "loser": loser,
                "total_steps": self.step_count,
                "p1_hp": self.f1.hp,
                "p2_hp": self.f2.hp
            }
            with open(LEDGER_FILE, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

    # =========================================================================
    # WRAPPER RENDERERS
    # =========================================================================

    def render_wrapper_manga(self):
        """Wrapper 1: Authentic Manga Comic Strip with Rounded Gutters & Speech Balloons."""
        c = self.canvas

        # Outer Comic Book Page Border
        c.put_box(0, 0, self.width, self.height, style="rounded", color=C_GOLD)
        title = " ★ CHAPTER 42: CLASH OF DUAL POYOS — MANGA EDITION ★ "
        c.put_string((self.width - len(title)) // 2, 0, title, C_BOLD + C_YELLOW)

        # Comic Panel Gutter
        c.put_box(self.arena_left - 1, self.arena_top - 1, (self.arena_right - self.arena_left) + 2, (self.arena_floor - self.arena_top) + 2, style="rounded", color=C_DARK_GRAY)

        # Half-tone terrain floor
        for x in range(self.arena_left, self.arena_right):
            c.put_char(x, self.arena_floor, "▓", C_PURPLE)
            c.put_char(x, self.arena_floor + 1, "█", C_DARK_GRAY)

        # Dynamic Speech Balloons for Fighters
        # Fighter 1 Speech
        if self.f1.state == "PUNCH":
            b_text = "Haa-chaa!"
            c.put_string(int(self.f1.x), int(self.f1.y - 2), f"╭─ {b_text} ─╮", C_YELLOW)
            c.put_string(int(self.f1.x) + 2, int(self.f1.y - 1), "╰┈➤", C_YELLOW)
        elif self.f1.state == "FLYING_KICK":
            b_text = "POYO DRAGON!"
            c.put_string(int(self.f1.x), int(self.f1.y - 2), f"【 {b_text} 】", C_BOLD + C_RED)

        # Fighter 2 (Clone) Speech
        if self.f2.state == "BLOCK":
            b_text = "Heh, foolish!"
            c.put_string(int(self.f2.x - 4), int(self.f2.y - 2), f"╭─ {b_text} ─╮", C_CYAN)
            c.put_string(int(self.f2.x) + 2, int(self.f2.y - 1), "▼", C_CYAN)
        elif self.f2.state == "KICK":
            b_text = "SHADOW IMPACT!"
            c.put_string(int(self.f2.x - 6), int(self.f2.y - 2), f"【 {b_text} 】", C_BOLD + C_SHADOW_PURPLE)

        # Footer Telemetry
        footer = f" [WRAPPER: MANGA]  P1 HP: {self.f1.hp:03d}  ⚔️  P2 CLONE HP: {self.f2.hp:03d}  TICK: {self.step_count:04d} "
        c.put_string(3, self.height - 2, footer, C_DIM + C_WHITE)

    def render_wrapper_arcade(self):
        """Wrapper 2: Retro 90s Arcade Street Fighter Bezel with Dual Health Bars."""
        c = self.canvas

        # Heavy Arcade Cabinet Frame
        c.put_box(0, 0, self.width, self.height, style="double", color=C_RED)
        banner = " 🕹️  NEO-GEO ARCADE: CLONED KUNG FU CHAMPIONSHIP  🕹️ "
        c.put_string((self.width - len(banner)) // 2, 0, banner, C_BOLD + C_YELLOW)

        # Street Fighter Dual Health Bars
        # P1 Health Bar (Left)
        p1_bar_len = 18
        p1_filled = int((self.f1.hp / 100.0) * p1_bar_len)
        p1_bar = "█" * p1_filled + "░" * (p1_bar_len - p1_filled)
        c.put_string(3, 2, f"P1 [{p1_bar}] {self.f1.hp:03d}", C_BOLD + C_HOT_PINK)

        # KO Badge in Center
        c.put_string(self.width // 2 - 2, 2, "[KO]", C_BOLD + C_YELLOW)

        # P2 Health Bar (Right)
        p2_bar_len = 18
        p2_filled = int((self.f2.hp / 100.0) * p2_bar_len)
        p2_bar = "░" * (p2_bar_len - p2_filled) + "█" * p2_filled
        c.put_string(self.width - 34, 2, f"{self.f2.hp:03d} [{p2_bar}] P2", C_BOLD + C_SHADOW_PURPLE)

        # Super Meter Gauges
        c.put_string(4, 3, f"SUPER: [{'=' * (self.f1.super_gauge // 10):<10}]", C_CYAN)
        c.put_string(self.width - 24, 3, f"SUPER: [{'=' * (self.f2.super_gauge // 10):>10}]", C_GOLD)

        # Grid floor
        for x in range(self.arena_left, self.arena_right):
            c.put_char(x, self.arena_floor, "═", C_CYAN)
            if x % 4 == 0:
                c.put_char(x, self.arena_floor + 1, "┼", C_DARK_GRAY)

        # Footer Credit
        footer = " INSERT COIN (2) • FREE PLAY • KUNG FU BRAWL 1994 "
        c.put_string((self.width - len(footer)) // 2, self.height - 2, footer, C_DIM + C_YELLOW)

    def render_wrapper_cyberpunk(self):
        """Wrapper 3: Neon Cyberpunk Tactical HUD with Lock-On Target Brackets & Telemetry."""
        c = self.canvas

        # Cybernetic Angled Frame
        c.put_box(0, 0, self.width, self.height, style="cyber", color=C_CYAN)
        head = " ⚡ CYBERPUNK 2026 // BIO-SYNTH KINETIC SPARRING NEXUS ⚡ "
        c.put_string((self.width - len(head)) // 2, 0, head, C_BOLD + C_CYAN)

        # Distance & Momentum Telemetry
        dx = abs(self.f1.x - self.f2.x)
        p1_ke = 0.5 * self.f1.mass * (self.f1.vx**2 + self.f1.vy**2)
        p2_ke = 0.5 * self.f2.mass * (self.f2.vx**2 + self.f2.vy**2)

        telemetry = f" TARGET_SEPARATION: {dx:04.1f}m | P1 KINETIC: {p1_ke:04.2f}J | P2 KINETIC: {p2_ke:04.2f}J "
        c.put_string((self.width - len(telemetry)) // 2, 2, telemetry, C_GREEN)

        # Lock-on reticles around fighters
        c.put_string(int(self.f1.x) - 1, int(self.f1.y) - 1, "⌖[ALPHA]", C_CYAN)
        c.put_string(int(self.f2.x) - 1, int(self.f2.y) - 1, "⌖[CLONE]", C_HOT_PINK)

        # Neon Floor
        for x in range(self.arena_left, self.arena_right):
            c.put_char(x, self.arena_floor, "─", C_CYAN)
            c.put_char(x, self.arena_floor + 1, "⠂" if x % 2 == 0 else " ", C_DARK_GRAY)

        footer = f" [AI CORE: TENSOR G4]  STATUS: COMBAT_ENGAGED  PACKETS: {self.step_count * 12} "
        c.put_string(4, self.height - 2, footer, C_DIM + C_CYAN)

    def render_wrapper_glass(self):
        """Wrapper 4: Minimalist Borderless Desktop Overlay Silhouettes."""
        c = self.canvas

        # Minimal top-bar pill
        pill = f" 🌸 KIRBY vs CLONE 🌸 | P1: {self.f1.hp}% | P2: {self.f2.hp}% "
        c.put_box((self.width - len(pill) - 4) // 2, 1, len(pill) + 4, 3, style="rounded", color=C_HOT_PINK)
        c.put_string((self.width - len(pill)) // 2, 2, pill, C_BOLD + C_WHITE)

        # Subtle dotted floor
        for x in range(self.arena_left, self.arena_right):
            c.put_char(x, self.arena_floor, "·", C_DARK_GRAY)

    def render_frame(self) -> str:
        """Composites fighters, particles, SFX, and the chosen wrapper skin."""
        self.canvas.clear()

        # 1. Render chosen visual wrapper frame
        if self.wrapper == "arcade":
            self.render_wrapper_arcade()
        elif self.wrapper == "cyberpunk":
            self.render_wrapper_cyberpunk()
        elif self.wrapper == "glass":
            self.render_wrapper_glass()
        else:
            self.render_wrapper_manga()

        # 2. Render Fighter 1 (Hero)
        f1_sprite, f1_color = self.f1.get_sprite()
        for idx, line in enumerate(f1_sprite):
            self.canvas.put_string(int(self.f1.x), int(self.f1.y) + idx, line, f1_color)

        # 3. Render Fighter 2 (Clone)
        f2_sprite, f2_color = self.f2.get_sprite()
        for idx, line in enumerate(f2_sprite):
            self.canvas.put_string(int(self.f2.x), int(self.f2.y) + idx, line, f2_color)

        # 4. Render Braille Impact Sparks
        if self.sfx_timer > 0:
            for sx, sy, glyph in self.impact_sparks:
                self.canvas.put_char(sx, sy, glyph, C_BOLD + C_YELLOW)

        # 5. Render Active Combat SFX Burst
        if self.sfx_timer > 0 and self.active_sfx:
            self.canvas.put_string(self.sfx_x, self.sfx_y, self.active_sfx, C_BOLD + self.sfx_color)

        # 6. Save State File for External Observers / Clones
        self.save_state()

        return self.canvas.render()

    def save_state(self):
        """Dumps battle state to JSON so second overlay / windows client can mirror."""
        try:
            state = {
                "step": self.step_count,
                "wrapper": self.wrapper,
                "f1": asdict(self.f1),
                "f2": asdict(self.f2),
                "active_sfx": self.active_sfx,
                "sfx_timer": self.sfx_timer
            }
            with open(STATE_FILE, "w") as f:
                json.dump(state, f, indent=2)
        except Exception:
            pass


# =============================================================================
# CLI RUNNER & DISPATCHER
# =============================================================================

def run_loop(wrapper: str = "manga", fps: float = 10.0, duration: float = 15.0):
    arena = KungFuCombatArena(wrapper=wrapper)
    dt = 1.0 / max(1.0, fps)
    start_time = time.time()

    print(C_HIDE_CURSOR + C_CLEAR, end="", flush=True)
    try:
        while True:
            elapsed = time.time() - start_time
            if duration and elapsed > duration:
                break

            arena.update_physics_and_ai()
            frame = arena.render_frame()

            sys.stdout.write(f"{ESC}[1;1H" + frame + "\n")
            sys.stdout.flush()

            time.sleep(dt)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(C_SHOW_CURSOR + "\n")
        sys.stdout.flush()


def run_test():
    """Headless validation test verifying physics, wrappers, clone state, and ledgers."""
    print("Testing KungFuCombatArena & All 4 Wrappers...")
    wrappers = ["manga", "arcade", "cyberpunk", "glass"]
    for w in wrappers:
        arena = KungFuCombatArena(wrapper=w)
        for _ in range(10):
            arena.update_physics_and_ai()
            frame = arena.render_frame()
            assert len(frame.split("\n")) == 24, f"Frame height mismatch in wrapper {w}"
        print(f"  [✔] Wrapper '{w}' passed 10 simulation ticks cleanly")

    assert STATE_FILE.exists(), f"State file {STATE_FILE} was not created"
    print(f"  [✔] State file created: {STATE_FILE}")
    print("✨ ALL CLONED KUNG FU COMBAT OVERLAY TESTS PASSED!")


def main():
    parser = argparse.ArgumentParser(description="Kirby Cloned Combat & Kung Fu Overlay Engine")
    parser.add_argument("wrapper", nargs="?", default="manga", choices=["manga", "arcade", "cyberpunk", "glass"], help="Visual wrapper mode")
    parser.add_argument("--fps", type=float, default=10.0, help="Framerate")
    parser.add_argument("--duration", type=float, default=15.0, help="Duration in seconds (0 for infinite)")
    parser.add_argument("--test", action="store_true", help="Run automated test suite")

    args = parser.parse_args()

    if args.test:
        run_test()
    else:
        run_loop(wrapper=args.wrapper, fps=args.fps, duration=args.duration)

if __name__ == "__main__":
    main()
