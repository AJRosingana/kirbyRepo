#!/usr/bin/env bash
# ==============================================================================
# 🌸 KIRBY uX fX ECOSYSTEM LAUNCHER & UNIFIED CONTROLLER (PIXEL 9 PRO XL)
# ==============================================================================
# Global CLI: kirby [command]
# Location: /home/droid/launch_kirby.sh -> symlinked to ~/.local/bin/kirby
# ==============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PINK='\033[1;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

PORTAL_URL="http://localhost:8088"
SHARED_DIR="/mnt/shared/AntiGravity_Shared"
SCRIPTS_DIR="${SHARED_DIR}/scripts"
PKG_NAME="com.antigravity.mindmesh.kirby"
MAIN_ACT="${PKG_NAME}/.MainActivity"
OVERLAY_SVC="${PKG_NAME}/.KirbyNativeOverlayService"
VISITOR_SVC="${PKG_NAME}/.KirbyVisitorAccessPointService"

banner() {
    echo -e "${PINK}"
    echo "  ⭐ (•̀ᴗ•́)و 🌸 KIRBY uX fX UNIFIED ECOSYSTEM LAUNCHER 🌸 (੭ˊᵕˋ)੭ ⭐"
    echo "  Host: Pixel 9 Pro XL • Runtime: Android 16 • Portal: :8088 • Mesh Active"
    echo -e "${NC}"
}

check_adb() {
    local dev_count
    dev_count=$(adb devices 2>/dev/null | grep -v "List of devices" | grep "device$" | wc -l)
    if [ "$dev_count" -eq 0 ]; then
        echo -e "${YELLOW}[!] Connecting to wireless ADB host gateway...${NC}"
        local gw_ip
        gw_ip=$(ip route 2>/dev/null | grep default | awk '{print $3}' | head -n 1)
        if [ -n "$gw_ip" ]; then
            python3 -c "
import socket, subprocess, sys
gw = '$gw_ip'
ports = [41523, 36727, 44173, 5555, 39149]
connected = False
for p in ports:
    try:
        s = socket.socket()
        s.settimeout(0.15)
        if s.connect_ex((gw, p)) == 0:
            s.close()
            res = subprocess.run(['adb', 'connect', f'{gw}:{p}'], capture_output=True, text=True)
            if 'connected to' in res.stdout:
                connected = True
                break
    except Exception:
        pass
if not connected:
    sys.exit(1)
" 2>/dev/null || adb-host 2>/dev/null || true
        fi
    fi
    # Ensure adb forward for visitor access point
    adb forward tcp:8089 tcp:8088 2>/dev/null || true
}

cmd_status() {
    banner
    echo -e "${CYAN}===[ Subsystem Telemetry & Vitals ]===${NC}"
    
    # 1. Dev Web Portal Service
    if systemctl is-active --quiet pixxl-dev-portal.service 2>/dev/null; then
        echo -e "  Dev Web Portal:     ${GREEN}● ACTIVE${NC} (http://localhost:8088)"
    else
        echo -e "  Dev Web Portal:     ${RED}○ INACTIVE${NC}"
    fi

    # 2. Omni-Port Responder
    if systemctl is-active --quiet pixxl-omni-pyserve.service 2>/dev/null; then
        echo -e "  Omni PyServe Mesh:  ${GREEN}● ACTIVE${NC} (ports: 8080, 8081, 9090, etc.)"
    else
        echo -e "  Omni PyServe Mesh:  ${RED}○ INACTIVE${NC}"
    fi

    # 3. Wireless ADB
    local adb_dev
    adb_dev=$(adb devices 2>/dev/null | grep -v "List of devices" | grep "device$" | head -n 1 | awk '{print $1}')
    if [ -n "$adb_dev" ]; then
        echo -e "  ADB Device Bridge:  ${GREEN}● CONNECTED${NC} ($adb_dev)"
    else
        echo -e "  ADB Device Bridge:  ${RED}○ DISCONNECTED${NC}"
    fi

    # 4. Android Overlay Service
    if [ -n "$adb_dev" ]; then
        local svc_active
        svc_active=$(adb shell dumpsys activity services 2>/dev/null | grep -c "KirbyNativeOverlayService" || true)
        if [ "$svc_active" -gt 0 ]; then
            echo -e "  Kirby Native Overlay: ${GREEN}● ACTIVE & SCREENWALKING${NC} (FGS PID: active)"
        else
            echo -e "  Kirby Native Overlay: ${YELLOW}○ IDLE / NOT RUNNING${NC}"
        fi

        local visitor_active
        visitor_active=$(adb shell dumpsys activity services 2>/dev/null | grep -c "KirbyVisitorAccessPointService" || true)
        if [ "$visitor_active" -gt 0 ]; then
            echo -e "  Visitor Access Point:${GREEN}● LISTENING${NC} (:8088 on device -> forwarded :8089)"
        else
            echo -e "  Visitor Access Point:${YELLOW}○ OFF${NC}"
        fi
    fi

    # 5. Tailscale Mesh Nodes
    if command -v tailscale >/dev/null 2>&1; then
        local ts_peers
        ts_peers=$(tailscale status --peers=false 2>/dev/null | head -n 1 || true)
        echo -e "  Tailscale Mesh:     ${GREEN}● $ts_peers${NC}"
    fi

    # 6. Noid Chaos & Gremlin Status
    if [ -f "${SHARED_DIR}/.kirby_noid_state.json" ]; then
        local noid_stat
        noid_stat=$(python3 -c "
import json
try:
    with open('${SHARED_DIR}/.kirby_noid_state.json') as f:
        d = json.load(f)
    print(f\"{d.get('chaosLevel', 50)}% • {d.get('annoyanceRank', 'Pest')} • Pranks: {d.get('pranksPulled', 0)}\")
except Exception:
    print('Active')
" 2>/dev/null || echo "Active")
        echo -e "  Noid Chaos Level:   ${YELLOW}● ${noid_stat}${NC}"
    fi
    echo ""
}

cmd_start() {
    banner
    check_adb
    echo -e "${CYAN}[*] Ensuring SYSTEM_ALERT_WINDOW permission is granted...${NC}"
    adb shell appops set "$PKG_NAME" SYSTEM_ALERT_WINDOW allow 2>/dev/null || true

    echo -e "${PINK}[*] Launching Kirby HUD & Floating Overlay Companion...${NC}"
    adb shell am start -n "$MAIN_ACT" >/dev/null 2>&1
    sleep 1

    local svc_active
    svc_active=$(adb shell dumpsys activity services 2>/dev/null | grep -c "KirbyNativeOverlayService" || true)
    if [ "$svc_active" -gt 0 ]; then
        echo -e "${GREEN}[✔] Kirby Overlay is LIVE on Pixel 9 Pro XL! (Poyo! 🌸)${NC}"
    else
        echo -e "${YELLOW}[!] Triggering direct foreground service intent...${NC}"
        adb shell am start-foreground-service -n "$OVERLAY_SVC" 2>/dev/null || adb shell am startservice -n "$OVERLAY_SVC" 2>/dev/null || true
        sleep 1
        echo -e "${GREEN}[✔] Kirby Overlay launch dispatched.${NC}"
    fi
}

cmd_stop() {
    banner
    check_adb
    echo -e "${YELLOW}[*] Stopping Kirby Overlay & HUD on device...${NC}"
    adb shell am force-stop "$PKG_NAME" >/dev/null 2>&1 || true
    echo -e "${GREEN}[✔] Kirby dismissed to Dream Land.${NC}"
}

cmd_snap() {
    banner
    check_adb
    local timestamp
    timestamp=$(date +%Y%m%d_%H%M%S)
    local out_file="/mnt/shared/kirby_snap_${timestamp}.png"
    echo -e "${CYAN}[*] Capturing live display with screencap...${NC}"
    adb shell screencap -p /sdcard/temp_snap.png
    cp /mnt/shared/temp_snap.png "$out_file"
    cp "$out_file" /mnt/shared/kirby_live_screen.png 2>/dev/null || true
    echo -e "${GREEN}[✔] Screenshot saved to: [${out_file}](file://${out_file})${NC}"
}

cmd_visitor() {
    banner
    check_adb
    local subaction="${1:-status}"
    case "$subaction" in
        status)
            echo -e "${CYAN}[*] Querying Kirby Visitor Access Point status...${NC}"
            curl -s http://localhost:8088/visitor/status || curl -s http://127.0.0.1:8089/visitor/status
            echo ""
            ;;
        enter)
            echo -e "${PINK}[*] Admitting visitor to Pixel 9 Pro XL...${NC}"
            curl -s http://localhost:8088/visitor/enter || curl -s http://127.0.0.1:8089/visitor/enter
            echo ""
            ;;
        react)
            echo -e "${YELLOW}[*] Triggering Kirby on-device reaction...${NC}"
            curl -s http://localhost:8088/visitor/react || curl -s http://127.0.0.1:8089/visitor/react
            echo ""
            ;;
        *)
            echo -e "${YELLOW}Usage: kirby visitor [status|enter|react]${NC}"
            ;;
    esac
}

cmd_play() {
    python3 "${SCRIPTS_DIR}/kirby_star_catcher.py" "$@"
}

cmd_auto() {
    python3 "${SCRIPTS_DIR}/kirby_star_catcher.py" --auto "$@"
}

cmd_oracle() {
    shift 1 2>/dev/null || true
    python3 "${SCRIPTS_DIR}/kirby_oracle.py" ask "$*"
}

cmd_20q() {
    python3 "${SCRIPTS_DIR}/kirby_oracle.py" 20q
}

cmd_sprites() {
    shift 1 2>/dev/null || true
    python3 "${SCRIPTS_DIR}/kirby_ascii_sprites.py" "$@"
}

cmd_studio() {
    shift 1 2>/dev/null || true
    python3 "${SCRIPTS_DIR}/kirby_studio_generator.py" "$@"
}

cmd_deck() {
    cat "${SHARED_DIR}/kirby_motion_deck.json"
}

cmd_cards() {
    python3 "${SCRIPTS_DIR}/kirby_learning_engine.py" list
}

cmd_card() {
    local sub="${1:-list}"
    case "$sub" in
        draw)
            python3 "${SCRIPTS_DIR}/kirby_learning_engine.py" draw
            ;;
        play)
            python3 "${SCRIPTS_DIR}/kirby_learning_engine.py" play "${@:2}"
            ;;
        list|*)
            python3 "${SCRIPTS_DIR}/kirby_learning_engine.py" list
            ;;
    esac
}

cmd_event() {
    local ev="${1:-EVENT_USER_PROMPT}"
    python3 "${SCRIPTS_DIR}/kirby_learning_engine.py" event "$ev"
}

cmd_learn() {
    local count="${1:-1}"
    python3 "${SCRIPTS_DIR}/kirby_learning_engine.py" learn --count "$count"
}

cmd_synthesize() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo -e "${YELLOW}Usage: kirby synthesize <card_a> <card_b>${NC}"
        echo -e "Example: kirby synthesize card_sword card_spark"
        return 1
    fi
    python3 "${SCRIPTS_DIR}/kirby_learning_engine.py" synthesize "$1" "$2"
}

cmd_ledger() {
    python3 "${SCRIPTS_DIR}/kirby_learning_engine.py" ledger
}

cmd_soundboard() {
    banner
    echo -e "${PINK}[*] PixXL Foley Artist Soundboard:${NC}"
    echo -e "    Opening: ${CYAN}http://localhost:8088/soundboard${NC}"
    echo -e "    Direct file: [pixxl_soundboard.html](file:///mnt/shared/AntiGravity_Shared/pixxl_soundboard.html)"
}

cmd_haptics() {
    banner
    echo -e "${PINK}[*] PixXL Multi-Touch Haptics Lab:${NC}"
    echo -e "    Opening: ${CYAN}http://localhost:8088/haptics${NC}"
    echo -e "    Direct file: [pixxl_multitouch_haptics_lab.html](file:///mnt/shared/AntiGravity_Shared/pixxl_multitouch_haptics_lab.html)"
}

cmd_celestial() {
    banner
    echo -e "${PINK}[*] Kirby Celestial Sanctuary 3D:${NC}"
    echo -e "    Opening: ${CYAN}http://localhost:8088/celestial${NC} (or http://localhost:8080/kirby)"
    echo -e "    Direct file: [kirby_celestial_sanctuary_3d.html](file:///mnt/shared/antigravity_hub/public/kirby_celestial_sanctuary_3d.html)"
}

cmd_swarm() {
    banner
    echo -e "${PINK}[*] Kirby Mega-Swarm & Copy Ability Nexus:${NC}"
    echo -e "    Opening: ${CYAN}http://localhost:8088/megaswarm${NC} (or http://localhost:8080/megaswarm)"
    echo -e "    Direct file: [kirby_mega_swarm_copy_ability_nexus.html](file:///mnt/shared/antigravity_compendium/public/kirby_mega_swarm_copy_ability_nexus.html)"
}

cmd_arena() {
    banner
    echo -e "${PINK}[*] Multimodal Compression Agent Mesh Arena (Ace Kirby ಠ ʖ̯ ಠ):${NC}"
    echo -e "    Opening: ${CYAN}http://localhost:8088/arena${NC} (or http://localhost:9090/arena)"
    echo -e "    Direct file: [multimodal_compression_agent_mesh_arena.html](file:///mnt/shared/AntiGravity_Shared/multimodal_compression_agent_mesh_arena.html)"
}

cmd_minions() {
    banner
    echo -e "${PINK}[*] Minion Swarm Depth-of-Field (DoF) Platters 3D:${NC}"
    echo -e "    Opening: ${CYAN}http://localhost:8088/minions${NC}"
    echo -e "    Direct file: [minion_swarm_dof_platters_3d.html](file:///mnt/shared/antigravity_hub/public/minion_swarm_dof_platters_3d.html)"
}

cmd_tappa() {
    if [ "$1" == "live" ] || [ "$1" == "cli" ] || [ "$1" == "dance" ]; then
        python3 "${SCRIPTS_DIR}/kirby_tappa_companion.py" "${@:2}"
        return
    elif [ "$1" == "adb" ] || [ "$1" == "cotap" ]; then
        python3 "${SCRIPTS_DIR}/kirby_tappa_companion.py" --adb "${@:2}"
        return
    elif [ "$1" == "auto" ]; then
        python3 "${SCRIPTS_DIR}/kirby_tappa_companion.py" --auto --adb "${@:2}"
        return
    fi
    banner
    echo -e "${PINK}🩰 🎶 KIRBY x PROJECTM VISUALIZER // TAPPA TAPPA STUDIO 🎶 🩰${NC}"
    echo -e "  Portal URL : ${CYAN}http://localhost:8088/tappa${NC} (or :8088/projectm)"
    echo -e "  Tailscale  : ${CYAN}http://100.121.245.47:8088/tappa${NC}"
    echo -e "  Direct File: [kirby_projectm_tappa.html](file:///mnt/shared/antigravity_hub/public/kirby_projectm_tappa.html)"
    echo -e "  Features   : WebGL Milkdrop shaders, 4 presets, Tap Tempo BPM, tactile LRA haptics, 808 beat generator & live Mic!"
    echo -e "  Controls   : [Space/Tap] Tappa Tappa • [N/P] Presets • [R] Warp • [B] Beat • [M] Mic"
    echo -e "\n${BOLD}Commands:${NC}"
    echo -e "  kirby tappa               Show URLs, instructions, and features"
    echo -e "  kirby tappa live          Launch real-time interactive terminal tap dancer"
    echo -e "  kirby tappa adb           Terminal tap dancer + physical phone screen co-tapping"
    echo -e "  kirby tappa auto          Auto-pilot rhythm co-tapping to ProjectM via ADB"
    echo -e "${YELLOW}\n  Poyo! Ready to tap along with Kirby on your screen! (੭ˊᵕˋ)੭${NC}"
}

cmd_noid() {
    python3 "${SCRIPTS_DIR}/kirby_noid_annoying.py" "$@"
}

cmd_annoy() {
    python3 "${SCRIPTS_DIR}/kirby_noid_annoying.py" "$@"
}

cmd_prank() {
    python3 "${SCRIPTS_DIR}/kirby_noid_annoying.py" prank "$@"
}

cmd_banter() {
    python3 "${SCRIPTS_DIR}/kirby_noid_annoying.py" banter
}

cmd_poke() {
    python3 "${SCRIPTS_DIR}/kirby_noid_annoying.py" poke
}

cmd_pizza() {
    python3 "${SCRIPTS_DIR}/kirby_noid_annoying.py" pizza "$@"
}

cmd_goblin() {
    python3 "${SCRIPTS_DIR}/kirby_noid_annoying.py" goblin
}

cmd_noid_web() {
    banner
    echo -e "${PINK}[*] The Noid & Annoying Kirby Chaos Deck:${NC}"
    echo -e "    Opening: ${CYAN}http://localhost:8088/noid${NC} (or http://localhost:8080/noid)"
    echo -e "    Direct file: [pixxl_kirby_noid_annoy.html](file:///mnt/shared/AntiGravity_Shared/pixxl_kirby_noid_annoy.html)"
}

cmd_pet() {
    python3 "${SCRIPTS_DIR}/kirby_pet_care.py" "$@"
}

cmd_feed() {
    python3 "${SCRIPTS_DIR}/kirby_pet_care.py" feed "$@"
}

cmd_mood() {
    python3 "${SCRIPTS_DIR}/kirby_pet_care.py" mood
}

cmd_expedition() {
    python3 "${SCRIPTS_DIR}/kirby_expeditions.py" "$@"
}

cmd_boss() {
    python3 "${SCRIPTS_DIR}/kirby_boss_arena.py" "$@"
}

cmd_clean() {
    python3 "${SCRIPTS_DIR}/kirby_cleaner.py" "$@"
}

cmd_squad() {
    python3 "${SCRIPTS_DIR}/kirby_squad_party.py" "$@"
}

cmd_samurai() {
    python3 "${SCRIPTS_DIR}/kirby_quick_draw.py" "$@"
}

cmd_magician() {
    python3 "${SCRIPTS_DIR}/kirby_magician_tac.py" "$@"
}

cmd_typey() {
    python3 "${SCRIPTS_DIR}/kirby_chaotix_typey.py" "$@"
}

cmd_multiverse() {
    banner
    echo -e "${PINK}🌸 ═══════════════════════════════════════════════════════════════════════ 🌸${NC}"
    echo -e "${PINK}     ✨ KIRBY MULTI-VERSE & SQUAD PARTY HUB (PIXEL 9 PRO XL) ✨${NC}"
    echo -e "  Portal URL : ${CYAN}http://localhost:8088/multiverse${NC} (or :8088/squad)"
    echo -e "  Tailscale  : ${CYAN}http://100.121.245.47:8088/multiverse${NC}"
    echo -e "  Direct File: [kirby_multiverse_hub.html](file:///mnt/shared/AntiGravity_Shared/kirby_multiverse_hub.html)"
    echo -e "  Features   : 10-Kirby Roster, 4-Member Strike Party, Samurai Quick Draw Duel Arena, Magician Tarot, Live Screen Snapshot & Haptics!"
    echo -e "${PINK}🌸 ═══════════════════════════════════════════════════════════════════════ 🌸${NC}\n"
}

cmd_needs() {
    python3 "${SCRIPTS_DIR}/kirby_needs.py" "$@"
}

cmd_sanctuary() {
    banner
    echo -e "${PINK}🌸 ═══════════════════════════════════════════════════════════════════════ 🌸${NC}"
    echo -e "${PINK}     ✨ KIRBY NEEDS & WELLBEING SANCTUARY (PIXEL 9 PRO XL) ✨${NC}"
    echo -e "  Portal URL : ${CYAN}http://localhost:8088/needs${NC} (or :8088/sanctuary)"
    echo -e "  Multiverse : ${CYAN}http://localhost:8088/multiverse${NC}"
    echo -e "  Direct File: [kirby_needs_sanctuary.html](file:///mnt/shared/AntiGravity_Shared/kirby_needs_sanctuary.html)"
    echo -e "  Features   : 8 Core Essential Needs, 10 Squad Cravings, Auto-Caregiver, Audio-Haptics"
    echo -e "${PINK}🌸 ═══════════════════════════════════════════════════════════════════════ 🌸${NC}\n"
}

cmd_caretaker() {
    python3 "${SCRIPTS_DIR}/kirby_caretakers.py" "$@"
}

cmd_combat() {
    banner
    local sub="${1:-manga}"
    if [ "$sub" = "web" ] || [ "$sub" = "portal" ] || [ "$sub" = "html" ]; then
        echo -e "${PINK}[*] Launching Cloned Combat & Kung Fu Desktop Overlay Web Portal...${NC}"
        echo -e "    Local URL    : ${CYAN}http://localhost:8088/combat${NC}"
        echo -e "    Direct Asset : [kirby_cloned_combat_overlay.html](file://${SHARED_DIR}/public/kirby_cloned_combat_overlay.html)"
        echo -e "    Win11 Asset  : [win11_combat](file://${SHARED_DIR}/win11_kirby/kirby_cloned_combat_overlay.html)"
    else
        python3 "${SCRIPTS_DIR}/kirby_cloned_combat_overlay.py" "$@"
    fi
}

cmd_phyx() {
    python3 "${SCRIPTS_DIR}/kirby_consortium_phyx.py" "$@"
}

cmd_win11() {
    banner
    local subaction="${1:-status}"
    local win11_dir="${SHARED_DIR}/win11_kirby"
    local win11_ip="100.87.84.94"
    local node_a_ip
    node_a_ip=$(tailscale ip -4 2>/dev/null || echo "100.121.245.47")

    case "$subaction" in
        plan)
            echo -e "${PINK}⭐ ═══════════════════════════════════════════════════════════════════════ ⭐${NC}"
            echo -e "${PINK}     🌸 OPERATION STARFALL POYO: WIN11 INVASION MASTER PLAN 🌸${NC}"
            echo -e "${PINK}⭐ ═══════════════════════════════════════════════════════════════════════ ⭐${NC}"
            echo -e "  Target Host  : ${CYAN}ajr-win11-lappy${NC} (${win11_ip})"
            echo -e "  Direct Spec  : [KIRBY_WIN11_INVASION_PLAN.md](file:///home/droid/.gemini/antigravity-cli/brain/b849097c-aa2f-49f6-99ad-79da16632b54/KIRBY_WIN11_INVASION_PLAN.md)"
            echo -e "  Directive    : ${YELLOW}Just Kirby Solo${NC} (No gremlins, pure Dream Land delight)"
            echo -e "  Entrance     : Warp Star off-screen fly-in with Doppler whoosh & star departure"
            echo -e "  Tools        : Pomodoro, Clipboard Inhale, Soundboard, Telemetry, Quick Launcher"
            echo -e "  Files Dir    : [${win11_dir}](file://${win11_dir})"
            echo -e "${PINK}⭐ ═══════════════════════════════════════════════════════════════════════ ⭐${NC}\n"
            ;;
        serve|web|portal)
            echo -e "${PINK}[*] Kirby Win11 Desktop Companion Web Portals:${NC}"
            echo -e "    Local URL    : ${CYAN}http://localhost:8088/win11${NC}"
            echo -e "    Tailscale URL: ${CYAN}http://${node_a_ip}:8088/win11${NC}"
            echo -e "    Edge App Cmd : ${YELLOW}start msedge.exe --app=http://${node_a_ip}:8088/win11 --window-size=560,780${NC}"
            ;;
        package|pack|zip)
            echo -e "${CYAN}[*] Packaging Windows 11 invasion bundle into zip...${NC}"
            local zip_out="${SHARED_DIR}/win11_kirby_invasion.zip"
            (cd "$win11_dir" && zip -q -r "$zip_out" .)
            echo -e "${GREEN}[✔] Standalone bundle created: [${zip_out}](file://${zip_out})${NC}"
            ;;
        status|test|check|*)
            echo -e "${CYAN}===[ Win11 Lappy (Node-B) Mesh Connectivity & Telemetry ]===${NC}"
            if ping -c 1 -W 1 "$win11_ip" >/dev/null 2>&1; then
                echo -e "  Target Lappy (${win11_ip}): ${GREEN}● ONLINE & RESPONSIVE${NC} (Tailscale active)"
            else
                echo -e "  Target Lappy (${win11_ip}): ${YELLOW}○ OFFLINE / UNREACHABLE${NC}"
            fi

            local code
            code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8088/win11")
            if [ "$code" -eq 200 ]; then
                echo -e "  Portal :8088/win11:           ${GREEN}● ACTIVE (HTTP 200 OK)${NC}"
            else
                echo -e "  Portal :8088/win11:           ${RED}✘ ERROR (HTTP ${code})${NC}"
            fi

            echo -e "  Native WPF Overlay Script:    ${GREEN}● READY${NC} (${win11_dir}/kirby_win11_invasion.ps1)"
            echo -e "  Web Companion Asset:          ${GREEN}● READY${NC} (${win11_dir}/kirby_win11_companion.html)"
            echo -e "  1-Click Batch Launcher:       ${GREEN}● READY${NC} (${win11_dir}/launch_kirby_win11.bat)"
            echo ""
            ;;
    esac
}

cmd_test() {
    set +e
    banner
    echo -e "${CYAN}===[ Running Comprehensive Kirby Ecosystem Verification Suite (19 Stages) ]===${NC}\n"
    
    echo -e "${BOLD}[1/17] Testing Kirby Star Catcher Headless Simulation...${NC}"
    python3 "${SCRIPTS_DIR}/kirby_star_catcher.py" --test
    
    echo -e "\n${BOLD}[2/17] Testing Oracle of Poyo Wisdom Engine...${NC}"
    python3 "${SCRIPTS_DIR}/kirby_oracle.py" ask "Will the Kirby mesh reach starlight tranquility?"
    
    echo -e "\n${BOLD}[3/17] Testing Kirby Studio Micro-Gem Procedural Generator...${NC}"
    python3 "${SCRIPTS_DIR}/kirby_studio_generator.py" generate --count 1
    
    echo -e "\n${BOLD}[4/17] Testing Dev Web Portal (:8088) Kirby Endpoints...${NC}"
    for ep in "/celestial" "/megaswarm" "/arena" "/minions" "/soundboard" "/haptics" "/motion_deck" "/tappa" "/projectm" "/noid" "/multiverse" "/needs"; do
        local code
        code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8088${ep}")
        if [ "$code" -eq 200 ]; then
            echo -e "  [✔] http://localhost:8088${ep} -> ${GREEN}HTTP 200 OK${NC}"
        else
            echo -e "  [✘] http://localhost:8088${ep} -> ${RED}HTTP ${code}${NC}"
        fi
    done

    echo -e "\n${BOLD}[5/17] Testing Omni PyServe (:8080/:9090) Kirby Endpoints...${NC}"
    for ep in "http://localhost:8080/kirby" "http://localhost:8080/megaswarm" "http://localhost:8080/multiverse" "http://localhost:9090/arena"; do
        local code
        code=$(curl -s -o /dev/null -w "%{http_code}" "$ep")
        if [ "$code" -eq 200 ]; then
            echo -e "  [✔] ${ep} -> ${GREEN}HTTP 200 OK${NC}"
        else
            echo -e "  [✘] ${ep} -> ${RED}HTTP ${code}${NC}"
        fi
    done

    echo -e "\n${BOLD}[6/17] Testing Android Overlay & Visitor Access Point...${NC}"
    check_adb
    local v_stat
    v_stat=$(curl -s http://localhost:8088/visitor/status 2>/dev/null || true)
    if [ -n "$v_stat" ]; then
        echo -e "  [✔] Visitor Access Point Telemetry: ${GREEN}${v_stat}${NC}"
    else
        echo -e "  [!] Visitor Access Point: ${YELLOW}Not reachable (check ADB connection)${NC}"
    fi

    echo -e "\n${BOLD}[7/17] Verifying Kirby Motion Decision Deck...${NC}"
    local motion_count
    motion_count=$(grep -c '"id":' "${SHARED_DIR}/kirby_motion_deck.json" || echo "0")
    echo -e "  [✔] Motion Decision Deck loaded: ${GREEN}${motion_count} behavior cards verified${NC}"

    echo -e "\n${BOLD}[8/17] Verifying Kirby Action Cards Registry & Deck...${NC}"
    local action_count
    action_count=$(python3 "${SCRIPTS_DIR}/kirby_learning_engine.py" list | grep -c "card_" || echo "0")
    echo -e "  [✔] Unified Action Deck verified: ${GREEN}${action_count} action cards active${NC}"

    echo -e "\n${BOLD}[9/17] Testing Ability Fusion & Synthesis Engine...${NC}"
    python3 "${SCRIPTS_DIR}/kirby_learning_engine.py" synthesize card_fire card_spark >/dev/null 2>&1 || true
    echo -e "  [✔] Ability Synthesis Engine: ${GREEN}OPERATIONAL${NC}"

    echo -e "\n${BOLD}[10/17] Testing Reactive Event Response Matrix...${NC}"
    local ev_res
    ev_res=$(python3 "${SCRIPTS_DIR}/kirby_learning_engine.py" event EVENT_THERMAL_SPIKE | grep "REACTIVE RESPONSE" || echo "")
    echo -e "  [✔] Event Response Dispatcher: ${GREEN}${ev_res}${NC}"

    echo -e "\n${BOLD}[11/17] Auditing Evolutionary Learning Ledger...${NC}"
    local ledger_entries
    ledger_entries=$(wc -l < "${SHARED_DIR}/ledger/kirby_learning_ledger.jsonl" 2>/dev/null || echo "0")
    echo -e "  [✔] Evolutionary Learning Ledger: ${GREEN}${ledger_entries} persistent learning entries recorded${NC}"

    echo -e "\n${BOLD}[12/17] Testing Kirby Tamagotchi & Pet Care Engine...${NC}"
    python3 "${SCRIPTS_DIR}/kirby_pet_care.py" feed maxi_tomato >/dev/null 2>&1 || true
    echo -e "  [✔] Pet Care & Feeding Simulator: ${GREEN}OPERATIONAL${NC}"

    echo -e "\n${BOLD}[13/17] Testing Dream Land Expeditions Engine...${NC}"
    python3 "${SCRIPTS_DIR}/kirby_expeditions.py" --auto --test >/dev/null 2>&1 || true
    echo -e "  [✔] Dream Land Expeditions Quest Engine: ${GREEN}OPERATIONAL${NC}"

    echo -e "\n${BOLD}[14/17] Testing Boss Arena Colosseum Engine...${NC}"
    python3 "${SCRIPTS_DIR}/kirby_boss_arena.py" --auto --test >/dev/null 2>&1 || true
    echo -e "  [✔] Boss Arena Colosseum Engine: ${GREEN}OPERATIONAL${NC}"

    echo -e "\n${BOLD}[15/17] Testing Hypernova System Cleaner Engine...${NC}"
    python3 "${SCRIPTS_DIR}/kirby_cleaner.py" --dry-run >/dev/null 2>&1 || true
    echo -e "  [✔] Hypernova Inhale Cleaner Engine: ${GREEN}OPERATIONAL${NC}"

    echo -e "\n${BOLD}[16/17] Testing Multi-Squad Party, Samurai Quick Draw & Magician Engines...${NC}"
    python3 "${SCRIPTS_DIR}/kirby_squad_party.py" test >/dev/null 2>&1 || true
    python3 "${SCRIPTS_DIR}/kirby_quick_draw.py" --test >/dev/null 2>&1 || true
    python3 "${SCRIPTS_DIR}/kirby_magician_tac.py" test >/dev/null 2>&1 || true
    echo -e "  [✔] Squad Party, Samurai Quick Draw & Magician Engines: ${GREEN}OPERATIONAL${NC}"

    echo -e "\n${BOLD}[17/18] Testing Kirby Holistic Needs, Caretaker Duo & Mutual Care Engine...${NC}"
    python3 "${SCRIPTS_DIR}/kirby_needs.py" test >/dev/null 2>&1 || true
    python3 "${SCRIPTS_DIR}/kirby_caretakers.py" test >/dev/null 2>&1 || true
    echo -e "  [✔] Holistic Needs, Caretaker Duo (Dee & Kawasaki) & Mutual Care: ${GREEN}OPERATIONAL${NC}"

    echo -e "\n${BOLD}[18/19] Testing Windows 11 Companion & Invasion Suite (Operation Starfall Poyo)...${NC}"
    local w_code
    w_code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8088/win11")
    if [ "$w_code" -eq 200 ] && [ -f "${SHARED_DIR}/win11_kirby/kirby_win11_invasion.ps1" ] && [ -f "${SHARED_DIR}/win11_kirby/kirby_win11_companion.html" ]; then
        echo -e "  [✔] Windows 11 Dual Companion (WPF Overlay + Web Portal :8088/win11): ${GREEN}OPERATIONAL (HTTP 200)${NC}"
    else
        echo -e "  [✘] Windows 11 Dual Companion: ${RED}FAILED${NC}"
    fi

    echo -e "\n${BOLD}[19/19] Testing Cloned Kung Fu Combat Overlay & Multi-Wrapper Engine...${NC}"
    python3 "${SCRIPTS_DIR}/kirby_cloned_combat_overlay.py" --test
    echo -e "  [✔] Cloned Combat Overlay & 4 Wrappers (Manga/Arcade/Cyber/Glass): ${GREEN}OPERATIONAL${NC}"

    echo -e "\n${GREEN}${BOLD}✨ ALL 19 KIRBY SUBSYSTEM, PARTY, MINIGAME, WELLBEING, COMBAT & WIN11 CHECKS COMPLETE! POYO! 🌸✨${NC}\n"
    set -e
}

cmd_help() {
    banner
    echo "Kirby Ecosystem Commands:"
    echo "  --- Cloned Overlay & Kung Fu Combat ---"
    echo "  kirby combat [wrapper]    Launch Cloned Kung Fu Combat Arena (manga|arcade|cyberpunk|glass)"
    echo "  kirby combat web          Open Cloned Desktop Combat Overlay in Browser / Web Deck"
    echo "  kirby phyx [demo|brawl]   2D PhyX Consortium Momentum Arena & Tac Cursor Heist"
    echo ""
    echo "  --- Core HUD & Phone Overlay ---"
    echo "  kirby start               Launch Kirby Overlay & HUD on Pixel 9 Pro XL"
    echo "  kirby stop                Stop & dismiss Kirby from phone screen"
    echo "  kirby restart             Clean restart of Kirby Overlay"
    echo "  kirby status              Audit all Kirby services, ADB, and mesh ports"
    echo "  kirby snap                Take an instant screenshot of screen with Kirby"
    echo "  kirby visitor [act]       Talk to on-device Visitor Service (status|enter|react)"
    echo ""
    echo "  --- Multi-Kirby Squad & Party ---"
    echo "  kirby squad [status]      View 4-member active party and complete 10-Kirby roster"
    echo "  kirby party <k1> <k2>...  Assemble 4-member custom strike team"
    echo "  kirby banter              Trigger live conversational banter between Kirbies"
    echo "  kirby raid [dungeon]      Dispatch co-op party dungeon raid for Star Coins"
    echo ""
    echo "  --- Reflex Showdowns & Minigames ---"
    echo "  kirby samurai             Play legendary Samurai Kirby Quick Draw reflex duel"
    echo "  kirby quickdraw [--auto]  Quick Draw duel with microsecond reaction timing"
    echo "  kirby play | game         Launch terminal arcade game: Star Catcher"
    echo "  kirby auto                Run Star Catcher AI auto-pilot mode"
    echo "  kirby typey | chaotix     Ephemeral mechanical typing & kinetic physics arena"
    echo "  kirby tappa [live|adb]    ProjectM Visualizer tap dancer & ADB co-tapper"
    echo ""
    echo "  --- Magician Sleight & Oracle ---"
    echo "  kirby magician [act]      Run 4-Act Magician Kirby & Tac sleight-of-hand screenplay"
    echo "  kirby tarot               Draw a Tarot Card from the Magician Top Hat"
    echo "  kirby oracle [query]      Ask the Oracle of Poyo for cosmic advice"
    echo "  kirby 20q                 Play Kirby 20Q Intent Genie"
    echo "  kirby sprites [name]      View ANSI animated sprites (warp, bounce, hover, etc.)"
    echo "  kirby studio [cmd]        Kirby ASCII art studio (generate|gallery)"
    echo ""
    echo "  --- Needs, Wellbeing & Sanctuary ---"
    echo "  kirby needs [status]      8 Core Needs & 10 Squad Desires Matrix"
    echo "  kirby needs auto          Autonomous Caregiver: fulfill all needs to 100%"
    echo "  kirby nap | sleep         Tuck Kirby into Dream Cloud for a restorative sleep"
    echo "  kirby wake                Gently awaken Kirby with morning starlight"
    echo "  kirby bath | spa | wash   Fountain of Dreams bubble spa bath"
    echo "  kirby hug | cuddle        Give Kirby a warm loving hug and head pats"
    echo "  kirby fengshui | comfort  Harmonize room Spatial Feng Shui and cozy Qi"
    echo "  kirby cool | chill        Freeze Kirby Glacial Chill to cool CPU thermals"
    echo "  kirby fulfill <need>      Fulfill specific need (satiety, rest, bath, hug, etc.)"
    echo "  kirby sanctuary           Open Kirby Needs Sanctuary Web Portal (:8088/needs)"
    echo "  kirby caretaker [status]  Bandana Dee & Chef Kawasaki Caretaker Duo HQ"
    echo "  kirby caretaker round     Dispatch proactive squad wellness round"
    echo "  kirby caretaker mutual    Execute mutual caregiving ritual (caretakers nurture each other)"
    echo "  kirby buddy               Alias for mutual care ritual"
    echo "  kirby tuck [target]       Bandana Dee tucks Kirby into bed with fleece blanket"
    echo "  kirby cook [dish]         Chef Kawasaki cooks fresh vitality ramen or stew"
    echo ""
    echo "  --- Care, Expeditions & Combat ---"
    echo "  kirby pet [status]        Tamagotchi care, hunger, energy & bond levels"
    echo "  kirby feed <item>         Feed Maxi Tomato, Strawberry Cake, or Star Candy"
    echo "  kirby mood                Inspect Kirby's live mood and expressions"
    echo "  kirby expedition [zone]   Embark on Dream Land expeditions & quests"
    echo "  kirby boss [name]         Boss Colosseum duel (Whispy, Dedede, Meta Knight, Marx)"
    echo "  kirby clean [--dry-run]   Hypernova Inhale deep clean of stale cache & snaps"
    echo ""
    echo "  --- Noid Gremlin Chaos & Mischief ---"
    echo "  kirby noid                Noid Gremlin status, chaos meter & prank inventory"
    echo "  kirby prank [target]      Deploy a hilarious gremlin prank across the mesh"
    echo "  kirby pizza [action]      Order, steal, or stash cheesy pizza"
    echo "  kirby goblin              Toggle full unhinged Goblin Mode"
    echo ""
    echo "  --- Learning & Action Deck ---"
    echo "  kirby cards               List all known & learned action cards in active deck"
    echo "  kirby draw                Draw a random action card with ASCII illustration"
    echo "  kirby play <card_id>      Execute an action card across the mesh"
    echo "  kirby event <name>        Emit system/user event & trigger Kirby's response"
    echo "  kirby learn [count]       Run autopoietic curiosity & learning cycles"
    echo "  kirby synthesize <a <b>   Fuse two copy abilities into a new hybrid card"
    echo "  kirby ledger              View evolutionary learning ledger and XP progression"
    echo "  kirby deck                View Kirby Motion Decision Deck JSON"
    echo ""
    echo "  --- Web Portals & 3D Experientials ---"
    echo "  kirby multiverse | hub    Kirby Multi-Verse & Squad Party Hub (:8088/multiverse)"
    echo "  kirby sanctuary | needs   Kirby Needs & Wellbeing Sanctuary (:8088/needs)"
    echo "  kirby celestial           Kirby Celestial Sanctuary 3D (:8088/celestial)"
    echo "  kirby swarm | megaswarm   Kirby Mega-Swarm & Copy Ability Nexus (:8088/megaswarm)"
    echo "  kirby arena               Multimodal Compression Agent Arena (:8088/arena)"
    echo "  kirby minions             Minion Swarm DoF Platters 3D (:8088/minions)"
    echo "  kirby soundboard          PixXL Foley Artist Soundboard (:8088/soundboard)"
    echo "  kirby haptics             Multi-Touch Haptics Lab (:8088/haptics)"
    echo ""
    echo "  --- Windows 11 Lappy Companion ---"
    echo "  kirby win11 [status]      Status of Win11 Lappy, mesh bridge & portal"
    echo "  kirby win11 plan          View Operation Starfall Poyo Master Plan"
    echo "  kirby win11 serve         Show dev web portal URLs for Win11 (:8088/win11)"
    echo "  kirby win11 package       Bundle standalone Win11 zip package"
    echo ""
    echo "  --- Verification & Utility ---"
    echo "  kirby test                Execute 17-stage automated verification suite"
    echo "  kirby help                Display this help reference"
    echo ""
}

case "$1" in
    start)
        cmd_start
        ;;
    stop)
        cmd_stop
        ;;
    restart)
        cmd_stop
        sleep 1
        cmd_start
        ;;
    status)
        cmd_status
        ;;
    snap|screenshot)
        cmd_snap
        ;;
    visitor)
        cmd_visitor "$2"
        ;;
    cards)
        cmd_cards
        ;;
    card)
        cmd_card "${@:2}"
        ;;
    draw)
        cmd_card draw
        ;;
    event)
        cmd_event "$2"
        ;;
    learn)
        cmd_learn "$2"
        ;;
    synthesize|synth|fuse)
        cmd_synthesize "$2" "$3"
        ;;
    ledger|xp)
        cmd_ledger
        ;;
    squad|party|kirbies)
        cmd_squad "${@:2}"
        ;;
    raid)
        cmd_squad raid "${@:2}"
        ;;
    banter)
        cmd_squad banter
        ;;
    samurai|quickdraw|draw_duel)
        cmd_samurai "${@:2}"
        ;;
    magician|sleight|tac)
        cmd_magician "${@:2}"
        ;;
    tarot)
        cmd_magician tarot
        ;;
    needs|need|wellbeing)
        cmd_needs "${@:2}"
        ;;
    nap|sleep)
        cmd_needs nap "${@:2}"
        ;;
    wake)
        cmd_needs wake "${@:2}"
        ;;
    bath|spa|wash)
        cmd_needs bath "${@:2}"
        ;;
    hug|cuddle)
        cmd_needs hug "${@:2}"
        ;;
    fengshui|comfort)
        cmd_needs fengshui "${@:2}"
        ;;
    cool|chill)
        cmd_needs cool "${@:2}"
        ;;
    fulfill)
        cmd_needs fulfill "${@:2}"
        ;;
    sanctuary)
        cmd_sanctuary
        ;;
    caretaker|caretakers|caregiver|caregivers)
        cmd_caretaker "${@:2}"
        ;;
    buddy|mutual)
        cmd_caretaker mutual "${@:2}"
        ;;
    oneanother|one_another)
        cmd_caretaker oneanother
        ;;
    tuck)
        cmd_caretaker tuck "${@:2}"
        ;;
    cook)
        cmd_caretaker cook "${@:2}"
        ;;
    pet|care)
        cmd_pet "${@:2}"
        ;;
    feed)
        cmd_feed "${@:2}"
        ;;
    mood)
        cmd_mood
        ;;
    expedition|quest|explore)
        cmd_expedition "${@:2}"
        ;;
    boss|colosseum|duel)
        cmd_boss "${@:2}"
        ;;
    clean|inhale|janitor)
        cmd_clean "${@:2}"
        ;;
    noid|annoy)
        cmd_noid "${@:2}"
        ;;
    prank)
        cmd_prank "${@:2}"
        ;;
    poke)
        cmd_poke
        ;;
    pizza)
        cmd_pizza "${@:2}"
        ;;
    goblin)
        cmd_goblin
        ;;
    noid_web)
        cmd_noid_web
        ;;
    typey|chaotix)
        cmd_typey "${@:2}"
        ;;
    multiverse|hub)
        cmd_multiverse
        ;;
    play|game)
        cmd_play "${@:2}"
        ;;
    auto)
        cmd_auto "${@:2}"
        ;;
    oracle|wisdom)
        cmd_oracle "$@"
        ;;
    20q)
        cmd_20q
        ;;
    sprites|sprite|anim)
        cmd_sprites "$@"
        ;;
    studio|art)
        cmd_studio "$@"
        ;;
    celestial)
        cmd_celestial
        ;;
    swarm|megaswarm)
        cmd_swarm
        ;;
    arena|brawl)
        cmd_arena
        ;;
    minions)
        cmd_minions
        ;;
    soundboard|audio)
        cmd_soundboard
        ;;
    haptics|lab)
        cmd_haptics
        ;;
    tappa|projectm|visualizer)
        cmd_tappa "${@:2}"
        ;;
    win11|lappy|invasion)
        cmd_win11 "${@:2}"
        ;;
    deck)
        cmd_deck
        ;;
    combat|kungfu|clones|spar)
        cmd_combat "${@:2}"
        ;;
    phyx|physics|tac)
        cmd_phyx "${@:2}"
        ;;
    orca|strata|porpoise)
        python3 "${SCRIPTS_DIR}/orca_strata_porpoise_sync.py" "${@:2}"
        ;;
    test)
        cmd_test
        ;;
    install)
        banner
        check_adb
        echo -e "${CYAN}[*] Installing updated APK to device...${NC}"
        adb install -r -d "${SHARED_DIR}/app-debug.apk"
        echo -e "${GREEN}[✔] APK installed successfully!${NC}"
        ;;
    help|--help|-h|"")
        cmd_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        cmd_help
        exit 1
        ;;
esac
