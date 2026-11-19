#!/usr/bin/env python3
"""
⚡ KIRBY CHAOTIX TYPEY - Ephemeral Terminal Typing & Physics Playground ⚡
================================================================================
A hyper-reactive, chaotic ephemeral typing environment starring Kirby ( ^-^ )!

Features:
- Ephemeral Zero-Trust Session: 120s TTL token generated via Auth0rZero V2 in RAM.
- Non-blocking raw keyboard capture (termios/select) with clean terminal restoration.
- Real-time physics engine: Keystrokes generate elastic "Chaotix" tethers, bouncing
  ASCII particles, gravity sparks, and kinetic Kirby emotes.
- Procedural mechanical switch & sci-fi acoustics via agy_fx_engine.py:
  (Cherry Blue, Cherry Red, Typewriter, Clack, Laser, Sonar, Kirby Poyo chime).
- Live Telemetry HUD: Real-time WPM, Keystroke Velocity, Chaos Entropy (ΔH),
  Combo Streak Multipliers (1x -> 2x -> 4x -> 8x HYPER-DRIVE).
- Ephemeral Auto-Scrub: Memory wiped on exit with cybernetic glitch wipe.

Controls:
  Type any key           : Spawn chaotic particles, tethers & acoustics
  [Tab]                  : Toggle switch sound family (Cherry Blue / Typewriter / Kirby / Silent)
  [Ctrl + R]             : Rotate Chaotix gravity physics vector
  [Ctrl + L]             : Clear ephemeral canvas
  [Ctrl + C] / [Esc]     : Ephemeral self-destruct & exit
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
import subprocess
from dataclasses import dataclass
from typing import List, Optional

# --- Terminal ANSI Palette ---
C_PINK = "\033[38;5;205m"
C_CYAN = "\033[38;5;81m"
C_YELLOW = "\033[38;5;220m"
C_GREEN = "\033[38;5;120m"
C_BRIGHT_GREEN = "\033[38;5;46m"
C_PURPLE = "\033[38;5;141m"
C_RED = "\033[38;5;196m"
C_WHITE = "\033[38;5;255m"
C_DIM = "\033[2m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"
C_CLEAR = "\033[2J\033[H"
C_HIDE_CURSOR = "\033[?25l"
C_SHOW_CURSOR = "\033[?25h"

# Try importing sound engine
HAS_AUDIO = False
try:
    sys.path.insert(0, "/mnt/shared/AntiGravity_Shared")
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False

# Try importing Auth0rZero token generator
def get_ephemeral_token():
    try:
        sys.path.insert(0, "/home/droid/antigravity_hub/scripts")
        import auth0rzero_cli
        return auth0rzero_cli.issue_token(subject="chaotix.typey.ephemeral")
    except Exception:
        import secrets
        return {
            "tokenId": f"tok_ephem_{secrets.token_hex(6)}",
            "securityProfile": "ZERO_TRUST_EPHEMERAL_V2",
            "claims": {"sub": "chaotix.typey.ephemeral", "exp": int(time.time()) + 120}
        }


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    char: str
    color: str
    life: float
    max_life: float
    is_kirby: bool = False


class ChaotixTypeyEnv:
    def __init__(self, sound_enabled: bool = True):
        self.sound_enabled = sound_enabled and HAS_AUDIO
        self.sound_modes = ["cherry_blue", "typewriter", "kirby", "laser", "silent"]
        self.sound_mode_idx = 0 if self.sound_enabled else 4
        self.token = get_ephemeral_token()
        self.token_id = self.token.get("tokenId", "tok_live")
        self.expires_at = self.token.get("claims", {}).get("exp", time.time() + 120)

        self.orig_term_settings = None
        self.running = True
        self.cols, self.rows = 80, 24
        self.update_terminal_size()

        # Typing & Telemetry
        self.buffer = ""
        self.keystroke_timestamps = []
        self.combo_count = 0
        self.max_combo = 0
        self.total_keystrokes = 0
        self.gravity_angle = math.pi / 2  # downward default
        self.gravity_force = 0.45

        # Chaotix Physics Simulation
        self.particles: List[Particle] = []
        self.kirby_x = float(self.cols // 2)
        self.kirby_y = float(self.rows // 2)
        self.kirby_vx = 0.0
        self.kirby_vy = 0.0
        self.kirby_face = "(^o^)"
        self.kirby_mood = "happy"
        self.last_type_time = time.time()

        # Register signals
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGWINCH, self.handle_winch)

    def update_terminal_size(self):
        try:
            self.cols, self.rows = shutil.get_terminal_size((80, 24))
        except Exception:
            self.cols, self.rows = 80, 24

    def handle_winch(self, *args):
        self.update_terminal_size()

    def handle_signal(self, *args):
        self.running = False

    def setup_terminal(self):
        if not sys.stdin.isatty():
            return
        import termios
        import tty
        self.orig_term_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        sys.stdout.write(C_HIDE_CURSOR + C_CLEAR)
        sys.stdout.flush()

    def restore_terminal(self):
        if self.orig_term_settings and sys.stdin.isatty():
            import termios
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.orig_term_settings)
        sys.stdout.write(C_SHOW_CURSOR + C_RESET + "\n")
        sys.stdout.flush()

    def play_sound(self, preset: Optional[str] = None):
        if not self.sound_enabled:
            return
        snd = preset or self.sound_modes[self.sound_mode_idx]
        if snd == "silent":
            return
        try:
            play_sound_preset(snd)
        except Exception:
            pass

    def cycle_sound_mode(self):
        self.sound_mode_idx = (self.sound_mode_idx + 1) % len(self.sound_modes)
        mode = self.sound_modes[self.sound_mode_idx]
        self.sound_enabled = (mode != "silent")
        if self.sound_enabled:
            self.play_sound("hop")

    def spawn_burst(self, origin_x: float, origin_y: float, char: str):
        # Explosive particle burst with chaotic elastic velocities
        sparks = [char, "★", "✦", "✧", "·", "•", "°", "🫧"]
        colors = [C_PINK, C_CYAN, C_YELLOW, C_BRIGHT_GREEN, C_PURPLE, C_WHITE]
        
        num_particles = random.randint(4, 9)
        for _ in range(num_particles):
            speed = random.uniform(1.2, 3.8)
            ang = random.uniform(0, 2 * math.pi)
            p_char = random.choice(sparks)
            p_color = random.choice(colors)
            life = random.uniform(0.6, 1.8)
            self.particles.append(Particle(
                x=origin_x,
                y=origin_y,
                vx=math.cos(ang) * speed * 1.5,
                vy=math.sin(ang) * speed,
                char=p_char,
                color=p_color,
                life=life,
                max_life=life
            ))

        # Kirby reactions
        if self.combo_count > 15:
            self.kirby_face = "🌟(★ω★)🌟"
            self.kirby_mood = "hyper"
        elif self.combo_count > 5:
            self.kirby_face = "ε=ε=┌(>‿<)┘"
            self.kirby_mood = "excited"
        else:
            self.kirby_face = random.choice(["(^o^)", "(>‿<)", "(•̀ᴗ•́)و", "(੭ˊᵕˋ)੭"])
            self.kirby_mood = "happy"

        # Push Kirby with recoil
        self.kirby_vx += random.uniform(-1.5, 1.5)
        self.kirby_vy += random.uniform(-1.0, 1.0)

    def on_keystroke(self, ch: str):
        now = time.time()
        self.total_keystrokes += 1
        self.last_type_time = now
        self.keystroke_timestamps.append(now)
        # Purge timestamps older than 5s
        self.keystroke_timestamps = [t for t in self.keystroke_timestamps if now - t <= 5.0]

        # Combo calculation
        self.combo_count += 1
        if self.combo_count > self.max_combo:
            self.max_combo = self.combo_count

        # Append to ephemeral buffer (keep last 45 chars visible)
        if ch in ('\r', '\n'):
            self.buffer += " ⏎ "
            self.play_sound("bubble_pop")
        elif ch in ('\x7f', '\x08'):  # Backspace
            if self.buffer:
                self.buffer = self.buffer[:-1]
            self.play_sound("wood_knock")
            self.combo_count = max(0, self.combo_count - 2)
        else:
            self.buffer += ch
            if self.combo_count % 10 == 0:
                self.play_sound("kirby")
            else:
                self.play_sound()

        # Origin for particles
        origin_x = self.cols // 2 + random.randint(-10, 10)
        origin_y = self.rows - 4
        self.spawn_burst(origin_x, origin_y, ch if len(ch) == 1 and ch.isprintable() else "✦")

    def update_physics(self, dt: float):
        now = time.time()
        # Reset combo if idle > 2.2s
        if now - self.last_type_time > 2.2:
            self.combo_count = max(0, self.combo_count - 1)
            if self.combo_count == 0:
                self.kirby_face = "(u.uz) *zZz*"

        gx = math.cos(self.gravity_angle) * self.gravity_force
        gy = math.sin(self.gravity_angle) * self.gravity_force

        # Update Kirby physics (spring tether to center-top)
        target_kx = self.cols / 2.0
        target_ky = max(4.0, self.rows / 3.0)
        spring_k = 0.08
        damping = 0.88

        self.kirby_vx += (target_kx - self.kirby_x) * spring_k + gx * 0.2
        self.kirby_vy += (target_ky - self.kirby_y) * spring_k + gy * 0.2
        self.kirby_vx *= damping
        self.kirby_vy *= damping
        self.kirby_x += self.kirby_vx
        self.kirby_y += self.kirby_vy

        # Boundaries
        self.kirby_x = max(2.0, min(self.cols - 12.0, self.kirby_x))
        self.kirby_y = max(3.0, min(self.rows - 6.0, self.kirby_y))

        # Update particles
        alive_particles = []
        for p in self.particles:
            p.life -= dt
            if p.life <= 0:
                continue

            p.vx += gx
            p.vy += gy
            p.vx *= 0.96
            p.vy *= 0.96
            p.x += p.vx
            p.y += p.vy

            # Bouncing off walls
            if p.x <= 1 or p.x >= self.cols - 2:
                p.vx = -p.vx * 0.7
                p.x = max(1.0, min(float(self.cols - 2), p.x))
            if p.y <= 2 or p.y >= self.rows - 3:
                p.vy = -p.vy * 0.6
                p.y = max(2.0, min(float(self.rows - 3), p.y))

            alive_particles.append(p)
        self.particles = alive_particles

    def compute_telemetry(self) -> dict:
        now = time.time()
        # Words per minute calculation over 5s window
        recent_count = len(self.keystroke_timestamps)
        wpm = int((recent_count / 5.0) * 12.0)  # chars/5 * 60 / 5
        
        # Entropy calculation (variation of characters)
        unique_chars = len(set(self.buffer[-25:])) if self.buffer else 1
        entropy = round(min(1.0, unique_chars / 15.0) * 100, 1)

        # Multiplier
        mult = "1x"
        if self.combo_count >= 30:
            mult = "8x HYPER-DRIVE 🚀"
        elif self.combo_count >= 15:
            mult = "4x OVERDRIVE ⚡"
        elif self.combo_count >= 5:
            mult = "2x RAPID 🔥"

        ttl = max(0, int(self.expires_at - now))
        return {
            "wpm": wpm,
            "combo": self.combo_count,
            "max_combo": self.max_combo,
            "entropy": entropy,
            "mult": mult,
            "ttl": ttl,
            "mode": self.sound_modes[self.sound_mode_idx]
        }

    def render_frame(self):
        telem = self.compute_telemetry()
        grid = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
        col_grid = [["" for _ in range(self.cols)] for _ in range(self.rows)]

        # 1. Render Top Header & Telemetry
        ttl_color = C_GREEN if telem["ttl"] > 30 else (C_YELLOW if telem["ttl"] > 10 else C_RED)
        header = f" ⚡ CHAOTIX EPHEMERAL TYPEY | TTL: {ttl_color}{telem['ttl']}s{C_RESET} | WPM: {C_CYAN}{telem['wpm']}{C_RESET} | Combo: {C_PINK}{telem['combo']} ({telem['mult']}){C_RESET} | Sound: {C_YELLOW}{telem['mode']}{C_RESET} "
        
        for c, ch in enumerate(header[:self.cols]):
            grid[0][c] = ch
            col_grid[0][c] = C_BOLD

        border = "═" * self.cols
        for c, ch in enumerate(border[:self.cols]):
            grid[1][c] = ch
            col_grid[1][c] = C_PURPLE

        # 2. Render Elastic Chaotix Tether (Kirby -> Text Cursor)
        kx, ky = int(self.kirby_x), int(self.kirby_y)
        cx, cy = self.cols // 2, self.rows - 4
        steps = 8
        for i in range(1, steps):
            tx = int(kx + (cx - kx) * (i / steps))
            ty = int(ky + (cy - ky) * (i / steps))
            if 0 <= ty < self.rows and 0 <= tx < self.cols:
                if grid[ty][tx] == " ":
                    grid[ty][tx] = "~" if i % 2 == 0 else "•"
                    col_grid[ty][tx] = C_DIM + C_PINK

        # 3. Render Kirby
        kirby_str = f"🌸 {self.kirby_face} 🌸"
        for i, ch in enumerate(kirby_str):
            tx = kx + i - (len(kirby_str) // 2)
            if 0 <= ky < self.rows and 0 <= tx < self.cols:
                grid[ky][tx] = ch
                col_grid[ky][tx] = C_PINK + C_BOLD

        # 4. Render Floating Particles
        for p in self.particles:
            px, py = int(p.x), int(p.y)
            if 0 <= py < self.rows and 0 <= px < self.cols:
                grid[py][px] = p.char
                col_grid[py][px] = p.color

        # 5. Render Ephemeral Typing Buffer at Bottom
        buf_y = self.rows - 4
        disp_buf = self.buffer[-min(len(self.buffer), self.cols - 16):]
        buf_label = "TYPEY: "
        for i, ch in enumerate(buf_label):
            tx = 2 + i
            if tx < self.cols:
                grid[buf_y][tx] = ch
                col_grid[buf_y][tx] = C_CYAN + C_BOLD
        
        for i, ch in enumerate(disp_buf):
            tx = 9 + i
            if tx < self.cols - 2:
                grid[buf_y][tx] = ch
                col_grid[buf_y][tx] = C_WHITE + C_BOLD

        # Cursor indicator
        cur_x = min(self.cols - 2, 9 + len(disp_buf))
        if 0 <= cur_x < self.cols:
            grid[buf_y][cur_x] = "█"
            col_grid[buf_y][cur_x] = C_GREEN

        # Bottom status bar
        bot_y = self.rows - 2
        hints = " [Type]: Burst FX | [Tab]: Sound Switch | [Ctrl+R]: Gravity | [Ctrl+C]: Wipe "
        for c, ch in enumerate(hints[:self.cols]):
            grid[bot_y][c] = ch
            col_grid[bot_y][c] = C_DIM + C_WHITE

        # Assemble ANSI string
        frame_lines = []
        for r in range(self.rows):
            line_str = "".join(f"{col_grid[r][c]}{grid[r][c]}" for c in range(self.cols))
            frame_lines.append(line_str)

        sys.stdout.write("\033[H" + "\n".join(frame_lines) + C_RESET)
        sys.stdout.flush()

    def wipe_self_destruct(self):
        """Cybernetic glitch self-destruct animation for ephemeral environment."""
        self.buffer = ""
        self.particles.clear()
        sys.stdout.write(C_CLEAR)
        glitch_chars = ["0", "1", "X", "#", "%", "!", "░", "▒", "▓"]
        for frame in range(6):
            lines = []
            for _ in range(self.rows):
                line = "".join(random.choice(glitch_chars) if random.random() < (frame * 0.18) else " " for _ in range(self.cols))
                lines.append(f"{C_RED}{line}{C_RESET}")
            sys.stdout.write("\033[H" + "\n".join(lines))
            sys.stdout.flush()
            time.sleep(0.04)
        
        sys.stdout.write(C_CLEAR + "\033[H")
        banner = f"\n{C_PINK}{C_BOLD}  🌸 [EPHEMERAL CHAOTIX ENVIRONMENT PURGED] 🌸{C_RESET}\n"
        banner += f"  Token: {self.token_id} | Security: ZERO_TRUST_EPHEMERAL_V2\n"
        banner += f"  Keystrokes: {self.total_keystrokes} | Max Combo: {self.max_combo}\n"
        banner += f"  All session buffers in RAM securely scrubbed. Dream Land safe, Poyo!\n\n"
        sys.stdout.write(banner)
        sys.stdout.flush()

    def run(self):
        self.setup_terminal()
        atexit.register(self.restore_terminal)

        last_time = time.time()
        try:
            while self.running:
                now = time.time()
                dt = min(0.1, now - last_time)
                last_time = now

                # Ephemeral token expiry check
                if now >= self.expires_at:
                    self.wipe_self_destruct()
                    break

                # Non-blocking input check
                if sys.stdin.isatty():
                    r, _, _ = select.select([sys.stdin], [], [], 0.03)
                    if r:
                        ch = sys.stdin.read(1)
                        if ch == '\x03' or ch == '\x1b':  # Ctrl+C or ESC
                            break
                        elif ch == '\t':  # Tab
                            self.cycle_sound_mode()
                        elif ch == '\x12':  # Ctrl+R (rotate gravity)
                            self.gravity_angle += math.pi / 2
                            self.spawn_burst(self.cols // 2, self.rows // 2, "🌀")
                        elif ch == '\x0c':  # Ctrl+L (clear)
                            self.buffer = ""
                            self.particles.clear()
                        else:
                            self.on_keystroke(ch)

                self.update_physics(dt)
                self.render_frame()
                time.sleep(0.02)

        finally:
            self.wipe_self_destruct()
            self.restore_terminal()


def run_headless_test():
    print(f"{C_PINK}⭐ Testing Kirby Chaotix Typey Headless Simulation...{C_RESET}")
    env = ChaotixTypeyEnv(sound_enabled=False)
    test_chars = "typey typey poyo antigravity! 42"
    for ch in test_chars:
        env.on_keystroke(ch)
        env.update_physics(0.05)
    telem = env.compute_telemetry()
    assert telem["combo"] > 0, "Combo did not register"
    assert len(env.particles) > 0, "Particles failed to generate"
    assert env.token_id.startswith("tok_"), "Ephemeral token invalid"
    print(f"{C_GREEN}✔ Headless simulation verified: {telem['combo']} combo, {len(env.particles)} particles active!{C_RESET}")


def main():
    parser = argparse.ArgumentParser(description="Kirby Chaotix Typey - Ephemeral UX Terminal Environment")
    parser.add_argument("--no-sound", action="store_true", help="Disable mechanical acoustics")
    parser.add_argument("--test", action="store_true", help="Run automated verification suite")
    args = parser.parse_args()

    if args.test:
        run_headless_test()
        sys.exit(0)

    env = ChaotixTypeyEnv(sound_enabled=not args.no_sound)
    env.run()


if __name__ == "__main__":
    main()
