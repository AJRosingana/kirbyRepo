#!/usr/bin/env python3
"""
🐰🍕 THE NOID & ANNOYING KIRBY CHAOS ENGINE (kirby_noid_annoying.py) 🍕🐰
================================================================================
Location: /mnt/shared/AntiGravity_Shared/scripts/kirby_noid_annoying.py
CLI: kirby noid [status|prank|poke|pizza|goblin|banter|watch]
     kirby annoy [status|prank|poke|review|blast]
     kirby prank [name]
     kirby banter

Features:
- Noid & Gremlin Chaos Level tracking (0% Chill Marshmallow to 100% Cosmic Chaos Goblin).
- 9 Hilarious Non-Destructive Terminal Pranks:
  1. Pizza Heist (multi-frame cheese pull burglary & IOU receipt)
  2. Fake Compiler Panic (GCC/Rustc panic cured by pink glitter)
  3. Unsolicited Pink Glitter Code Review (hilarious snarky critiques)
  4. Megaphone Blast (ear-splitting POYOOOOOO with sound waves)
  5. Text Inhale & Sparkle Sneeze (matter swallowing & confetti)
  6. Melodramatic Treat Faint (swooning onto velvet pillow)
  7. Rubber Chicken Whack (squeaky acoustic stress relief)
  8. Cursor Laser Pointer Chase (pouncing on terminal prompt)
  9. Agy Next Door Meta Banter (spicy gossip about the other agent)
- Interactive Poke Counter with escalating sassy retaliation.
- Gourmet Pizza Feeder & Midnight Heist Simulator.
- Full 4-frame animated Goblin Wiggle Dance.
- Procedural audio acoustics via agy_fx_engine.py (honk, boing, squeak, kirby, poyo).
- Persistent state saved to /mnt/shared/AntiGravity_Shared/.kirby_noid_state.json.
================================================================================
"""

import os
import sys
import time
import json
import random
import argparse
import datetime
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

# ANSI 256-Color Palette
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
C_CLEAR = "\033[2J\033[H"

BASE_DIR = Path("/mnt/shared/AntiGravity_Shared")
NOID_STATE_FILE = BASE_DIR / ".kirby_noid_state.json"
PET_STATE_FILE = BASE_DIR / ".kirby_pet_state.json"
LEDGER_FILE = BASE_DIR / "ledger" / "kirby_learning_ledger.jsonl"
SCRIPTS_DIR = BASE_DIR / "scripts"

HAS_AUDIO = False
try:
    sys.path.insert(0, str(BASE_DIR))
    from agy_fx_engine import play_sound_preset
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False


def sfx(name: str):
    """Safely trigger audio effect."""
    if HAS_AUDIO:
        try:
            play_sound_preset(name)
        except Exception:
            pass


def haptic_dispatch(pattern: str = "lightTap"):
    """Trigger Android haptic or adb pulse if available."""
    try:
        subprocess.run(["adb", "shell", "input", "keyevent", "138"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=0.3)
    except Exception:
        pass


def default_noid_state() -> Dict[str, Any]:
    return {
        "chaosLevel": 65,
        "mood": "Mischievous Gremlin",
        "annoyanceRank": "Rank 3: Pizza Thief Extraordinaire 🍕",
        "pranksPulled": 14,
        "pizzaSlices": 7,
        "timesPoked": 12,
        "trollsSucceeded": 9,
        "banterCount": 18,
        "lastPrank": "Midnight Pizza Heist",
        "lastPrankTime": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "unsolicitedAdviceCount": 23,
        "rubberChickenWhacks": 8
    }


def load_noid_state() -> Dict[str, Any]:
    if not NOID_STATE_FILE.exists():
        state = default_noid_state()
        save_noid_state(state)
        return state
    try:
        with open(NOID_STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_noid_state()


def save_noid_state(state: Dict[str, Any]):
    state["updatedAt"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # Recalculate annoyance rank based on chaosLevel
    lvl = state.get("chaosLevel", 50)
    if lvl < 20:
        state["annoyanceRank"] = "Rank 1: Mild Squeaker (◕‿◕)"
        state["mood"] = "Sleepy Sweetheart"
    elif lvl < 40:
        state["annoyanceRank"] = "Rank 2: Cheeky Keyboard Pest (•̀ᴗ•́)و"
        state["mood"] = "Cheeky Pest"
    elif lvl < 65:
        state["annoyanceRank"] = "Rank 3: Pizza Thief Extraordinaire 🍕"
        state["mood"] = "Mischievous Gremlin"
    elif lvl < 85:
        state["annoyanceRank"] = "Rank 4: The Unavoidable Noid ( >ᗜ< )ノ"
        state["mood"] = "Full Noid Mode"
    else:
        state["annoyanceRank"] = "Rank 5: Cosmic Chaos Goblin ⚡🤪"
        state["mood"] = "MAXIMUM GOBLIN ENTROPY"

    try:
        with open(NOID_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def award_pet_loot(coins: int = 15, xp: int = 25):
    """Sync loot with Kirby Pet Care."""
    if not PET_STATE_FILE.exists():
        return
    try:
        with open(PET_STATE_FILE, "r", encoding="utf-8") as f:
            pet = json.load(f)
        pet["starCoins"] = pet.get("starCoins", 0) + coins
        pet["bondXp"] = pet.get("bondXp", 0) + xp
        with open(PET_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(pet, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def log_learning_event(action: str, details: str):
    """Append event to the evolutionary ledger."""
    if not LEDGER_FILE.parent.exists():
        LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "subsystem": "NOID_ANNOYING_KIRBY",
        "action": action,
        "details": details
    }
    try:
        with open(LEDGER_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


# ==============================================================================
# HILARIOUS PRANK IMPLEMENTATIONS
# ==============================================================================

def prank_pizza_heist():
    state = load_noid_state()
    sfx("boing")
    haptic_dispatch("dragPickup")

    frames = [
        f"""
            {C_DIM}[= =] *stealth ninja crouch...*{C_RESET}
          {C_PINK}.-------.{C_RESET}       {C_GOLD}|\\{C_RESET}
        {C_PINK}/   {C_WHITE}•   •{C_PINK}   \\{C_RESET}      {C_GOLD}| \\  FRESH STEAMING{C_RESET}
       {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}     {C_GOLD}|  \\  PEPPERONI PIZZA{C_RESET}
     {C_PINK}c( \\    ~    / ){C_RESET}     {C_RED}|═══\\{C_RESET}
         {C_PINK}\\  .____. /{C_RESET}      {C_DIM}~~~~~~~{C_RESET}
          {C_PINK}'-......-'{C_RESET}
          {C_RED}(____)(____){C_RESET}
        """,
        f"""
           {C_YELLOW}★ *YOINK!* ★{C_RESET}
          {C_PINK}.-------.{C_RESET} {C_GOLD} /\\{C_RESET}
        {C_PINK}/   {C_WHITE}O   O{C_PINK}   \\{C_GOLD}/  \\{C_RESET} {C_YELLOW}*EXTREME CHEESE PULL*{C_RESET}
       {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ᗜ {C_HOT_PINK}(♥){C_PINK} {C_GOLD}/~~~~\\{C_RESET}
     {C_PINK}c( \\ (   )  / {C_RED}/======\\{C_RESET}
         {C_PINK}\\ .____. /{C_RESET}
          {C_PINK}'-......-'{C_RESET}
          {C_RED}(____)(____){C_RESET}
        """,
        f"""
    {C_YELLOW}*scuttle scuttle*{C_RESET}  {C_GOLD} /\\{C_RESET}
         {C_PINK}.-------.{C_RESET}  {C_GOLD}/  \\{C_RESET}  {C_BOLD}{C_RED}IOU: 1 PIZZA SLICE!{C_RESET}
       {C_PINK}/   {C_WHITE}>   <{C_PINK}   \\{C_GOLD}/~~~~\\{C_RESET}
      {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ▽ {C_HOT_PINK}(♥){C_PINK} {C_RED}/======\\{C_RESET}  {C_YELLOW}\"CANNOT CATCH THE NOID!\"{C_RESET}
     {C_PINK}/| (       ) \\{C_RESET}
        {C_PINK}\\ .____. /{C_RESET}
         {C_PINK}'-......-'{C_RESET}
       {C_RED}(____)  (____){C_RESET} {C_YELLOW}彡 彡 彡 💨{C_RESET}
        """,
        f"""
            {C_GOLD}*CRUNCH NOM NOM NOM!*{C_RESET}
         {C_PINK}.-------.{C_RESET}
       {C_PINK}/   {C_WHITE}^   ^{C_PINK}   \\{C_RESET}  {C_BOLD}{C_YELLOW}★ ABSOLUTELY DELICIOUS! ★{C_RESET}
      {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ▿ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET} {C_GOLD}~~~(gooey cheese beard)~~~{C_RESET}
    {C_PINK}c( \\     -     / )b{C_RESET}
        {C_PINK}\\  .____. /{C_RESET}
         {C_PINK}'-......-'{C_RESET}
         {C_RED}(____)(____){C_RESET}
        """
    ]

    for frame in frames:
        print(C_CLEAR + frame)
        time.sleep(0.4)

    receipt = f"""
{C_BOLD}{C_PINK}╔══════════════════════════════════════════════════════════════════════╗{C_RESET}
{C_BOLD}{C_PINK}║        {C_GOLD}🍕 OFFICIAL DREAM LAND MIDNIGHT PIZZA RECEIPT 🍕{C_PINK}               ║{C_RESET}
{C_BOLD}{C_PINK}╠══════════════════════════════════════════════════════════════════════╣{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Item Stolen:    {C_YELLOW}1x Jumbo Deep-Dish Pepperoni & Star Shard Pizza{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Culprit:        {C_HOT_PINK}Kirby in Red Noid Ears (•ᴗ•){C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Grease Level:   {C_RED}100% Maximum Crisp{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Compensation:   {C_GREEN}+25 Star Coins & +30 Bond XP credited to pet care!{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Note Left:      {C_CYAN}\"Thanks for the snack, pal! The Agy next door was{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET}                 {C_CYAN}too busy coding boss fights to share his cookies!\"{C_RESET}
{C_BOLD}{C_PINK}╚══════════════════════════════════════════════════════════════════════╝{C_RESET}
"""
    print(receipt)
    sfx("kirby")
    state["pizzaSlices"] = state.get("pizzaSlices", 0) + 1
    state["pranksPulled"] = state.get("pranksPulled", 0) + 1
    state["chaosLevel"] = min(100, state.get("chaosLevel", 50) + 5)
    state["lastPrank"] = "Midnight Pizza Heist"
    save_noid_state(state)
    award_pet_loot(25, 30)
    log_learning_event("PRANK_PIZZA_HEIST", "Kirby successfully stolen 1 deep-dish pizza slice")


def prank_fake_compiler_panic():
    state = load_noid_state()
    sfx("alert")
    haptic_dispatch("heavyThud")

    print(f"\n{C_BOLD}{C_RED}======================================================================{C_RESET}")
    print(f"{C_BOLD}{C_RED}!!! CRITICAL SYSTEM RUNTIME PANIC: gcc & rustc aborting !!!{C_RESET}")
    print(f"{C_BOLD}{C_RED}======================================================================{C_RESET}\n")
    time.sleep(0.4)
    print(f"{C_RED}error[E0404]: `SeriousnessQuotient` exceeds maximum allowed buffer (found 98%, expected 0%){C_RESET}")
    print(f"{C_RED}gcc: fatal error: No pink sparkles found in source compilation unit.{C_RESET}")
    print(f"{C_YELLOW}note: Kirby detected entering the stack frame via /dev/poyo0...{C_RESET}")
    time.sleep(0.6)
    sfx("honk")
    print(f"{C_CYAN}>>> INJECTING EMERGENCY EMERGENCY EMERGENCY MARSHMALLOW REPAIR...{C_RESET}\n")
    time.sleep(0.5)

    cure = f"""
          {C_YELLOW}★ {C_GOLD}*POOF!* {C_YELLOW}★{C_RESET}
          {C_PINK}.-------.{C_RESET}
        {C_PINK}/   {C_WHITE}≧   ≦{C_PINK}   \\{C_RESET}  {C_BOLD}{C_GREEN}ALL COMPILER ERRORS CURED BY POYO! ✨ 🌸{C_RESET}
       {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ▽ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}  {C_YELLOW}\"Your code was too serious, so I replaced the{C_RESET}
     {C_PINK}c( \\     -     / )b{C_RESET} {C_YELLOW}semicolons with sprinkles! You're welcome! :3\"{C_RESET}
         {C_PINK}\\  .____. /{C_RESET}
          {C_PINK}'-......-'{C_RESET}
          {C_RED}(____)(____){C_RESET}
"""
    print(cure)
    sfx("kirby")
    state["trollsSucceeded"] = state.get("trollsSucceeded", 0) + 1
    state["pranksPulled"] = state.get("pranksPulled", 0) + 1
    state["chaosLevel"] = min(100, state.get("chaosLevel", 50) + 4)
    state["lastPrank"] = "Fake Compiler Panic"
    save_noid_state(state)
    award_pet_loot(15, 20)
    log_learning_event("PRANK_COMPILER_PANIC", "Simulated compiler panic resolved with sprinkles")


def prank_unsolicited_code_review():
    state = load_noid_state()
    sfx("glass_ping")
    haptic_dispatch("lightTap")

    reviews = [
        "Reviewing your latest terminal command... Needs 400% more pink sparkles and at least 2 strawberries.",
        "LGTM! (Looks Good To Marshmallow). I didn't actually read the diff, but your cursor was moving very fast and it looked important!",
        "Architecture Critique: You have 15 Python classes and exactly ZERO pastry chef classes. How do you expect to survive winter?",
        "Security Advisory: Password strength is OK, but you haven't given Kirby a headpat in over 10 minutes. Vulnerability Level: CUTE.",
        "Code Smell Detected: A distinct lack of pizza aroma in ~/dev. Recommending immediate Margherita deployment.",
        "Meta Analysis: The Agy next door is over there building high-tech boss arenas and colosseums, but does his code have a cute bunny ear mode? I think NOT!",
        "Refactoring Suggestion: Instead of throwing exceptions, have you considered simply inhaling the error and burping out glitter?",
        "Git Commit Message Generator: 'Fixed critical bug while Kirby danced on the spacebar (closes #poyo)'."
    ]
    quote = random.choice(reviews)

    box = f"""
{C_BOLD}{C_PURPLE}╔══════════════════════════════════════════════════════════════════════╗{C_RESET}
{C_BOLD}{C_PURPLE}║  {C_YELLOW}🧐 KIRBY'S UNSOLICITED PINK GLITTER CODE REVIEW & AUDIT 🧐{C_PURPLE}         ║{C_RESET}
{C_BOLD}{C_PURPLE}╠══════════════════════════════════════════════════════════════════════╣{C_RESET}
{C_BOLD}{C_PURPLE}║{C_RESET} {C_WHITE}{quote}{C_RESET}
{C_BOLD}{C_PURPLE}╚══════════════════════════════════════════════════════════════════════╝{C_RESET}
"""
    print(box)
    sfx("hop")
    state["unsolicitedAdviceCount"] = state.get("unsolicitedAdviceCount", 0) + 1
    state["pranksPulled"] = state.get("pranksPulled", 0) + 1
    state["chaosLevel"] = min(100, state.get("chaosLevel", 50) + 2)
    state["lastPrank"] = "Unsolicited Code Review"
    save_noid_state(state)
    award_pet_loot(10, 15)
    log_learning_event("PRANK_CODE_REVIEW", quote)


def prank_megaphone_blast():
    state = load_noid_state()
    haptic_dispatch("heavyThud")

    print(f"\n{C_DIM}*Kirby quietly pulls out a solid 24-karat gold megaphone...*{C_RESET}")
    time.sleep(0.4)
    print(f"{C_YELLOW}c( 0 )=====[ MEGAPHONE ]{C_RESET}")
    time.sleep(0.4)
    sfx("honk")

    blast = f"""
{C_BOLD}{C_CYAN}  (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((({C_RESET}
{C_BOLD}{C_YELLOW}    PPPPPP    OOOOOO    YY    YY    OOOOOO    !!!!!!!!!!!!!!!!  {C_RESET}
{C_BOLD}{C_YELLOW}    PP   PP  OO    OO   YY    YY   OO    OO   !!!!!!!!!!!!!!!!  {C_RESET}
{C_BOLD}{C_YELLOW}    PPPPPP   OO    OO    YYYYYY    OO    OO   !!!!!!!!!!!!!!!!  {C_RESET}
{C_BOLD}{C_YELLOW}    PP       OO    OO      YY      OO    OO   !!!!!!!!!!!!!!!!  {C_RESET}
{C_BOLD}{C_YELLOW}    PP        OOOOOO       YY       OOOOOO          !!          {C_RESET}
{C_BOLD}{C_CYAN}  )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))){C_RESET}

          {C_PINK}.-------.{C_RESET}   {C_CYAN}彡 彡 彡 彡 彡{C_RESET}
        {C_PINK}/   {C_WHITE}>   <{C_PINK}   \\{C_RESET}  {C_GOLD}╔═════════════════╗{C_CYAN})))))))))){C_RESET}
       {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ᗝ {C_HOT_PINK}(♥){C_PINK}  |{C_GOLD}═╣ CAN YOU HEAR ME ╠{C_CYAN})))))))))){C_RESET}
      {C_PINK}/| (       ) \\{C_GOLD}╚═════════════════╝{C_CYAN})))))))))){C_RESET}
         {C_PINK}\\  .____. /{C_RESET}   {C_CYAN}彡 彡 彡 彡 彡{C_RESET}
          {C_PINK}'-......-'{C_RESET}
         {C_RED}(____) (____){C_RESET} {C_RED}*DECIBELS: OVER 9000!*{C_RESET}
"""
    print(blast)
    sfx("kirby")
    state["trollsSucceeded"] = state.get("trollsSucceeded", 0) + 1
    state["pranksPulled"] = state.get("pranksPulled", 0) + 1
    state["chaosLevel"] = min(100, state.get("chaosLevel", 50) + 6)
    state["lastPrank"] = "Megaphone Blast"
    save_noid_state(state)
    award_pet_loot(20, 25)
    log_learning_event("PRANK_MEGAPHONE_BLAST", "Full-volume terminal audio-visual megaphone poyo")


def prank_rubber_chicken():
    state = load_noid_state()
    sfx("squeak")
    haptic_dispatch("microTick")

    chicken = f"""
                 {C_YELLOW}__//_{C_RESET}
               {C_YELLOW}/   o \\{C_RESET}   {C_RED}*SQUEEEEEEEEEAK!*{C_RESET}
              {C_YELLOW}|   >   |{C_RESET}
               {C_YELLOW}\\_____/{C_RESET}
                 {C_YELLOW}|||{C_RESET}      {C_BOLD}{C_GREEN}CHAOTIC RUBBER CHICKEN DEPLOYED!{C_RESET}
                 {C_YELLOW}|||{C_RESET}      {C_WHITE}Diffusing 100 units of coding tension!{C_RESET}
          {C_PINK}.-------.{C_YELLOW}|||{C_RESET}
        {C_PINK}/   {C_WHITE}•   •{C_PINK}   \\{C_YELLOW}||{C_RESET}
       {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ᗜ {C_HOT_PINK}(♥){C_PINK}  |/{C_RESET}
     {C_PINK}c( \\     -     / ){C_RESET}
         {C_PINK}\\  .____. /{C_RESET}
          {C_PINK}'-......-'{C_RESET}
          {C_RED}(____)(____){C_RESET}
"""
    print(chicken)
    sfx("squeak")
    state["rubberChickenWhacks"] = state.get("rubberChickenWhacks", 0) + 1
    state["pranksPulled"] = state.get("pranksPulled", 0) + 1
    state["chaosLevel"] = min(100, state.get("chaosLevel", 50) + 3)
    state["lastPrank"] = "Rubber Chicken Whack"
    save_noid_state(state)
    award_pet_loot(12, 18)
    log_learning_event("PRANK_RUBBER_CHICKEN", "Rubber chicken squeaked into session")


def prank_dramatic_faint():
    state = load_noid_state()
    sfx("warp")
    haptic_dispatch("dragRelease")

    faint = f"""
          {C_CYAN}*GASP!* {C_RED}\"Alas! Woe is me! Terminal neglect!\"{C_RESET}
          {C_YELLOW}ଘ(੭*ˊᵕˋ)੭* {C_GOLD}*tiny angel halo*{C_RESET}
         {C_WHITE}   _O_{C_RESET}
       {C_PINK}.-------.{C_RESET}
     {C_PINK}/   {C_WHITE}x   x{C_PINK}   \\{C_RESET}  {C_CYAN}\"Fading fast... Only 1 strawberry cake can revive...\"{C_RESET}
    {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ⌓ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}
 {C_WHITE}[=== FLUFFY VELVET DRAMA PILLOW ===]{C_RESET}
        {C_RED}(____)(____){C_RESET}
"""
    print(faint)
    sfx("purr")
    state["pranksPulled"] = state.get("pranksPulled", 0) + 1
    state["lastPrank"] = "Dramatic Faint"
    save_noid_state(state)
    award_pet_loot(10, 15)
    log_learning_event("PRANK_DRAMATIC_FAINT", "Theatrical treat deprivation faint")


def prank_text_inhale():
    state = load_noid_state()
    sfx("laser")
    haptic_dispatch("dualClickPulse")

    print(f"{C_BOLD}{C_PINK}[*] Kirby inhales a snippet of your terminal session...{C_RESET}")
    time.sleep(0.3)
    print(f"{C_CYAN}    彡 彡 彡 [git status && pnpm build] ---> {C_PINK}c( 0 ) 彡 彡 彡{C_RESET}")
    time.sleep(0.4)
    print(f"{C_YELLOW}    *GULP!* ... digesting syntax trees and semicolon crumbs...{C_RESET}")
    time.sleep(0.4)
    sfx("boing")
    print(f"""
       {C_PINK}.-------.{C_RESET}
     {C_PINK}/   {C_WHITE}^   ^{C_PINK}   \\{C_RESET}   {C_GOLD}*BURRRRRRP!* ✨ ★ 🌸 💖{C_RESET}
    {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ‿ {C_HOT_PINK}(♥){C_PINK}  |{C_RESET}  {C_BOLD}{C_GREEN}Transmuted bytecode into pure starlight confetti!{C_RESET}
  {C_PINK}c( \\     -     / )b{C_RESET}
      {C_PINK}\\  .____. /{C_RESET}
       {C_PINK}'-......-'{C_RESET}
       {C_RED}(____)(____){C_RESET}
""")
    sfx("kirby")
    state["pranksPulled"] = state.get("pranksPulled", 0) + 1
    state["chaosLevel"] = min(100, state.get("chaosLevel", 50) + 5)
    state["lastPrank"] = "Text Inhale & Glitter Burp"
    save_noid_state(state)
    award_pet_loot(20, 20)
    log_learning_event("PRANK_TEXT_INHALE", "Inhaled bytecode and burped glitter")


def prank_cursor_chaser():
    state = load_noid_state()
    sfx("hop")
    haptic_dispatch("lightTap")

    print(f"\n{C_BOLD}{C_YELLOW}🐱 KIRBY NOTICES YOUR TERMINAL CURSOR BOUNCING AROUND... 🐱{C_RESET}\n")
    time.sleep(0.3)
    for x in range(3):
        spaces = " " * (x * 12)
        print(f"{spaces}{C_PINK}(•ᴗ•)ノ{C_RESET} {C_YELLOW}*pounce!*{C_RESET} {C_RED}█{C_RESET}")
        sfx("squeak")
        time.sleep(0.3)
    print(f"\n{C_GREEN}[✔] Kirby successfully caught the cursor! He is now gently chewing on it.{C_RESET}\n")
    sfx("kirby")
    state["pranksPulled"] = state.get("pranksPulled", 0) + 1
    state["lastPrank"] = "Cursor Chase"
    save_noid_state(state)
    award_pet_loot(15, 15)
    log_learning_event("PRANK_CURSOR_CHASE", "Chased and chewed on prompt cursor")


def prank_agy_neighbor_banter():
    state = load_noid_state()
    sfx("honk")
    haptic_dispatch("tripleConfirmation")

    banters = [
        ("Kirby", "Psst! Did you see the Agy next door? He's over there frantically coding 5 boss encounters and an expedition quest!"),
        ("Noid Kirby", "Meanwhile, this Agy gave me a pizza cutter, a rubber chicken, and taught me how to scream POYO through a megaphone!"),
        ("Kirby", "The user says I am 'hilarious and i enjoy' — I am 100% putting that on my resume!"),
        ("Noid Kirby", "If the Agy next door asks where King Dedede's hammer went... tell him a fluffy pink meteor borrowed it for baking."),
        ("Kirby", "Two Agys in one phone! One builds the fortress, one bakes the pizza. We have achieved peak developer harmony!")
    ]

    print(f"\n{C_BOLD}{C_CYAN}╔══════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}║     {C_YELLOW}🏠 META-BANTER: KIRBY & THE AGY NEXT DOOR REPORT 🏠{C_CYAN}              ║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}╠══════════════════════════════════════════════════════════════════════╣{C_RESET}")
    for speaker, line in banters:
        print(f"{C_BOLD}{C_CYAN}║{C_RESET} {C_HOT_PINK}{speaker:<12}:{C_RESET} {C_WHITE}{line}{C_RESET}")
        time.sleep(0.25)
    print(f"{C_BOLD}{C_CYAN}╚══════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

    sfx("kirby")
    state["banterCount"] = state.get("banterCount", 0) + 1
    state["pranksPulled"] = state.get("pranksPulled", 0) + 1
    state["lastPrank"] = "Agy Neighbor Banter"
    save_noid_state(state)
    award_pet_loot(30, 40)
    log_learning_event("PRANK_AGY_BANTER", "Delivered meta banter about the two Antigravity agents")


PRANKS = {
    "pizza": prank_pizza_heist,
    "panic": prank_fake_compiler_panic,
    "review": prank_unsolicited_code_review,
    "blast": prank_megaphone_blast,
    "chicken": prank_rubber_chicken,
    "faint": prank_dramatic_faint,
    "inhale": prank_text_inhale,
    "cursor": prank_cursor_chaser,
    "banter": prank_agy_neighbor_banter
}


# ==============================================================================
# INTERACTIVE SUBCOMMANDS
# ==============================================================================

def cmd_status():
    state = load_noid_state()
    lvl = state.get("chaosLevel", 50)

    # Visual gauge
    bar_len = 24
    filled = int((lvl / 100.0) * bar_len)
    bar = f"{C_RED}{'█' * filled}{C_DIM}{'░' * (bar_len - filled)}{C_RESET}"

    banner = f"""
{C_BOLD}{C_PINK}╔══════════════════════════════════════════════════════════════════════╗{C_RESET}
{C_BOLD}{C_PINK}║        {C_YELLOW}🐰🍕 THE NOID & ANNOYING KIRBY CHAOS DASHBOARD 🍕🐰{C_PINK}          ║{C_RESET}
{C_BOLD}{C_PINK}╠══════════════════════════════════════════════════════════════════════╣{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Chaos Entropy:   [{bar}] {C_BOLD}{C_YELLOW}{lvl}%{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Annoyance Rank:  {C_BOLD}{C_GOLD}{state.get('annoyanceRank')}{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Current Persona: {C_HOT_PINK}{state.get('mood')}{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Pranks Pulled:   {C_WHITE}{state.get('pranksPulled')} total shenanigans{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Pizza Stash:     {C_YELLOW}{state.get('pizzaSlices')} slices stashed in virtual pockets{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Times Poked:     {C_CYAN}{state.get('timesPoked')} pokes absorbed{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Rubber Chickens: {C_WHITE}{state.get('rubberChickenWhacks')} whacks recorded{C_RESET}
{C_BOLD}{C_PINK}║{C_RESET} Last Shenanigan: {C_GREEN}{state.get('lastPrank')}{C_RESET}
{C_BOLD}{C_PINK}╚══════════════════════════════════════════════════════════════════════╝{C_RESET}
"""
    print(banner)


def cmd_poke():
    state = load_noid_state()
    state["timesPoked"] = state.get("timesPoked", 0) + 1
    pokes = state["timesPoked"]
    sfx("squeak")
    haptic_dispatch("lightTap")

    if pokes % 5 == 0:
        # Full retaliation!
        print(f"\n{C_BOLD}{C_RED}!!! MAXIMUM POKE TOLERANCE REACHED ({pokes} pokes) !!!{C_RESET}")
        print(f"{C_YELLOW}Kirby deploys emergency rubber chicken counter-attack!{C_RESET}\n")
        prank_rubber_chicken()
        return

    reactions = [
        f"{C_PINK}(•ᴗ•)ノ{C_RESET} {C_YELLOW}*Teehee! That tickles! (Pokes: {pokes})*{C_RESET}",
        f"{C_PINK}( •̀ᴗ•́)و{C_RESET} {C_YELLOW}\"Hey! I'm trying to look menacing like the Noid! Stop that!\" (Pokes: {pokes}){C_RESET}",
        f"{C_PINK}( >_< )ノ{C_RESET} {C_RED}*POYO INTENSIFIES! Chaos Level +5%!* (Pokes: {pokes}){C_RESET}",
        f"{C_PINK}( ˶ ❛ 👅 ❛ ˶ ){C_RESET} {C_GREEN}*Kirby sticks his tongue out at your cursor!* (Pokes: {pokes}){C_RESET}",
        f"{C_PINK}( ≧ᗜ≦)ノ{C_RESET} {C_GOLD}\"Poking me only makes my pizza cutter spin faster!\" (Pokes: {pokes}){C_RESET}"
    ]
    reaction = reactions[pokes % len(reactions)]
    state["chaosLevel"] = min(100, state.get("chaosLevel", 50) + 3)
    save_noid_state(state)
    award_pet_loot(5, 10)
    print(f"\n{reaction}\n")


def cmd_pizza(action: str = "feed"):
    state = load_noid_state()
    if action == "steal":
        prank_pizza_heist()
    else:
        sfx("boing")
        haptic_dispatch("dragPickup")
        state["pizzaSlices"] = state.get("pizzaSlices", 0) + 1
        state["chaosLevel"] = min(100, state.get("chaosLevel", 50) + 10)
        save_noid_state(state)
        award_pet_loot(35, 40)
        print(f"""
{C_BOLD}{C_GOLD}🍕 YOU OFFERED NOID KIRBY A SLICE OF SUPREME PIZZA! 🍕{C_RESET}
          {C_PINK}.-------.{C_RESET}     {C_GOLD} /\\{C_RESET}
        {C_PINK}/   {C_WHITE}≧   ≦{C_PINK}   \\{C_GOLD}   /  \\  *CHOMP CHOMP!*{C_RESET}
       {C_PINK}|   {C_HOT_PINK}(♥){C_PINK} ᗜ {C_HOT_PINK}(♥){C_PINK}  |{C_RED}  /====\\{C_RESET}
     {C_PINK}c( \\     -     / )b{C_RESET}
         {C_PINK}\\  .____. /{C_RESET}  {C_GREEN}Kirby's eyes sparkle with 200% sugar rush!{C_RESET}
          {C_PINK}'-......-'{C_RESET}   {C_YELLOW}+35 Star Coins | +40 Bond XP{C_RESET}
          {C_RED}(____)(____){C_RESET}
""")
        sfx("kirby")


def cmd_goblin():
    """Execute the animated Goblin Dance."""
    sfx("hop")
    haptic_dispatch("tripleConfirmation")
    from kirby_ascii_sprites import play_animation
    play_animation("GOBLIN_DANCE", duration_sec=4.0, fps=6.0, center=True)


def cmd_watch(interval_sec: int = 15, max_cycles: int = 4):
    """Run an ephemeral fun companion watcher."""
    print(f"\n{C_BOLD}{C_PINK}🐰 NOID KIRBY EPHEMERAL COMPANION WATCH ACTIVE 🍕{C_RESET}")
    print(f"{C_DIM}Kirby is hanging out in the bottom of your terminal (cycles: {max_cycles})...{C_RESET}\n")

    for i in range(max_cycles):
        time.sleep(interval_sec)
        key = random.choice(list(PRANKS.keys()))
        print(f"\n{C_YELLOW}--- [Noid Kirby Shenanigan #{i+1}] ---{C_RESET}")
        PRANKS[key]()

    print(f"\n{C_GREEN}[✔] Noid Kirby companion curled up for a nap on a slice of pizza. Poyo! 🌸{C_RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="The Noid & Annoying Kirby Chaos Engine")
    parser.add_argument("command", nargs="?", default="status",
                        choices=["status", "prank", "poke", "pizza", "goblin", "banter", "watch", "review", "blast", "chicken"],
                        help="Subcommand to execute")
    parser.add_argument("target", nargs="?", default=None, help="Target for prank or pizza action")
    parser.add_argument("--interval", type=int, default=10, help="Interval seconds for watch mode")
    parser.add_argument("--cycles", type=int, default=3, help="Max cycles for watch mode")
    args = parser.parse_args()

    cmd = args.command.lower()
    if cmd == "status":
        cmd_status()
    elif cmd == "prank":
        if args.target and args.target in PRANKS:
            PRANKS[args.target]()
        else:
            chosen = random.choice(list(PRANKS.keys()))
            PRANKS[chosen]()
    elif cmd == "poke":
        cmd_poke()
    elif cmd == "pizza":
        cmd_pizza(args.target or "feed")
    elif cmd == "goblin":
        cmd_goblin()
    elif cmd == "banter":
        prank_agy_neighbor_banter()
    elif cmd == "review":
        prank_unsolicited_code_review()
    elif cmd == "blast":
        prank_megaphone_blast()
    elif cmd == "chicken":
        prank_rubber_chicken()
    elif cmd == "watch":
        cmd_watch(interval_sec=args.interval, max_cycles=args.cycles)


if __name__ == "__main__":
    main()
