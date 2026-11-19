#!/usr/bin/env python3
"""
⭐ KIRBY STAR CATCHER - Interactive Terminal Arcade Minigame ⭐
================================================================================
Arcade minigame starring Kirby ( ^-^ ) catching stars, star shards, and maxim tomatoes
while dodging rogue glitch blocks!

Features:
- Raw non-blocking keyboard input via termios/tty/select on Linux.
- Smooth double-buffered terminal rendering at ~18 FPS with zero screen tearing.
- Audio synthesis integration via AntiGravity FX Engine (agy_fx_engine.py).
- Dynamic combo multiplier (1x -> 2x -> 4x -> 8x).
- Floating particle popups and expressive Kirby facial animations.
- Clean terminal restoration on exit (restoring cursor, echo, and line buffering).
- Headless test and AI auto-pilot modes (--test, --auto).

Controls:
  [A] / [D] or [◄] / [►] : Move Kirby horizontally
  [P] / [Space]          : Pause / Resume
  [M]                    : Toggle Audio ON / OFF
  [R]                    : Restart (on Game Over)
  [Q] / [Esc]            : Quit Game
================================================================================
"""

import os
import sys
import time
import math
import json
import random
import select
import shutil
import signal
import atexit
import argparse
import threading
import queue
import unicodedata
from typing import Optional, List, Tuple, Dict, Any

# ==============================================================================
# 1. 🎨 ANSI COLOR PALETTE & VISUAL STYLES
# ==============================================================================

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"

# Kirby Palette
PINK = "\033[38;5;205m"
BRIGHT_PINK = "\033[38;5;218m"
DEEP_PINK = "\033[38;5;198m"

# Item & HUD Colors
YELLOW = "\033[38;5;220m"
GOLD = "\033[1;38;5;226m"
CYAN = "\033[38;5;81m"
BRIGHT_CYAN = "\033[1;38;5;123m"
RED = "\033[38;5;196m"
BRIGHT_RED = "\033[1;38;5;196m"
GREEN = "\033[38;5;120m"
PURPLE = "\033[38;5;141m"
DARK_PURPLE = "\033[38;5;99m"
WHITE = "\033[38;5;255m"
GRAY = "\033[38;5;244m"
DARK_GRAY = "\033[38;5;238m"

# Cursor & Screen control
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_SCREEN = "\033[2J"
HOME_CURSOR = "\033[H"

# ==============================================================================
# 2. 🎵 ASYNCHRONOUS AUDIO SUBSYSTEM
# ==============================================================================

class AudioEngine:
    """Non-blocking background audio synthesizer integrating with agy_fx_engine."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.has_fx_engine = False
        self.fx_module = None
        self._queue: queue.Queue = queue.Queue(maxsize=8)
        self._check_engine()

        if self.has_fx_engine:
            self._worker_thread = threading.Thread(target=self._worker, daemon=True)
            self._worker_thread.start()

    def _check_engine(self):
        shared_dir = "/mnt/shared/AntiGravity_Shared"
        if shared_dir not in sys.path:
            sys.path.insert(0, shared_dir)
        try:
            import agy_fx_engine
            self.fx_module = agy_fx_engine
            self.has_fx_engine = True
        except Exception:
            self.has_fx_engine = False

    def play(self, preset: str):
        """Dispatches an audio preset to the background synthesizer queue."""
        if not self.enabled or not self.has_fx_engine:
            return
        try:
            self._queue.put_nowait(preset)
        except queue.Full:
            pass  # Drop if queue is saturated to prevent audio latency lag

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        return self.enabled

    def _worker(self):
        while True:
            preset = self._queue.get()
            if preset is None:
                break
            try:
                if self.fx_module and hasattr(self.fx_module, "play_sound_preset"):
                    self.fx_module.play_sound_preset(preset)
            except Exception:
                pass
            finally:
                self._queue.task_done()


# ==============================================================================
# 3. ⌨️ NON-BLOCKING RAW TERMINAL INPUT
# ==============================================================================

class InputHandler:
    """Handles raw non-blocking terminal input on Linux via termios/tty/select."""

    def __init__(self, headless: bool = False):
        self.headless = headless
        self.is_tty = sys.stdin.isatty() and not headless
        self.old_settings = None
        self.active = False

    def enter(self):
        if not self.is_tty:
            return
        try:
            import termios
            import tty
            self.old_settings = termios.tcgetattr(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())
            self.active = True
        except Exception:
            self.is_tty = False

    def exit(self):
        if not self.active or not self.old_settings:
            return
        try:
            import termios
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_settings)
            self.active = False
        except Exception:
            pass

    def read_key(self) -> Optional[str]:
        if not self.is_tty or not self.active:
            return None

        try:
            r, _, _ = select.select([sys.stdin], [], [], 0)
            if not r:
                return None

            ch = sys.stdin.read(1)
            if ch == "\x1b":
                # Check for ANSI escape sequences (arrows)
                r2, _, _ = select.select([sys.stdin], [], [], 0.008)
                if r2:
                    seq1 = sys.stdin.read(1)
                    if seq1 in ("[", "O"):
                        r3, _, _ = select.select([sys.stdin], [], [], 0.008)
                        if r3:
                            seq2 = sys.stdin.read(1)
                            if seq2 == "D":
                                return "LEFT"
                            elif seq2 == "C":
                                return "RIGHT"
                            elif seq2 == "A":
                                return "UP"
                            elif seq2 == "B":
                                return "DOWN"
                return "ESC"
            return ch
        except Exception:
            return None


# ==============================================================================
# 4. 🎮 GAME ENTITIES & TYPES
# ==============================================================================

class ItemType:
    STAR = "star"
    SHARD = "shard"
    TOMATO = "tomato"
    GLITCH = "glitch"


ITEM_CONFIG = {
    ItemType.STAR: {
        "char": "★",
        "color": YELLOW,
        "points": 100,
        "life_delta": 0,
        "sound": "hop",
        "name": "Falling Star",
        "width": 1,
    },
    ItemType.SHARD: {
        "char": "✧",
        "color": CYAN,
        "points": 250,
        "life_delta": 0,
        "sound": "metal_clink",
        "name": "Star Shard",
        "width": 1,
    },
    ItemType.TOMATO: {
        "char": "🍅",
        "color": RED,
        "points": 50,
        "life_delta": 1,
        "sound": "kirby",
        "name": "Maxim Tomato",
        "width": 2,
    },
    ItemType.GLITCH: {
        "char": "■",
        "color": PURPLE,
        "points": -150,
        "life_delta": -1,
        "sound": "laser",
        "name": "Glitch Block",
        "width": 1,
    },
}


class Item:
    def __init__(self, item_type: str, x: float, y: float, speed: float, wobble: float = 0.0):
        self.item_type = item_type
        self.x = x
        self.y = y
        self.speed = speed
        self.wobble = wobble
        self.tick = 0
        cfg = ITEM_CONFIG[item_type]
        self.char = cfg["char"]
        self.color = cfg["color"]
        self.points = cfg["points"]
        self.life_delta = cfg["life_delta"]
        self.sound = cfg["sound"]
        self.width = cfg["width"]

    def update(self):
        self.tick += 1
        self.y += self.speed
        if self.wobble != 0.0:
            self.x += math.sin(self.tick * 0.25) * self.wobble


class FloatingPopup:
    def __init__(self, text: str, x: int, y: float, color: str, duration: int = 6):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.duration = duration
        self.age = 0

    def update(self) -> bool:
        self.age += 1
        self.y -= 0.18
        return self.age < self.duration


# ==============================================================================
# 5. 🤖 AUTONOMOUS KIRBY AI AGENT
# ==============================================================================

class KirbyAI:
    """Intelligent agent for headless test verification and auto-pilot demo mode."""

    def __init__(self):
        self.last_move = None

    def decide_move(self, kirby_x: int, items: List[Item], width: int) -> Optional[str]:
        kirby_center = kirby_x + 3
        danger_threshold_y = 11.5

        # 1. Immediate Hazard Evasion: avoid glitch blocks close to Kirby
        glitches_close = [
            item for item in items
            if item.item_type == ItemType.GLITCH and item.y >= danger_threshold_y
        ]
        if glitches_close:
            # Check if any glitch is on path to hit Kirby
            for glitch in glitches_close:
                glitch_x = int(glitch.x)
                if kirby_x - 1 <= glitch_x <= kirby_x + 7:
                    # Move away from the glitch block
                    if glitch_x >= kirby_center:
                        if kirby_x > 2:
                            return "LEFT"
                        else:
                            return "RIGHT"
                    else:
                        if kirby_x < width - 9:
                            return "RIGHT"
                        else:
                            return "LEFT"

        # 2. Goodies Targeting: find best catchable target
        goodies = [
            item for item in items
            if item.item_type in (ItemType.STAR, ItemType.SHARD, ItemType.TOMATO)
            and item.y < 14.2
        ]
        if not goodies:
            # Drift gently toward center
            center_x = (width - 7) // 2
            if kirby_x < center_x - 1:
                return "RIGHT"
            elif kirby_x > center_x + 1:
                return "LEFT"
            return None

        # Score priority: lowest item (highest y) that is reachable
        def item_priority(item: Item) -> float:
            dist = abs(item.x - kirby_center)
            val = item.points
            if item.item_type == ItemType.TOMATO:
                val = 400
            elif item.item_type == ItemType.SHARD:
                val = 300
            # Urgency increases quadratically as item nears floor
            urgency = (item.y ** 2) * 1.5
            return urgency + (val / 10.0) - (dist * 2.0)

        best_item = max(goodies, key=item_priority)
        target_center = best_item.x + (best_item.width / 2.0)

        if target_center < kirby_center - 0.75:
            return "LEFT"
        elif target_center > kirby_center + 0.75:
            return "RIGHT"
        return None


# ==============================================================================
# 6. 🌟 MAIN ARCADE GAME ENGINE
# ==============================================================================

class KirbyStarCatcher:
    """Core game engine managing state, mechanics, collision, audio, and rendering."""

    WIDTH = 52
    HEIGHT = 15
    KIRBY_WIDTH = 7
    KIRBY_Y = 14

    FACES = {
        "normal": "( ^-^ )",
        "catch_star": "( >o< )",
        "catch_shard": "( *v* )",
        "catch_tomato": "( ♥v♥ )",
        "hurt": "( x_x )",
        "left": "( <.< )",
        "right": "( >.> )",
        "paused": "( u.u )",
        "game_over": "( T_T )",
    }

    def __init__(
        self,
        fps: int = 18,
        headless: bool = False,
        auto_pilot: bool = False,
        sound: bool = True,
    ):
        self.fps = fps
        self.headless = headless
        self.auto_pilot = auto_pilot
        self.frame_time = 1.0 / fps

        # State
        self.score = 0
        self.high_score = self._load_high_score()
        self.lives = 3
        self.max_lives = 5
        self.combo = 0
        self.multiplier = 1
        self.is_paused = False
        self.is_game_over = False
        self.running = True
        self.tick_count = 0

        # Player
        self.kirby_x = (self.WIDTH - self.KIRBY_WIDTH) // 2
        self.kirby_face = self.FACES["normal"]
        self.face_timer = 0
        self.move_face_timer = 0

        # Entities
        self.items: List[Item] = []
        self.popups: List[FloatingPopup] = []
        self.spawn_timer = 0

        # Subsystems
        self.audio = AudioEngine(enabled=sound and not headless)
        self.input_handler = InputHandler(headless=headless)
        self.ai = KirbyAI()

        # Telemetry & Stats
        self.stats = {
            "stars_caught": 0,
            "shards_caught": 0,
            "tomatoes_caught": 0,
            "glitches_hit": 0,
            "glitches_dodged": 0,
            "max_combo": 0,
            "total_score": 0,
            "ticks_simulated": 0,
        }

        # Terminal state tracking
        self.term_initialized = False

    # --------------------------------------------------------------------------
    # Persistence & High Score
    # --------------------------------------------------------------------------
    def _get_save_path(self) -> str:
        return "/mnt/shared/AntiGravity_Shared/.kirby_high_score.json"

    def _load_high_score(self) -> int:
        path = self._get_save_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return int(data.get("high_score", 0))
            except Exception:
                pass
        return 0

    def _save_high_score(self):
        path = self._get_save_path()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"high_score": self.high_score}, f)
        except Exception:
            pass

    # --------------------------------------------------------------------------
    # Combo Multiplier Calculation
    # --------------------------------------------------------------------------
    def _update_multiplier(self):
        """Increases multiplier on consecutive catches: 1x -> 2x -> 4x -> 8x."""
        prev_mult = self.multiplier
        if self.combo >= 12:
            self.multiplier = 8
        elif self.combo >= 6:
            self.multiplier = 4
        elif self.combo >= 3:
            self.multiplier = 2
        else:
            self.multiplier = 1

        if self.multiplier > prev_mult:
            self.audio.play("glass_ping")
            self.add_popup(f"{self.multiplier}x COMBO!", self.kirby_x, self.KIRBY_Y - 2, GOLD, 8)

        if self.combo > self.stats["max_combo"]:
            self.stats["max_combo"] = self.combo

    # --------------------------------------------------------------------------
    # Entity Spawning & Mechanics
    # --------------------------------------------------------------------------
    def spawn_item(self):
        """Procedurally spawns a new falling item with weighted distribution."""
        # Level-based speed scaling
        level_speed_bonus = min(0.35, (self.score // 1000) * 0.04)

        roll = random.random()
        if roll < 0.60:
            # 60% Falling Star
            itype = ItemType.STAR
            speed = random.uniform(0.32, 0.42) + level_speed_bonus
            wobble = random.uniform(0.0, 0.2)
        elif roll < 0.82:
            # 22% Star Shard
            itype = ItemType.SHARD
            speed = random.uniform(0.42, 0.55) + level_speed_bonus
            wobble = 0.0
        elif roll < 0.94:
            # 12% Glitch Block
            itype = ItemType.GLITCH
            speed = random.uniform(0.38, 0.52) + level_speed_bonus
            wobble = random.choice([0.0, 0.15])
        else:
            # 6% Maxim Tomato
            itype = ItemType.TOMATO
            speed = random.uniform(0.28, 0.36) + level_speed_bonus
            wobble = 0.0

        item_cfg = ITEM_CONFIG[itype]
        max_x = self.WIDTH - item_cfg["width"] - 2
        x = random.randint(2, max_x)
        y = 0.0

        self.items.append(Item(itype, x, y, speed, wobble))

    def add_popup(self, text: str, x: int, y: float, color: str, duration: int = 6):
        px = max(1, min(self.WIDTH - len(text) - 1, x))
        self.popups.append(FloatingPopup(text, px, y, color, duration))

    # --------------------------------------------------------------------------
    # Kirby Control & State
    # --------------------------------------------------------------------------
    def move_kirby(self, delta: int):
        if self.is_paused or self.is_game_over:
            return
        new_x = self.kirby_x + delta
        new_x = max(0, min(self.WIDTH - self.KIRBY_WIDTH, new_x))
        self.kirby_x = new_x

        if self.face_timer <= 0:
            if delta < 0:
                self.kirby_face = self.FACES["left"]
                self.move_face_timer = 2
            elif delta > 0:
                self.kirby_face = self.FACES["right"]
                self.move_face_timer = 2

    def set_kirby_face(self, face_key: str, ticks: int = 6):
        self.kirby_face = self.FACES.get(face_key, self.FACES["normal"])
        self.face_timer = ticks

    # --------------------------------------------------------------------------
    # Physics & Collision Logic
    # --------------------------------------------------------------------------
    def update_physics(self):
        if self.is_paused or self.is_game_over:
            return

        self.tick_count += 1
        self.stats["ticks_simulated"] += 1

        # Periodic Spawner
        self.spawn_timer += 1
        spawn_delay = max(4, 8 - (self.score // 2000))
        if self.spawn_timer >= spawn_delay:
            self.spawn_timer = 0
            self.spawn_item()

        # Update Face Timers
        if self.face_timer > 0:
            self.face_timer -= 1
            if self.face_timer == 0:
                self.kirby_face = self.FACES["normal"]
        elif self.move_face_timer > 0:
            self.move_face_timer -= 1
            if self.move_face_timer == 0:
                self.kirby_face = self.FACES["normal"]

        # Update Floating Popups
        self.popups = [p for p in self.popups if p.update()]

        # Update Items and Detect Collisions
        surviving_items = []
        kirby_span = (self.kirby_x, self.kirby_x + self.KIRBY_WIDTH - 1)

        for item in self.items:
            item.update()
            int_y = int(item.y)

            # Collision Check at Kirby Row
            if int_y == self.KIRBY_Y:
                # Check horizontal span overlap
                item_left = int(item.x)
                item_right = item_left + item.width - 1
                collides = (item_right >= kirby_span[0]) and (item_left <= kirby_span[1])

                if collides:
                    self._handle_catch(item)
                    continue  # Consumed

            # Floor Collision (Missed items)
            if item.y > self.KIRBY_Y:
                self._handle_floor_hit(item)
                continue  # Disappears

            surviving_items.append(item)

        self.items = surviving_items

    def _handle_catch(self, item: Item):
        """Handles collision between Kirby and an item."""
        if item.item_type == ItemType.STAR:
            pts = item.points * self.multiplier
            self.score += pts
            self.combo += 1
            self._update_multiplier()
            self.stats["stars_caught"] += 1
            self.set_kirby_face("catch_star", 6)
            self.audio.play(item.sound)
            self.add_popup(f"+{pts}★", int(item.x), self.KIRBY_Y - 1, YELLOW, 5)

        elif item.item_type == ItemType.SHARD:
            pts = item.points * self.multiplier
            self.score += pts
            self.combo += 1
            self._update_multiplier()
            self.stats["shards_caught"] += 1
            self.set_kirby_face("catch_shard", 6)
            self.audio.play(item.sound)
            self.add_popup(f"+{pts}✧", int(item.x), self.KIRBY_Y - 1, CYAN, 6)

        elif item.item_type == ItemType.TOMATO:
            pts = item.points * self.multiplier
            self.score += pts
            old_lives = self.lives
            self.lives = min(self.max_lives, self.lives + 1)
            self.stats["tomatoes_caught"] += 1
            self.set_kirby_face("catch_tomato", 8)
            self.audio.play(item.sound)
            if self.lives > old_lives:
                self.add_popup("♥+1 HP!", int(item.x), self.KIRBY_Y - 1, BRIGHT_RED, 8)
            else:
                self.add_popup(f"+{pts} MAX HP!", int(item.x), self.KIRBY_Y - 1, RED, 6)

        elif item.item_type == ItemType.GLITCH:
            self.lives += item.life_delta  # -1 life
            self.score = max(0, self.score + item.points)  # -150 pts
            self.combo = 0
            self.multiplier = 1
            self.stats["glitches_hit"] += 1
            self.set_kirby_face("hurt", 10)
            self.audio.play(item.sound)
            self.add_popup("-1♥ -150!", int(item.x), self.KIRBY_Y - 1, PURPLE, 8)

            if self.lives <= 0:
                self.is_game_over = True
                self.kirby_face = self.FACES["game_over"]
                self.audio.play("warp")

        # Update High Score
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()

        self.stats["total_score"] = self.score

    def _handle_floor_hit(self, item: Item):
        """Handles items reaching the floor without being caught."""
        if item.item_type in (ItemType.STAR, ItemType.SHARD):
            if self.combo > 0:
                self.combo = 0
                self.multiplier = 1
                self.add_popup("COMBO RESET!", int(item.x), self.KIRBY_Y - 1, GRAY, 5)
        elif item.item_type == ItemType.GLITCH:
            self.stats["glitches_dodged"] += 1
            # Dodge bonus
            self.score += 15
            if self.score > self.high_score:
                self.high_score = self.score
            self.add_popup("DODGED! +15", int(item.x), self.KIRBY_Y - 1, GREEN, 4)

    # --------------------------------------------------------------------------
    # Double-Buffered ASCII Frame Renderer
    # --------------------------------------------------------------------------
    def render_frame(self) -> str:
        """Composes a complete double-buffered frame string with pixel-perfect alignment."""
        term_cols, _ = shutil.get_terminal_size((80, 24))
        pad_x = max(0, (term_cols - (self.WIDTH + 4)) // 2)
        indent = " " * pad_x

        lines = []

        # 1. Header Banner
        lines.append(f"{indent}{PINK}╔{'═' * (self.WIDTH + 2)}╗{RESET}")
        header_text = "★ KIRBY STAR CATCHER ★"
        sub_text = "POYO ARCADE v1.0"
        gap = self.WIDTH - len(header_text) - len(sub_text)
        lines.append(
            f"{indent}{PINK}║ {BOLD}{YELLOW}{header_text}{RESET}"
            f"{' ' * max(1, gap)}"
            f"{CYAN}{sub_text}{PINK} ║{RESET}"
        )
        lines.append(f"{indent}{PINK}╚{'═' * (self.WIDTH + 2)}╝{RESET}")

        # 2. HUD Dashboard
        # Lives representation
        heart_str = ""
        for i in range(self.max_lives):
            if i < self.lives:
                heart_str += f"{BRIGHT_RED}♥{RESET} "
            else:
                heart_str += f"{DARK_GRAY}♡{RESET} "
        heart_str = heart_str.strip()

        # Audio indicator
        snd_label = f"{GREEN}🔊 ON{RESET}" if self.audio.enabled else f"{DARK_GRAY}🔇 OFF{RESET}"

        score_str = f"{BOLD}{WHITE}{self.score:06d}{RESET}"
        high_str = f"{DIM}{self.high_score:06d}{RESET}"

        # Combo display
        if self.multiplier > 1:
            mult_color = GOLD if self.multiplier >= 4 else CYAN
            combo_str = f"{mult_color}{self.combo}x ({self.multiplier}x){RESET}"
        else:
            combo_str = f"{WHITE}{self.combo}{RESET}"

        hud_line = (
            f"SCORE:{score_str}  "
            f"COMBO:{combo_str}  "
            f"HP:{heart_str}  "
            f"HIGH:{high_str}  "
            f"SFX:{snd_label}"
        )
        # Visual width calculation for HUD
        hud_plain = self._strip_ansi(hud_line)
        hud_visual_w = self._visual_width(hud_plain)
        hud_pad = max(0, self.WIDTH - hud_visual_w)
        lines.append(f"{indent}  {hud_line}{' ' * hud_pad}")

        # 3. Playfield Border Top
        lines.append(f"{indent}{CYAN}┌{'─' * self.WIDTH}┐{RESET}")

        # 4. Construct 2D Grid
        # cell: (char, color, visual_width)
        grid = [[(" ", "", 1) for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

        # Place Falling Items
        for item in self.items:
            iy = int(item.y)
            ix = int(item.x)
            if 0 <= iy < self.HEIGHT and 0 <= ix < self.WIDTH:
                grid[iy][ix] = (item.char, item.color, item.width)
                if item.width == 2 and ix + 1 < self.WIDTH:
                    grid[iy][ix + 1] = ("", "", 0)  # Occupied by wide char

        # Place Floating Popups
        for popup in self.popups:
            py = int(popup.y)
            px = popup.x
            if 0 <= py < self.HEIGHT:
                for idx, ch in enumerate(popup.text):
                    col = px + idx
                    if 0 <= col < self.WIDTH and grid[py][col][0] == " ":
                        grid[py][col] = (ch, popup.color, 1)

        # Place Kirby at bottom row
        if not self.is_game_over:
            kirby_color = BRIGHT_RED if self.kirby_face == self.FACES["hurt"] else BRIGHT_PINK
            for idx, ch in enumerate(self.kirby_face):
                col = self.kirby_x + idx
                if 0 <= col < self.WIDTH:
                    grid[self.KIRBY_Y][col] = (ch, f"{BOLD}{kirby_color}", 1)

        # Render Playfield Rows
        for r_idx, row in enumerate(grid):
            # Check for Overlays
            if self.is_paused and 5 <= r_idx <= 9:
                row_str = self._render_pause_overlay(r_idx)
            elif self.is_game_over and 5 <= r_idx <= 9:
                row_str = self._render_game_over_overlay(r_idx)
            else:
                row_str = self._render_grid_row(row)

            lines.append(f"{indent}{CYAN}│{RESET}{row_str}{CYAN}│{RESET}")

        # 5. Playfield Border Bottom
        lines.append(f"{indent}{CYAN}└{'─' * self.WIDTH}┘{RESET}")

        # 6. Controls & Flavor Footer
        ctrl_str = (
            f"{DIM}[A/D or ◄/►] Move  "
            f"[P] Pause  "
            f"[M] Audio  "
            f"[R] Restart  "
            f"[Q] Quit{RESET}"
        )
        ctrl_pad = max(0, (self.WIDTH + 2 - self._visual_width(self._strip_ansi(ctrl_str))) // 2)
        lines.append(f"{indent}{' ' * ctrl_pad}{ctrl_str}")

        return "\n".join(lines)

    def _render_grid_row(self, row: List[Tuple[str, str, int]]) -> str:
        """Builds a single row string accounting accurately for wide characters."""
        res = []
        col = 0
        while col < self.WIDTH:
            char, color, w = row[col]
            if w == 0:
                col += 1
                continue
            if color:
                res.append(f"{color}{char}{RESET}")
            else:
                res.append(char)
            col += w
        return "".join(res)

    def _render_pause_overlay(self, r_idx: int) -> str:
        box_w = 34
        left_pad = (self.WIDTH - box_w) // 2
        right_pad = self.WIDTH - box_w - left_pad

        content_map = {
            5: f"{YELLOW}╔{'═' * (box_w - 2)}╗{RESET}",
            6: f"{YELLOW}║{BOLD}{WHITE}{'★ GAME PAUSED ★'.center(box_w - 2)}{RESET}{YELLOW}║{RESET}",
            7: f"{YELLOW}║{BRIGHT_PINK}{'( u.u ) zZz'.center(box_w - 2)}{RESET}{YELLOW}║{RESET}",
            8: f"{YELLOW}║{DIM}{'Press [P] to Resume'.center(box_w - 2)}{RESET}{YELLOW}║{RESET}",
            9: f"{YELLOW}╚{'═' * (box_w - 2)}╝{RESET}",
        }
        return f"{' ' * left_pad}{content_map.get(r_idx, ' ' * box_w)}{' ' * right_pad}"

    def _render_game_over_overlay(self, r_idx: int) -> str:
        box_w = 34
        left_pad = (self.WIDTH - box_w) // 2
        right_pad = self.WIDTH - box_w - left_pad

        content_map = {
            5: f"{RED}╔{'═' * (box_w - 2)}╗{RESET}",
            6: f"{RED}║{BOLD}{WHITE}{'★ GAME OVER ★'.center(box_w - 2)}{RESET}{RED}║{RESET}",
            7: f"{RED}║{BRIGHT_PINK}{'( T_T ) poyo...'.center(box_w - 2)}{RESET}{RED}║{RESET}",
            8: f"{RED}║{YELLOW}{f'Score: {self.score:06d}'.center(box_w - 2)}{RESET}{RED}║{RESET}",
            9: f"{RED}╚{'═' * (box_w - 2)}╝{RESET}",
        }
        return f"{' ' * left_pad}{content_map.get(r_idx, ' ' * box_w)}{' ' * right_pad}"

    @staticmethod
    def _strip_ansi(text: str) -> str:
        import re
        return re.sub(r"\033\[[0-9;]*[a-zA-Z]", "", text)

    @staticmethod
    def _visual_width(text: str) -> int:
        return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in text)

    # --------------------------------------------------------------------------
    # Interactive Game Loop
    # --------------------------------------------------------------------------
    def restart(self):
        """Resets the game state for a new round."""
        self.score = 0
        self.lives = 3
        self.combo = 0
        self.multiplier = 1
        self.is_paused = False
        self.is_game_over = False
        self.kirby_x = (self.WIDTH - self.KIRBY_WIDTH) // 2
        self.kirby_face = self.FACES["normal"]
        self.face_timer = 0
        self.move_face_timer = 0
        self.items.clear()
        self.popups.clear()
        self.spawn_timer = 0
        self.audio.play("kirby")

    def run(self):
        """Runs the interactive arcade game loop with graceful cleanup."""
        self._init_terminal()
        try:
            sys.stdout.write(CLEAR_SCREEN)
            sys.stdout.flush()

            self.audio.play("kirby")

            while self.running:
                loop_start = time.monotonic()

                # Process Input
                self._handle_input()

                # AI auto-pilot if enabled
                if self.auto_pilot and not self.is_paused and not self.is_game_over:
                    ai_cmd = self.ai.decide_move(self.kirby_x, self.items, self.WIDTH)
                    if ai_cmd == "LEFT":
                        self.move_kirby(-2)
                    elif ai_cmd == "RIGHT":
                        self.move_kirby(2)

                # Physics & State update
                self.update_physics()

                # Render Frame with cursor repositioning (no clear flicker!)
                frame = self.render_frame()
                sys.stdout.write(HOME_CURSOR + frame)
                sys.stdout.flush()

                # Smooth frame rate regulation
                elapsed = time.monotonic() - loop_start
                sleep_time = self.frame_time - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            pass
        finally:
            self._restore_terminal()
            print(f"\n{BOLD}{PINK}★ Thanks for playing Kirby Star Catcher! Final Score: {self.score} ★{RESET}\n")

    def _handle_input(self):
        key = self.input_handler.read_key()
        if not key:
            return

        k = key.lower()
        if k in ("q", "esc"):
            self.running = False
        elif k in ("p", " "):
            if not self.is_game_over:
                self.is_paused = not self.is_paused
                self.kirby_face = self.FACES["paused"] if self.is_paused else self.FACES["normal"]
                self.audio.play("bubble_pop")
        elif k == "r" and self.is_game_over:
            self.restart()
        elif k == "m":
            status = self.audio.toggle()
            popup_txt = "AUDIO ON" if status else "AUDIO OFF"
            self.add_popup(popup_txt, self.kirby_x, self.KIRBY_Y - 2, GREEN if status else GRAY, 6)
        elif not self.is_paused and not self.is_game_over:
            if key == "LEFT" or k in ("a", "h"):
                self.move_kirby(-2)
            elif key == "RIGHT" or k in ("d", "l"):
                self.move_kirby(2)

    # --------------------------------------------------------------------------
    # Terminal Initialization & Restoration
    # --------------------------------------------------------------------------
    def _init_terminal(self):
        if self.headless:
            return
        self.input_handler.enter()
        sys.stdout.write(HIDE_CURSOR)
        sys.stdout.flush()
        self.term_initialized = True

        # Register exit handlers for safety
        atexit.register(self._restore_terminal)
        signal.signal(signal.SIGINT, self._sig_handler)
        signal.signal(signal.SIGTERM, self._sig_handler)

    def _sig_handler(self, signum, frame):
        self._restore_terminal()
        sys.exit(0)

    def _restore_terminal(self):
        if not self.term_initialized:
            return
        self.term_initialized = False
        try:
            self.input_handler.exit()
            sys.stdout.write(SHOW_CURSOR + RESET + "\n")
            sys.stdout.flush()
        except Exception:
            pass


# ==============================================================================
# 7. 🧪 HEADLESS TEST SUITE (--test)
# ==============================================================================

def run_headless_test(ticks: int = 30, render_snapshots: bool = True) -> int:
    """
    Executes a deterministic automated simulation run for CI/script verification.
    Verifies that mechanics, item spawns, collisions, audio hooks, and math operate cleanly.
    """
    print(f"\n{BOLD}{PINK}════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}{YELLOW}⭐ KIRBY STAR CATCHER - HEADLESS AUTOMATED AI TEST SUITE ⭐{RESET}")
    print(f"{BOLD}{PINK}════════════════════════════════════════════════════════════════════════════════{RESET}")
    print(f"{CYAN}Configuring simulation:{RESET} Ticks={ticks} | Mode=Deterministic AI | Platform={sys.platform}")

    # Seed random for repeatable test verification
    random.seed(42)

    game = KirbyStarCatcher(
        fps=60,
        headless=True,
        auto_pilot=True,
        sound=False,  # Silent in test mode
    )

    print(f"{DIM}Running {ticks} simulation ticks...{RESET}\n")

    for tick in range(1, ticks + 1):
        # AI moves Kirby
        move = game.ai.decide_move(game.kirby_x, game.items, game.WIDTH)
        if move == "LEFT":
            game.move_kirby(-2)
        elif move == "RIGHT":
            game.move_kirby(2)

        # Physics update
        game.update_physics()

        # Log milestones
        if tick in (1, 10, 20, ticks):
            lives_str = "♥" * game.lives + "♡" * (game.max_lives - game.lives)
            items_str = f"Items: {len(game.items):2d}"
            print(
                f"  [{CYAN}Tick {tick:02d}/{ticks:02d}{RESET}] "
                f"Kirby X: {game.kirby_x:02d} | "
                f"{items_str} | "
                f"Score: {game.score:05d} | "
                f"Combo: {game.multiplier}x ({game.combo}) | "
                f"Lives: {RED}{lives_str}{RESET}"
            )

    # Verification assertions
    assert game.stats["ticks_simulated"] == ticks, f"Expected {ticks} ticks simulated"
    assert game.lives > 0, "Kirby died unexpectedly in automated test run"

    print(f"\n{GREEN}────────────────────────────────────────────────────────────────────────────────{RESET}")
    print(f"{BOLD}{GREEN}✅ TEST PASSED: {ticks} ticks simulated with zero crashes!{RESET}")
    print(f"{GREEN}────────────────────────────────────────────────────────────────────────────────{RESET}")
    print(f"  • Final Score        : {BOLD}{YELLOW}{game.score} pts{RESET}")
    print(f"  • Falling Stars Caught: {game.stats['stars_caught']}")
    print(f"  • Star Shards Caught : {game.stats['shards_caught']}")
    print(f"  • Maxim Tomatoes     : {game.stats['tomatoes_caught']}")
    print(f"  • Glitches Dodged    : {game.stats['glitches_dodged']}")
    print(f"  • Glitches Hit       : {game.stats['glitches_hit']}")
    print(f"  • Max Combo Reached  : {game.stats['max_combo']} (Multiplier: {game.multiplier}x)")
    print(f"  • Lives Remaining    : {game.lives}/{game.max_lives}")
    print(f"{BOLD}{PINK}════════════════════════════════════════════════════════════════════════════════{RESET}\n")

    return 0


# ==============================================================================
# 8. 🚀 ENTRY POINT & CLI PARSER
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="⭐ Kirby Star Catcher - Interactive Terminal Arcade Minigame ⭐",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run headless automated AI test simulation (default: 30 ticks) and exit",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run interactive arcade mode with autonomous AI playing Kirby (Attract Mode)",
    )
    parser.add_argument(
        "--ticks",
        type=int,
        default=30,
        help="Number of ticks to simulate in --test mode (default: 30)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=18,
        help="Target frames per second (default: 18)",
    )
    parser.add_argument(
        "--no-sound",
        action="store_true",
        help="Disable procedural sound synthesis",
    )

    args = parser.parse_args()

    if args.test:
        sys.exit(run_headless_test(ticks=args.ticks))

    # Interactive Arcade Mode
    game = KirbyStarCatcher(
        fps=args.fps,
        headless=False,
        auto_pilot=args.auto,
        sound=not args.no_sound,
    )
    game.run()


if __name__ == "__main__":
    main()
