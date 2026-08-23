/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { ATBHero, CustomBattlefield, MultiplayerRoomState, VFXParticle } from '../types';
import { INITIAL_HERO_ROSTER, RAID_BOSSES } from '../data/heroes';
import { audioEngine } from '../utils/audio';
import { multiplayerEngine } from '../utils/multiplayerEngine';
import { HeroArtRenderer } from './HeroArtRenderer';
import {
  Swords,
  Zap,
  Shield,
  Sparkles,
  Users,
  Send,
  Trophy,
  Activity,
  Layers,
  Wand2,
  RefreshCw,
  Flame,
  Volume2,
  VolumeX,
} from 'lucide-react';

interface ATBMultiplayerArenaProps {
  onOpenBuilder?: () => void;
  onExit?: () => void;
}

export const ATBMultiplayerArena: React.FC<ATBMultiplayerArenaProps> = ({
  onOpenBuilder,
  onExit,
}) => {
  // Multiplayer & Persistence State
  const [room, setRoom] = useState<MultiplayerRoomState>(multiplayerEngine.getCurrentRoom());
  const [profile, setProfile] = useState(multiplayerEngine.getProfile());
  const [stats, setStats] = useState(multiplayerEngine.getStats());
  const [chatInput, setChatInput] = useState('');
  const [isMuted, setIsMuted] = useState(audioEngine.getMuted());

  // Battle Roster & Arena State
  const [heroes, setHeroes] = useState<ATBHero[]>(INITIAL_HERO_ROSTER);
  const [boss, setBoss] = useState<ATBHero>(RAID_BOSSES[0]);
  const [selectedHeroId, setSelectedHeroId] = useState<string>(INITIAL_HERO_ROSTER[0].id);
  const [activeBattlefield, setActiveBattlefield] = useState<CustomBattlefield>(
    multiplayerEngine.getBattlefields()[0] || {
      id: 'field_citadel',
      name: 'Dreamland Floating Citadel',
      theme: '3D Stepped Terraces & Chutes',
      gridSize: 7,
      accentColor: '#38bdf8',
      tiles: [],
      chutes: [],
      ladders: [],
      creator: 'Foreman',
      createdAt: Date.now(),
    }
  );

  // Combat Execution State
  const [isBattleRunning, setIsBattleRunning] = useState<boolean>(true);
  const [autoBattle, setAutoBattle] = useState<boolean>(true);
  const [gameSpeed, setGameSpeed] = useState<number>(1);
  const [activeAutocastBanner, setActiveAutocastBanner] = useState<{
    heroName: string;
    skillName: string;
    avatar: string;
    color: string;
    equation: string;
  } | null>(null);

  // Floating Combat Text & Particle Effects
  const [particles, setParticles] = useState<VFXParticle[]>([]);
  const [screenShake, setScreenShake] = useState<number>(0);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const chatScrollRef = useRef<HTMLDivElement>(null);

  // Subscribe to multiplayer room events
  useEffect(() => {
    const unsubRoom = multiplayerEngine.subscribe((updatedRoom) => {
      setRoom({ ...updatedRoom });
    });
    return () => {
      unsubRoom();
    };
  }, []);

  // Sync active battlefield with room
  useEffect(() => {
    const fields = multiplayerEngine.getBattlefields();
    const found = fields.find((f) => f.id === room.battlefieldId) || fields[0];
    if (found) {
      setActiveBattlefield(found);
    }
  }, [room.battlefieldId]);

  // Handle Autocast Trigger (CENTERPIECE MECHANIC: 3X ATB Overdrive)
  const trigger3XAutocast = useCallback(
    (caster: ATBHero, isPlayerParty: boolean) => {
      audioEngine.init();
      audioEngine.playATBAutocast();

      // Trigger specific character sound
      if (caster.characterClass === 'majin_kirby') {
        audioEngine.playMajinCandyBeam();
      } else if (caster.characterClass === 'aether_knight') {
        audioEngine.playAetherSlash();
      } else if (caster.characterClass === 'adventurer') {
        audioEngine.playFlameBurst();
      } else {
        audioEngine.playHitImpact();
      }

      // Visual Screen Shake & Banner
      setScreenShake(12);
      setTimeout(() => setScreenShake(0), 700);

      const skill = caster.skills.charge3Autocast;
      setActiveAutocastBanner({
        heroName: caster.name,
        skillName: skill.name,
        avatar: caster.avatar,
        color: caster.color,
        equation: skill.equationSnippet || 'Energy = Mass × C²',
      });
      setTimeout(() => setActiveAutocastBanner(null), 2400);

      // Multiplayer Chat Broadcast
      multiplayerEngine.sendChatMessage(
        `⚡ [3X AUTOCAST] ${caster.name} unleashed ${skill.name}!`,
        'autocast'
      );

      // Calculate Damage & Apply
      const baseDmg = Math.round(caster.atk * (skill.damageMultiplier || 3.5));

      if (isPlayerParty) {
        // Player team attacking Boss
        const totalDmg = baseDmg + Math.floor(Math.random() * 40);
        setBoss((prev) => {
          const nextHp = Math.max(0, prev.hp - totalDmg);
          return { ...prev, hp: nextHp };
        });

        // Add damage particle on Boss
        spawnDamageNumber(totalDmg, 550, 180, '#f43f5e', true);
        multiplayerEngine.addAutocastStat(totalDmg);
        setProfile(multiplayerEngine.getProfile());
        setStats(multiplayerEngine.getStats());
      } else {
        // Boss attacking party
        const partyDmg = Math.round(baseDmg / 2.5);
        setHeroes((prev) =>
          prev.map((h) => ({
            ...h,
            hp: Math.max(0, h.hp - partyDmg),
          }))
        );
        spawnDamageNumber(partyDmg, 220, 240, '#fbbf24', true);
      }

      // Spawn burst particles
      spawnSkillVFX(caster.x, caster.y, caster.skills.charge3Autocast.vfxType, caster.color);
    },
    []
  );

  // Spawn visual floating damage numbers
  const spawnDamageNumber = (
    amount: number,
    x: number,
    y: number,
    color: string = '#ffffff',
    isCrit: boolean = false
  ) => {
    setParticles((prev) => [
      ...prev,
      {
        x,
        y,
        vx: (Math.random() - 0.5) * 40,
        vy: -70 - Math.random() * 30,
        ax: 0,
        ay: 60,
        life: 1.2,
        maxLife: 1.2,
        size: isCrit ? 22 : 16,
        color,
        type: 'text',
        text: isCrit ? `CRIT ${amount}!` : `-${amount}`,
      },
    ]);
  };

  // Spawn VFX Particles for 3D visual math
  const spawnSkillVFX = (gridX: number, gridY: number, vfxType: string, baseColor: string) => {
    const screenPos = gridToScreen(gridX, gridY, 1);
    const count = vfxType === 'chocolate_nova' ? 35 : 25;
    const newParticles: VFXParticle[] = [];

    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 60 + Math.random() * 140;
      newParticles.push({
        x: screenPos.x,
        y: screenPos.y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        ax: 0,
        ay: 30,
        life: 0.8 + Math.random() * 0.6,
        maxLife: 1.4,
        size: 4 + Math.random() * 8,
        color: vfxType === 'chocolate_nova' ? (i % 2 === 0 ? '#f472b6' : '#fbbf24') : baseColor,
        type: vfxType === 'flame_tempest' ? 'flame' : 'aether_blade',
      });
    }

    setParticles((prev) => [...prev, ...newParticles]);
  };

  // Manual Trigger for 1X or 2X skills
  const executeManualSkill = (hero: ATBHero, skillTier: 1 | 2) => {
    const skill = skillTier === 1 ? hero.skills.charge1 : hero.skills.charge2;
    if (hero.atbGauge < skill.cost) return;

    audioEngine.init();
    audioEngine.playHitImpact();

    // Deduct ATB
    setHeroes((prev) =>
      prev.map((h) => {
        if (h.id === hero.id) {
          return { ...h, atbGauge: Math.max(0, h.atbGauge - skill.cost) };
        }
        return h;
      })
    );

    // Apply effect
    const dmg = Math.round(hero.atk * (skill.damageMultiplier || 1.2));
    setBoss((prev) => ({ ...prev, hp: Math.max(0, prev.hp - dmg) }));
    spawnDamageNumber(dmg, 550, 180, hero.color, false);
    spawnSkillVFX(hero.x, hero.y, skill.vfxType, hero.color);

    multiplayerEngine.sendChatMessage(
      `🗡️ ${hero.name} cast ${skill.name} (-${dmg} HP)`,
      'cast'
    );
  };

  // Continuous Combat Loop (RequestAnimationFrame ticking ATB Gauges)
  useEffect(() => {
    if (!isBattleRunning) return;

    let lastTime = performance.now();
    let animationFrameId: number;

    const gameLoop = (currentTime: number) => {
      const dt = Math.min((currentTime - lastTime) / 1000, 0.1) * gameSpeed;
      lastTime = currentTime;

      // 1. Tick Heroes' ATB
      setHeroes((prevHeroes) => {
        return prevHeroes.map((hero) => {
          if (hero.hp <= 0) return hero;

          let newGauge = hero.atbGauge + hero.atbSpeed * dt;

          // 3X ATB THRESHOLD (300 points) => AUTOCAST!
          if (newGauge >= 300) {
            trigger3XAutocast(hero, true);
            newGauge = 0; // Reset ATB after 3x Autocast burst
          } else if (autoBattle && newGauge >= 100 && hero.atbGauge < 100) {
            // Soft normal auto-attack blip
            audioEngine.playTextBlip(hero.spd);
          }

          return { ...hero, atbGauge: newGauge };
        });
      });

      // 2. Tick Boss ATB
      setBoss((prevBoss) => {
        if (prevBoss.hp <= 0) return prevBoss;

        let bossGauge = prevBoss.atbGauge + prevBoss.atbSpeed * dt;
        if (bossGauge >= 300) {
          trigger3XAutocast(prevBoss, false);
          bossGauge = 0;
        }
        return { ...prevBoss, atbGauge: bossGauge };
      });

      // 3. Update Particles
      setParticles((prev) => {
        return prev
          .map((p) => ({
            ...p,
            x: p.x + p.vx * dt,
            y: p.y + p.vy * dt,
            vx: p.vx + p.ax * dt,
            vy: p.vy + p.ay * dt,
            life: p.life - dt,
          }))
          .filter((p) => p.life > 0);
      });

      animationFrameId = requestAnimationFrame(gameLoop);
    };

    animationFrameId = requestAnimationFrame(gameLoop);

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [isBattleRunning, autoBattle, gameSpeed, trigger3XAutocast]);

  // Render 3D Isometric Battlefield on Canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const originX = canvas.width / 2;
    const originY = 160;
    const tileW = 64;
    const tileH = 32;

    // Draw 3D Isometric Grid Floor
    for (let gx = 0; gx < 7; gx++) {
      for (let gy = 0; gy < 7; gy++) {
        const isoX = originX + (gx - gy) * (tileW / 2);
        const isoY = originY + (gx + gy) * (tileH / 2);

        // Tile height tier elevation
        const customTile = activeBattlefield.tiles.find((t) => t.x === gx && t.y === gy);
        const tier = customTile ? customTile.tier : (gx + gy) % 3 === 0 ? 1 : 0;
        const elevY = isoY - tier * 24;

        // Draw 3D Base Block
        ctx.fillStyle = tier === 2 ? '#1e293b' : tier === 1 ? '#0f172a' : '#090d16';
        ctx.beginPath();
        ctx.moveTo(isoX, elevY + tileH / 2);
        ctx.lineTo(isoX + tileW / 2, elevY);
        ctx.lineTo(isoX + tileW / 2, elevY + 16);
        ctx.lineTo(isoX, elevY + tileH / 2 + 16);
        ctx.closePath();
        ctx.fill();

        // Top Face
        ctx.fillStyle = customTile?.color || (tier === 2 ? '#38bdf822' : tier === 1 ? '#1e293b' : '#111827');
        ctx.strokeStyle = '#334155';
        ctx.lineWidth = 1;

        ctx.beginPath();
        ctx.moveTo(isoX, elevY - tileH / 2);
        ctx.lineTo(isoX + tileW / 2, elevY);
        ctx.lineTo(isoX, elevY + tileH / 2);
        ctx.lineTo(isoX - tileW / 2, elevY);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        // Draw Ladders & Chutes
        activeBattlefield.chutes.forEach((chute) => {
          if (chute.topX === gx && chute.topY === gy) {
            ctx.strokeStyle = '#f59e0b';
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(isoX, elevY);
            const botPos = gridToScreen(chute.botX, chute.botY, 0);
            ctx.lineTo(botPos.x, botPos.y);
            ctx.stroke();
          }
        });
      }
    }

    // Draw Particles on 2D Overlay
    particles.forEach((p) => {
      ctx.save();
      const alpha = Math.max(0, p.life / p.maxLife);
      ctx.globalAlpha = alpha;

      if (p.type === 'text' && p.text) {
        ctx.fillStyle = p.color;
        ctx.font = `bold ${p.size}px monospace`;
        ctx.textAlign = 'center';
        ctx.shadowColor = '#000000';
        ctx.shadowBlur = 4;
        ctx.fillText(p.text, p.x, p.y);
      } else if (p.type === 'flame') {
        ctx.fillStyle = p.color;
        ctx.shadowColor = '#f97316';
        ctx.shadowBlur = 10;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
      } else {
        ctx.fillStyle = p.color;
        ctx.fillRect(p.x - p.size / 2, p.y - p.size / 2, p.size, p.size);
      }
      ctx.restore();
    });
  }, [heroes, boss, activeBattlefield, particles]);

  // Coordinate conversion
  const gridToScreen = (gx: number, gy: number, tier: number = 0) => {
    const originX = 400;
    const originY = 160;
    const tileW = 64;
    const tileH = 32;
    return {
      x: originX + (gx - gy) * (tileW / 2),
      y: originY + (gx + gy) * (tileH / 2) - tier * 24,
    };
  };

  // Send Chat message
  const handleSendChat = (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    multiplayerEngine.sendChatMessage(chatInput.trim(), 'chat');
    audioEngine.playChatPing();
    setChatInput('');
  };

  // Check victory / restart
  const handleRestartBattle = () => {
    setHeroes(INITIAL_HERO_ROSTER.map((h) => ({ ...h, hp: h.maxHp, atbGauge: Math.random() * 60 })));
    setBoss({ ...RAID_BOSSES[0], hp: RAID_BOSSES[0].maxHp, atbGauge: 40 });
    multiplayerEngine.sendChatMessage('🔄 Battle reset! Starting fresh raid encounter.', 'system');
  };

  const selectedHero = heroes.find((h) => h.id === selectedHeroId) || heroes[0];

  return (
    <div
      className={`relative w-full h-full min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans select-none overflow-hidden transition-transform duration-75 ${
        screenShake > 0 ? 'translate-x-1 translate-y-1' : ''
      }`}
    >
      {/* 1. TOP MULTIPLAYER & PERSISTENCE NAVIGATION BAR */}
      <header className="h-14 border-b border-slate-800/80 bg-slate-900/90 backdrop-blur px-4 flex items-center justify-between z-20">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-cyan-500 flex items-center justify-center shadow-md">
            <Swords className="w-4 h-4 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm text-slate-100">{room.roomName}</span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                {room.roomId}
              </span>
              <span className="text-[10px] font-mono text-emerald-400 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                28ms
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              Active Map: <span className="text-cyan-300">{activeBattlefield.name}</span>
            </p>
          </div>
        </div>

        {/* Persistence Player Summary */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-slate-800/80 px-2.5 py-1 rounded-md border border-slate-700/60 text-xs">
            <span className="text-sm">{profile.avatar}</span>
            <div>
              <span className="font-semibold text-slate-200">{profile.name}</span>
              <span className="text-[10px] text-amber-400 ml-1.5">Lv.{profile.level}</span>
            </div>
            <div className="h-4 w-px bg-slate-700 mx-1" />
            <span className="text-amber-300 font-mono text-xs flex items-center gap-1">
              ✨ {profile.multiverseShards} Shards
            </span>
          </div>

          {/* Quick Audio Mute & Speed Controls */}
          <button
            onClick={() => setIsMuted(audioEngine.toggleMute())}
            className="p-1.5 rounded bg-slate-800 text-slate-300 hover:text-white border border-slate-700"
            title="Toggle Audio"
          >
            {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
          </button>

          <button
            onClick={() => setAutoBattle(!autoBattle)}
            className={`px-2.5 py-1 rounded text-xs font-semibold flex items-center gap-1 border transition-colors ${
              autoBattle
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                : 'bg-slate-800 text-slate-400 border-slate-700'
            }`}
          >
            <Zap className="w-3.5 h-3.5" />
            {autoBattle ? 'AUTO 3X ON' : 'MANUAL'}
          </button>

          <button
            onClick={() => setGameSpeed(gameSpeed === 1 ? 1.5 : gameSpeed === 1.5 ? 2 : 1)}
            className="px-2 py-1 rounded bg-slate-800 text-xs font-mono text-cyan-300 border border-slate-700 hover:bg-slate-700"
          >
            {gameSpeed}x SPD
          </button>

          {onOpenBuilder && (
            <button
              onClick={onOpenBuilder}
              className="px-3 py-1 rounded-md bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium flex items-center gap-1.5 shadow-sm transition-colors"
            >
              <Layers className="w-3.5 h-3.5" />
              World Builder
            </button>
          )}

          {onExit && (
            <button
              onClick={onExit}
              className="px-2.5 py-1 rounded-md bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white text-xs font-bold shadow-[0_0_10px_rgba(168,85,247,0.4)]"
            >
              3D Cross-Table Matrix
            </button>
          )}
        </div>
      </header>

      {/* 2. MAIN BATTLE ARENA & MULTIPLAYER HUD */}
      <div className="flex-1 flex overflow-hidden">
        {/* LEFT COLUMN: HERO ROSTER & ATB STATUS GAUGES */}
        <aside className="w-80 border-r border-slate-800/80 bg-slate-900/60 p-3 flex flex-col gap-2.5 overflow-y-auto">
          <div className="flex items-center justify-between">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Users className="w-3.5 h-3.5 text-cyan-400" />
              Raid Vanguard (P1 & Allies)
            </h3>
            <span className="text-[10px] text-slate-500 font-mono">3X Charge Engine</span>
          </div>

          {heroes.map((hero) => {
            const isSelected = hero.id === selectedHeroId;
            const atbPercent = Math.min(100, (hero.atbGauge / 300) * 100);
            const isAtbFull = hero.atbGauge >= 300;
            const chargeLevel = hero.atbGauge >= 200 ? 2 : hero.atbGauge >= 100 ? 1 : 0;

            return (
              <div
                key={hero.id}
                onClick={() => setSelectedHeroId(hero.id)}
                className={`p-2.5 rounded-lg border transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-slate-800/90 border-cyan-500/60 ring-1 ring-cyan-500/30'
                    : 'bg-slate-900/40 border-slate-800/60 hover:bg-slate-800/40'
                } ${hero.hp <= 0 ? 'opacity-40 grayscale' : ''}`}
              >
                <div className="flex items-start gap-2.5">
                  <HeroArtRenderer
                    hero={hero}
                    size={48}
                    isAutocasting={isAtbFull}
                    isDamaged={hero.hp < hero.maxHp * 0.3}
                  />

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-xs text-slate-200 truncate">{hero.name}</span>
                      <span className="text-[10px] font-mono text-slate-400">
                        {hero.hp}/{hero.maxHp} HP
                      </span>
                    </div>

                    {/* HP Bar */}
                    <div className="w-full h-1.5 bg-slate-950 rounded-full overflow-hidden my-1">
                      <div
                        className="h-full bg-emerald-500 transition-all duration-300"
                        style={{ width: `${(hero.hp / hero.maxHp) * 100}%` }}
                      />
                    </div>

                    {/* ATB 3X Segmented Gauge */}
                    <div className="space-y-0.5">
                      <div className="flex items-center justify-between text-[9px] font-mono">
                        <span className={isAtbFull ? 'text-amber-300 font-bold animate-pulse' : 'text-slate-400'}>
                          {isAtbFull ? '⚡ 3X AUTOCAST READY' : `ATB Charge ${chargeLevel}x`}
                        </span>
                        <span className="text-slate-500">{Math.round(hero.atbGauge)}/300</span>
                      </div>

                      {/* 3 Segmented ATB Progress Bar */}
                      <div className="grid grid-cols-3 gap-0.5 h-2 bg-slate-950 p-0.5 rounded border border-slate-800">
                        {/* Segment 1 (1X: 0-100) */}
                        <div className="relative bg-slate-900 rounded-sm overflow-hidden">
                          <div
                            className="h-full bg-cyan-500 transition-all duration-75"
                            style={{ width: `${Math.min(100, (hero.atbGauge / 100) * 100)}%` }}
                          />
                        </div>
                        {/* Segment 2 (2X: 100-200) */}
                        <div className="relative bg-slate-900 rounded-sm overflow-hidden">
                          <div
                            className="h-full bg-indigo-500 transition-all duration-75"
                            style={{
                              width: `${Math.min(100, Math.max(0, ((hero.atbGauge - 100) / 100) * 100))}%`,
                            }}
                          />
                        </div>
                        {/* Segment 3 (3X: 200-300 AUTOCAST) */}
                        <div className="relative bg-slate-900 rounded-sm overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-amber-400 to-rose-500 transition-all duration-75"
                            style={{
                              width: `${Math.min(100, Math.max(0, ((hero.atbGauge - 200) / 100) * 100))}%`,
                            }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}

          {/* ACTIVE HERO ACTION CONTROLS */}
          <div className="mt-auto p-3 rounded-lg bg-slate-950/80 border border-slate-800/80">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-base">{selectedHero.avatar}</span>
              <span className="font-bold text-xs text-slate-200">{selectedHero.name} Tactics</span>
            </div>

            <div className="grid grid-cols-2 gap-1.5">
              <button
                onClick={() => executeManualSkill(selectedHero, 1)}
                disabled={selectedHero.atbGauge < 100 || selectedHero.hp <= 0}
                className="p-1.5 rounded bg-slate-800 hover:bg-slate-700 disabled:opacity-30 text-[10px] font-medium border border-slate-700 flex items-center justify-between"
              >
                <span>{selectedHero.skills.charge1.icon} 1X Skill</span>
                <span className="font-mono text-cyan-400">100 ATB</span>
              </button>

              <button
                onClick={() => executeManualSkill(selectedHero, 2)}
                disabled={selectedHero.atbGauge < 200 || selectedHero.hp <= 0}
                className="p-1.5 rounded bg-indigo-900/40 hover:bg-indigo-800/60 disabled:opacity-30 text-[10px] font-medium border border-indigo-700/60 flex items-center justify-between"
              >
                <span>{selectedHero.skills.charge2.icon} 2X Burst</span>
                <span className="font-mono text-indigo-300">200 ATB</span>
              </button>
            </div>

            <div className="mt-2 p-1.5 rounded bg-amber-500/10 border border-amber-500/30 text-[10px] text-amber-200">
              <p className="font-semibold flex items-center gap-1">
                <Sparkles className="w-3 h-3 text-amber-400" />
                3X Auto-Trigger:
              </p>
              <p className="text-[9px] text-slate-300 mt-0.5">
                {selectedHero.skills.charge3Autocast.name} fires automatically when gauge hits 300!
              </p>
            </div>
          </div>
        </aside>

        {/* CENTER COLUMN: 3D ISOMETRIC COMBAT STAGE */}
        <main className="flex-1 relative flex flex-col items-center justify-center bg-radial from-slate-900 to-slate-950 overflow-hidden">
          {/* 3X AUTOCAST CINEMATIC OVERDRIVE BANNER */}
          {activeAutocastBanner && (
            <div className="absolute top-8 z-30 flex flex-col items-center animate-bounce">
              <div
                className="px-6 py-2 rounded-full border shadow-2xl flex items-center gap-3 backdrop-blur-md"
                style={{
                  backgroundColor: 'rgba(15, 23, 42, 0.92)',
                  borderColor: activeAutocastBanner.color,
                }}
              >
                <span className="text-2xl">{activeAutocastBanner.avatar}</span>
                <div>
                  <div className="text-[10px] font-mono tracking-widest text-amber-400 font-bold uppercase">
                    ★ 3X OVERDRIVE AUTOCAST TRIGGERED ★
                  </div>
                  <div className="text-sm font-black text-white">{activeAutocastBanner.skillName}</div>
                </div>
              </div>
              <div className="text-[10px] font-mono text-cyan-300 mt-1 bg-slate-950/80 px-2 py-0.5 rounded border border-cyan-500/30">
                {activeAutocastBanner.equation}
              </div>
            </div>
          )}

          {/* BOSS HUD AT TOP RIGHT */}
          <div className="absolute top-4 right-4 z-10 w-72 bg-slate-900/80 backdrop-blur p-3 rounded-lg border border-red-500/40 shadow-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-xl">{boss.avatar}</span>
                <div>
                  <span className="font-bold text-xs text-red-300">{boss.name}</span>
                  <p className="text-[9px] text-slate-400">{boss.title}</p>
                </div>
              </div>
              <span className="font-mono text-xs text-red-400 font-bold">
                {boss.hp}/{boss.maxHp} HP
              </span>
            </div>

            {/* Boss HP Bar */}
            <div className="w-full h-2 bg-slate-950 rounded-full overflow-hidden my-1.5 border border-slate-800">
              <div
                className="h-full bg-gradient-to-r from-red-600 to-rose-400 transition-all duration-300"
                style={{ width: `${(boss.hp / boss.maxHp) * 100}%` }}
              />
            </div>

            {/* Boss 3X ATB Gauge */}
            <div className="space-y-0.5">
              <div className="flex items-center justify-between text-[9px] font-mono text-slate-400">
                <span>Boss ATB Gauge</span>
                <span>{Math.round(boss.atbGauge)}/300</span>
              </div>
              <div className="w-full h-1.5 bg-slate-950 rounded-full overflow-hidden">
                <div
                  className="h-full bg-amber-500 transition-all duration-75"
                  style={{ width: `${(boss.atbGauge / 300) * 100}%` }}
                />
              </div>
            </div>
          </div>

          {/* 3D Isometric Canvas Layer */}
          <canvas
            ref={canvasRef}
            width={800}
            height={520}
            className="w-full h-full max-w-[800px] max-h-[520px] object-contain cursor-crosshair"
          />

          {/* Interactive Character Overlay on Stage */}
          <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
            {/* Player Frontline Sprites */}
            <div className="absolute left-28 bottom-28 flex items-center gap-4 pointer-events-auto">
              <HeroArtRenderer
                hero={heroes[0]}
                size={80}
                showMeshToggle
                isAutocasting={heroes[0].atbGauge >= 300}
              />
              <HeroArtRenderer
                hero={heroes[1]}
                size={84}
                showMeshToggle
                isAutocasting={heroes[1].atbGauge >= 300}
              />
            </div>

            {/* Boss Sprite on Upper Plateau */}
            <div className="absolute right-32 top-28 pointer-events-auto">
              <HeroArtRenderer
                hero={boss}
                size={110}
                showMeshToggle
                isAutocasting={boss.atbGauge >= 300}
              />
            </div>
          </div>

          {/* Boss Victory / Defeat Overlay */}
          {boss.hp <= 0 && (
            <div className="absolute inset-0 bg-slate-950/85 backdrop-blur-sm flex flex-col items-center justify-center z-40">
              <div className="p-6 rounded-2xl bg-slate-900 border border-amber-500/50 shadow-2xl text-center max-w-sm">
                <Trophy className="w-12 h-12 text-amber-400 mx-auto mb-2 animate-bounce" />
                <h2 className="text-xl font-bold text-white">RAID BOSS DEFEATED!</h2>
                <p className="text-xs text-slate-300 mt-1">
                  You conquered the 3D Multiverse Citadel and earned 200 Multiverse Shards!
                </p>
                <div className="mt-4 flex gap-2 justify-center">
                  <button
                    onClick={handleRestartBattle}
                    className="px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs flex items-center gap-1.5 shadow-md"
                  >
                    <RefreshCw className="w-3.5 h-3.5" /> Next Raid Round
                  </button>
                  {onOpenBuilder && (
                    <button
                      onClick={onOpenBuilder}
                      className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs border border-slate-700"
                    >
                      Customize Arena
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}
        </main>

        {/* RIGHT COLUMN: MULTIPLAYER LOBBY, REAL-TIME CHAT & BLUEPRINT LOADER */}
        <aside className="w-80 border-l border-slate-800/80 bg-slate-900/60 p-3 flex flex-col gap-3">
          {/* Room Peers */}
          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
              <Activity className="w-3.5 h-3.5 text-indigo-400" />
              Connected Combatants ({room.players.length}/4)
            </h3>
            <div className="space-y-1.5">
              {room.players.map((player) => (
                <div
                  key={player.id}
                  className="p-2 rounded bg-slate-950/60 border border-slate-800/80 flex items-center justify-between text-xs"
                >
                  <div className="flex items-center gap-2">
                    <span>{player.avatar}</span>
                    <div>
                      <span className="font-semibold text-slate-200">{player.name}</span>
                      {player.isHost && (
                        <span className="text-[9px] text-amber-400 font-mono ml-1 px-1 bg-amber-400/10 rounded">
                          HOST
                        </span>
                      )}
                    </div>
                  </div>
                  <span className="text-[10px] font-mono text-emerald-400">{player.ping}ms</span>
                </div>
              ))}
            </div>
          </div>

          {/* Battlefield Terrain Blueprint Selector */}
          <div className="p-2.5 rounded bg-slate-950/60 border border-slate-800/80">
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="font-bold text-slate-300 flex items-center gap-1">
                <Layers className="w-3.5 h-3.5 text-cyan-400" />
                Battlefield Map
              </span>
              <span className="text-[10px] text-slate-500 font-mono">
                {multiplayerEngine.getBattlefields().length} maps
              </span>
            </div>
            <select
              value={room.battlefieldId}
              onChange={(e) => multiplayerEngine.setBattlefield(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded p-1.5 outline-none focus:border-cyan-500"
            >
              {multiplayerEngine.getBattlefields().map((f) => (
                <option key={f.id} value={f.id}>
                  {f.name} ({f.theme})
                </option>
              ))}
            </select>
          </div>

          {/* Real-Time Combat Chat & Telemetry */}
          <div className="flex-1 min-h-[160px] flex flex-col bg-slate-950/90 rounded-lg border border-slate-800/80 p-2 overflow-hidden">
            <div className="text-[10px] font-bold uppercase text-slate-400 pb-1.5 border-b border-slate-800 flex items-center justify-between">
              <span>Raid Telemetry Log</span>
              <span className="text-slate-500 font-mono">BroadcastBus</span>
            </div>

            <div ref={chatScrollRef} className="flex-1 overflow-y-auto space-y-1.5 py-2 text-[11px]">
              {room.chatMessages.map((msg) => (
                <div
                  key={msg.id}
                  className={`p-1.5 rounded ${
                    msg.type === 'autocast'
                      ? 'bg-amber-500/15 border border-amber-500/30 text-amber-200 font-medium'
                      : msg.type === 'system'
                      ? 'bg-indigo-500/10 text-indigo-300 font-mono text-[10px]'
                      : 'bg-slate-900/80 text-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between text-[9px] text-slate-500 mb-0.5">
                    <span className="font-semibold text-slate-400">{msg.sender}</span>
                    <span>{msg.time}</span>
                  </div>
                  <p>{msg.text}</p>
                </div>
              ))}
            </div>

            {/* Chat Input Form */}
            <form onSubmit={handleSendChat} className="pt-1.5 border-t border-slate-800 flex gap-1.5">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Message team or emote..."
                className="flex-1 bg-slate-900 border border-slate-700 rounded px-2 py-1 text-xs text-slate-200 outline-none focus:border-indigo-500"
              />
              <button
                type="submit"
                className="px-2.5 py-1 bg-indigo-600 hover:bg-indigo-500 text-white rounded text-xs"
              >
                <Send className="w-3 h-3" />
              </button>
            </form>
          </div>
        </aside>
      </div>
    </div>
  );
};
