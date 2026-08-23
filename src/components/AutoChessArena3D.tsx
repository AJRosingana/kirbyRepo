/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useRef, useEffect } from 'react';
import { ChessUnit, CrossPortalSpell, PortalSurface } from '../types';
import { audioEngine } from '../utils/audio';
import {
  Swords,
  Dices,
  Sparkles,
  Zap,
  RotateCcw,
  Flame,
  Sun,
  Radio,
  Wind,
  Shield,
  Heart,
  Skull,
  Eye,
  Layers,
  ArrowDownRight,
  TrendingUp,
} from 'lucide-react';
import confetti from 'canvas-confetti';

interface AutoChessArena3DProps {
  portals: PortalSurface[];
  onSelectPortal?: (portal: PortalSurface) => void;
}

export const AutoChessArena3D: React.FC<AutoChessArena3DProps> = ({
  portals,
  onSelectPortal,
}) => {
  // Mana & Dice
  const [mana, setMana] = useState(100);
  const [diceValue, setDiceValue] = useState<number | null>(null);
  const [isRollingDice, setIsRollingDice] = useState(false);
  const [activeSpellLog, setActiveSpellLog] = useState<string>('Arena ready. Roll dice to harvest cross-portal mana!');
  const [battleRound, setBattleRound] = useState(1);
  const [isAutoBattling, setIsAutoBattling] = useState(false);

  // Units on the multi-tiered 3D board
  const [units, setUnits] = useState<ChessUnit[]>([
    {
      id: 'p1',
      name: 'Golden Knight',
      type: 'knight',
      team: 'player',
      tier: 2, // Upper plateau
      x: 2,
      y: 2,
      hp: 120,
      maxHp: 120,
      attack: 25,
      range: 2,
      mana: 40,
      maxMana: 100,
      color: '#fbbf24',
    },
    {
      id: 'p2',
      name: 'Arch-Bishop',
      type: 'bishop',
      team: 'player',
      tier: 1, // Middle terrace
      x: 4,
      y: 3,
      hp: 85,
      maxHp: 85,
      attack: 30,
      range: 3,
      mana: 70,
      maxMana: 100,
      color: '#f8fafc',
    },
    {
      id: 'p3',
      name: 'Kirb Builder',
      type: 'kirb_builder',
      team: 'player',
      tier: 0, // Lower ground
      x: 1,
      y: 5,
      hp: 140,
      maxHp: 140,
      attack: 18,
      range: 1,
      mana: 30,
      maxMana: 100,
      color: '#f472b6',
    },
    {
      id: 'e1',
      name: 'Pharaoh Scarab',
      type: 'scarab',
      team: 'enemy',
      tier: 1,
      x: 5,
      y: 4,
      hp: 95,
      maxHp: 95,
      attack: 22,
      range: 2,
      mana: 20,
      maxMana: 100,
      color: '#eab308',
    },
    {
      id: 'e2',
      name: 'Mimic Chest',
      type: 'mimic',
      team: 'enemy',
      tier: 0,
      x: 5,
      y: 6,
      hp: 160,
      maxHp: 160,
      attack: 28,
      range: 1,
      mana: 10,
      maxMana: 100,
      color: '#ef4444',
    },
    {
      id: 'e3',
      name: 'Vector Tesseract',
      type: 'tesseract',
      team: 'enemy',
      tier: 2,
      x: 5,
      y: 1,
      hp: 75,
      maxHp: 75,
      attack: 35,
      range: 3,
      mana: 50,
      maxMana: 100,
      color: '#38bdf8',
    },
  ]);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Available Cross-Portal Spells harnessed from nearby 3D overworld portals
  const spells: CrossPortalSpell[] = [
    {
      id: 'psi_mindwarp',
      name: 'PSI Rift Mindwarp',
      portalId: 'cosmic_psi_rift',
      portalName: 'Cosmic PSI Rift',
      icon: '🌀',
      color: '#ec4899',
      manaCost: 35,
      description: 'Stuns enemy units on the upper plateau and deals 30 psychic damage.',
      effect: 'stun_tier',
      targetTier: 2,
    },
    {
      id: 'ra_solar_wrath',
      name: "Ra's Solar Wrath",
      portalId: 'pharaoh_sun_gate',
      portalName: "Pharaoh's Gate",
      icon: '☀️',
      color: '#f59e0b',
      manaCost: 45,
      description: 'Calls a golden sun ray scorching all enemy pieces for 40 damage.',
      effect: 'damage_all',
    },
    {
      id: 'phosphor_emp',
      name: 'Phosphor EMP Stun',
      portalId: 'cyber_vector_matrix',
      portalName: 'Cyber Archaeology',
      icon: '⚡',
      color: '#10b981',
      manaCost: 30,
      description: 'Shuts down enemy shields and resets enemy turn cooldowns.',
      effect: 'stun_tier',
      targetTier: 1,
    },
    {
      id: 'zeal_uplift',
      name: 'Zeal Stratosphere Uplift',
      portalId: 'sky_citadel_zeal',
      portalName: 'Sky Citadel of Zeal',
      icon: '🌪️',
      color: '#38bdf8',
      manaCost: 40,
      description: 'Elevates a friendly unit up a ladder to a higher tactical terrace.',
      effect: 'elevate_ladder',
    },
    {
      id: 'magma_eruption',
      name: 'Magma Fissure Quake',
      portalId: 'lava_foundry_core',
      portalName: 'Geothermal Lava Foundry',
      icon: '🌋',
      color: '#f97316',
      manaCost: 50,
      description: 'Erupts molten lava on the lower ground, dealing 50 damage to tier 0 units.',
      effect: 'damage_all',
      targetTier: 0,
    },
    {
      id: 'spore_regen',
      name: 'Bioluminescent Spore Rain',
      portalId: 'spore_forest_deep',
      portalName: 'Spore Arbor',
      icon: '🍄',
      color: '#06b6d4',
      manaCost: 25,
      description: 'Heals all friendly chess pieces for 45 HP with floating spores.',
      effect: 'heal_team',
    },
  ];

  // 3D Isometric Board & Diorama Canvas Render Loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId: number;
    let startTime = performance.now();

    const render = (now: number) => {
      const time = (now - startTime) * 0.001;
      const w = canvas.width;
      const h = canvas.height;

      // Rich Warm Mahogany Wood Table Backdrop
      const grad = ctx.createRadialGradient(w / 2, h / 2, 50, w / 2, h / 2, w * 0.65);
      grad.addColorStop(0, '#1c130d');
      grad.addColorStop(0.7, '#110b07');
      grad.addColorStop(1, '#080503');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);

      // Isometric Board Parameters
      const originX = w * 0.5;
      const originY = h * 0.22;
      const tileW = 44;
      const tileH = 22;
      const boardSize = 8;

      // Helper function to get world height offset for 3 board tiers
      const getTierHeight = (x: number, y: number) => {
        if (x < 4 && y < 4) return 60; // Tier 2 (Upper Plateau)
        if (x >= 3 && y >= 3 && (x < 6 || y < 6)) return 30; // Tier 1 (Middle Terrace)
        return 0; // Tier 0 (Lower Ground)
      };

      // 1. Draw Multi-Tiered Chess Squares
      for (let x = 0; x < boardSize; x++) {
        for (let y = 0; y < boardSize; y++) {
          const tierHeight = getTierHeight(x, y);
          const screenX = originX + (x - y) * (tileW / 2);
          const screenY = originY + (x + y) * (tileH / 2) - tierHeight;

          const isDarkSquare = (x + y) % 2 === 1;

          // Top Diamond Tile Face
          ctx.beginPath();
          ctx.moveTo(screenX, screenY);
          ctx.lineTo(screenX + tileW / 2, screenY + tileH / 2);
          ctx.lineTo(screenX, screenY + tileH);
          ctx.lineTo(screenX - tileW / 2, screenY + tileH / 2);
          ctx.closePath();

          // Rich Oak / Walnut Wood Grain Colors
          if (isDarkSquare) {
            ctx.fillStyle = '#452b1b'; // Dark walnut
          } else {
            ctx.fillStyle = '#c49a6c'; // Light maple
          }
          ctx.fill();
          ctx.strokeStyle = '#29180c';
          ctx.lineWidth = 1;
          ctx.stroke();

          // Extruded Wood Platform Risers between Tiers
          if (tierHeight > 0 && (x === boardSize - 1 || y === boardSize - 1 || x === 3 || y === 3)) {
            const wallDepth = tierHeight === 60 ? 30 : 25;
            // Right Side Face
            ctx.beginPath();
            ctx.moveTo(screenX + tileW / 2, screenY + tileH / 2);
            ctx.lineTo(screenX, screenY + tileH);
            ctx.lineTo(screenX, screenY + tileH + wallDepth);
            ctx.lineTo(screenX + tileW / 2, screenY + tileH / 2 + wallDepth);
            ctx.closePath();
            ctx.fillStyle = '#2d1b11';
            ctx.fill();
            ctx.stroke();

            // Left Side Face
            ctx.beginPath();
            ctx.moveTo(screenX - tileW / 2, screenY + tileH / 2);
            ctx.lineTo(screenX, screenY + tileH);
            ctx.lineTo(screenX, screenY + tileH + wallDepth);
            ctx.lineTo(screenX - tileW / 2, screenY + tileH / 2 + wallDepth);
            ctx.closePath();
            ctx.fillStyle = '#1e110a';
            ctx.fill();
            ctx.stroke();
          }
        }
      }

      // 2. Draw Inset Miniature Moving Picture Frames on Platform Walls
      const frames = [
        { x: w * 0.32, y: h * 0.48, color: '#f59e0b', label: 'Fireplace' },
        { x: w * 0.46, y: h * 0.55, color: '#38bdf8', label: 'Windmill' },
        { x: w * 0.60, y: h * 0.62, color: '#ec4899', label: 'PSI Rift' },
      ];

      frames.forEach((f, idx) => {
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(f.x - 14, f.y - 12, 28, 22);
        ctx.strokeStyle = '#d97706';
        ctx.lineWidth = 2;
        ctx.strokeRect(f.x - 14, f.y - 12, 28, 22);

        // Animated wave inside frame
        ctx.beginPath();
        ctx.strokeStyle = f.color;
        ctx.lineWidth = 1.2;
        for (let fx = 0; fx < 24; fx += 3) {
          const fy = Math.sin(fx * 0.5 + time * 5 + idx) * 4;
          if (fx === 0) ctx.moveTo(f.x - 12 + fx, f.y + fy);
          else ctx.lineTo(f.x - 12 + fx, f.y + fy);
        }
        ctx.stroke();
      });

      // 3. Draw Stepped Wooden Ladders
      const ladders = [
        { start: { x: 3, y: 1 }, end: { x: 2, y: 1 } },
        { start: { x: 4, y: 4 }, end: { x: 3, y: 3 } },
      ];

      ladders.forEach((l) => {
        const sx = originX + (l.start.x - l.start.y) * (tileW / 2);
        const sy = originY + (l.start.x + l.start.y) * (tileH / 2) - getTierHeight(l.start.x, l.start.y);
        const ex = originX + (l.end.x - l.end.y) * (tileW / 2);
        const ey = originY + (l.end.x + l.end.y) * (tileH / 2) - getTierHeight(l.end.x, l.end.y);

        ctx.strokeStyle = '#854d0e';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(sx - 4, sy);
        ctx.lineTo(ex - 4, ey);
        ctx.moveTo(sx + 4, sy);
        ctx.lineTo(ex + 4, ey);
        ctx.stroke();

        // Rungs
        ctx.strokeStyle = '#ca8a04';
        ctx.lineWidth = 2;
        for (let r = 0; r <= 4; r++) {
          const rx = sx + (ex - sx) * (r / 4);
          const ry = sy + (ey - sy) * (r / 4);
          ctx.beginPath();
          ctx.moveTo(rx - 4, ry);
          ctx.lineTo(rx + 4, ry);
          ctx.stroke();
        }
      });

      // 4. Draw Curved Copper Slide Chutes
      const chutes = [
        { topX: 2, topY: 3, botX: 1, botY: 5 },
        { topX: 4, topY: 1, botX: 6, botY: 2 },
      ];

      chutes.forEach((c) => {
        const topH = getTierHeight(c.topX, c.topY);
        const botH = getTierHeight(c.botX, c.botY);
        const tx = originX + (c.topX - c.topY) * (tileW / 2);
        const ty = originY + (c.topX + c.topY) * (tileH / 2) - topH;
        const bx = originX + (c.botX - c.botY) * (tileW / 2);
        const by = originY + (c.botX + c.botY) * (tileH / 2) - botH;

        // Curved Copper Tube
        ctx.beginPath();
        ctx.strokeStyle = '#d97706';
        ctx.lineWidth = 7;
        ctx.moveTo(tx, ty);
        ctx.quadraticCurveTo((tx + bx) / 2 + 15, (ty + by) / 2 - 10, bx, by);
        ctx.stroke();

        // Metallic Highlight
        ctx.beginPath();
        ctx.strokeStyle = '#fef08a';
        ctx.lineWidth = 2;
        ctx.moveTo(tx, ty - 1);
        ctx.quadraticCurveTo((tx + bx) / 2 + 15, (ty + by) / 2 - 11, bx, by - 1);
        ctx.stroke();
      });

      // 5. Render Active 3D Chess Pieces
      units.forEach((unit) => {
        const uHeight = getTierHeight(unit.x, unit.y);
        const ux = originX + (unit.x - unit.y) * (tileW / 2);
        const uy = originY + (unit.x + unit.y) * (tileH / 2) - uHeight;

        // Idle Bobbing Animation
        const uBob = Math.sin(time * 4 + unit.x * 3) * 3;
        const px = ux;
        const py = uy - 12 + uBob;

        // Shadow under piece
        ctx.fillStyle = 'rgba(0,0,0,0.5)';
        ctx.beginPath();
        ctx.ellipse(ux, uy + 6, 12, 6, 0, 0, Math.PI * 2);
        ctx.fill();

        // Draw Specific 3D Piece Models
        if (unit.type === 'knight') {
          // Carved Wooden Knight Horsehead
          ctx.fillStyle = unit.team === 'player' ? '#f59e0b' : '#94a3b8';
          ctx.beginPath();
          ctx.arc(px, py - 8, 9, 0, Math.PI * 2);
          ctx.fill();
          // Mane & Snout
          ctx.fillRect(px - 10, py - 12, 7, 8);
          ctx.fillRect(px - 4, py - 4, 10, 16);
          // Golden Crown/Highlight
          ctx.strokeStyle = '#fef08a';
          ctx.lineWidth = 1.5;
          ctx.strokeRect(px - 4, py - 14, 8, 4);
        } else if (unit.type === 'bishop') {
          // Bishop with Miter Hat
          ctx.fillStyle = '#f8fafc';
          ctx.beginPath();
          ctx.arc(px, py - 10, 8, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillRect(px - 5, py - 6, 10, 16);
          // Cross topper
          ctx.fillStyle = '#eab308';
          ctx.fillRect(px - 1.5, py - 17, 3, 7);
          ctx.fillRect(px - 4, py - 15, 8, 2.5);
        } else if (unit.type === 'kirb_builder') {
          // Pink Kirby Builder Piece with Hardhat
          ctx.fillStyle = '#f472b6';
          ctx.beginPath();
          ctx.arc(px, py - 6, 10, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#fbbf24';
          ctx.fillRect(px - 8, py - 14, 16, 5);
        } else if (unit.type === 'scarab') {
          // Gold Pharaoh Scarab
          ctx.fillStyle = '#eab308';
          ctx.beginPath();
          ctx.ellipse(px, py - 4, 10, 7, 0, 0, Math.PI * 2);
          ctx.fill();
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 1.5;
          ctx.stroke();
        } else if (unit.type === 'mimic') {
          // Mimic Chest with Teeth
          ctx.fillStyle = '#78350f';
          ctx.fillRect(px - 10, py - 12, 20, 16);
          ctx.strokeStyle = '#ef4444';
          ctx.lineWidth = 2;
          ctx.strokeRect(px - 10, py - 12, 20, 16);
          // Sharp White Teeth
          ctx.fillStyle = '#ffffff';
          for (let t = 0; t < 4; t++) {
            ctx.fillRect(px - 8 + t * 4, py - 5, 2.5, 4);
          }
        } else if (unit.type === 'tesseract') {
          // Cyan Hypercube piece
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 1.5;
          ctx.strokeRect(px - 8, py - 14, 16, 16);
          ctx.fillStyle = 'rgba(56, 189, 248, 0.4)';
          ctx.fillRect(px - 8, py - 14, 16, 16);
        }

        // Mini HP Bar over unit
        const hpPercent = unit.hp / unit.maxHp;
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(px - 14, py - 24, 28, 4);
        ctx.fillStyle = unit.team === 'player' ? '#22c55e' : '#ef4444';
        ctx.fillRect(px - 14, py - 24, 28 * hpPercent, 4);
      });

      animId = requestAnimationFrame(render);
    };

    animId = requestAnimationFrame(render);
    return () => cancelAnimationFrame(animId);
  }, [units]);

  // Dice Roll Handler (Harvests Cross-Portal Mana)
  const handleRollDice = () => {
    if (isRollingDice) return;
    setIsRollingDice(true);
    audioEngine.playDiceRoll();

    let rollCount = 0;
    const interval = setInterval(() => {
      const randomVal = Math.floor(Math.random() * 6) + 1;
      setDiceValue(randomVal);
      rollCount++;

      if (rollCount >= 8) {
        clearInterval(interval);
        setIsRollingDice(false);
        const finalManaGain = randomVal * 15;
        setMana((m) => Math.min(150, m + finalManaGain));
        setActiveSpellLog(`Rolled a ${randomVal}! Harnessed +${finalManaGain} cross-portal mana from nearby overworld portals.`);
      }
    }, 60);
  };

  // Cross-Portal Spell Casting
  const handleCastSpell = (spell: CrossPortalSpell) => {
    if (mana < spell.manaCost) {
      audioEngine.playTextBlip(-6);
      setActiveSpellLog(`Not enough cross-portal mana (${mana}/${spell.manaCost}) to cast ${spell.name}!`);
      return;
    }

    setMana((m) => m - spell.manaCost);
    audioEngine.playSpellCast(spell.portalId.includes('pharaoh') ? 'pharaoh' : spell.portalId.includes('lava') ? 'magma' : 'psi');
    confetti({ particleCount: 40, spread: 60, origin: { y: 0.6 } });

    if (spell.effect === 'damage_all') {
      setUnits((prev) =>
        prev.map((u) => {
          if (u.team === 'enemy') {
            const damage = spell.targetTier !== undefined && u.tier !== spell.targetTier ? 15 : 40;
            return { ...u, hp: Math.max(0, u.hp - damage) };
          }
          return u;
        })
      );
      setActiveSpellLog(`⚡ Cast ${spell.name}! Channeled direct elemental destruction across the tiered chessboard.`);
    } else if (spell.effect === 'heal_team') {
      setUnits((prev) =>
        prev.map((u) => {
          if (u.team === 'player') {
            return { ...u, hp: Math.min(u.maxHp, u.hp + 45) };
          }
          return u;
        })
      );
      setActiveSpellLog(`🍄 Cast ${spell.name}! Spore mists restored 45 HP to all friendly pieces.`);
    } else if (spell.effect === 'stun_tier') {
      setUnits((prev) =>
        prev.map((u) => {
          if (u.team === 'enemy' && u.tier === spell.targetTier) {
            return { ...u, hp: Math.max(0, u.hp - 30) };
          }
          return u;
        })
      );
      setActiveSpellLog(`🌀 Cast ${spell.name}! Paralyzed all enemy pieces on Tier ${spell.targetTier}.`);
    } else if (spell.effect === 'elevate_ladder') {
      setUnits((prev) =>
        prev.map((u) => {
          if (u.id === 'p3' && u.tier < 2) {
            audioEngine.playLadderClimb ? audioEngine.playLadderClimb() : audioEngine.playSuccessFanfare();
            return { ...u, tier: (u.tier + 1) as 0 | 1 | 2, x: u.x + 1, y: u.y - 1 };
          }
          return u;
        })
      );
      setActiveSpellLog(`🪜 Cast ${spell.name}! Kirb Builder scaled the wooden ladder to a higher tactical terrace!`);
    }
  };

  // Step Auto-Battle Round
  const handleStepTurn = () => {
    audioEngine.playSporeChime(600);
    setBattleRound((r) => r + 1);

    // Friendly units attack nearest enemies
    setUnits((prev) => {
      let updated = [...prev];

      // Kirb slides down copper chute if on upper level
      updated = updated.map((u) => {
        if (u.id === 'p1' && u.tier === 2 && Math.random() > 0.5) {
          audioEngine.playSlideDown();
          return { ...u, tier: 0, x: 2, y: 5 };
        }
        return u;
      });

      // Simple combat tick
      return updated
        .map((u) => {
          if (u.team === 'player') {
            return { ...u, mana: Math.min(u.maxMana, u.mana + 15) };
          } else {
            const damageTaken = Math.floor(Math.random() * 25) + 10;
            return { ...u, hp: Math.max(0, u.hp - damageTaken) };
          }
        })
        .filter((u) => u.hp > 0);
    });

    setActiveSpellLog(`Battle Round ${battleRound}: Golden Knight slid down the copper chute into close combat!`);
  };

  return (
    <div className="w-full rounded-2xl bg-gradient-to-b from-amber-950/90 via-slate-950 to-amber-950/80 border-2 border-amber-500/60 p-3 sm:p-5 shadow-[0_0_40px_rgba(245,158,11,0.25)] flex flex-col gap-4 text-amber-100">
      {/* ========================================================================= */}
      {/* 3D DIORAMA AUTO-CHESS ARENA HEADER */}
      {/* ========================================================================= */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-amber-500/40">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/40 shadow-[0_0_15px_rgba(245,158,11,0.4)] flex items-center justify-center">
            <Swords className="w-6 h-6 animate-pulse" />
          </div>
          <div>
            <h2 className="text-base sm:text-lg font-black tracking-wider text-amber-300 drop-shadow-[0_0_10px_#f59e0b] flex items-center gap-2">
              <span>3D MULTIVERSE AUTO-CHESS ARENA</span>
              <span className="text-[10px] text-amber-400 bg-amber-950/90 px-2 py-0.5 rounded border border-amber-500/40 font-mono">
                TIERED CHUTES & LADDERS
              </span>
            </h2>
            <p className="text-xs text-amber-400/80 font-sans">
              Autonomous 3D Chess Board with Slide Chutes, Mimic Chests & Cross-Portal Spells
            </p>
          </div>
        </div>

        {/* Dice & Mana Resource Bank */}
        <div className="flex items-center gap-3 bg-slate-950/90 px-3 py-1.5 rounded-xl border border-amber-500/40 text-xs">
          {/* Mana Pool */}
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-sky-400 fill-sky-400" />
            <div>
              <span className="text-slate-400 block text-[9px] font-mono">PORTAL MANA</span>
              <span className="font-black text-sky-300 text-sm">{mana} / 150</span>
            </div>
          </div>

          <div className="w-px h-7 bg-amber-800/60" />

          {/* Glowing Roll Dice Button */}
          <button
            onClick={handleRollDice}
            disabled={isRollingDice}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-amber-500 to-yellow-600 hover:from-amber-400 hover:to-yellow-500 text-slate-950 font-black text-xs shadow-[0_0_15px_rgba(245,158,11,0.4)] transition-transform hover:scale-105 active:scale-95 disabled:opacity-50"
          >
            <Dices className={`w-4 h-4 ${isRollingDice ? 'animate-spin' : ''}`} />
            <span>{diceValue ? `DICE: [${diceValue}]` : 'ROLL DICE'}</span>
          </button>
        </div>
      </div>

      {/* Main Arena: Left Spell Deck + Center 3D Board Canvas + Right Unit Roster */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        {/* Left Column: Cross-Portal Spells Harness Bar */}
        <div className="lg:col-span-1 flex flex-col gap-2.5 bg-slate-950/80 p-3 rounded-xl border border-amber-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-amber-300 tracking-wider flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-amber-400" />
              <span>CROSS-PORTAL SPELLS</span>
            </span>
            <span className="text-[10px] font-mono text-slate-400">Nearby Worlds</span>
          </div>

          <div className="flex flex-col gap-2 overflow-y-auto max-h-[340px] pr-1">
            {spells.map((spell) => {
              const canAfford = mana >= spell.manaCost;
              return (
                <button
                  key={spell.id}
                  onClick={() => handleCastSpell(spell)}
                  disabled={!canAfford}
                  className={`text-left p-2.5 rounded-xl border transition-all flex flex-col gap-1 ${
                    canAfford
                      ? 'bg-slate-900/90 hover:bg-slate-800/90 border-slate-700 hover:border-amber-400 shadow-md hover:scale-[1.02]'
                      : 'bg-slate-950/50 border-slate-900 opacity-50 cursor-not-allowed'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-white flex items-center gap-1.5">
                      <span>{spell.icon}</span>
                      <span>{spell.name}</span>
                    </span>
                    <span className="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded bg-sky-950 text-sky-300 border border-sky-500/40">
                      {spell.manaCost} MP
                    </span>
                  </div>
                  <span className="text-[9px] font-mono text-amber-400/80">{spell.portalName}</span>
                  <p className="text-[10px] text-slate-300 line-clamp-2 leading-tight">{spell.description}</p>
                </button>
              );
            })}
          </div>
        </div>

        {/* Center: 3D Isometric Wooden Tiered Chess Canvas */}
        <div className="lg:col-span-2 relative flex flex-col items-center justify-center bg-black rounded-xl border border-amber-500/40 overflow-hidden shadow-2xl min-h-[350px]">
          <canvas
            ref={canvasRef}
            width={540}
            height={350}
            className="w-full h-full"
          />

          {/* In-Canvas Action Controls */}
          <div className="absolute bottom-2.5 right-2.5 flex items-center gap-2">
            <button
              onClick={handleStepTurn}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-500 to-rose-600 hover:from-amber-400 hover:to-rose-500 text-white font-bold text-xs shadow-lg transition-transform hover:scale-105 active:scale-95"
            >
              <Swords className="w-3.5 h-3.5" />
              <span>STEP TURN #{battleRound}</span>
            </button>
          </div>

          {/* Tier Label Overlays */}
          <div className="absolute top-2 left-2 flex flex-col gap-1 pointer-events-none text-[9px] font-mono">
            <span className="px-2 py-0.5 rounded bg-slate-900/80 text-amber-300 border border-amber-500/30">
              ▲ TIER 2: HIGH PLATEAU
            </span>
            <span className="px-2 py-0.5 rounded bg-slate-900/80 text-sky-300 border border-sky-500/30">
              ■ TIER 1: MID TERRACE
            </span>
            <span className="px-2 py-0.5 rounded bg-slate-900/80 text-emerald-300 border border-emerald-500/30">
              ▼ TIER 0: GROUND CHUTE EXIT
            </span>
          </div>
        </div>

        {/* Right Column: Piece Roster & Tactical Board Overview */}
        <div className="lg:col-span-1 flex flex-col gap-2.5 bg-slate-950/80 p-3 rounded-xl border border-amber-500/30">
          <span className="text-xs font-bold text-amber-300 tracking-wider flex items-center gap-1.5">
            <Layers className="w-4 h-4 text-sky-400" />
            <span>ACTIVE PIECES ({units.length})</span>
          </span>

          <div className="flex flex-col gap-1.5 overflow-y-auto max-h-[340px] pr-1">
            {units.map((unit) => (
              <div
                key={unit.id}
                className="p-2 rounded-lg bg-slate-900/70 border border-slate-800 flex items-center justify-between text-xs"
              >
                <div className="flex items-center gap-2">
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: unit.color }}
                  />
                  <div>
                    <span className="font-bold text-white block text-[11px] leading-tight">
                      {unit.name}
                    </span>
                    <span className="text-[9px] font-mono text-slate-400">
                      Tier {unit.tier} • Pos ({unit.x},{unit.y})
                    </span>
                  </div>
                </div>

                <div className="text-right">
                  <span className={`font-mono text-[10px] font-bold ${unit.team === 'player' ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {unit.hp}/{unit.maxHp} HP
                  </span>
                  <span className="block text-[8px] font-mono text-slate-400">
                    ATK: {unit.attack}
                  </span>
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={() => {
              setUnits((prev) => [
                ...prev,
                {
                  id: `hero_${Date.now()}`,
                  name: 'Reinforcement Pawn',
                  type: 'pawn',
                  team: 'player',
                  tier: 0,
                  x: 0,
                  y: 7,
                  hp: 90,
                  maxHp: 90,
                  attack: 20,
                  range: 1,
                  mana: 0,
                  maxMana: 100,
                  color: '#34d399',
                },
              ]);
              audioEngine.playTextBlip(2);
            }}
            className="mt-auto py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-amber-300 font-mono text-[10px] border border-amber-500/40 text-center transition-colors"
          >
            + Deploy Reinforcement Piece
          </button>
        </div>
      </div>

      {/* Dynamic Battle & Spell Log Banner */}
      <div className="p-2.5 rounded-xl bg-slate-950/90 border border-amber-500/30 flex items-center gap-2 text-xs font-mono text-amber-200">
        <Radio className="w-4 h-4 text-amber-400 shrink-0 animate-pulse" />
        <span className="line-clamp-1">{activeSpellLog}</span>
      </div>
    </div>
  );
};
