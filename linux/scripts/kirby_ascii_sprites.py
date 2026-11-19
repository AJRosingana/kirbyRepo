#!/usr/bin/env python3
"""
===============================================================================
★ AntiGravity Mesh — Kirby ANSI ASCII Sprite & Terminal Animator ★
===============================================================================
A high-fidelity, expressive ANSI character art, multi-frame sprite sheet,
and smooth terminal animation library featuring classic and specialized
Kirby variants.

Supported Sprites:
  1. IDLE_BOUNCE     (3 frames) - Dream Land rhythmic bounce & squash-and-stretch
  2. WARP_STAR_DASH   (4 frames) - Hyperspace cosmic star-surfing with speed trails
  3. HOVER_FLOAT     (4 frames) - Ballooned puff floating with flapping hands
  4. INHALE_VORTEX   (4 frames) - Cosmic suction vortex pulling matter & stars
  5. SNOOZE_CATNAP   (3 frames) - Starry nightcap nap with ascending Zzz bubbles
  6. EASEL_PAINTER   (3 frames) - Beret artist with palette creating a portrait
  7. ACE_BRAWLER     (3 frames) - Fighting headband Kirby firing hyper laser
  8. MAGICIAN        (3 frames) - Star wand magician conjuring cards & miracles

CLI Usage:
  python3 kirby_ascii_sprites.py [sprite_name|demo|all] [options]

Examples:
  python3 kirby_ascii_sprites.py demo
  python3 kirby_ascii_sprites.py idle_bounce
  python3 kirby_ascii_sprites.py warp_star_dash --duration 5 --fps 8
  python3 kirby_ascii_sprites.py all --fps 6
  python3 kirby_ascii_sprites.py --list
  python3 kirby_ascii_sprites.py --static
===============================================================================
"""

import sys
import os
import time
import re
import argparse
import shutil
from typing import Dict, List, Optional, Tuple

# =============================================================================
# ANSI COLOR ENGINE & CONSTANTS
# =============================================================================

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"

# Kirby Body & Blush
PINK = "\033[38;5;218m"       # Soft pastel Kirby pink
HOT_PINK = "\033[38;5;205m"   # Rosy blush cheeks & vibrant accents
ROSE = "\033[38;5;212m"       # Kirby contour shadow
RED = "\033[38;5;196m"        # Ruby red shoes, headband, hearts
DARK_RED = "\033[38;5;160m"   # Shaded red

# Cosmic & Elemental Palettes
GOLD = "\033[38;5;220m"       # Warp star gold & wand stars
YELLOW = "\033[38;5;226m"     # Radiant sparkles, notes, stars
CYAN = "\033[38;5;51m"        # Suction vortex, speed trails, laser beam
SKY_BLUE = "\033[38;5;117m"   # Floating bubbles, breath, sleep vapor
BLUE = "\033[38;5;75m"        # Eyes & beret shadow
DEEP_BLUE = "\033[38;5;33m"   # Nightcap base
PURPLE = "\033[38;5;141m"     # Magician hat & nightcap trim
MAGENTA = "\033[38;5;201m"    # Laser burst flare & magic sparks
GREEN = "\033[38;5;120m"      # Paint palette green
ORANGE = "\033[38;5;208m"     # Boxing gloves & palette orange
BROWN = "\033[38;5;130m"      # Wooden easel
WHITE = "\033[1;37m"          # Bright highlights & core stars
GRAY = "\033[38;5;245m"       # Subtle shading & dust
DARK_GRAY = "\033[38;5;238m"  # Ground shadows

# Regex to strip ANSI escape codes for width/height measurements
ANSI_ESCAPE_RE = re.compile(r'\033\[[0-9;]*[a-zA-Z]')

def strip_ansi(text: str) -> str:
    """Strip ANSI escape sequences from text to get printable length."""
    return ANSI_ESCAPE_RE.sub('', text)

def visible_length(text: str) -> int:
    """Return visual length of a string without ANSI sequences."""
    return len(strip_ansi(text))

# =============================================================================
# SPRITE DEFINITIONS
# =============================================================================

# -----------------------------------------------------------------------------
# 1. IDLE_BOUNCE (3 Frames)
# -----------------------------------------------------------------------------
# Frame 0: Standing upright, cute bob with musical note overhead.
# Frame 1: Squish down, cheeks puffed, anticipation squash.
# Frame 2: Joyful leap, arms stretched high, sparkling star overhead, shadow below.

IDLE_BOUNCE_FRAMES: List[str] = [
    # Frame 0: Upright Neutral Bob
    "\n".join([
        f"             {YELLOW}(♪){RESET}",
        f"          {PINK}.-------.{RESET}",
        rf"        {PINK}/   {WHITE}●   ●{PINK}   \\{RESET}",
        f"       {PINK}|   {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK} |{RESET}",
        rf"     {PINK}c( \\\\     -     / ){RESET}",
        rf"         {PINK}\\ .______. /{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"          {RED}(____)(____){RESET}",
        f"       {DARK_GRAY}~~~~~~~~~~~~~~~~~{RESET}",
        f" ",
    ]),
    # Frame 1: Squash & Squeeze Down
    "\n".join([
        f" ",
        f" ",
        f"          {PINK}.---------.{RESET}",
        rf"        {PINK}/   {WHITE}>     <{PINK}   \\{RESET}",
        f"      {PINK}(|   {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}   |){RESET}",
        rf"       {PINK}\\     .____.    /{RESET}",
        f"        {PINK}'-..________..-'{RESET}",
        f"         {RED}(_____) (_____){RESET}",
        f"       {DARK_GRAY}~~~~~~~~~~~~~~~~~{RESET}",
        f" ",
    ]),
    # Frame 2: Airborne Stretch Leap!
    "\n".join([
        rf"           {WHITE}\\{RESET}  {YELLOW}(★){RESET}  {WHITE}/{RESET}",
        f"          {PINK}.-------.{RESET}",
        rf"        {PINK}/   {WHITE}^   ^{PINK}   \\{RESET}",
        rf"      {PINK}\\|   {HOT_PINK}(♥){PINK} ▽ {HOT_PINK}(♥){PINK} |/{RESET}",
        rf"        {PINK}\\     -     /{RESET}",
        rf"         {PINK}\\ .______. /{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"           {RED}( ){PINK}  {RED}( ){RESET}",
        f" ",
        f"         {DARK_GRAY}( . - - . ){RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 2. WARP_STAR_DASH (4 Frames)
# -----------------------------------------------------------------------------
# Frame 0: Surfing Warp Star, wind blowing, cosmic cruise.
# Frame 1: Star engine flares, sonic acceleration.
# Frame 2: Max warp velocity, warp stream sonic boom, arms raised cheering!
# Frame 3: Cosmic drift banked turn with trailing stardust.

WARP_STAR_DASH_FRAMES: List[str] = [
    # Frame 0: Warp Cruise
    "\n".join([
        f" ",
        f"                        {PINK}.-----.{RESET}",
        rf"                       {PINK}/  {WHITE}^ ^{PINK}  \\{RESET}",
        rf"                {PINK}\\O    |  {HOT_PINK}(♥){PINK}‿{HOT_PINK}(♥){PINK}|{RESET}",
        rf"          {YELLOW}*       {PINK}\\__ |   ---   |{RESET}",
        rf"        {WHITE}. + .        {PINK}\\ '-------'{RESET}",
        rf"   {CYAN}. - *     \\     {RED}.-'  ( ) ( ){RESET}",
        f"  {CYAN}===       {GOLD}.-'---'            '-.{RESET}",
        f"   {CYAN}=====  {GOLD}<     {YELLOW}★   WARP STAR     {GOLD}>=====>{RESET}",
        f"           {GOLD}'-.________________.-'{RESET}",
    ]),
    # Frame 1: Thrusters Igniting
    "\n".join([
        f" ",
        f"                           {PINK}.-----.{RESET}",
        rf"                          {PINK}/  {WHITE}> <{PINK}  \\{RESET}",
        rf"                    {PINK}\\O   |  {HOT_PINK}(♥){PINK}o{HOT_PINK}(♥){PINK}|{RESET}",
        rf"        {YELLOW}*   {WHITE}✧         {PINK}\\__|   ---   |{RESET}",
        rf"      {WHITE}.   +              {PINK}\\ '-------'{RESET}",
        f"   {CYAN}======   {YELLOW}*          {RED}.-'  ( ) ( ){RESET}",
        f"  {CYAN}=======   {WHITE}. - .  {GOLD}.--'            '-.{RESET}",
        f"   {CYAN}============  {GOLD}<      {YELLOW}★  HYPER     {GOLD}>======>{RESET}",
        f"                   {GOLD}'-.____________.-'{RESET}",
    ]),
    # Frame 2: Hyperspace Warp Speed Sonic Boom
    "\n".join([
        rf"                            {WHITE}\\{RESET} {YELLOW}(★){RESET} {WHITE}/{RESET}",
        f"                            {PINK}.-----.{RESET}",
        rf"                           {PINK}/  {WHITE}^ ^{PINK}  \\{RESET}",
        f"                          {PINK}|  {HOT_PINK}(♥){PINK}▽{HOT_PINK}(♥){PINK}|{RESET}",
        rf"      {CYAN}✧    {YELLOW}*          {PINK}c(   \\ .---. /  )o{RESET}",
        f"   {CYAN}=======    {WHITE}✦            {RED}( )   ( ){RESET}",
        f"  {CYAN}=============        {GOLD}_.-'         '-._{RESET}",
        f"   {CYAN}=================={GOLD}<    {YELLOW}★  WARP SPEED {GOLD}>========>{RESET}",
        f"                       {GOLD}'-.___________.-'{RESET}",
        f" ",
    ]),
    # Frame 3: Cosmic Drift & Barrel Roll
    "\n".join([
        f"                             {CYAN}(✧){RESET}",
        f"                            {PINK}.-----.{RESET}",
        rf"                           {PINK}/  {WHITE}^ -{PINK}  \\{RESET}",
        f"                     {PINK}(v)  |  {HOT_PINK}(♥){PINK}‿{HOT_PINK}(♥){PINK}|{RESET}",
        rf"        {YELLOW}*       {WHITE}*      {PINK}\\__|   ---   |{RESET}",
        rf"      {WHITE}+    ✦              {PINK}\\ '-------'{RESET}",
        f"   {CYAN}=======              {RED}.-'  ( ) ( ){RESET}",
        f"  {CYAN}========         {GOLD}_.-'             '-._{RESET}",
        f"   {CYAN}============= {GOLD}<   {YELLOW}★  COSMIC DASH   {GOLD}>======>{RESET}",
        f"                   {GOLD}'-._______________.-'{RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 3. HOVER_FLOAT (4 Frames)
# -----------------------------------------------------------------------------
# Frame 0: Kirby inhaled deep breath, chubby balloon body resting low.
# Frame 1: Flapping stubby arms downward, lifting body upward.
# Frame 2: Floating at peak height, arms spread wide, puffing air bubbles.
# Frame 3: Arms flapping back upward, gliding gently downward.

HOVER_FLOAT_FRAMES: List[str] = [
    # Frame 0: Puffed Balloon Low
    "\n".join([
        f" ",
        f" ",
        f"              {PINK}.-------.{RESET}",
        f"           {PINK}.-'         '-.{RESET}",
        rf"          {PINK}/   {WHITE}●       ●{PINK}   \\{RESET}",
        f"        {PINK}<|   {HOT_PINK}(♥){PINK}  (o)  {HOT_PINK}(♥){PINK}   |>{RESET}",
        f"         {PINK}|                 |{RESET}",
        rf"          {PINK}\\   ._______..  /{RESET}",
        f"           {PINK}'-.________..-'{RESET}",
        f"            {RED}(____) (____){RESET}",
        f"             {SKY_BLUE}~   ~   ~   ~{RESET}",
    ]),
    # Frame 1: Flap Down! Rising Upward
    "\n".join([
        f" ",
        f"              {PINK}.-------.{RESET}",
        f"           {PINK}.-'         '-.{RESET}",
        rf"          {PINK}/   {WHITE}^       ^{PINK}   \\{RESET}",
        f"         {PINK}|   {HOT_PINK}(♥){PINK}  (o)  {HOT_PINK}(♥){PINK}   |{RESET}",
        rf"        {PINK}/ \\                 / \\{RESET}",
        f"       {PINK}(___)  ._______..   (___){RESET}",
        f"           {PINK}'-.________..-'{RESET}",
        f"            {RED}(____) (____){RESET}",
        f" ",
        f"             {SKY_BLUE}~   ~   ~   ~{RESET}",
    ]),
    # Frame 2: Apex Float & Bubble Exhale
    "\n".join([
        f"              {PINK}.-------.{RESET}",
        f"           {PINK}.-'   {SKY_BLUE}~~~{PINK}   '-.      {SKY_BLUE}o{RESET}",
        rf"          {PINK}/   {WHITE}●       ●{PINK}   \\    {SKY_BLUE}o .{RESET}",
        f"        {PINK}--|  {HOT_PINK}(♥){PINK}  (o)  {HOT_PINK}(♥){PINK}  |-- {SKY_BLUE}O{RESET}",
        f"          {PINK}|                 |{RESET}",
        rf"           {PINK}\\   ._______..  /{RESET}",
        f"            {PINK}'-.________..-'{RESET}",
        f"             {RED}( )     ( ){RESET}",
        f" ",
        f" ",
        f"             {SKY_BLUE}~   ~   ~   ~{RESET}",
    ]),
    # Frame 3: Flap Up! Floating Down
    "\n".join([
        f" ",
        rf"        {PINK}\\ /   .-------.   \\ /{RESET}",
        f"        {PINK}( )-'         '-( ){RESET}",
        rf"          {PINK}/   {WHITE}^       ^{PINK}   \\{RESET}",
        f"         {PINK}|   {HOT_PINK}(♥){PINK}  (o)  {HOT_PINK}(♥){PINK}   |{RESET}",
        f"         {PINK}|                 |{RESET}",
        rf"          {PINK}\\   ._______..  /{RESET}",
        f"           {PINK}'-.________..-'{RESET}",
        f"            {RED}(____) (____){RESET}",
        f"             {SKY_BLUE}~   ~   ~   ~{RESET}",
        f" ",
    ]),
]

# -----------------------------------------------------------------------------
# 4. INHALE_VORTEX (4 Frames)
# -----------------------------------------------------------------------------
# Frame 0: Mouth opening, wind currents swirl toward mouth.
# Frame 1: Gaping mouth, vortex accelerates, particles swirling inwards.
# Frame 2: Maximum suction vortex! Funnel of cosmic stars, wind, and debris sucked in!
# Frame 3: Mouth snaps shut, cheeks chubby and full, particle dissipating.

INHALE_VORTEX_FRAMES: List[str] = [
    # Frame 0: Opening Inhale Maw
    "\n".join([
        f" ",
        f"          {PINK}.-----.{RESET}",
        rf"        {PINK}/  {WHITE}ò   ó{PINK}  \\                 {WHITE}.{RESET}",
        rf"      {PINK}(|  {HOT_PINK}(♥){PINK} {HOT_PINK}(♥){PINK}  \\        {CYAN}~ ~ ≪ ≪       {YELLOW}*{RESET}",
        f"      {PINK}(|      ( {DARK_RED}O{PINK} ) |    {CYAN}~ ~ ≪ ≪ ≪ ≪    {WHITE}.{RESET}",
        rf"       {PINK}\\     .____./      {CYAN}~ ≪ ≪ ≪{RESET}",
        f"        {PINK}'-.____.-'          {CYAN}~ ~{RESET}",
        f"        {RED}(____)(____){RESET}",
        f"      {DARK_GRAY}~~~~~~~~~~~~~~~~{RESET}",
        f" ",
    ]),
    # Frame 1: Suction Cyclone Builds
    "\n".join([
        f"          {PINK}.-----.             {YELLOW}*{RESET}",
        rf"        {PINK}/  {WHITE}Ò   Ó{PINK}  \\        {CYAN}~ ~ ≪ ≪ ≪ {WHITE}✦{RESET}",
        rf"      {PINK}(|  {HOT_PINK}(♥){PINK}      \\     {CYAN}~ ≪ ≪ ≪ ≪ ≪ ≪ ≪   {WHITE}.{RESET}",
        rf"      {PINK}(|    /  {DARK_RED}( ){PINK}  \\   {CYAN}~ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪    {YELLOW}*{RESET}",
        rf"       {PINK}\\   |   {DARK_RED}(_){PINK}   |    {CYAN}~ ≪ ≪ ≪ ≪ ≪ ≪ ≪  {WHITE}.{RESET}",
        rf"        {PINK}\\   \\       /      {CYAN}~ ~ ≪ ≪ ≪ ≪ {WHITE}✦{RESET}",
        f"         {PINK}'-.____.-'             {CYAN}~ ~ ≪ ≪{RESET}",
        f"         {RED}(____)(____){RESET}",
        f"      {DARK_GRAY}~~~~~~~~~~~~~~~~{RESET}",
        f" ",
    ]),
    # Frame 2: MAXIMUM HYPER VORTEX!
    "\n".join([
        f"          {PINK}.-----.           {WHITE}.   {YELLOW}*    {WHITE}✦    {CYAN}.   {YELLOW}*{RESET}",
        rf"        {PINK}/  {WHITE}>   <{PINK}  \\       {CYAN}~ ~ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ {YELLOW}★{RESET}",
        rf"      {PINK}(|  {HOT_PINK}(♥){PINK}      \\    {CYAN}~ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪{RESET}",
        rf"      {PINK}(|    /  {DARK_RED}( ){PINK}  \\  {CYAN}~ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ {WHITE}✧{RESET}",
        rf"       {PINK}\\   |   {DARK_RED}(_){PINK}   |  {CYAN}~ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪{RESET}",
        rf"        {PINK}\\   \\       /    {CYAN}~ ~ ≪ ≪ ≪ ≪ ≪ ≪ ≪ ≪ {YELLOW}★{RESET}",
        f"         {PINK}'-.____.-'         {CYAN}~ ~ ≪ ≪ ≪ ≪ {WHITE}✦  {CYAN}.{RESET}",
        f"         {RED}(____)(____){RESET}",
        f"      {DARK_GRAY}~~~~~~~~~~~~~~~~{RESET}",
        f" ",
    ]),
    # Frame 3: Swallowed & Satisfied
    "\n".join([
        f" ",
        f"           {PINK}.-------.{RESET}",
        rf"         {PINK}/   {WHITE}>   <{PINK}   \\           {CYAN}.{RESET}",
        f"       {PINK}(|   {HOT_PINK}(♥){PINK} {HOT_PINK}(♥){PINK}   |)       {YELLOW}*   {WHITE}.{RESET}",
        f"       {PINK}(|     ( {DARK_RED}O{PINK} )   |)     {CYAN}~ ~ ≪   {YELLOW}*{RESET}",
        rf"        {PINK}\\    ._____.  /        {CYAN}~{RESET}",
        f"         {PINK}'-._______.-'{RESET}",
        f"         {RED}(____) (____){RESET}",
        f"      {DARK_GRAY}~~~~~~~~~~~~~~~~{RESET}",
        f" ",
    ]),
]

# -----------------------------------------------------------------------------
# 5. SNOOZE_CATNAP (3 Frames)
# -----------------------------------------------------------------------------
# Frame 0: Sleeping peacefully in starry nightcap, small 'z' drifting up.
# Frame 1: Deep sleep, snot bubble 'o' expands, 'Z' rises higher.
# Frame 2: Huge blissful smile, big sleep bubble 'O', multiple 'Z's in the sky.

SNOOZE_CATNAP_FRAMES: List[str] = [
    # Frame 0: Cozy Catnap
    "\n".join([
        f" ",
        f" ",
        rf"            {PURPLE}/\\\____{RESET}",
        rf"           {PURPLE}/  __  \\__ {YELLOW}(★){RESET}",
        rf"          {PURPLE}/  /  \\\____){RESET}          {CYAN}z{RESET}",
        f"         {PINK}.-----.{RESET}               {CYAN}z{RESET}",
        rf"       {PINK}/  {WHITE}˘   ˘{PINK}  \\{RESET}",
        f"      {PINK}|  {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}|{RESET}",
        f"     {PINK}(|     -     |){RESET}",
        rf"     {PINK}\\   .____.  /{RESET}",
        f"      {PINK}'-.____.-'    {RED}(____)(____){RESET}",
        f"     {SKY_BLUE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
    # Frame 1: Dream Bubble Forming
    "\n".join([
        f" ",
        f"                                 {CYAN}Z{RESET}",
        rf"            {PURPLE}/\\\____{RESET}              {CYAN}z{RESET}",
        rf"           {PURPLE}/  __  \\__ {YELLOW}(★){RESET}      {SKY_BLUE}.{RESET}",
        rf"          {PURPLE}/  /  \\\____){RESET}        {SKY_BLUE}o{RESET}",
        f"         {PINK}.-----.{RESET}",
        rf"       {PINK}/  {WHITE}-   -{PINK}  \\{RESET}",
        f"      {PINK}|  {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}|{RESET}",
        f"     {PINK}(|     ~     |){RESET}",
        rf"     {PINK}\\   .____.  /{RESET}",
        f"      {PINK}'-.____.-'    {RED}(____)(____){RESET}",
        f"     {SKY_BLUE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
    # Frame 2: Deep Cosmic Snooze
    "\n".join([
        f"                                 {CYAN}Z{RESET}",
        f"                                {CYAN}Z{RESET}",
        rf"            {PURPLE}/\\\____{RESET}             {CYAN}z{RESET}",
        rf"           {PURPLE}/  __  \\__ {YELLOW}(★){RESET}     {SKY_BLUE}O{RESET}",
        rf"          {PURPLE}/  /  \\\____){RESET}       {SKY_BLUE}.{RESET}",
        f"         {PINK}.-----.{RESET}",
        rf"       {PINK}/  {WHITE}˘   ˘{PINK}  \\{RESET}",
        f"      {PINK}|  {HOT_PINK}(♥){PINK} ▿ {HOT_PINK}(♥){PINK}|{RESET}",
        f"     {PINK}(|     -     |){RESET}",
        rf"     {PINK}\\   .____.  /{RESET}",
        f"      {PINK}'-.____.-'    {RED}(____)(____){RESET}",
        f"     {SKY_BLUE}~~~~~~~~~~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 6. EASEL_PAINTER (3 Frames)
# -----------------------------------------------------------------------------
# Frame 0: Beret Kirby holding paint palette, dipping brush, looking at easel.
# Frame 1: Kirby swoops brush across canvas with colorful paint stroke!
# Frame 2: Ta-da! Kirby unveils masterpiece: a painted portrait of Kirby!

EASEL_PAINTER_FRAMES: List[str] = [
    # Frame 0: Contemplating the Canvas
    "\n".join([
        f" ",
        rf"          {BLUE}.__/\\__.{RESET}",
        f"         {BLUE}(  BERET )'{RESET}",
        f"          {BLUE}'--. .-'            {BROWN}.---------.{RESET}",
        rf"           {PINK}/ {WHITE}◕   ◕{PINK} \\          {BROWN}|  {WHITE}.---.{BROWN}  |{RESET}",
        f"          {PINK}| {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}|        {BROWN}|  {WHITE}|   |{BROWN}  |{RESET}",
        f"     {WHITE}[{RED}●{GREEN}●{YELLOW}●{WHITE}] {PINK}|    ---   |/{BROWN}---{WHITE}🖌  {BROWN}|  {WHITE}| {YELLOW}★{WHITE} |{BROWN}  |{RESET}",
        rf"    {WHITE}({CYAN}• {ORANGE}•{WHITE})  {PINK}\\\  .____. /        {BROWN}|  {WHITE}'---'{BROWN}  |{RESET}",
        f"     {WHITE}'---'  {PINK}'-.____.-'        {BROWN}'----+----'{RESET}",
        f"           {RED}(____)(____)            {BROWN}|{RESET}",
        rf"      {DARK_GRAY}~~~~~~~~~~~~~~~~~~          {BROWN}/ \\{RESET}",
        f" ",
    ]),
    # Frame 1: Painting Dynamic Swatch
    "\n".join([
        f" ",
        rf"          {BLUE}.__/\\__.{RESET}",
        f"         {BLUE}(  BERET )'{RESET}",
        f"          {BLUE}'--. .-'            {BROWN}.---------.{RESET}",
        rf"           {PINK}/ {WHITE}^   -{PINK} \\          {BROWN}|  {WHITE}.---.{BROWN}  |{RESET}",
        f"          {PINK}| {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}|        {BROWN}|  {WHITE}| {YELLOW}★{WHITE} |{CYAN}~✦{BROWN}|{RESET}",
        rf"     {WHITE}[{RED}●{GREEN}●{YELLOW}●{WHITE}] {PINK}|    ---    \\{BROWN}---{WHITE}🖌{MAGENTA}==={BROWN}|  {WHITE}'---'{BROWN}  |{RESET}",
        rf"    {WHITE}({CYAN}• {ORANGE}•{WHITE})  {PINK}\\\  .____. /        {BROWN}| {MAGENTA}~~~~~~~ {BROWN}|{RESET}",
        f"     {WHITE}'---'  {PINK}'-.____.-'        {BROWN}'----+----'{RESET}",
        f"           {RED}(____)(____)            {BROWN}|{RESET}",
        rf"      {DARK_GRAY}~~~~~~~~~~~~~~~~~~          {BROWN}/ \\{RESET}",
        f" ",
    ]),
    # Frame 2: Masterpiece Kirby Portrait!
    "\n".join([
        f" ",
        rf"          {BLUE}.__/\\__.{RESET}",
        f"         {BLUE}(  BERET )'{RESET}",
        f"          {BLUE}'--. .-'            {BROWN}.---------.{RESET}",
        rf"         {PINK}\\ / {WHITE}^   ^{PINK} \\ /        {BROWN}|  {PINK}\\ O /  {BROWN}|{RESET}",
        f"     {WHITE}🖌{BROWN}---{PINK}| {HOT_PINK}(♥){PINK} ▽ {HOT_PINK}(♥){PINK}|---{WHITE}[{RED}●{GREEN}●{YELLOW}●{WHITE}] {BROWN}| {PINK}( •‿• ) {BROWN}|{RESET}",
        f"          {PINK}|    ---   |        {BROWN}|  {RED}(___)♥ {BROWN}|{RESET}",
        rf"           {PINK}\\\  .____. /        {BROWN}| {YELLOW}*  {WHITE}✦  {YELLOW}* {BROWN}|{RESET}",
        f"            {PINK}'-.____.-'        {BROWN}'----+----'{RESET}",
        f"            {RED}(____)(____)           {BROWN}|{RESET}",
        rf"       {DARK_GRAY}~~~~~~~~~~~~~~~~~~         {BROWN}/ \\{RESET}",
        f" ",
    ]),
]

# -----------------------------------------------------------------------------
# 7. ACE_BRAWLER (3 Frames)
# -----------------------------------------------------------------------------
# Frame 0: Fighter stance, headband fluttering, boxing gloves up in guard.
# Frame 1: Ki charge up, gloves crackling with electricity, energy charging!
# Frame 2: Unleashes massive straight hyper laser cannon blast!

ACE_BRAWLER_FRAMES: List[str] = [
    # Frame 0: Warrior Stance
    "\n".join([
        f" ",
        f"          {RED}.=========.         {RESET}",
        f"     {RED}~ ~ [  FIGHTER  ]        {RESET}",
        rf"    {RED}~ ~   {PINK}/  {WHITE}ò   ó{PINK}  \\       {RESET}",
        f"        {PINK}(|  {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK} |)      {RESET}",
        f"     {ORANGE}[🥊]{PINK}|     -     |{ORANGE}[🥊]   {RESET}",
        rf"          {PINK}\\  .____.  /        {RESET}",
        f"           {PINK}'-.____.-'         {RESET}",
        f"           {RED}(____)(____)        {RESET}",
        f"       {DARK_GRAY}~~~~~~~~~~~~~~~~~      {RESET}",
        f" ",
    ]),
    # Frame 1: Charging Ki Energy
    "\n".join([
        f" ",
        f"          {RED}.=========.         {RESET}",
        f"    {RED}~~~  [  FIGHTER  ]        {YELLOW}*   {WHITE}✦   {YELLOW}*{RESET}",
        rf"   {RED}~~~    {PINK}/  {WHITE}Ò   Ó{PINK}  \\       {WHITE}✦  {ORANGE}[🥊]  {CYAN}✧{RESET}",
        rf"        {PINK}(|  {HOT_PINK}(♥){PINK} ᗜ {HOT_PINK}(♥){PINK} |)    {YELLOW}*  {YELLOW}/{WHITE}⚡{YELLOW}\\  *{RESET}",
        rf"         {PINK}\\     -     /{CYAN}======={ORANGE}'----'{RESET}",
        rf"          {PINK}\\\  .____. /      {YELLOW}⚡ {WHITE}CHARGING! {YELLOW}⚡{RESET}",
        f"           {PINK}'-.____.-'         {RESET}",
        f"           {RED}(____)(____)        {RESET}",
        f"       {DARK_GRAY}~~~~~~~~~~~~~~~~~      {RESET}",
        f" ",
    ]),
    # Frame 2: HYPER LASER CANNON BLAST!
    "\n".join([
        f"          {RED}.=========.         {RESET}",
        f"    {RED}~~~~ [  FIGHTER  ]        {RESET}",
        rf"   {RED}~~~~   {PINK}/  {WHITE}>   <{PINK}  \\      {ORANGE}[🥊][🥊]{CYAN}=================================>{RESET}",
        rf"        {PINK}(|  {HOT_PINK}(♥){PINK} ᗣ {HOT_PINK}(♥){PINK} |)====//{WHITE}  \\\\  {MAGENTA}<<< HYPER LASER CANNON >>>{CYAN}=======>",
        rf"         {PINK}\\     -     /    {CYAN}\\\\__{WHITE}//{CYAN}===================================>",
        rf"          {PINK}\\\  .____. /           {YELLOW}*   {CYAN}✧   {WHITE}✦   {YELLOW}*   {CYAN}✧   {WHITE}✦   {YELLOW}*{RESET}",
        f"           {PINK}'-.____.-'         {RESET}",
        f"           {RED}(____)(____)        {RESET}",
        f"       {DARK_GRAY}~~~~~~~~~~~~~~~~~      {RESET}",
        f" ",
        f" ",
    ]),
]

# -----------------------------------------------------------------------------
# 8. MAGICIAN (3 Frames)
# -----------------------------------------------------------------------------
# Frame 0: Magician Kirby holding star wand, bowing with purple top hat.
# Frame 1: Wand raised high, star tip flaring with arcane magic.
# Frame 2: Abracadabra! Magic cards, doves, and starlight burst into the air!

MAGICIAN_FRAMES: List[str] = [
    # Frame 0: The Magician's Bow
    "\n".join([
        f" ",
        f"             {PURPLE}.--------.{RESET}",
        rf"            {PURPLE}/   {YELLOW}★  {WHITE}✦   {PURPLE}\\{RESET}",
        f"           {PURPLE}|   {WHITE}MAGIC    {PURPLE}|{RESET}",
        f"          {GOLD}[==============]]{RESET}",
        rf"             {PINK}/  {WHITE}^   ^{PINK}  \\{RESET}",
        f"            {PINK}|  {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}|{RESET}",
        rf"        {PINK}c(   \\\   ---   /   ){GOLD}o---{YELLOW}☆ {WHITE}✧{RESET}",
        rf"              {PINK}\\\ .____. /{RESET}",
        f"              {PINK}'-.____.-'{RESET}",
        f"              {RED}(____)(____){RESET}",
        f"          {DARK_GRAY}~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
    # Frame 1: Incantation & Star Surge
    "\n".join([
        f"                       {YELLOW}(★) {WHITE}✦{RESET}",
        f"                      {GOLD}/{RESET}",
        f"             {PURPLE}.--------.{GOLD}----{YELLOW}☆ {WHITE}✧{RESET}",
        rf"            {PURPLE}/   {YELLOW}★  {WHITE}✦   {PURPLE}\\{RESET}",
        f"           {PURPLE}|   {WHITE}MAGIC    {PURPLE}|{RESET}",
        f"          {GOLD}[==============]]{RESET}",
        rf"             {PINK}/  {YELLOW}★   ★{PINK}  \\{RESET}",
        f"            {PINK}|  {HOT_PINK}(♥){PINK} ▿ {HOT_PINK}(♥){PINK}|{RESET}",
        rf"        {PINK}c(   \\\   ---   /   ){RESET}",
        rf"              {PINK}\\\ .____. /{RESET}",
        f"              {PINK}'-.____.-'{RESET}",
        f"              {RED}(____)(____){RESET}",
    ]),
    # Frame 2: Grand Arcane Explosion
    "\n".join([
        f"       {WHITE}✦    {CYAN}[♠]     {YELLOW}*     {GOLD}(★)     {WHITE}✦    {RED}[♥]    {YELLOW}*{RESET}",
        rf"         {GOLD}\\     {PURPLE}.--------.    {GOLD}/    {WHITE}✧{RESET}",
        rf"          {GOLD}\\   {PURPLE}/   {YELLOW}★  {WHITE}✦   {PURPLE}\\  {GOLD}/{RESET}",
        rf"           {GOLD}\\ {PURPLE}|   {WHITE}MAGIC    {PURPLE}|{GOLD}/{RESET}",
        f"           {GOLD}[==============]]{RESET}",
        rf"         {GOLD}\\    {PINK}/  {WHITE}^   -{PINK}  \\    {GOLD}/{RESET}",
        f"     {YELLOW}☆{GOLD}---{PINK}o(  |  {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}|  )o{GOLD}---{YELLOW}☆{RESET}",
        rf"              {PINK}\\\   ---   /{RESET}",
        rf"               {PINK}\\\ .____. /{RESET}",
        f"               {PINK}'-.____.-'{RESET}",
        f"               {RED}(____)(____){RESET}",
        f"           {DARK_GRAY}~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
]


# -----------------------------------------------------------------------------
# 9. SWORD_HERO (4 Frames)
# -----------------------------------------------------------------------------
SWORD_HERO_FRAMES: List[str] = [
    # Frame 0: Green Link Cap & Starlight Guard
    "\n".join([
        f"              {GREEN}.-----.{RESET}",
        rf"             {GREEN}/  HERO \\{RESET}",
        f"       {GREEN}___.-'         '--.{RESET}",
        rf"      {GREEN}\\____             /{RESET}",
        rf"            {PINK}/  {WHITE}•   •{PINK}  \      {CYAN}|\\{RESET}",
        f"           {PINK}|  {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}|     {CYAN}||{RESET}",
        rf"        {PINK}c(  \\\   ---   /  )o==={CYAN}[>========->{RESET}",
        rf"             {PINK}\\ .____. /       {CYAN}||{RESET}",
        f"             {PINK}'-.____.-'        {CYAN}|/{RESET}",
        f"             {RED}(____)(____){RESET}",
        f"         {DARK_GRAY}~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
    # Frame 1: Starlight Charged Blade
    "\n".join([
        f"                               {YELLOW}(★) {WHITE}✦{RESET}",
        rf"              {GREEN}.-----.{RESET}         {CYAN}/|\\{RESET}",
        rf"             {GREEN}/  HERO \\{RESET}        {CYAN}|||{RESET}",
        f"       {GREEN}___.-'         '--.{RESET}    {CYAN}|||{RESET}",
        rf"      {GREEN}\\____             /{RESET}    {CYAN}|||{RESET}",
        rf"            {PINK}/  {WHITE}ò   ó{PINK}  \   o==={CYAN}[>========->{RESET}",
        f"           {PINK}|  {HOT_PINK}(♥){PINK} ᗜ {HOT_PINK}(♥){PINK}|/     {YELLOW}*  {WHITE}CHARGE! {YELLOW}*{RESET}",
        rf"        {PINK}c(  \\\   ---   /      {CYAN}\\|/{RESET}",
        rf"             {PINK}\\ .____. /{RESET}",
        f"             {PINK}'-.____.-'{RESET}",
        f"             {RED}(____)(____){RESET}",
    ]),
    # Frame 2: Spinning 360 Starlight Cleave!
    "\n".join([
        f"       {CYAN}==={GOLD}* {WHITE}✦ {CYAN}==============================={GOLD}* {WHITE}✦ {CYAN}===>{RESET}",
        f"      {CYAN}===   {GREEN}.-----.{RESET}                      {CYAN}==={RESET}",
        rf"      {CYAN}===  {GREEN}/  HERO \\{RESET}   {YELLOW}*   {WHITE}✦   {YELLOW}*        {CYAN}==={RESET}",
        rf"      {CYAN}==  {GREEN}\\____     /{RESET}    {PINK}( > ▽ < ){RESET}       {CYAN}==={RESET}",
        f"      {CYAN}===  {PINK}( |{HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}| )o==={CYAN}[>=====SPIN SLASH====->{RESET}",
        rf"      {CYAN}===   {PINK}\\ .____. /{RESET}    {YELLOW}*   {WHITE}✦   {YELLOW}*        {CYAN}==={RESET}",
        f"      {CYAN}===    {PINK}'-.____.-'{RESET}                     {CYAN}==={RESET}",
        f"      {CYAN}===    {RED}(____)(____){RESET}                   {CYAN}==={RESET}",
        f"       {CYAN}==={GOLD}* {WHITE}✦ {CYAN}==============================={GOLD}* {WHITE}✦ {CYAN}===>{RESET}",
    ]),
    # Frame 3: Sheathing Blade with Wink & Sparkle
    "\n".join([
        f"              {GREEN}.-----.{RESET}",
        rf"             {GREEN}/  HERO \\{RESET}",
        f"       {GREEN}___.-'         '--.{RESET}    {YELLOW}★ {WHITE}✦{RESET}",
        rf"      {GREEN}\\____             /{RESET}    {YELLOW}*{RESET}",
        rf"            {PINK}/  {WHITE}^   ~{PINK}  \  {CYAN}|\\{RESET}",
        f"           {PINK}|  {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}| {CYAN}||{RESET}",
        rf"        {PINK}c(  \\\   ---   /  )o==={CYAN}[>====={RESET}",
        rf"             {PINK}\\ .____. /{RESET}  {YELLOW}* {WHITE}POYO! {YELLOW}★{RESET}",
        f"             {PINK}'-.____.-'{RESET}",
        f"             {RED}(____)(____){RESET}",
        f"         {DARK_GRAY}~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 10. CHEF_GOURMET (4 Frames)
# -----------------------------------------------------------------------------
CHEF_GOURMET_FRAMES: List[str] = [
    # Frame 0: Chef Toque & Frying Pan Ready
    "\n".join([
        f"             {WHITE}.---------.{RESET}",
        f"            {WHITE}|  CHEF   |{RESET}",
        f"            {WHITE}|   COOK  |{RESET}",
        f"            {WHITE}'---------'{RESET}",
        rf"             {PINK}/  {WHITE}•   •{PINK}  \{RESET}",
        f"            {PINK}|  {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}|{RESET}",
        rf"        {PINK}c(   \\   ---   /   ){BROWN}==={DARK_GRAY}[________]{RESET}",
        rf"              {PINK}\\ .____. /         {RED}( M ){RESET} {RED}TOMATO{RESET}",
        f"              {PINK}'-.____.-'{RESET}",
        f"              {RED}(____)(____){RESET}",
        f"          {DARK_GRAY}~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
    # Frame 1: Tossing Maxi Tomato High!
    "\n".join([
        f"                               {RED}.-------.{RESET}",
        f"                               {RED}| {WHITE}M-MAX {RED}|{RESET}",
        f"             {WHITE}.---------.{RESET}       {RED}'-------'{RESET}",
        f"            {WHITE}|  CHEF   |{RESET}         {YELLOW}* {WHITE}FLIP! {YELLOW}*{RESET}",
        f"            {WHITE}|   COOK  |{RESET}",
        f"            {WHITE}'---------'{RESET}",
        rf"             {PINK}/  {WHITE}O   O{PINK}  \{RESET}",
        f"            {PINK}|  {HOT_PINK}(♥){PINK} ᗜ {HOT_PINK}(♥){PINK}|  /{BROWN}==={DARK_GRAY}[________]{RESET}",
        rf"        {PINK}c(   \\   ---   / /{RESET}",
        rf"              {PINK}\\ .____. /{RESET}",
        f"              {PINK}'-.____.-'{RESET}",
        f"              {RED}(____)(____){RESET}",
    ]),
    # Frame 2: Catch & Sizzling Fire Crackle!
    "\n".join([
        f"             {WHITE}.---------.{RESET}",
        f"            {WHITE}|  CHEF   |{RESET}         {YELLOW}♨️ {WHITE}SIZZLE! {YELLOW}♨️{RESET}",
        f"            {WHITE}|   COOK  |{RESET}       {RED}( M ) {ORANGE}🔥 🔥{RESET}",
        f"            {WHITE}'---------'{RESET}     {DARK_GRAY}[__________]{BROWN}==={RESET}",
        rf"             {PINK}/  {WHITE}^   ^{PINK}  \   /{RESET}",
        f"            {PINK}|  {HOT_PINK}(♥){PINK} ▽ {HOT_PINK}(♥){PINK}|_/{RESET}",
        rf"        {PINK}c(   \\   ---   /{RESET}",
        rf"              {PINK}\\ .____. /{RESET}",
        f"              {PINK}'-.____.-'{RESET}",
        f"              {RED}(____)(____){RESET}",
        f"          {DARK_GRAY}~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
    # Frame 3: Gourmet Feast Banquet Presented!
    "\n".join([
        f"             {WHITE}.---------.{RESET}",
        f"            {WHITE}|  CHEF   |{RESET}      {YELLOW}★ {WHITE}GOURMET FEAST! {YELLOW}★{RESET}",
        f"            {WHITE}|   COOK  |{RESET}     {GOLD}╔══════════════╗{RESET}",
        f"            {WHITE}'---------'{RESET}     {GOLD}║ {RED}🍅 {PINK}🍰 {YELLOW}⭐ {WHITE}🍲  {GOLD}║{RESET}",
        rf"             {PINK}/  {WHITE}^   ^{PINK}  \    {GOLD}╚══════╦═══════╝{RESET}",
        f"            {PINK}|  {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}|____/       {BROWN}||{RESET}",
        rf"        {PINK}c(   \\   ---   /{RESET}          {DARK_GRAY}~~~~~~{RESET}",
        rf"              {PINK}\\ .____. /{RESET}",
        f"              {PINK}'-.____.-'{RESET}",
        f"              {RED}(____)(____){RESET}",
        f"          {DARK_GRAY}~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 11. CAR_MOUTH (4 Frames)
# -----------------------------------------------------------------------------
CAR_MOUTH_FRAMES: List[str] = [
    # Frame 0: Car Mouth Idle at Starting Line
    "\n".join([
        f"             {PINK}.-------------------------.{RESET}",
        rf"            {PINK}/   {WHITE}●     ●{PINK}     CAR MOUTH    \\{RESET}",
        f"           {PINK}|   {HOT_PINK}(♥){PINK}   {HOT_PINK}(♥){PINK}   HONK HONK!    |{RESET}",
        f"          {RED}.+-----------------------------+.{RESET}",
        rf"         {RED}/ [ ]        CABIN          [ ] \\{RESET}",
        f"        {RED}[=================================]{RESET}",
        f"        {YELLOW}(O){RED}-----------------------------{YELLOW}(O){RESET}",
        f"         {DARK_GRAY}###                           ###{RESET}",
        f"       {DARK_GRAY}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
    # Frame 1: Revving Engine with Smoke Puffs
    "\n".join([
        f"             {PINK}.-------------------------.{RESET}",
        rf"            {PINK}/   {WHITE}>     <{PINK}     REV ENGINE!   \\{RESET}",
        f"           {PINK}|   {HOT_PINK}(♥){PINK}   {HOT_PINK}(♥){PINK}   VROOOOM!!     |{RESET}",
        f"          {RED}.+-----------------------------+.{RESET}",
        rf"    {GRAY}o O{RED}  / [ ]        CABIN          [ ] \\{RESET}",
        f"   {GRAY}O o O{RED}[=================================]{RESET}",
        f"   {GRAY}o O  {YELLOW}(O){RED}-----------------------------{YELLOW}(O){RESET}",
        f"         {DARK_GRAY}###                           ###{RESET}",
        f"       {DARK_GRAY}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
    # Frame 2: Max Turbo Acceleration Sprint!
    "\n".join([
        f"   {CYAN}==={PINK}.-------------------------.{RESET}",
        rf"  {CYAN}====={PINK}/   {WHITE}ò     ó{PINK}     TURBO VROOM!  \\{YELLOW}====>>{RESET}",
        f"  {CYAN}===={PINK}|   {HOT_PINK}(♥){PINK}   {HOT_PINK}(♥){PINK}   200 MPH POYO! |{YELLOW}====>>{RESET}",
        f"  {CYAN}==={RED}.+-----------------------------+.{YELLOW}====>>{RESET}",
        rf" {GRAY}o o{CYAN}=={RED}/ [ ]        CABIN          [ ] \\{YELLOW}====>>{RESET}",
        f" {GRAY}O O{CYAN}={RED}[=================================]{YELLOW}====>>{RESET}",
        f"  {GRAY}o {CYAN}=={YELLOW}(O){RED}-----------------------------{YELLOW}(O){YELLOW}====>>{RESET}",
        f"       {DARK_GRAY}###                           ###{RESET}",
        f"       {DARK_GRAY}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
    # Frame 3: Tokyo Drift Slide!
    "\n".join([
        f"                {PINK}.-------------------------.{RESET}",
        rf"               {PINK}/   {WHITE}^     ^{PINK}     DRIFT SLIDE!  \\{RESET}",
        f"              {PINK}|   {HOT_PINK}(♥){PINK}   {HOT_PINK}(♥){PINK}   SKRRRRT!      |{RESET}",
        f"             {RED}.+-----------------------------+.{RESET}",
        rf"            {RED}/ [ ]        CABIN          [ ] \\{RESET}",
        f"    {YELLOW}*  {WHITE}✦   {RED}[=================================]{RESET}",
        f"     {YELLOW}*   * {YELLOW}(O){RED}-----------------------------{YELLOW}(O){RESET}",
        f"           {DARK_GRAY}//                             //   {YELLOW}* {WHITE}✦{RESET}",
        f"       {DARK_GRAY}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 12. STAR_FISHING (4 Frames)
# -----------------------------------------------------------------------------
STAR_FISHING_FRAMES: List[str] = [
    # Frame 0: Patient Starlight Pond Cast
    "\n".join([
        f"             {PINK}.-------.{RESET}",
        rf"           {PINK}/   {WHITE}˘   ˘{PINK}   \\{BROWN}==============.{RESET}",
        rf"          {PINK}|   {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}  |              \{RESET}",
        rf"        {PINK}c( \     -     / )              \{RESET}",
        rf"            {PINK}\\ .____. /                  \{RESET}",
        f"             {PINK}'-......-'{RESET}                   {CYAN}|{RESET}",
        f"             {RED}(____)(____){RESET}                 {CYAN}|{RESET}",
        f"         {DARK_GRAY}~~~~~~~~~~~~~~~~~{RESET}               {CYAN}o{RESET}",
        f"       {CYAN}~~~~~~~~~~~~~~~~~~~~~~~~~ ( . ~ . ) ~~~{RESET}",
    ]),
    # Frame 1: Ripple and Nibble!
    "\n".join([
        f"             {PINK}.-------.{RESET}",
        rf"           {PINK}/   {WHITE}•   •{PINK}   \\{BROWN}==============.{RESET}",
        rf"          {PINK}|   {HOT_PINK}(♥){PINK} ▿ {HOT_PINK}(♥){PINK}  |              \{RESET}",
        rf"        {PINK}c( \     -     / )              \{RESET}",
        rf"            {PINK}\\ .____. /                  \{RESET}",
        f"             {PINK}'-......-'{RESET}                   {CYAN}|{RESET}",
        f"             {RED}(____)(____){RESET}                 {CYAN}|{RESET}",
        f"         {DARK_GRAY}~~~~~~~~~~~~~~~~~{RESET}              {YELLOW}* {CYAN}o {YELLOW}*{RESET}",
        f"       {CYAN}~~~~~~~~~~~~~~~~~~~~~~~ ( ( BLOOP ) ) ~{RESET}",
    ]),
    # Frame 2: ROD BENDING! HEAVY STRIKE!
    "\n".join([
        f"             {PINK}.-------.{RESET}      {YELLOW}* {RED}!! BITE !! {YELLOW}*{RESET}",
        rf"           {PINK}/   {WHITE}>   <{PINK}   \\{BROWN}====\\{RESET}",
        rf"          {PINK}|   {HOT_PINK}(♥){PINK} ᗜ {HOT_PINK}(♥){PINK}  |     \{BROWN}\{RESET}",
        rf"       {PINK}/| c( \    -    / )       \{BROWN}\{RESET}",
        rf"           {PINK}\\  .____. /             \{BROWN}\{RESET}",
        rf"            {PINK}'-......-'{RESET}               {CYAN}\{RESET}",
        rf"            {RED}(____)(____){RESET}               {CYAN}\{RESET}",
        rf"        {DARK_GRAY}~~~~~~~~~~~~~~~~~{RESET}              {CYAN}\{RESET}",
        rf"       {CYAN}~~~~~~~~~~~~~~~~~~~~~ {WHITE}/ / / SPLASH! \\ \\{RESET}",
    ]),
    # Frame 3: REELING UP A GOLDEN STAR ROD!
    "\n".join([
        f"                                     {YELLOW}(★) {GOLD}GOLDEN{RESET}",
        rf"                                    {GOLD}/|\\ {GOLD}STAR ROD!{RESET}",
        f"             {PINK}.-------.{RESET}              {GOLD}|||{RESET}",
        rf"           {PINK}/   {WHITE}^   ^{PINK}   \\{BROWN}============o{GOLD}[★]{RESET}",
        f"          {PINK}|   {HOT_PINK}(♥){PINK} ▽ {HOT_PINK}(♥){PINK}  |             {WHITE}✦   {YELLOW}*{RESET}",
        rf"       {PINK}/| c( \    -    / )           {YELLOW}*  {WHITE}POYO! {YELLOW}*{RESET}",
        rf"           {PINK}\\  .____. /{RESET}",
        f"            {PINK}'-......-'{RESET}",
        f"            {RED}(____)(____){RESET}",
        f"        {DARK_GRAY}~~~~~~~~~~~~~~~~~{RESET}",
        f"       {CYAN}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{RESET}",
    ]),
]


# -----------------------------------------------------------------------------
# 13. NOID_CHAOS (3 Frames)
# -----------------------------------------------------------------------------
NOID_CHAOS_FRAMES: List[str] = [
    # Frame 0: Crouching noid bunny ears, sneaky smirk
    "\n".join([
        f"            {RED}(\\__/){RESET} {YELLOW}*twitch*{RESET}",
        f"            {RED}( •ᴗ•){RESET}     {GOLD}🍕{RESET}",
        f"          {PINK}.-------.{RESET}",
        rf"        {PINK}/   {WHITE}¬   ¬{PINK}   \\{RESET}  {RED}c[══]{RESET} {YELLOW}PIZZA{RESET}",
        rf"       {PINK}|   {HOT_PINK}(♥){PINK} ᗜ {HOT_PINK}(♥){PINK}  |/{RED}CUTTER{RESET}",
        rf"     {PINK}c( \\     -     / ){RESET}",
        rf"         {PINK}\\  .____. /{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"          {RED}(____)(____){RESET}",
    ]),
    # Frame 1: Frantic noid twitch, ears vibrating!
    "\n".join([
        f"          {YELLOW}彡 {RED}(\\__/){RESET} {YELLOW}ミ  *SPARK!*{RESET}",
        f"            {RED}( >_<){RESET} {YELLOW}⚡ ⚡{RESET}",
        f"          {PINK}.-------.{RESET}",
        rf"        {PINK}/   {WHITE}⊙   ⊙{PINK}   \\{RESET}  {RED}==/ {RESET} {RED}!NOID!{RESET}",
        rf"       {PINK}|   {HOT_PINK}(♥){PINK} ⌂ {HOT_PINK}(♥){PINK}  |{RESET}   {YELLOW}CHAOS 100%{RESET}",
        rf"     {PINK}c( \\    ~    / )b{RESET}",
        rf"         {PINK}\\  .____. /{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"          {RED}(____)(____){RESET} {YELLOW}*tiptoe*{RESET}",
    ]),
    # Frame 2: Leaping noid strike! AVOID THE NOID!
    "\n".join([
        f"        {YELLOW}★ {RED}(\\__/){RESET} {YELLOW}★  {GOLD}AVOID THE NOID!{RESET}",
        f"          {RED}( ≧ᗜ≦)ノ{RESET} {GOLD}🍕 🍕 🍕{RESET}",
        f"          {PINK}.-------.{RESET}",
        rf"        {PINK}/   {WHITE}^   ^{PINK}   \\{RESET}  {YELLOW}*POYO!*{RESET}",
        rf"       {PINK}|   {HOT_PINK}(♥){PINK} ▽ {HOT_PINK}(♥){PINK}  |{RESET}",
        rf"        {PINK}\\  .____. /{RESET}",
        f"         {PINK}'-......-'{RESET}",
        f"        {RED}(____)  (____){RESET}",
        f"           {DARK_GRAY}(shadow){RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 14. ANNOYING_POYO (3 Frames)
# -----------------------------------------------------------------------------
ANNOYING_POYO_FRAMES: List[str] = [
    # Frame 0: Preparing giant golden megaphone
    "\n".join([
        f"             {YELLOW}*AHEM...*{RESET}",
        f"          {PINK}.-------.{RESET}",
        rf"        {PINK}/   {WHITE}•   •{PINK}   \\{RESET}  {GOLD}┌───────┐{RESET}",
        rf"       {PINK}|   {HOT_PINK}(♥){PINK} 0 {HOT_PINK}(♥){PINK}  |{GOLD}─┤MEGAPHONE│{RESET}",
        rf"     {PINK}c( \\    -    / ) {GOLD}└───────┘{RESET}",
        rf"         {PINK}\\  .____. /{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"          {RED}(____)(____){RESET}",
    ]),
    # Frame 1: BLASTING POYOOOOOOOOOOO!
    "\n".join([
        f"      {CYAN}(((( {YELLOW}POYOOOOOOOOOOOOOOOOOOO! {CYAN})))) {RESET}",
        f"          {PINK}.-------.{RESET}   {CYAN}彡 彡 彡 彡 彡{RESET}",
        rf"        {PINK}/   {WHITE}>   <{PINK}   \\{RESET}  {GOLD}╔═════════╗{CYAN}))))){RESET}",
        rf"       {PINK}|   {HOT_PINK}(♥){PINK} ᗝ {HOT_PINK}(♥){PINK}  |{GOLD}═╣  POYO!  ╠{CYAN}))))){RESET}",
        rf"      {PINK}/| (       ) \\{GOLD}╚═════════╝{CYAN}))))){RESET}",
        rf"         {PINK}\\  .____. /{RESET}   {CYAN}彡 彡 彡 彡 彡{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"         {RED}(____) (____){RESET} {YELLOW}*EAR DRUM CRITICAL*{RESET}",
    ]),
    # Frame 2: Giggle after deafening the room
    "\n".join([
        f"             {YELLOW}*snicker giggle*{RESET}",
        f"          {PINK}.-------.{RESET}",
        rf"        {PINK}/   {WHITE}˶ ❛ ‿ ❛ ˶{PINK} \\{RESET}  {GOLD}[megaphone down]{RESET}",
        rf"       {PINK}|   {HOT_PINK}(♥){PINK}   {HOT_PINK}(♥){PINK} |{RESET}   {GREEN}Did you hear me? :3{RESET}",
        rf"     {PINK}c( \\    ~    / )b{RESET}",
        rf"         {PINK}\\  .____. /{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"          {RED}(____)(____){RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 15. PIZZA_HEIST (4 Frames)
# -----------------------------------------------------------------------------
PIZZA_HEIST_FRAMES: List[str] = [
    # Frame 0: Sneaking in ninja mask
    "\n".join([
        f"            {DARK_GRAY}[= =]{RESET} {YELLOW}*stealth sneak*{RESET}",
        f"          {PINK}.-------.{RESET}       {GOLD}|\\{RESET}",
        rf"        {PINK}/   {WHITE}•   •{PINK}   \\{RESET}      {GOLD}| \\  HOT PIZZA{RESET}",
        rf"       {PINK}|   {HOT_PINK}(♥){PINK} ‿ {HOT_PINK}(♥){PINK}  |{RESET}     {GOLD}|  \\  SLICE!{RESET}",
        rf"     {PINK}c( \\    ~    / ){RESET}     {RED}|═══\\{RESET}",
        rf"         {PINK}\\  .____. /{RESET}      {DARK_GRAY}~~~~~~~{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"          {RED}(____)(____){RESET}",
    ]),
    # Frame 1: The Snatch!
    "\n".join([
        f"           {YELLOW}★ *YOINK!* ★{RESET}",
        f"          {PINK}.-------.{RESET} {GOLD} /\\{RESET}",
        rf"        {PINK}/   {WHITE}O   O{PINK}   \\{GOLD}/  \\{RESET} {YELLOW}*CHEESE PULL*{RESET}",
        rf"       {PINK}|   {HOT_PINK}(♥){PINK} ᗜ {HOT_PINK}(♥){PINK} {GOLD}/~~~~\\{RESET}",
        rf"     {PINK}c( \\ (   )  / {RED}/======\\{RESET}",
        rf"         {PINK}\\ .____. /{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"          {RED}(____)(____){RESET}",
    ]),
    # Frame 2: Running away holding the giant slice!
    "\n".join([
        f"    {YELLOW}*scuttle scuttle*{RESET}  {GOLD} /\\{RESET}",
        f"         {PINK}.-------.{RESET}  {GOLD}/  \\{RESET}  {RED}IOU: 1 SLICE!{RESET}",
        rf"       {PINK}/   {WHITE}>   <{PINK}   \\{GOLD}/~~~~\\{RESET}",
        rf"      {PINK}|   {HOT_PINK}(♥){PINK} ▽ {HOT_PINK}(♥){PINK} {RED}/======\\{RESET}",
        rf"     {PINK}/| (       ) \\{RESET}",
        rf"        {PINK}\\ .____. /{RESET}",
        f"         {PINK}'-......-'{RESET}",
        f"       {RED}(____)  (____){RESET} {YELLOW}彡 彡 彡{RESET}",
    ]),
    # Frame 3: Delicious munching with cheese beard
    "\n".join([
        f"            {GOLD}*CRUNCH NOM NOM*{RESET}",
        f"         {PINK}.-------.{RESET}",
        rf"       {PINK}/   {WHITE}^   ^{PINK}   \\{RESET}  {YELLOW}★ DELICIOUS! ★{RESET}",
        rf"      {PINK}|   {HOT_PINK}(♥){PINK} ▿ {HOT_PINK}(♥){PINK}  |{RESET} {GOLD}~~~(cheese)~~~{RESET}",
        rf"    {PINK}c( \\     -     / )b{RESET}",
        rf"        {PINK}\\  .____. /{RESET}",
        f"         {PINK}'-......-'{RESET}",
        f"         {RED}(____)(____){RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 16. GOBLIN_DANCE (4 Frames)
# -----------------------------------------------------------------------------
GOBLIN_DANCE_FRAMES: List[str] = [
    # Frame 0: Goblin shimmy left
    "\n".join([
        f"        {YELLOW}♪ ┏(･o･)┛ ♪{RESET} {GREEN}GOBLIN MODE{RESET}",
        f"          {PINK}.-------.{RESET}",
        rf"        {PINK}/   {WHITE}•   •{PINK}   \\{RESET}",
        rf"      {PINK}\\(   {HOT_PINK}(♥){PINK} 👅 {HOT_PINK}(♥){PINK} |{RESET}",
        rf"        \\( \\    -    / ){RESET}",
        rf"          {PINK}\\ .____. /{RESET}",
        f"           {PINK}'-......-'{RESET}",
        f"         {RED}(____) {RED}(____){RESET}",
    ]),
    # Frame 1: Goblin squat bounce
    "\n".join([
        f"           {YELLOW}*WIGGLE WIGGLE*{RESET}",
        f"        {PINK}.-----------.{RESET}",
        rf"      {PINK}/   {WHITE}>   <{PINK}     \\{RESET}",
        rf"     {PINK}|   {HOT_PINK}(♥){PINK}  ᗜ  {HOT_PINK}(♥){PINK}   |{RESET} {YELLOW}★ WUB WUB ★{RESET}",
        rf"    {PINK}c( \\      -       / )b{RESET}",
        rf"        {PINK}\\   ._____.   /{RESET}",
        f"         {PINK}'-.........-'{RESET}",
        f"        {RED}(_____) (_____){RESET}",
    ]),
    # Frame 2: Goblin shimmy right
    "\n".join([
        f"        {GREEN}UNSTOPPABLE!{RESET} {YELLOW}♪ ┗(･o･)┓ ♪{RESET}",
        f"          {PINK}.-------.{RESET}",
        rf"        {PINK}/   {WHITE}•   •{PINK}   \\{RESET}",
        rf"       {PINK}|   {HOT_PINK}(♥){PINK} 👅 {HOT_PINK}(♥){PINK}   )/{RESET}",
        rf"     {PINK}c( \\    -    / )/{RESET}",
        rf"         {PINK}\\ .____. /{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"          {RED}(____) {RED}(____){RESET}",
    ]),
    # Frame 3: Victory Star Confetti Spin
    "\n".join([
        f"     {YELLOW}★ {GOLD}*TA-DAAAA!* {YELLOW}★ {PINK}POYO!{RESET}",
        f"          {PINK}.-------.{RESET}",
        rf"       {PINK}\\/   {WHITE}^   ^{PINK}   \\/{RESET} {WHITE}✦ ✧ ✦{RESET}",
        rf"       {PINK}|   {HOT_PINK}(♥){PINK} ▽ {HOT_PINK}(♥){PINK}  |{RESET}  {YELLOW}✨ CONFETTI! ✨{RESET}",
        rf"     {PINK}c( \\     -     / )b{RESET}",
        rf"         {PINK}\\  .____. /{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"          {RED}(____)(____){RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 17. DRAMATIC_FAINT (3 Frames)
# -----------------------------------------------------------------------------
DRAMATIC_FAINT_FRAMES: List[str] = [
    # Frame 0: Melodramatic woe
    "\n".join([
        f"          {CYAN}*GASP!* {RED}\"Alas, cruel world!\"{RESET}",
        f"          {PINK}.-------.{RESET}",
        rf"        {PINK}/   {WHITE}T   T{PINK}   \\{RESET}",
        rf"       {PINK}|   {HOT_PINK}(♥){PINK} ⌓ {HOT_PINK}(♥){PINK}  |/{RESET} {CYAN}*hand to forehead*{RESET}",
        rf"     {PINK}c( \\     -     / ){RESET}",
        rf"         {PINK}\\  .____. /{RESET}",
        f"          {PINK}'-......-'{RESET}",
        f"          {RED}(____)(____){RESET}",
    ]),
    # Frame 1: Dizzy wobble
    "\n".join([
        f"         {YELLOW}*wobble wobble...*{RESET}",
        f"            {PINK}.-------.{RESET}",
        rf"          {PINK}/   {WHITE}@   @{PINK}   \\{RESET}  {YELLOW}*stars spinning*{RESET}",
        rf"         {PINK}|   {HOT_PINK}(♥){PINK} ᗝ {HOT_PINK}(♥){PINK}  |{RESET}   {GOLD}💫 💫{RESET}",
        rf"       {PINK}c( \\      -    / ){RESET}",
        rf"           {PINK}\\  .____. /{RESET}",
        f"            {PINK}'-......-'{RESET}",
        f"           {RED}(____)(____){RESET}",
    ]),
    # Frame 2: Flop onto pillow with tiny halo
    "\n".join([
        f"              {YELLOW}ଘ(੭*ˊᵕˋ)੭* {GOLD}*halo*{RESET}",
        f"             {WHITE}   _O_{RESET}",
        f"           {PINK}.-------.{RESET}",
        rf"         {PINK}/   {WHITE}x   x{PINK}   \\{RESET}  {CYAN}\"Needs 1 cookie to revive...\"{RESET}",
        rf"        {PINK}|   {HOT_PINK}(♥){PINK}   {HOT_PINK}(♥){PINK} |{RESET}",
        f"     {WHITE}[=== FLUFFY VELVET PILLOW ===]{RESET}",
        f"            {RED}(____)(____){RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 18. METTAUR_HELMET (3 Frames)
# -----------------------------------------------------------------------------
METTAUR_HELMET_FRAMES: List[str] = [
    # Frame 0: Standing proud in yellow hardhat
    "\n".join([
        f"               {YELLOW}.------------------.{RESET}",
        f"            .-'      {WHITE}[+] SAFETY{YELLOW}    '-.{RESET}",
        f"          .'     {WHITE}__________________{YELLOW}  '.{RESET}",
        f"         /     {WHITE}/                  \\{YELLOW}   \\{RESET}",
        f"        |====={WHITE}(  METTAUR HARDHAT   ){YELLOW}====|{RESET}",
        f"        |================================|{RESET}",
        f"         '------------------------------'{RESET}",
        f"                 {PINK}.------------.{RESET}",
        f"               {PINK}/   {WHITE}●      ●{PINK}   \\{RESET}",
        f"          {HOT_PINK}(> {PINK}(    {HOT_PINK}♥      ♥{PINK}     ) <){RESET}",
        f"              {PINK}\\     {RED}▽{PINK}      /{RESET}       {YELLOW}⛑️ \"Poyo Builder!\" ✨{RESET}",
        f"             {RED}.'---.    .---'.{RESET}",
        f"            {RED}(______)  (______){RESET}",
    ]),
    # Frame 1: Crouch Deflect under Hardhat with TING! sparks
    "\n".join([
        f"              {YELLOW}.--------------------.{RESET}",
        f"           .-'       {WHITE}[+] SAFETY{YELLOW}       '-.{RESET}",
        f"         .'      {WHITE}__________________{YELLOW}      '.{RESET}",
        f"        /      {WHITE}/                  \\{YELLOW}       \\{RESET}",
        f"       |======{WHITE}(  METTAUR MARK-IV  ){YELLOW}======|  {CYAN}✨ *TING!* ✨{RESET}",
        f"       |===================================|  {WHITE}💥 DEFLECT!{RESET}",
        f"        \\_                               _/{RESET}",
        f"          '--{PINK}( {WHITE}●       ●{PINK} ){YELLOW}----------------'{RESET}",
        f"              {RED}(___)     (___){RESET}",
    ]),
    # Frame 2: Pneumatic Pickaxe Quarry Strike
    "\n".join([
        f"               {YELLOW}.------------------.{RESET}",
        f"            .-'      {WHITE}[+] SAFETY{YELLOW}    '-.      {CYAN}⛏️ *CLANG!*{RESET}",
        f"          .'     {WHITE}__________________{YELLOW}  '.     {WHITE}_____{RESET}",
        f"         /     {WHITE}/                  \\{YELLOW}   \\   {WHITE}/  |  \\{RESET}",
        f"        |====={WHITE}(  METTAUR HARDHAT   ){YELLOW}====| {WHITE}/___|___\\{RESET}",
        f"         '------------------------------'      {YELLOW}| |{RESET}",
        f"                 {PINK}.------------.{YELLOW}                | |{RESET}",
        f"               {PINK}/   {WHITE}●      ●{PINK}   \\               | |{RESET}",
        f"          {HOT_PINK}(> {PINK}(    {HOT_PINK}♥      ♥{PINK}     ) {YELLOW}===O========' '{RESET}",
        f"              {PINK}\\     {RED}▽{PINK}      /       {GOLD}*QUARRY SHARD!* 💎{RESET}",
        f"             {RED}.'---.    .---'.{RESET}",
        f"            {RED}(______)  (______){RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 19. MINION_BUDDY (3 Frames)
# -----------------------------------------------------------------------------
MINION_BUDDY_FRAMES: List[str] = [
    # Frame 0: Minion offering banana to Kirby
    "\n".join([
        f"        {YELLOW}.--------.{RESET}                     {YELLOW}(♪){RESET}",
        f"     .-'   {WHITE}(o)(o){YELLOW} '-.{RESET}                {PINK}.-------.{RESET}",
        f"    /    {DARK_GRAY}[======]{YELLOW}   \\{RESET}              {PINK}/   {WHITE}●   ●{PINK}   \\{RESET}",
        f"   |       {RED}\\__/{YELLOW}     |  {GOLD}🍌 \"Bello!\"{RESET} {HOT_PINK}(> {PINK}(    {HOT_PINK}♥   ♥{PINK}   ) <){RESET}",
        f"   |    {BLUE}.--------.{YELLOW}  |   {GOLD}*banana*{RESET}       {PINK}\\     {RED}▽{PINK}     /{RESET}",
        f"   |   {BLUE}/   {WHITE}(G){BLUE}   \\{YELLOW} |                   {RED}.'---.   .---'.{RESET}",
        f"   '--{BLUE}|  OVERALLS |{YELLOW}-'                  {RED}(_____) (_____){RESET}",
        f"      {DARK_GRAY}(____)(____){RESET}",
    ]),
    # Frame 1: Kirby eating banana with stars & Minion wrench click
    "\n".join([
        f"        {YELLOW}.--------.{RESET}                  {GOLD}✨ *YUMMY POYO!* ✨{RESET}",
        f"     .-'   {WHITE}(^)(^){YELLOW} '-.  {CYAN}🔧 *clink*{RESET}       {PINK}.-------.{RESET}",
        f"    /    {DARK_GRAY}[======]{YELLOW}   \\{RESET}              {PINK}/   {WHITE}^   ^{PINK}   \\{RESET}",
        f"   |       {RED}▽{YELLOW}       |            {HOT_PINK}(> {PINK}(    {HOT_PINK}♥   ♥{PINK}   ) <){RESET}",
        f"   |    {BLUE}.--------.{YELLOW}  |                 {PINK}\\    {RED}~~~{PINK}    /{RESET}",
        f"   |   {BLUE}/   {WHITE}(G){BLUE}   \\{YELLOW} |                   {RED}.'---.   .---'.{RESET}",
        f"   '--{BLUE}|  OVERALLS |{YELLOW}-'                  {RED}(_____) (_____){RESET}",
        f"      {DARK_GRAY}(____)(____){RESET}",
    ]),
    # Frame 2: Minion and Kirby jumping High-Five with BEE-DO siren
    "\n".join([
        f"      {RED}🚨 BEE-DO! BEE-DO! 🚨{RESET}         {YELLOW}⭐ HIGH FIVE! ⭐{RESET}",
        f"        {YELLOW}.--------.{RESET}                 {PINK}.-------.{RESET}",
        f"     .-'   {WHITE}(*){YELLOW}   '-.  {GOLD}\\(੭ˊᵕˋ)੭{RESET}    {HOT_PINK}(੭ˊᵕˋ)੭{PINK} /   {WHITE}★   ★{PINK}   \\{RESET}",
        f"    /    {DARK_GRAY}[======]{YELLOW}   \\{RESET}             {PINK}(    {HOT_PINK}♥   ♥{PINK}   ) <){RESET}",
        f"   |       {RED}\\__/{YELLOW}     |              {PINK}\\     {RED}▽{PINK}     /{RESET}",
        f"   '--{BLUE}|  OVERALLS |{YELLOW}-'               {RED}.'---.   .---'.{RESET}",
        f"      {DARK_GRAY}(____)(____){RESET}               {RED}(_____) (_____){RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 20. METROID_BUDDY (3 Frames)
# -----------------------------------------------------------------------------
METROID_BUDDY_FRAMES: List[str] = [
    # Frame 0: Baby Metroid hovering overhead
    "\n".join([
        f"                {GREEN}.----------------.{RESET}",
        f"             .-'   {RED}(●)      (●){GREEN}   '-.{RESET}       {CYAN}🛸 \"Skreeeee!\"{RESET}",
        f"           .'      {CYAN}~~~      ~~~{GREEN}      '.{RESET}",
        f"          /     {RED}*  (●)  *{GREEN}             \\{RESET}    {HOT_PINK}✨ BIOTIC PULSE ✨{RESET}",
        f"         |     {CYAN}3 PULSING NUCLEI{GREEN}        |{RESET}",
        f"          \\_         {WHITE}\\  /{GREEN}            _/{RESET}",
        f"            '--.     {WHITE}\\/{GREEN}         .--'{RESET}",
        f"                {WHITE}/\\        /\\{RESET}",
        f"                   {PINK}.-------.{RESET}",
        f"                 {PINK}/   {WHITE}●   ●{PINK}   \\{RESET}       {PINK}🌸 \"Metroid buddy!\"{RESET}",
        f"            {HOT_PINK}(> {PINK}(    {HOT_PINK}♥   ♥{PINK}   ) <){RESET}",
        f"                {PINK}\\     {RED}▽{PINK}     /{RESET}",
        f"               {RED}.'---.   .---'.{RESET}",
        f"              {RED}(_____) (_____){RESET}",
    ]),
    # Frame 1: Baby Metroid descending and nuzzling Kirby
    "\n".join([
        f"                {GREEN}.----------------.{RESET}",
        f"             .-'   {RED}(♥)      (♥){GREEN}   '-.{RESET}       {GREEN}*snuggle nuzzle*{RESET}",
        f"            /     {RED}*  (♥)  *{GREEN}           \\{RESET}",
        f"           |     {CYAN}TRANSLUCENT JELLY{GREEN}    |{RESET}",
        f"            \\_       {WHITE}\\  /{GREEN}          _/{RESET}     {CYAN}*purr hum...*{RESET}",
        f"              '--.   {WHITE}\\/{GREEN}       .--'{RESET}",
        f"                  {WHITE}/\\      /\\{RESET}",
        f"                   {PINK}.-------.{RESET}",
        f"                 {PINK}/   {WHITE}^   ^{PINK}   \\{RESET}       {HOT_PINK}💖 \"Ticklish poyo!\"{RESET}",
        f"            {HOT_PINK}(> {PINK}(    {HOT_PINK}♥   ♥{PINK}   ) <){RESET}",
        f"                {PINK}\\    {RED}~~~{PINK}    /{RESET}",
        f"               {RED}.'---.   .---'.{RESET}",
        f"              {RED}(_____) (_____){RESET}",
    ]),
    # Frame 2: Biotic Bubble Cryo Barrier
    "\n".join([
        f"         {CYAN}.----------------------------------.{RESET}",
        f"        {CYAN}/   {GREEN}*BIOTIC BUBBLE CRYO BARRIER*     {CYAN}\\{RESET}",
        f"       {CYAN}|      {GREEN}.-------.                       {CYAN}|{RESET}   {CYAN}❄️ -45°C THERMALS{RESET}",
        f"       {CYAN}|    {GREEN}.-' {RED}(●) (●){GREEN} '-.    {PINK}.-------.       {CYAN}|{RESET}   {GREEN}🛡️ DEFENSE: 100%{RESET}",
        f"       {CYAN}|   {GREEN}/   {CYAN}~~ {RED}(●){CYAN} ~~{GREEN}   \\  {PINK}/   {WHITE}★   ★{PINK}   \\     {CYAN}|{RESET}",
        f"       {CYAN}|   {GREEN}|  {CYAN}BIOTIC DOME{GREEN} | {HOT_PINK}(> {PINK}(    {HOT_PINK}♥   ♥{PINK}   ) <)   {CYAN}|{RESET}",
        f"       {CYAN}|    {GREEN}\\_  {WHITE}\\/{GREEN}      _/     {PINK}\\     {RED}▽{PINK}     /     {CYAN}|{RESET}",
        f"        {CYAN}\\      {WHITE}/\\    /\\{CYAN}       {RED}.'---.   .---'.   /{RESET}",
        f"         {CYAN}'----------------------------------'{RESET}",
    ]),
]

# -----------------------------------------------------------------------------
# 21. TOOLBOX_ENGINEER (3 Frames)
# -----------------------------------------------------------------------------
TOOLBOX_ENGINEER_FRAMES: List[str] = [
    # Frame 0: Kirby with closed steel toolbox
    "\n".join([
        f"        {PINK}.-------.{RESET}           {CYAN}._________________________.{RESET}",
        f"      {PINK}/   {WHITE}●   ●{PINK}   \\{RESET}         {CYAN}| {YELLOW}⭐ KIRBY MASTER TOOLBOX ⭐{CYAN} |{RESET}",
        f" {HOT_PINK}(> {PINK}(    {HOT_PINK}♥   ♥{PINK}   ) <){RESET}       {CYAN}|=========================|{RESET}",
        f"     {PINK}\\     {RED}▽{PINK}     /{RESET}          {CYAN}| [1] CONSTRUCTION  [⛑️ ⛏️] |{RESET}",
        f"    {RED}.'---.   .---'.{RESET}         {CYAN}| [2] SYSTEMS RUNTIME [🔧 🪛] |{RESET}",
        f"   {RED}(_____) (_____){RESET}          {CYAN}| [3] MINION PIT CREW [🍌 📢] |{RESET}",
        f"                           {CYAN}'-------------------------'{RESET}",
    ]),
    # Frame 1: Toolbox open with glowing tools flying out
    "\n".join([
        f"                           {YELLOW}✨ *UNLATCH CLINK!* ✨{RESET}",
        f"        {PINK}.-------.{RESET}           {CYAN}  /=========================\\{RESET}",
        f"      {PINK}/   {WHITE}★   ★{PINK}   \\{RESET}  {YELLOW}🔧 ⛏️{RESET}   {CYAN}| {YELLOW}5-DRAWER CARBYNE WORKBENCH{CYAN}|{RESET}",
        f" {HOT_PINK}(> {PINK}(    {HOT_PINK}♥   ♥{PINK}   )====O        {CYAN}|=========================|{RESET}",
        f"     {PINK}\\     {RED}▽{PINK}     /{RESET}          {CYAN}| [4] METROID BIOTIC [🛸 🧪] |{RESET}",
        f"    {RED}.'---.   .---'.{RESET}         {CYAN}| [5] FOLEY HAPTICS  [📳 ⌨️] |{RESET}",
        f"   {RED}(_____) (_____){RESET}          {CYAN}'-------------------------'{RESET}",
    ]),
    # Frame 2: Torquing bolts with sparks & gears
    "\n".join([
        f"         {YELLOW}⚙️ *SPARKS FLYING* ⚙️{RESET}      {CYAN}🏗️ SCAFFOLDING ERECTED!{RESET}",
        f"        {PINK}.-------.{RESET}                {WHITE}  /\\     /\\{RESET}",
        f"      {PINK}/   {WHITE}•̀   •́{PINK}   \\{RESET}  {CYAN}🔧 *TORQUE*{RESET}    {WHITE} /  \\___/  \\{RESET}",
        f" {HOT_PINK}(> {PINK}(    {HOT_PINK}♥   ♥{PINK}   )====O=======[*] {WHITE}|   [PORTAL]  |{RESET}",
        f"     {PINK}\\     {RED}▽{PINK}     /{RESET}                 {WHITE}|   :8088 OK  |{RESET}",
        f"    {RED}.'---.   .---'.{RESET}               {WHITE}'------------'{RESET}",
        f"   {RED}(_____) (_____){RESET}",
    ]),
]

SPRITES: Dict[str, List[str]] = {
    "IDLE_BOUNCE": IDLE_BOUNCE_FRAMES,
    "WARP_STAR_DASH": WARP_STAR_DASH_FRAMES,
    "HOVER_FLOAT": HOVER_FLOAT_FRAMES,
    "INHALE_VORTEX": INHALE_VORTEX_FRAMES,
    "SNOOZE_CATNAP": SNOOZE_CATNAP_FRAMES,
    "EASEL_PAINTER": EASEL_PAINTER_FRAMES,
    "ACE_BRAWLER": ACE_BRAWLER_FRAMES,
    "MAGICIAN": MAGICIAN_FRAMES,
    "SWORD_HERO": SWORD_HERO_FRAMES,
    "CHEF_GOURMET": CHEF_GOURMET_FRAMES,
    "CAR_MOUTH": CAR_MOUTH_FRAMES,
    "STAR_FISHING": STAR_FISHING_FRAMES,
    "NOID_CHAOS": NOID_CHAOS_FRAMES,
    "ANNOYING_POYO": ANNOYING_POYO_FRAMES,
    "PIZZA_HEIST": PIZZA_HEIST_FRAMES,
    "GOBLIN_DANCE": GOBLIN_DANCE_FRAMES,
    "DRAMATIC_FAINT": DRAMATIC_FAINT_FRAMES,
    "METTAUR_HELMET": METTAUR_HELMET_FRAMES,
    "MINION_BUDDY": MINION_BUDDY_FRAMES,
    "METROID_BUDDY": METROID_BUDDY_FRAMES,
    "TOOLBOX_ENGINEER": TOOLBOX_ENGINEER_FRAMES,
}

SPRITE_DESCRIPTIONS: Dict[str, str] = {
    "IDLE_BOUNCE": "Classic Dream Land rhythmic bounce with squish-and-stretch joy.",
    "WARP_STAR_DASH": "Riding the legendary Warp Star through hyperspace cosmic speed-lanes.",
    "HOVER_FLOAT": "Ballooned up with fresh air, flapping little hands to hover skyward.",
    "INHALE_VORTEX": "Endless suction vortex funneling stars, cosmic dust, and matter inward.",
    "SNOOZE_CATNAP": "Sleepy snooze under starry nightcap with dreamy ascending Zzz bubbles.",
    "EASEL_PAINTER": "Beret-donning master artist painting a vibrant self-portrait on easel.",
    "ACE_BRAWLER": "Fighter Kirby charging up chi and firing a devastating Hyper Laser Cannon!",
    "MAGICIAN": "Mystic magician waving his star wand to conjure cards, doves, and starlight.",
    "SWORD_HERO": "Heroic swordmaster Kirby executing charged starlight strikes and 360 spin cleaves.",
    "CHEF_GOURMET": "Master chef Kirby tossing Maxi Tomatoes in sizzling pans and presenting royal feasts.",
    "CAR_MOUTH": "Mouthful Mode Car Kirby revving engines, turbo boosting, and Tokyo drifting.",
    "STAR_FISHING": "Peaceful starlight pond fishing, reeling in aquatic wonders and the Golden Star Rod.",
    "NOID_CHAOS": "Chaotic red bunny-eared Noid Kirby wielding a pizza cutter with 100% gremlin energy.",
    "ANNOYING_POYO": "Ear-splitting megaphone-toting Kirby blasting deafening Poyos across the terminal.",
    "PIZZA_HEIST": "Sneaky burglar Kirby tip-toeing away with an enormous hot dripping pizza slice.",
    "GOBLIN_DANCE": "Absurd high-entropy comedic wiggle dance with tongue-poking and star confetti.",
    "DRAMATIC_FAINT": "Over-the-top melodramatic faint onto a velvet pillow due to 2 minutes without treats.",
    "METTAUR_HELMET": "Wearing the iconic yellow Mettaur Hardhat, ducking for 100% deflection and swinging pneumatic pickaxe.",
    "MINION_BUDDY": "Loyal Bob the Minion offering banana boost, tightening bolts with socket wrench, and high-fiving Kirby.",
    "METROID_BUDDY": "The Baby Metroid floating with bioluminescent nuclei, nuzzling Kirby and deploying biotic cryo barrier.",
    "TOOLBOX_ENGINEER": "Kirby opening the 5-drawer Master Engineering Toolbox, torquing bolts and erecting scaffolds.",
}

SPRITE_DEFAULT_FPS: Dict[str, float] = {
    "IDLE_BOUNCE": 4.5,
    "WARP_STAR_DASH": 7.0,
    "HOVER_FLOAT": 5.0,
    "INHALE_VORTEX": 6.5,
    "SNOOZE_CATNAP": 3.0,
    "EASEL_PAINTER": 3.5,
    "ACE_BRAWLER": 5.0,
    "MAGICIAN": 4.0,
    "SWORD_HERO": 4.5,
    "CHEF_GOURMET": 3.5,
    "CAR_MOUTH": 5.0,
    "STAR_FISHING": 3.0,
    "NOID_CHAOS": 5.5,
    "ANNOYING_POYO": 4.0,
    "PIZZA_HEIST": 4.5,
    "GOBLIN_DANCE": 6.0,
    "DRAMATIC_FAINT": 2.5,
    "METTAUR_HELMET": 3.5,
    "MINION_BUDDY": 4.0,
    "METROID_BUDDY": 3.5,
    "TOOLBOX_ENGINEER": 4.0,
}

# Synonyms and aliases for easy CLI matching
SPRITE_ALIASES: Dict[str, str] = {
    "IDLE": "IDLE_BOUNCE",
    "BOUNCE": "IDLE_BOUNCE",
    "WARP": "WARP_STAR_DASH",
    "WARP_STAR": "WARP_STAR_DASH",
    "DASH": "WARP_STAR_DASH",
    "STAR": "WARP_STAR_DASH",
    "HOVER": "HOVER_FLOAT",
    "FLOAT": "HOVER_FLOAT",
    "FLY": "HOVER_FLOAT",
    "INHALE": "INHALE_VORTEX",
    "VORTEX": "INHALE_VORTEX",
    "SUCK": "INHALE_VORTEX",
    "SNOOZE": "SNOOZE_CATNAP",
    "SLEEP": "SNOOZE_CATNAP",
    "CATNAP": "SNOOZE_CATNAP",
    "PAINTER": "EASEL_PAINTER",
    "EASEL": "EASEL_PAINTER",
    "PAINT": "EASEL_PAINTER",
    "ARTIST": "EASEL_PAINTER",
    "BRAWLER": "ACE_BRAWLER",
    "FIGHTER": "ACE_BRAWLER",
    "ACE": "ACE_BRAWLER",
    "LASER": "ACE_BRAWLER",
    "MAGIC": "MAGICIAN",
    "MAGICIAN_KIRBY": "MAGICIAN",
    "WIZARD": "MAGICIAN",
    "SWORD": "SWORD_HERO",
    "HERO": "SWORD_HERO",
    "CHEF": "CHEF_GOURMET",
    "COOK": "CHEF_GOURMET",
    "CAR": "CAR_MOUTH",
    "CAR_KIRBY": "CAR_MOUTH",
    "FISH": "STAR_FISHING",
    "FISHING": "STAR_FISHING",
    "NOID": "NOID_CHAOS",
    "CHAOS": "NOID_CHAOS",
    "ANNOY": "ANNOYING_POYO",
    "ANNOYING": "ANNOYING_POYO",
    "LOUD": "ANNOYING_POYO",
    "MEGAPHONE": "ANNOYING_POYO",
    "PIZZA": "PIZZA_HEIST",
    "HEIST": "PIZZA_HEIST",
    "THIEF": "PIZZA_HEIST",
    "GOBLIN": "GOBLIN_DANCE",
    "DANCE": "GOBLIN_DANCE",
    "WIGGLE": "GOBLIN_DANCE",
    "FAINT": "DRAMATIC_FAINT",
    "DRAMA": "DRAMATIC_FAINT",
    "MELODRAMA": "DRAMATIC_FAINT",
    "METTAUR": "METTAUR_HELMET",
    "HARDHAT": "METTAUR_HELMET",
    "HELMET": "METTAUR_HELMET",
    "CONSTRUCTION": "METTAUR_HELMET",
    "MINION": "MINION_BUDDY",
    "BOB": "MINION_BUDDY",
    "BANANA": "MINION_BUDDY",
    "METROID": "METROID_BUDDY",
    "BABY": "METROID_BUDDY",
    "ALIEN": "METROID_BUDDY",
    "TOOLBOX": "TOOLBOX_ENGINEER",
    "ENGINEER": "TOOLBOX_ENGINEER",
    "TOOLS": "TOOLBOX_ENGINEER",
    "WORKBENCH": "TOOLBOX_ENGINEER",
}

# =============================================================================
# CORE UTILITY FUNCTIONS
# =============================================================================

def resolve_sprite_name(name: str) -> str:
    """
    Resolve a user-provided sprite name or alias (case-insensitive, allows hyphens).
    Raises ValueError if name cannot be resolved.
    """
    cleaned = name.strip().upper().replace("-", "_")
    if cleaned in SPRITES:
        return cleaned
    if cleaned in SPRITE_ALIASES:
        return SPRITE_ALIASES[cleaned]
    
    # Prefix search
    for canonical in SPRITES:
        if canonical.startswith(cleaned) or cleaned in canonical:
            return canonical
            
    available = ", ".join(list_sprites())
    raise ValueError(f"Unknown sprite '{name}'. Available sprites: {available}")

def list_sprites() -> List[str]:
    """Return an ordered list of all canonical sprite names."""
    return list(SPRITES.keys())

def get_sprite(sprite_name: str) -> List[str]:
    """Return the list of multi-line ANSI frame strings for a sprite."""
    canonical = resolve_sprite_name(sprite_name)
    return SPRITES[canonical]

def render_frame(frame: str, header: str = "", footer: str = "", clear: bool = True, center: bool = False):
    """
    Render a single multi-line frame to stdout with optional header, footer, and screen clearing.
    """
    term_width = shutil.get_terminal_size((80, 24)).columns
    lines = frame.split("\n")
    
    output_lines = []
    if header:
        output_lines.append(header)
    
    for line in lines:
        if center:
            vis_len = visible_length(line)
            pad = max(0, (term_width - vis_len) // 2)
            output_lines.append(" " * pad + line + "\033[K")
        else:
            output_lines.append(line + "\033[K")
            
    if footer:
        output_lines.append(footer)
        
    full_output = "\n".join(output_lines)
    
    if clear:
        # Reposition cursor home and overwrite
        sys.stdout.write("\033[H" + full_output + "\n")
    else:
        sys.stdout.write(full_output + "\n")
        
    sys.stdout.flush()

# =============================================================================
# ANIMATION PLAYERS
# =============================================================================

def play_animation(
    sprite_name: str,
    duration_sec: Optional[float] = None,
    fps: Optional[float] = None,
    center: bool = False
) -> None:
    """
    Play a Kirby sprite animation in the terminal.
    
    Parameters:
      sprite_name: Canonical name or alias of the sprite to play.
      duration_sec: How long to run the animation in seconds. If None or <= 0, runs
                    indefinitely until interrupted (Ctrl+C).
      fps: Frames per second. If None, uses the sprite's recommended FPS.
      center: Whether to center the sprite horizontally in the terminal.
    """
    canonical = resolve_sprite_name(sprite_name)
    frames = SPRITES[canonical]
    frame_count = len(frames)
    
    target_fps = fps if (fps and fps > 0) else SPRITE_DEFAULT_FPS.get(canonical, 5.0)
    frame_delay = 1.0 / target_fps
    
    desc = SPRITE_DESCRIPTIONS.get(canonical, "")
    term_width = min(80, shutil.get_terminal_size((80, 24)).columns)
    bar = "━" * (term_width - 2)
    
    # Hide cursor and clear screen
    sys.stdout.write("\033[?25l\033[2J")
    sys.stdout.flush()
    
    start_time = time.time()
    frame_idx = 0
    
    try:
        while True:
            current_frame = frames[frame_idx % frame_count]
            current_num = (frame_idx % frame_count) + 1
            
            header = (
                rf"{PINK}★{RESET}{bar}{PINK}★{RESET}\n"
                f"  {BOLD}{WHITE}KIRBY ANIMATION:{RESET} {GOLD}[{canonical}]{RESET} "
                rf"{DARK_GRAY}(Frame {current_num}/{frame_count} @ {target_fps:.1f} FPS){RESET}\n"
                rf"  {ITALIC}{SKY_BLUE}{desc}{RESET}\n"
                f"{PINK}★{RESET}{bar}{PINK}★{RESET}"
            )
            
            if duration_sec and duration_sec > 0:
                elapsed = time.time() - start_time
                remaining = max(0.0, duration_sec - elapsed)
                footer = f"\n  {DARK_GRAY}[Time remaining: {remaining:4.1f}s | Press Ctrl+C to exit]{RESET}"
            else:
                footer = f"\n  {DARK_GRAY}[Looping continuously | Press Ctrl+C to stop]{RESET}"
                
            render_frame(current_frame, header=header, footer=footer, clear=True, center=center)
            
            frame_idx += 1
            time.sleep(frame_delay)
            
            if duration_sec and duration_sec > 0:
                if (time.time() - start_time) >= duration_sec:
                    break
                    
    except KeyboardInterrupt:
        pass
    finally:
        # Restore cursor and clean line
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()

def play_all(duration_per_sprite: float = 3.5, fps: Optional[float] = None, center: bool = False) -> None:
    """
    Play all Kirby animations in sequence.
    """
    all_sprites = list_sprites()
    total = len(all_sprites)
    
    sys.stdout.write("\033[?25l\033[2J\033[H")
    banner = f"""
{GOLD}★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★{RESET}
  {BOLD}{PINK}★  ANTIGRAVITY MESH: KIRBY TERMINAL ANIMATION SHOWCASE  ★{RESET}
  {WHITE}Playing all {total} animated Kirby sprites ({duration_per_sprite:.1f}s each){RESET}
{GOLD}★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★{RESET}
"""
    sys.stdout.write(banner + "\n")
    sys.stdout.flush()
    time.sleep(1.2)
    
    try:
        for idx, name in enumerate(all_sprites, 1):
            play_animation(name, duration_sec=duration_per_sprite, fps=fps, center=center)
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h\n")
        sys.stdout.write(f"\n{HOT_PINK}(> ^‿^ )>{RESET} {BOLD}{GOLD}[Demo Complete! Poyo!]{RESET}\n\n")
        sys.stdout.flush()

def print_static_sheet(sprite_name: Optional[str] = None) -> None:
    """
    Print static frames of one or all sprites. Useful for inspectability,
    non-interactive environments, and capturing text art.
    """
    targets = [resolve_sprite_name(sprite_name)] if sprite_name else list_sprites()
    
    for name in targets:
        frames = SPRITES[name]
        desc = SPRITE_DESCRIPTIONS.get(name, "")
        print(f"\n{GOLD}╔══════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{GOLD}║{RESET}  {BOLD}{PINK}{name:18}{RESET} {DARK_GRAY}({len(frames)} frames){RESET}                                  {GOLD}║{RESET}")
        print(f"{GOLD}║{RESET}  {SKY_BLUE}{desc:<64}{RESET}  {GOLD}║{RESET}")
        print(f"{GOLD}╚══════════════════════════════════════════════════════════════════════╝{RESET}")
        
        for f_idx, frame in enumerate(frames, 1):
            print(f"\n{DARK_GRAY}--- Frame {f_idx}/{len(frames)} ---{RESET}")
            print(frame)
        print()

def print_sprite_table() -> None:
    """Print a clean summary table of all available sprites and their details."""
    print(f"\n{GOLD}★ Available Kirby ASCII Sprite Animations ★{RESET}")
    print(f"{DARK_GRAY}{'─' * 76}{RESET}")
    print(f"{BOLD}{'Name':<18} {'Frames':<8} {'Rec FPS':<10} {'Description'}{RESET}")
    print(f"{DARK_GRAY}{'─' * 76}{RESET}")
    for name, frames in SPRITES.items():
        fps = SPRITE_DEFAULT_FPS.get(name, 5.0)
        desc = SPRITE_DESCRIPTIONS.get(name, "")
        print(f"{PINK}{name:<18}{RESET} {WHITE}{len(frames):<8}{RESET} {CYAN}{fps:<10.1f}{RESET} {desc}")
    print(f"{DARK_GRAY}{'─' * 76}{RESET}\n")

# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="★ AntiGravity Mesh: Kirby ANSI ASCII Terminal Sprite Animator ★",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python3 kirby_ascii_sprites.py demo
  python3 kirby_ascii_sprites.py all
  python3 kirby_ascii_sprites.py idle_bounce
  python3 kirby_ascii_sprites.py warp_star_dash --duration 5 --fps 8
  python3 kirby_ascii_sprites.py --list
  python3 kirby_ascii_sprites.py --static
        """
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Sprite name (e.g. idle_bounce, warp_star_dash), 'demo', or 'all'"
    )
    parser.add_argument(
        "-d", "--duration",
        type=float,
        default=None,
        help="Animation duration in seconds (default: infinite for single sprite, 3.5s per sprite in demo)"
    )
    parser.add_argument(
        "-f", "--fps",
        type=float,
        default=None,
        help="Custom playback speed in frames per second"
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all available Kirby sprite animations and exit"
    )
    parser.add_argument(
        "-s", "--static",
        action="store_true",
        help="Print static frames without running terminal animation"
    )
    parser.add_argument(
        "-c", "--center",
        action="store_true",
        help="Center sprite horizontally in the terminal window"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color codes (renders in plain text)"
    )

    args = parser.parse_args()

    # Handle --no-color
    if args.no_color or os.environ.get("NO_COLOR"):
        global RESET, BOLD, DIM, ITALIC, PINK, HOT_PINK, ROSE, RED, DARK_RED
        global GOLD, YELLOW, CYAN, SKY_BLUE, BLUE, DEEP_BLUE, PURPLE, MAGENTA
        global GREEN, ORANGE, BROWN, WHITE, GRAY, DARK_GRAY
        RESET = BOLD = DIM = ITALIC = ""
        PINK = HOT_PINK = ROSE = RED = DARK_RED = ""
        GOLD = YELLOW = CYAN = SKY_BLUE = BLUE = DEEP_BLUE = PURPLE = MAGENTA = ""
        GREEN = ORANGE = BROWN = WHITE = GRAY = DARK_GRAY = ""

    if args.list:
        print_sprite_table()
        sys.exit(0)

    # Static frame print mode
    if args.static:
        target = args.target if (args.target and args.target.lower() not in ("all", "demo")) else None
        print_static_sheet(target)
        sys.exit(0)

    # Default to demo if no target specified
    target = args.target
    if target is None:
        print_sprite_table()
        print(f"{YELLOW}★ No target specified. Launching Kirby Showcase Demo! ★{RESET}")
        time.sleep(1.0)
        target = "demo"

    target_lower = target.lower()

    if target_lower in ("demo", "all"):
        dur = args.duration if args.duration else 3.5
        play_all(duration_per_sprite=dur, fps=args.fps, center=args.center)
    else:
        try:
            canonical = resolve_sprite_name(target)
            play_animation(canonical, duration_sec=args.duration, fps=args.fps, center=args.center)
        except ValueError as e:
            print(f"{RED}Error:{RESET} {e}")
            print_sprite_table()
            sys.exit(1)

if __name__ == "__main__":
    main()
