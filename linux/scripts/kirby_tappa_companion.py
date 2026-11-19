#!/usr/bin/env python3
"""
🩰 KIRBY x PROJECTM TAPPA TAPPA RHYTHM COMPANION & ADB CO-TAPPER 🎶
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_tappa_companion.py
Unified CLI: kirby tappa live [--bpm 128] [--adb] [--auto]

Features:
1. Real-time Non-blocking Terminal Tap Dancer (termios / select)
2. Live Tap-Tempo BPM & Rhythm Streak Multiplier (1x -> 2x -> 4x -> 8x)
3. Wireless ADB Screen Co-Tapping: Physical screen taps sent to ProjectM on Pixel 9 Pro XL
4. Procedural 16-bit PCM Acoustics via agy_fx_engine.py
5. Autopoietic Event Mesh Integration: Emits EVENT_PROJECTM_TAP & gains Rhythm XP
================================================================================
"""

import os
import sys
import time
import math
import select
import shutil
import random
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional

# --- ANSI Styling ---
C_PINK = "\033[38;5;205m"
C_HOT_PINK = "\033[38;5;197m"
C_CYAN = "\033[38;5;81m"
C_GOLD = "\033[38;5;220m"
C_GREEN = "\033[38;5;120m"
C_PURPLE = "\033[38;5;141m"
C_WHITE = "\033[38;5;255m"
C_DIM = "\033[2m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"
C_CLEAR = "\033[2J\033[H"
C_HIDE = "\033[?25l"
C_SHOW = "\033[?25h"

BASE_DIR = Path("/mnt/shared/AntiGravity_Shared")
sys.path.insert(0, str(BASE_DIR))

# Sound FX
HAS_AUDIO = False
try:
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False

# Learning Engine
try:
    sys.path.insert(0, str(BASE_DIR / "scripts"))
    from kirby_learning_engine import KirbyLearningEngine
    learning_engine = KirbyLearningEngine()
except Exception:
    learning_engine = None


# --- ASCII Kirby Tap-Dance Frames ---
KIRBY_TAP_FRAMES = [
    # Frame 0: Left foot tap!
    f"""
        {C_GOLD}♪ (੭ˊᵕˋ)੭ *TAP!*{C_RESET}
      {C_PINK}.-------.{C_RESET}
     {C_PINK}/  {C_WHITE}●   ●{C_PINK}  \\{C_RESET}
    {C_PINK}|   {C_HOT_PINK}♥   ♥{C_PINK}   |{C_RESET}  {C_CYAN}*clack*{C_RESET}
     {C_PINK}\\  {C_WHITE}︶{C_PINK}     /{C_RESET}
     {C_HOT_PINK}/_/{C_RESET}  {C_DIM}'-'-'{C_RESET}   {C_HOT_PINK}(Left Shoe Tap!){C_RESET}
    """,
    # Frame 1: Center bounce!
    f"""
         {C_GOLD}♫ *(^o^)* ♫{C_RESET}
      {C_PINK}.-------.{C_RESET}
     {C_PINK}/  {C_WHITE}★   ★{C_PINK}  \\{C_RESET}
    {C_PINK}|   {C_HOT_PINK}♥   ♥{C_PINK}   |{C_RESET}
     {C_PINK}\\  {C_WHITE}▽{C_PINK}     /{C_RESET}
    {C_DIM}'-'-'{C_RESET}   {C_DIM}'-'-'{C_RESET}   {C_GREEN}(Bounce & Groove){C_RESET}
    """,
    # Frame 2: Right foot tap!
    f"""
        {C_GOLD}♬ (•̀ᴗ•́)و *TAP!*{C_RESET}
      {C_PINK}.-------.{C_RESET}
     {C_PINK}/  {C_WHITE}●   ●{C_PINK}  \\{C_RESET}
    {C_PINK}|   {C_HOT_PINK}♥   ♥{C_PINK}   |{C_RESET}  {C_CYAN}*tappa!*{C_RESET}
     {C_PINK}\\  {C_WHITE}︶{C_PINK}     /{C_RESET}
      {C_DIM}'-'-'{C_RESET}  {C_HOT_PINK}\\_\\{C_RESET}  {C_HOT_PINK}(Right Shoe Tap!){C_RESET}
    """,
    # Frame 3: Double tap jump!
    f"""
       {C_GOLD}✨ ⭐ *DOUBLE TAP!* ⭐ ✨{C_RESET}
        {C_PINK}.-------.{C_RESET}
       {C_PINK}/  {C_WHITE}★   ★{C_PINK}  \\{C_RESET}
      {C_PINK}\\   {C_HOT_PINK}♥   ♥{C_PINK}   /{C_RESET}   {C_GOLD}\\( ﾟヮﾟ)/{C_RESET}
       {C_PINK}'-------'{C_RESET}
       {C_HOT_PINK}/_/     \\_\\{C_RESET}     {C_GOLD}(Airborne Tap!){C_RESET}
    """
]


class KirbyTappaCompanion:
    def __init__(self, target_bpm: int = 120, adb_enabled: bool = False, auto_pilot: bool = False):
        self.bpm = target_bpm
        self.adb_enabled = adb_enabled
        self.auto_pilot = auto_pilot
        self.streak = 0
        self.total_taps = 0
        self.tap_timestamps: List[float] = []
        self.current_frame_idx = 0
        self.speech_bubble = "Tappa tappa tappa with me! (੭ˊᵕˋ)੭ 🎶"
        self.adb_connected = self.check_adb_status()
        self.screen_width = 1080
        self.screen_height = 2400

    def check_adb_status(self) -> bool:
        try:
            res = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=1.5)
            lines = [l for l in res.stdout.strip().split("\n") if "\tdevice" in l]
            return len(lines) > 0
        except Exception:
            return False

    def send_adb_tap(self, x: Optional[int] = None, y: Optional[int] = None):
        """Simulates physical touch input on Pixel 9 Pro XL screen."""
        if not self.adb_connected:
            return
        if x is None:
            # Random position within visualizer active area
            x = random.randint(200, self.screen_width - 200)
        if y is None:
            y = random.randint(400, self.screen_height - 500)

        subprocess.Popen(
            ["adb", "shell", f"input tap {x} {y}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def trigger_tap(self):
        """Executes a single tappa step."""
        now = time.time()
        self.total_taps += 1
        self.streak += 1
        self.tap_timestamps.append(now)
        if len(self.tap_timestamps) > 8:
            self.tap_timestamps.pop(0)

        # Calculate BPM
        if len(self.tap_timestamps) >= 3:
            intervals = [self.tap_timestamps[i] - self.tap_timestamps[i - 1] for i in range(1, len(self.tap_timestamps))]
            avg_interval = sum(intervals) / len(intervals)
            if 0.15 < avg_interval < 2.0:
                self.bpm = int(round(60.0 / avg_interval))

        # Cycle animation frame
        self.current_frame_idx = (self.current_frame_idx + 1) % len(KIRBY_TAP_FRAMES)

        # Audio sound
        if HAS_AUDIO:
            try:
                preset = "synth" if self.total_taps % 4 == 0 else "kirby"
                play_sound_preset(preset)
            except Exception:
                pass

        # ADB Co-tap
        if self.adb_enabled and self.adb_connected:
            self.send_adb_tap()

        # Dynamic quotes
        quotes = [
            "Tappa tappa! (੭ˊᵕˋ)੭ 🎶",
            "Feel the Milkdrop groove! 🌀",
            "Harmonic overdrive! ⚡",
            "Co-tapping with you! 💕",
            "Preset Warp Shockwave! ✨",
            "Pixel 9 Pro XL on beat! 🔥",
            "Double tap combo! 🩰"
        ]
        if self.total_taps % 5 == 0:
            self.speech_bubble = random.choice(quotes)

        # Mesh Event Dispatch
        if self.total_taps % 10 == 0 and learning_engine:
            try:
                learning_engine.dispatch_event("EVENT_PROJECTM_TAP")
            except Exception:
                pass

    def render(self):
        multiplier = 1
        if self.streak >= 32:
            multiplier = 8
        elif self.streak >= 16:
            multiplier = 4
        elif self.streak >= 8:
            multiplier = 2

        adb_status_str = f"{C_GREEN}CONNECTED{C_RESET}" if self.adb_connected else f"{C_DIM}OFFLINE{C_RESET}"
        adb_mode_str = f"{C_GREEN}ON{C_RESET}" if (self.adb_enabled and self.adb_connected) else f"{C_DIM}OFF{C_RESET}"
        auto_str = f"{C_GOLD}ACTIVE{C_RESET}" if self.auto_pilot else f"{C_DIM}MANUAL{C_RESET}"

        term_cols = shutil.get_terminal_size().columns
        bar = "─" * min(term_cols - 2, 68)

        hud = [
            C_CLEAR,
            f"{C_PINK}{C_BOLD}  ⭐ 🌸 KIRBY x PROJECTM TAPPA TAPPA COMPANION 🌸 ⭐{C_RESET}",
            f"{C_DIM}  {bar}{C_RESET}",
            f"  {C_CYAN}Tempo BPM{C_RESET}     : {C_GOLD}{C_BOLD}{self.bpm} BPM{C_RESET}    {C_CYAN}Multiplier{C_RESET} : {C_HOT_PINK}{multiplier}x HYPER-TAP{C_RESET}",
            f"  {C_CYAN}Total Taps{C_RESET}    : {C_WHITE}{self.total_taps}{C_RESET}        {C_CYAN}Streak{C_RESET}     : {C_GREEN}{self.streak}{C_RESET}",
            f"  {C_CYAN}ADB Bridge{C_RESET}    : {adb_status_str}   {C_CYAN}Co-Tap{C_RESET}     : {adb_mode_str}   {C_CYAN}Auto{C_RESET} : {auto_str}",
            f"  {C_CYAN}Web Portal{C_RESET}    : {C_WHITE}http://localhost:8088/tappa{C_RESET}",
            f"{C_DIM}  {bar}{C_RESET}",
            f"  {C_HOT_PINK}Speech Bubble{C_RESET} : {C_WHITE}\"{self.speech_bubble}\"{C_RESET}",
            KIRBY_TAP_FRAMES[self.current_frame_idx],
            f"{C_DIM}  {bar}{C_RESET}",
            f"  {C_DIM}[Space/Enter] Tappa Tappa • [A] Toggle ADB Co-Tap • [T] Auto-Pilot • [Q] Exit{C_RESET}"
        ]
        sys.stdout.write("\n".join(hud) + "\n")
        sys.stdout.flush()

    def run(self):
        # Raw terminal mode for non-blocking key capture
        is_tty = sys.stdin.isatty()
        old_settings = None
        if is_tty:
            import termios
            import tty
            old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

        sys.stdout.write(C_HIDE)
        sys.stdout.flush()

        last_auto_tick = time.time()

        try:
            while True:
                self.render()

                now = time.time()
                beat_interval = 60.0 / max(40, self.bpm)

                # Auto-pilot tap tick
                if self.auto_pilot and (now - last_auto_tick >= beat_interval):
                    self.trigger_tap()
                    last_auto_tick = now

                # Non-blocking poll for user keys
                r, _, _ = select.select([sys.stdin], [], [], 0.05)
                if r:
                    ch = sys.stdin.read(1)
                    if ch in (" ", "\r", "\n"):
                        self.trigger_tap()
                    elif ch in ("a", "A"):
                        self.adb_enabled = not self.adb_enabled
                        if self.adb_enabled and not self.adb_connected:
                            self.adb_connected = self.check_adb_status()
                    elif ch in ("t", "T"):
                        self.auto_pilot = not self.auto_pilot
                        last_auto_tick = time.time()
                    elif ch in ("q", "Q", "\x03", "\x1b"): # Q, Ctrl+C, Esc
                        break

                time.sleep(0.02)

        finally:
            sys.stdout.write(C_SHOW + C_RESET + "\n")
            sys.stdout.flush()
            if is_tty and old_settings:
                import termios
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            print(f"\n{C_PINK}✨ Poyo! You and Kirby tapped {self.total_taps} times at {self.bpm} BPM! See you at the visualizer! 🌸✨{C_RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Kirby x ProjectM Tappa Tappa Companion")
    parser.add_argument("--bpm", type=int, default=120, help="Initial target BPM")
    parser.add_argument("--adb", action="store_true", help="Enable ADB co-tapping on Pixel 9 Pro XL")
    parser.add_argument("--auto", action="store_true", help="Start in auto-pilot co-tap mode")
    args = parser.parse_args()

    companion = KirbyTappaCompanion(target_bpm=args.bpm, adb_enabled=args.adb, auto_pilot=args.auto)
    companion.run()


if __name__ == "__main__":
    main()
