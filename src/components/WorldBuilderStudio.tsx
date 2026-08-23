/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useRef, useEffect } from 'react';
import { PortalSurface, BuilderVoxel, EpochEra, CustomBattlefield } from '../types';
import { audioEngine } from '../utils/audio';
import { multiplayerEngine } from '../utils/multiplayerEngine';
import {
  Hammer,
  HardHat,
  Box,
  Layers,
  Sparkles,
  Plus,
  Play,
  RotateCcw,
  Download,
  AlertTriangle,
  Terminal,
  Cpu,
  CheckCircle2,
  Sliders,
  Swords,
} from 'lucide-react';
import confetti from 'canvas-confetti';

interface WorldBuilderStudioProps {
  onDeployWorld: (portal: PortalSurface) => void;
  onDeployToMultiplayer?: (battlefield: CustomBattlefield) => void;
  onClose?: () => void;
}

export const WorldBuilderStudio: React.FC<WorldBuilderStudioProps> = ({
  onDeployWorld,
  onDeployToMultiplayer,
  onClose,
}) => {
  const [activeTool, setActiveTool] = useState<BuilderVoxel['type']>('kirb_worker');
  const [worldName, setWorldName] = useState('Dreamland Construction Zone');
  const [worldSubtitle, setWorldSubtitle] = useState('Zone A: Foundation & Assembly Matrix');
  const [frequency, setFrequency] = useState(528);
  const [epoch, setEpoch] = useState<EpochEra>('16bit');
  const [builderCount, setBuilderCount] = useState(54);
  const [progressPercent, setProgressPercent] = useState(88);
  const [terminalLog, setTerminalLog] = useState<string[]>([
    '[SYSTEM] Kirby Builders Engine v3.0 initialized.',
    '[USER] did you make me type ascnid?',
    '[USER] didnt mean it.',
    '[KIRB_AI] WHYOD YOU ALL CAPS AT ME? BIG AND BRIGHT ☆',
    '[SYSTEM] Ready to assemble new macro portal world.',
  ]);

  // Placed Elements on the Isometric Grid
  const [voxels, setVoxels] = useState<BuilderVoxel[]>([
    { id: '1', x: 2, y: 2, zone: 'foundation', type: 'crane', color: '#eab308' },
    { id: '2', x: 4, y: 3, zone: 'assembly', type: 'kirb_worker', color: '#f472b6', label: 'Builder' },
    { id: '3', x: 5, y: 3, zone: 'assembly', type: 'kirb_worker', color: '#fb7185', label: 'Hardhat' },
    { id: '4', x: 3, y: 4, zone: 'foundation', type: 'question_block', color: '#fbbf24' },
    { id: '5', x: 6, y: 2, zone: 'assembly', type: 'chute', color: '#f97316' },
    { id: '6', x: 1, y: 4, zone: 'foundation', type: 'portal_frame', color: '#38bdf8' },
  ]);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Isometric Canvas Rendering Loop
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

      // Dark Pixel Green Retro CRT Screen
      ctx.fillStyle = '#021a14';
      ctx.fillRect(0, 0, w, h);

      // Grid Dimensions
      const originX = w * 0.5;
      const originY = h * 0.28;
      const tileW = 48;
      const tileH = 24;
      const gridSize = 7;

      // Draw Distant Mountain & Cloud Pixel Wireframe
      ctx.strokeStyle = 'rgba(52, 211, 153, 0.2)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(0, h * 0.3);
      ctx.lineTo(w * 0.25, h * 0.15);
      ctx.lineTo(w * 0.45, h * 0.28);
      ctx.lineTo(w * 0.75, h * 0.12);
      ctx.lineTo(w, h * 0.25);
      ctx.stroke();

      // Draw Isometric Stepped Platforms (Zone A: Foundation vs Zone B: Assembly)
      for (let x = 0; x < gridSize; x++) {
        for (let y = 0; y < gridSize; y++) {
          const isAssembly = x >= 3 && y <= 3;
          const heightOffset = isAssembly ? 24 : 0;

          const screenX = originX + (x - y) * (tileW / 2);
          const screenY = originY + (x + y) * (tileH / 2) - heightOffset;

          // Top Diamond Face
          ctx.beginPath();
          ctx.moveTo(screenX, screenY);
          ctx.lineTo(screenX + tileW / 2, screenY + tileH / 2);
          ctx.lineTo(screenX, screenY + tileH);
          ctx.lineTo(screenX - tileW / 2, screenY + tileH / 2);
          ctx.closePath();

          ctx.fillStyle = isAssembly ? '#064e3b' : '#042f2e';
          ctx.fill();
          ctx.strokeStyle = isAssembly ? '#34d399' : '#10b981';
          ctx.lineWidth = 1;
          ctx.stroke();

          // Isometric Extruded Platform Walls
          if (x === gridSize - 1 || y === gridSize - 1 || (!isAssembly && (x === 2 || y === 3))) {
            const depth = 20;
            // Right Wall
            ctx.beginPath();
            ctx.moveTo(screenX + tileW / 2, screenY + tileH / 2);
            ctx.lineTo(screenX, screenY + tileH);
            ctx.lineTo(screenX, screenY + tileH + depth);
            ctx.lineTo(screenX + tileW / 2, screenY + tileH / 2 + depth);
            ctx.closePath();
            ctx.fillStyle = '#022c22';
            ctx.fill();
            ctx.stroke();

            // Left Wall
            ctx.beginPath();
            ctx.moveTo(screenX - tileW / 2, screenY + tileH / 2);
            ctx.lineTo(screenX, screenY + tileH);
            ctx.lineTo(screenX, screenY + tileH + depth);
            ctx.lineTo(screenX - tileW / 2, screenY + tileH / 2 + depth);
            ctx.closePath();
            ctx.fillStyle = '#011c16';
            ctx.fill();
            ctx.stroke();
          }
        }
      }

      // Zone Markers
      ctx.font = '10px monospace';
      ctx.fillStyle = '#fbbf24';
      ctx.fillText('ZONE A: FOUNDATION', w * 0.15, h * 0.72);
      ctx.fillStyle = '#34d399';
      ctx.fillText('ZONE B: ASSEMBLY', w * 0.62, h * 0.52);

      // Render Voxels & Active Kirby Workers
      voxels.forEach((v) => {
        const isAssembly = v.x >= 3 && v.y <= 3;
        const heightOffset = isAssembly ? 24 : 0;
        const vx = originX + (v.x - v.y) * (tileW / 2);
        const vy = originY + (v.x + v.y) * (tileH / 2) - heightOffset;

        if (v.type === 'kirb_worker') {
          // Animated Bobbing Kirby Builder with Hardhat
          const bob = Math.sin(time * 6 + v.x * 2) * 4;
          const kx = vx;
          const ky = vy - 10 + bob;

          // Pink Body
          ctx.fillStyle = '#f472b6';
          ctx.beginPath();
          ctx.arc(kx, ky, 14, 0, Math.PI * 2);
          ctx.fill();
          ctx.strokeStyle = '#db2777';
          ctx.lineWidth = 1.5;
          ctx.stroke();

          // Red Shoes
          ctx.fillStyle = '#e11d48';
          ctx.beginPath();
          ctx.ellipse(kx - 7, ky + 11, 6, 4, 0, 0, Math.PI * 2);
          ctx.ellipse(kx + 7, ky + 11, 6, 4, 0, 0, Math.PI * 2);
          ctx.fill();

          // Yellow Hardhat
          ctx.fillStyle = '#fbbf24';
          ctx.beginPath();
          ctx.arc(kx, ky - 10, 11, Math.PI, Math.PI * 2);
          ctx.fill();
          ctx.fillRect(kx - 13, ky - 11, 26, 4);

          // Cheerful Eyes & Blush
          ctx.fillStyle = '#0f172a';
          ctx.fillRect(kx - 4, ky - 4, 2.5, 5);
          ctx.fillRect(kx + 2, ky - 4, 2.5, 5);
          ctx.fillStyle = '#fb7185';
          ctx.beginPath();
          ctx.arc(kx - 7, ky + 1, 3, 0, Math.PI * 2);
          ctx.arc(kx + 7, ky + 1, 3, 0, Math.PI * 2);
          ctx.fill();

          // Hammer / Tool in Hand
          ctx.strokeStyle = '#94a3b8';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.moveTo(kx + 12, ky + 4);
          ctx.lineTo(kx + 18, ky - 6 + Math.sin(time * 10) * 4);
          ctx.stroke();
          ctx.fillStyle = '#64748b';
          ctx.fillRect(kx + 14, ky - 10 + Math.sin(time * 10) * 4, 8, 6);
        } else if (v.type === 'crane') {
          // Yellow Construction Gantry Crane
          ctx.strokeStyle = '#eab308';
          ctx.lineWidth = 2.5;
          ctx.beginPath();
          ctx.moveTo(vx, vy);
          ctx.lineTo(vx, vy - 60);
          ctx.lineTo(vx + 45, vy - 60);
          ctx.stroke();

          // Hanging Voxel Block from Crane Cable
          const cableLen = 25 + Math.sin(time * 2) * 8;
          ctx.strokeStyle = '#cbd5e1';
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(vx + 35, vy - 60);
          ctx.lineTo(vx + 35, vy - 60 + cableLen);
          ctx.stroke();

          // Hanging Block
          ctx.fillStyle = '#f472b6';
          ctx.fillRect(vx + 25, vy - 60 + cableLen, 20, 20);
          ctx.strokeStyle = '#fbbf24';
          ctx.strokeRect(vx + 25, vy - 60 + cableLen, 20, 20);
        } else if (v.type === 'question_block') {
          // Floating Gold Question Block
          const bBob = Math.sin(time * 4) * 3;
          ctx.fillStyle = '#f59e0b';
          ctx.fillRect(vx - 12, vy - 24 + bBob, 24, 24);
          ctx.strokeStyle = '#fef08a';
          ctx.lineWidth = 1.5;
          ctx.strokeRect(vx - 12, vy - 24 + bBob, 24, 24);
          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 12px monospace';
          ctx.fillText('?', vx - 4, vy - 8 + bBob);
        } else if (v.type === 'chute') {
          // Curved Slide / Copper Chute
          ctx.strokeStyle = '#f97316';
          ctx.lineWidth = 4;
          ctx.beginPath();
          ctx.moveTo(vx + 20, vy - 35);
          ctx.quadraticCurveTo(vx, vy - 10, vx - 20, vy + 5);
          ctx.stroke();
        } else if (v.type === 'portal_frame') {
          // Micro Live Moving Picture Portal
          ctx.fillStyle = '#0f172a';
          ctx.fillRect(vx - 16, vy - 32, 32, 28);
          ctx.strokeStyle = '#38bdf8';
          ctx.lineWidth = 2;
          ctx.strokeRect(vx - 16, vy - 32, 32, 28);

          // Moving wave inside picture frame
          ctx.strokeStyle = '#34d399';
          ctx.lineWidth = 1;
          ctx.beginPath();
          for (let px = 0; px < 28; px += 4) {
            const py = Math.sin(px * 0.4 + time * 6) * 6;
            if (px === 0) ctx.moveTo(vx - 14 + px, vy - 18 + py);
            else ctx.lineTo(vx - 14 + px, vy - 18 + py);
          }
          ctx.stroke();
        }
      });

      // Sparks & Construction Weld FX
      const sparkX = originX + 20;
      const sparkY = originY + 40;
      for (let s = 0; s < 5; s++) {
        const sx = sparkX + Math.sin(time * 20 + s) * 12;
        const sy = sparkY + Math.cos(time * 20 + s) * 12;
        ctx.fillStyle = '#fde047';
        ctx.fillRect(sx, sy, 2, 2);
      }

      animId = requestAnimationFrame(render);
    };

    animId = requestAnimationFrame(render);
    return () => cancelAnimationFrame(animId);
  }, [voxels]);

  // Click Canvas to place active tool
  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    const w = canvas.width;
    const h = canvas.height;
    const originX = w * 0.5;
    const originY = h * 0.28;
    const tileW = 48;
    const tileH = 24;

    // Convert Screen coordinates to approximate isometric tile (x, y)
    const relX = clickX - originX;
    const relY = clickY - originY;
    const gridX = Math.round((relX / (tileW / 2) + relY / (tileH / 2)) / 2);
    const gridY = Math.round((relY / (tileH / 2) - relX / (tileW / 2)) / 2);

    if (gridX >= 0 && gridX < 7 && gridY >= 0 && gridY < 7) {
      audioEngine.playHammerTap();
      const newVoxel: BuilderVoxel = {
        id: Date.now().toString(),
        x: gridX,
        y: gridY,
        zone: gridX >= 3 && gridY <= 3 ? 'assembly' : 'foundation',
        type: activeTool,
        color: activeTool === 'kirb_worker' ? '#f472b6' : '#eab308',
      };
      setVoxels((prev) => [...prev, newVoxel]);
      setBuilderCount((c) => c + 1);
      setProgressPercent((p) => Math.min(100, p + 2));

      setTerminalLog((prev) => [
        ...prev.slice(-4),
        `[BUILD] Deployed ${activeTool.toUpperCase()} to Grid (${gridX}, ${gridY})`,
      ]);
    }
  };

  // Deploy this custom builder world as an active 3D Portal in the Overworld & Save as a Multiplayer Arena Map
  const handleDeployToOverworld = (launchMultiplayer: boolean = false) => {
    audioEngine.playSuccessFanfare();
    confetti({ particleCount: 75, spread: 80, origin: { y: 0.5 } });

    const newFieldId = `field_${Date.now()}`;
    const customTiles = voxels.map((v) => ({
      x: v.x,
      y: v.y,
      tier: (v.zone === 'assembly' ? 1 : v.zone === 'canopy' ? 2 : 0) as 0 | 1 | 2,
      type: v.type,
      color: v.color,
    }));

    const chuteVoxels = voxels.filter((v) => v.type === 'chute');
    const customChutes = chuteVoxels.map((c) => ({
      topX: c.x,
      topY: c.y,
      botX: Math.min(6, c.x + 2),
      botY: Math.min(6, c.y + 2),
    }));

    const newBattlefield: CustomBattlefield = {
      id: newFieldId,
      name: worldName,
      theme: worldSubtitle,
      gridSize: 7,
      accentColor: '#f472b6',
      tiles: customTiles,
      chutes: customChutes,
      ladders: [{ startX: 2, startY: 2, endX: 3, endY: 3 }],
      creator: 'Foreman Kirby',
      createdAt: Date.now(),
    };

    multiplayerEngine.saveBattlefield(newBattlefield);

    const newPortal: PortalSurface = {
      id: `builder_world_${Date.now()}`,
      name: worldName,
      subtitle: worldSubtitle,
      theme: 'Kirby Builders Voxel Construction',
      epoch: epoch,
      accentColor: '#f472b6',
      frameStyle: 'custom',
      ambientFrequency: frequency,
      lore: `A living construction realm forged in the Kirby Builders Studio with ${voxels.length} voxel scaffolds, active hammer workers, and curved chutes connecting assembly tiers.`,
      interactiveHint: 'Click to spawn hammer builders, tap crane blocks, and ride the chutes.',
      isGenerated: true,
    };

    onDeployWorld(newPortal);

    if (launchMultiplayer && onDeployToMultiplayer) {
      onDeployToMultiplayer(newBattlefield);
    } else if (onClose) {
      onClose();
    }
  };

  return (
    <div className="w-full rounded-2xl bg-slate-950 border-2 border-emerald-500/70 p-3 sm:p-5 shadow-[0_0_40px_rgba(16,185,129,0.25)] flex flex-col gap-4 font-mono text-emerald-400">
      {/* ========================================================================= */}
      {/* RETRO CRT HEADER: KIRBY BUILDERS - CONSTRUCTION IN PROGRESS */}
      {/* ========================================================================= */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b-2 border-emerald-500/40">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-pink-500/20 text-pink-400 border border-pink-500/40 shadow-[0_0_15px_rgba(244,114,182,0.4)] flex items-center justify-center">
            <HardHat className="w-6 h-6 animate-bounce" />
          </div>
          <div>
            <h2 className="text-base sm:text-lg font-black tracking-wider text-pink-400 drop-shadow-[0_0_10px_#f472b6] flex items-center gap-2">
              <span>KIRBY BUILDERS — CONSTRUCTION IN PROGRESS</span>
              <span className="text-[10px] text-emerald-300 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-500/50">
                VERSION 3.0 BIG AND BRIGHT ☆
              </span>
            </h2>
            <p className="text-xs text-emerald-500">
              Interactive 3D Voxel World Creator & Live Moving Picture Portal Generator
            </p>
          </div>
        </div>

        {/* Telemetry Status Gauges */}
        <div className="flex items-center gap-3 bg-slate-900/90 px-3 py-1.5 rounded-xl border border-emerald-500/40 text-xs">
          <div>
            <span className="text-emerald-600 block text-[10px]">PROGRESS</span>
            <span className="font-bold text-emerald-300">{progressPercent}%</span>
          </div>
          <div className="w-px h-6 bg-emerald-800" />
          <div>
            <span className="text-emerald-600 block text-[10px]">BUILDERS</span>
            <span className="font-bold text-pink-400">{builderCount}</span>
          </div>
          <div className="w-px h-6 bg-emerald-800" />
          <div>
            <span className="text-emerald-600 block text-[10px]">POWER</span>
            <span className="font-bold text-amber-400">HIGH</span>
          </div>
        </div>
      </div>

      {/* Main Studio Workspace: Left Palette + Center Canvas + Right Settings */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        {/* Left Palette: Kirb-Types & Construction Blocks */}
        <div className="lg:col-span-1 flex flex-col gap-3 bg-slate-900/80 p-3 rounded-xl border border-emerald-500/30">
          <span className="text-xs font-bold text-emerald-300 tracking-wider flex items-center gap-1.5">
            <Hammer className="w-4 h-4 text-pink-400" />
            <span>■ KIRB-TYPES & BLOCKS</span>
          </span>

          <div className="grid grid-cols-2 gap-2">
            {[
              { type: 'kirb_worker', label: 'Kirby Builder', icon: '👷' },
              { type: 'crane', label: 'Gantry Crane', icon: '🏗️' },
              { type: 'question_block', label: 'Voxel Block', icon: '📦' },
              { type: 'chute', label: 'Copper Chute', icon: '🛝' },
              { type: 'portal_frame', label: 'Picture Frame', icon: '🖼️' },
              { type: 'ladder', label: 'Wood Ladder', icon: '🪜' },
            ].map((t) => (
              <button
                key={t.type}
                onClick={() => {
                  setActiveTool(t.type as BuilderVoxel['type']);
                  audioEngine.playSporeChime(500);
                }}
                className={`flex flex-col items-center justify-center p-2.5 rounded-lg border text-xs transition-all ${
                  activeTool === t.type
                    ? 'bg-pink-950/80 text-pink-200 border-pink-500 shadow-[0_0_12px_rgba(244,114,182,0.3)] scale-105'
                    : 'bg-slate-950 text-slate-400 border-slate-800 hover:border-emerald-500/50 hover:text-emerald-300'
                }`}
              >
                <span className="text-lg">{t.icon}</span>
                <span className="mt-1 font-bold text-[10px] text-center">{t.label}</span>
              </button>
            ))}
          </div>

          <div className="mt-2 pt-2 border-t border-slate-800 text-[11px] text-slate-400">
            <p>✦ Click anywhere on the 3D isometric grid to build structures and spawn hardhat workers.</p>
          </div>

          {/* Warning Banner from user artwork */}
          <div className="mt-auto bg-rose-950/40 border border-rose-500/40 p-2 rounded-lg text-[10px] text-rose-300 flex items-start gap-1.5">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-rose-400 animate-pulse" />
            <div>
              <span className="font-bold">WARNING:</span> HIGH CAPS LEVEL DETECTED
              <p className="text-[9px] text-rose-400/80 mt-0.5">"WHYOD YOU ALL CAPS AT ME?"</p>
            </div>
          </div>
        </div>

        {/* Center Canvas Stage: Live Isometric Construction Matrix */}
        <div className="lg:col-span-2 relative flex flex-col items-center justify-center bg-black rounded-xl border border-emerald-500/40 overflow-hidden shadow-inner min-h-[340px]">
          <canvas
            ref={canvasRef}
            width={540}
            height={340}
            onClick={handleCanvasClick}
            className="w-full h-full cursor-crosshair"
          />

          {/* Quick Clear / Reset Tool */}
          <div className="absolute top-2 right-2 flex items-center gap-1.5">
            <button
              onClick={() => {
                setVoxels([]);
                audioEngine.playTextBlip(-4);
              }}
              className="px-2 py-1 rounded bg-slate-950/80 hover:bg-slate-900 text-slate-400 hover:text-rose-300 text-[10px] border border-slate-700"
              title="Clear Grid"
            >
              <RotateCcw className="w-3 h-3" />
            </button>
          </div>
        </div>

        {/* Right Configuration & Deploy Panel */}
        <div className="lg:col-span-1 flex flex-col gap-3 bg-slate-900/80 p-3 rounded-xl border border-emerald-500/30">
          <span className="text-xs font-bold text-emerald-300 tracking-wider flex items-center gap-1.5">
            <Sliders className="w-4 h-4 text-sky-400" />
            <span>■ WORLD CONFIG</span>
          </span>

          <div>
            <label className="text-[10px] text-slate-400 block mb-1">World Dimension Name</label>
            <input
              type="text"
              value={worldName}
              onChange={(e) => setWorldName(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 focus:border-emerald-400 px-2 py-1 rounded text-xs text-white"
            />
          </div>

          <div>
            <label className="text-[10px] text-slate-400 block mb-1">Theme Subtitle</label>
            <input
              type="text"
              value={worldSubtitle}
              onChange={(e) => setWorldSubtitle(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 focus:border-emerald-400 px-2 py-1 rounded text-xs text-white"
            />
          </div>

          <div>
            <label className="text-[10px] text-slate-400 block mb-1">Harmonic Tone ({frequency} Hz)</label>
            <input
              type="range"
              min="100"
              max="900"
              value={frequency}
              onChange={(e) => {
                const val = Number(e.target.value);
                setFrequency(val);
                audioEngine.setPortalHum(val);
              }}
              className="w-full accent-emerald-400"
            />
          </div>

          {/* Deploy Buttons */}
          <div className="mt-auto flex flex-col gap-2">
            <button
              onClick={() => handleDeployToOverworld(false)}
              className="flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-gradient-to-r from-emerald-500 via-teal-500 to-sky-500 hover:from-emerald-400 hover:to-sky-400 text-slate-950 font-black text-xs shadow-[0_0_20px_rgba(16,185,129,0.5)] transition-all hover:scale-105 active:scale-95"
            >
              <Sparkles className="w-4 h-4" />
              <span>DEPLOY TO OVERWORLD</span>
            </button>

            <button
              onClick={() => handleDeployToOverworld(true)}
              className="flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-xs shadow-[0_0_20px_rgba(168,85,247,0.4)] transition-all hover:scale-105 active:scale-95"
            >
              <Swords className="w-4 h-4" />
              <span>HOST ATB MULTIPLAYER RAID</span>
            </button>
          </div>
        </div>
      </div>

      {/* Bottom Retro User Log & Diagnostic Terminal */}
      <div className="bg-slate-950 p-2.5 rounded-xl border border-emerald-500/30 flex flex-col gap-1 text-[11px]">
        <div className="flex items-center gap-1.5 text-emerald-400 font-bold">
          <Terminal className="w-3.5 h-3.5" />
          <span>USER LOG & SYSTEM CONSOLE</span>
        </div>
        <div className="bg-black/60 p-2 rounded border border-emerald-950 font-mono text-[10px] flex flex-col gap-0.5 text-emerald-400/90">
          {terminalLog.map((log, idx) => (
            <div key={idx}>{log}</div>
          ))}
        </div>
      </div>
    </div>
  );
};
