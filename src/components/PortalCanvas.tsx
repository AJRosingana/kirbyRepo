/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useRef, useState, useCallback } from 'react';
import { PortalSurface, EpochEra } from '../types';
import { audioEngine } from '../utils/audio';
import { SporeNetworkSim } from './SporeNetworkSim';
import { Sparkles, Terminal, CheckCircle2, RotateCw, Flame, Eye } from 'lucide-react';
import confetti from 'canvas-confetti';

interface PortalCanvasProps {
  portal: PortalSurface;
  epoch: EpochEra;
  isActive: boolean;
  onQuestProgress?: (nodeId: string, value?: any) => void;
  isQuestCompleted?: boolean;
}

export const PortalCanvas: React.FC<PortalCanvasProps> = ({
  portal,
  epoch,
  isActive,
  onQuestProgress,
  isQuestCompleted,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animationFrameRef = useRef<number | null>(null);

  // Interactive quest state for PSI nodes (Cosmic PSI Rift)
  const [psiNodesClicked, setPsiNodesClicked] = useState<number[]>([]);
  // Interactive quest state for Pharaoh Ka orbs (Pharaoh's Radiant Dune Gate)
  const [kaOrbsClicked, setKaOrbsClicked] = useState<number[]>([]);
  // Interactive hex state for Cyber-Archaeology
  const [hexInput, setHexInput] = useState('');
  const [hexUnlocked, setHexUnlocked] = useState(false);
  // Interactive ring state for Sky Citadel
  const [ringAngles, setRingAngles] = useState<[number, number, number]>([45, 140, 260]);
  const [isAligning, setIsAligning] = useState(false);
  // Interactive magma crystals for Lava Foundry
  const [magmaCrystals, setMagmaCrystals] = useState<number>(0);

  // Mouse coords
  const mousePos = useRef({ x: 0, y: 0, isDown: false });

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    mousePos.current.x = (e.clientX - rect.left) * (e.currentTarget.width / rect.width);
    mousePos.current.y = (e.clientY - rect.top) * (e.currentTarget.height / rect.height);
  };

  const handleMouseDown = () => {
    mousePos.current.isDown = true;
    audioEngine.playTextBlip(2);
  };

  const handleMouseUp = () => {
    mousePos.current.isDown = false;
  };

  // Trigger quest progress callbacks for Pharaoh Ka Orbs
  const handleKaOrbClick = (orbIdx: number) => {
    if (kaOrbsClicked.includes(orbIdx)) return;
    const next = [...kaOrbsClicked, orbIdx];
    setKaOrbsClicked(next);
    audioEngine.playMelodyNote(1 + orbIdx * 2);
    if (next.length >= 3 && onQuestProgress) {
      onQuestProgress('node_pharaoh');
      audioEngine.playSuccessFanfare();
      confetti({ particleCount: 60, spread: 75, origin: { y: 0.6 } });
    }
  };

  // Trigger quest progress callbacks
  const handlePsiNodeClick = (nodeIdx: number) => {
    if (psiNodesClicked.includes(nodeIdx)) return;
    const next = [...psiNodesClicked, nodeIdx];
    setPsiNodesClicked(next);
    audioEngine.playMelodyNote(nodeIdx * 2);
    if (next.length >= 3 && onQuestProgress) {
      onQuestProgress('node_psi');
      audioEngine.playSuccessFanfare();
      confetti({ particleCount: 50, spread: 60, origin: { y: 0.6 } });
    }
  };

  const handleHexSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (hexInput.trim().toUpperCase() === '0X9F4B' || hexInput.trim().toUpperCase() === '9F4B') {
      setHexUnlocked(true);
      audioEngine.playSuccessFanfare();
      if (onQuestProgress) onQuestProgress('node_cyber');
      confetti({ particleCount: 50, spread: 70, origin: { y: 0.6 } });
    } else {
      audioEngine.playTextBlip(-8);
    }
  };

  const handleRotateRing = (ringIdx: number) => {
    const newAngles: [number, number, number] = [ringAngles[0], ringAngles[1], ringAngles[2]];
    newAngles[ringIdx] = (newAngles[ringIdx] + 30) % 360;
    setRingAngles(newAngles);
    audioEngine.playSporeChime(500 + ringIdx * 150);

    // Check alignment within 20 deg of 0/360
    const isAligned = newAngles.every((a) => a <= 15 || a >= 345);
    if (isAligned && onQuestProgress && !isQuestCompleted) {
      onQuestProgress('node_sky');
      audioEngine.playSuccessFanfare();
      confetti({ particleCount: 60, spread: 80, origin: { y: 0.5 } });
    }
  };

  const handleCollectCrystal = () => {
    if (magmaCrystals >= 3) return;
    const next = magmaCrystals + 1;
    setMagmaCrystals(next);
    audioEngine.playSporeChime(300 + next * 180);
    if (next >= 3 && onQuestProgress) {
      onQuestProgress('node_foundry');
      audioEngine.playSuccessFanfare();
      confetti({ particleCount: 60, spread: 70, origin: { y: 0.6 } });
    }
  };

  // Canvas render loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let startTime = performance.now();
    let isCancelled = false;

    // Precompiled user custom script if present
    let customFunction: Function | null = null;
    if (portal.canvasCode) {
      try {
        customFunction = new Function('ctx', 'width', 'height', 'time', 'mouseX', 'mouseY', 'isMouseDown', portal.canvasCode);
      } catch (err) {
        console.warn('Could not compile custom portal code:', err);
      }
    }

    const render = (now: number) => {
      if (isCancelled) return;
      const time = now - startTime;
      const width = canvas.width;
      const height = canvas.height;

      ctx.save();

      // Dispatch specific portal renderer
      if (customFunction) {
        try {
          customFunction(ctx, width, height, time, mousePos.current.x, mousePos.current.y, mousePos.current.isDown);
        } catch (e) {
          ctx.fillStyle = '#0f172a';
          ctx.fillRect(0, 0, width, height);
          ctx.fillStyle = '#38bdf8';
          ctx.font = '14px monospace';
          ctx.fillText('Rendering Generative Portal...', 20, 40);
        }
      } else if (portal.id === 'pharaoh_tomb') {
        renderPharaohDunes(ctx, width, height, time, epoch, mousePos.current);
      } else if (portal.id === 'cosmic_psi_rift') {
        renderCosmicPsiRift(ctx, width, height, time, epoch, mousePos.current);
      } else if (portal.id === 'cyber_archaeology') {
        renderCyberArchaeology(ctx, width, height, time, epoch, mousePos.current);
      } else if (portal.id === 'sky_citadel') {
        renderSkyCitadel(ctx, width, height, time, epoch, ringAngles, mousePos.current);
      } else if (portal.id === 'lava_foundry') {
        renderLavaFoundry(ctx, width, height, time, epoch, magmaCrystals, mousePos.current);
      } else if (portal.id === 'epoch_matrix') {
        renderEpochMatrix(ctx, width, height, time, epoch, mousePos.current);
      }

      // Apply Epoch post-processing shaders (CRT scanlines, pixelation)
      applyEpochPostFX(ctx, width, height, epoch);

      ctx.restore();

      animationFrameRef.current = requestAnimationFrame(render);
    };

    animationFrameRef.current = requestAnimationFrame(render);

    return () => {
      isCancelled = true;
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [portal, epoch, ringAngles, magmaCrystals]);

  // Special full interactive UI for Spore Network
  if (portal.id === 'spore_forest') {
    return (
      <div className="relative w-full h-full min-h-[420px] rounded-xl overflow-hidden bg-slate-950 border border-purple-500/20 shadow-2xl">
        <SporeNetworkSim isActive={isActive} onQuestComplete={() => onQuestProgress && onQuestProgress('node_spore')} />
      </div>
    );
  }

  return (
    <div className="relative w-full h-full min-h-[420px] rounded-xl overflow-hidden bg-slate-950 border border-slate-800/80 shadow-2xl group select-none">
      <canvas
        ref={canvasRef}
        width={720}
        height={480}
        onMouseMove={handleMouseMove}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        className="w-full h-full object-cover cursor-crosshair"
      />

      {/* Interactive Overlays for Quests & Epoch Features */}

      {/* Pharaoh's Radiant Ka Sun Orbs Interactive Overlay */}
      {portal.id === 'pharaoh_tomb' && (
        <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
          {[
            { id: 0, x: '28%', y: '25%', name: 'Ra Ka Orb 1' },
            { id: 1, x: '50%', y: '16%', name: 'Solar Apex Core' },
            { id: 2, x: '74%', y: '26%', name: 'Scarab Ka Orb 2' },
          ].map((orb) => {
            const isClicked = kaOrbsClicked.includes(orb.id) || isQuestCompleted;
            return (
              <button
                key={orb.id}
                onClick={() => handleKaOrbClick(orb.id)}
                style={{ left: orb.x, top: orb.y }}
                className={`absolute pointer-events-auto -translate-x-1/2 -translate-y-1/2 p-2 rounded-full transition-all duration-300 ${
                  isClicked
                    ? 'bg-amber-400 text-amber-950 shadow-[0_0_24px_#fde047] scale-110'
                    : 'bg-amber-950/90 text-amber-300 border border-amber-400/60 hover:scale-125 hover:bg-amber-400 hover:text-amber-950 animate-bounce'
                }`}
                title={orb.name}
              >
                <Sparkles className="w-5 h-5" />
              </button>
            );
          })}
        </div>
      )}

      {/* Cosmic PSI Nodes Interactive Overlay */}
      {portal.id === 'cosmic_psi_rift' && (
        <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
          {[
            { id: 0, x: '25%', y: '35%' },
            { id: 1, x: '72%', y: '28%' },
            { id: 2, x: '48%', y: '70%' },
          ].map((node) => {
            const isClicked = psiNodesClicked.includes(node.id) || isQuestCompleted;
            return (
              <button
                key={node.id}
                onClick={() => handlePsiNodeClick(node.id)}
                style={{ left: node.x, top: node.y }}
                className={`absolute pointer-events-auto -translate-x-1/2 -translate-y-1/2 p-2 rounded-full transition-all duration-300 ${
                  isClicked
                    ? 'bg-rose-500 text-white shadow-[0_0_24px_#f43f5e] scale-110'
                    : 'bg-rose-950/80 text-rose-300 border border-rose-500/50 hover:scale-125 hover:bg-rose-500 hover:text-white animate-pulse'
                }`}
                title="Resonant PSI Node"
              >
                <Sparkles className="w-5 h-5" />
              </button>
            );
          })}
        </div>
      )}

      {/* Cyber-Archaeology Decipher Terminal Overlay */}
      {portal.id === 'cyber_archaeology' && (
        <div className="absolute bottom-4 left-4 right-4 bg-slate-900/90 backdrop-blur-md border border-emerald-500/40 rounded-lg p-3 text-emerald-400 font-mono text-xs flex flex-wrap items-center justify-between gap-3 shadow-lg">
          <div className="flex items-center gap-2">
            <Terminal className="w-4 h-4 text-emerald-400 animate-pulse" />
            <span>CIPHER VAULT: {hexUnlocked || isQuestCompleted ? 'UNLOCKED (0x9F4B)' : 'LOCKED [Enter 0x9F4B]'}</span>
          </div>
          {!(hexUnlocked || isQuestCompleted) ? (
            <form onSubmit={handleHexSubmit} className="flex items-center gap-2">
              <input
                type="text"
                value={hexInput}
                onChange={(e) => setHexInput(e.target.value)}
                placeholder="0x...."
                className="bg-slate-950 border border-emerald-500/50 rounded px-2 py-1 text-emerald-300 uppercase tracking-widest focus:outline-none focus:border-emerald-400 text-xs w-28"
              />
              <button
                type="submit"
                className="bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold px-3 py-1 rounded transition-colors text-xs"
              >
                DECODE
              </button>
            </form>
          ) : (
            <div className="flex items-center gap-1 text-emerald-300 font-bold">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>PARITY RESTORED</span>
            </div>
          )}
        </div>
      )}

      {/* Sky Citadel Ring Alignment Controls Overlay */}
      {portal.id === 'sky_citadel' && (
        <div className="absolute bottom-4 left-4 right-4 bg-slate-900/90 backdrop-blur-md border border-sky-500/40 rounded-lg p-3 text-sky-300 font-mono text-xs flex items-center justify-between gap-2 shadow-lg">
          <div className="flex items-center gap-2">
            <RotateCw className="w-4 h-4 text-sky-400" />
            <span>ZEAL CELESTIAL RINGS:</span>
          </div>
          <div className="flex items-center gap-2">
            {[0, 1, 2].map((idx) => (
              <button
                key={idx}
                onClick={() => handleRotateRing(idx)}
                className="px-2.5 py-1 rounded bg-sky-950 hover:bg-sky-700 text-sky-200 border border-sky-500/40 transition-colors text-xs flex items-center gap-1"
              >
                <span>Ring {idx + 1}</span>
                <span className="text-[10px] text-sky-400">({ringAngles[idx]}°)</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Lava Foundry Magma Smelt Overlay */}
      {portal.id === 'lava_foundry' && (
        <div className="absolute bottom-4 left-4 right-4 bg-slate-900/90 backdrop-blur-md border border-orange-500/40 rounded-lg p-3 text-orange-300 font-mono text-xs flex items-center justify-between gap-3 shadow-lg">
          <div className="flex items-center gap-2">
            <Flame className="w-4 h-4 text-orange-500 animate-bounce" />
            <span>FIRE CRYSTALS SMELTED: {magmaCrystals}/3</span>
          </div>
          {magmaCrystals < 3 && !isQuestCompleted ? (
            <button
              onClick={handleCollectCrystal}
              className="bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-500 hover:to-amber-500 text-slate-950 font-bold px-3 py-1 rounded transition-all text-xs flex items-center gap-1 shadow-md shadow-orange-900/50"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>SMELT VENT (+1)</span>
            </button>
          ) : (
            <div className="flex items-center gap-1 text-amber-300 font-bold">
              <CheckCircle2 className="w-4 h-4 text-amber-400" />
              <span>PRIMORDIAL CRYSTAL HARVESTED</span>
            </div>
          )}
        </div>
      )}

      {/* Portal Meta Badge */}
      <div className="absolute top-3 left-3 bg-slate-950/80 backdrop-blur-md border border-slate-700/60 rounded-md px-2.5 py-1 text-[11px] font-mono text-slate-300 flex items-center gap-1.5 shadow-md">
        <span className="w-2 h-2 rounded-full" style={{ backgroundColor: portal.accentColor }} />
        <span className="font-semibold text-slate-200">{portal.name}</span>
        <span className="text-slate-500">|</span>
        <span className="uppercase text-[10px] text-slate-400">{epoch}</span>
      </div>

      {/* Interactive Cursor Hint */}
      <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-200 bg-slate-950/80 backdrop-blur-md border border-slate-700/60 rounded-md px-2.5 py-1 text-[10px] font-mono text-slate-300 flex items-center gap-1.5 shadow-md">
        <Eye className="w-3 h-3 text-slate-400" />
        <span>{portal.interactiveHint}</span>
      </div>
    </div>
  );
};

// ==========================================
// PROCEDURAL CANVAS RENDERERS
// ==========================================

function renderPharaohDunes(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  t: number,
  epoch: EpochEra,
  mouse: { x: number; y: number; isDown: boolean }
) {
  const time = t * 0.001;

  // Egyptian Dusk Sky Gradient
  const sky = ctx.createLinearGradient(0, 0, 0, h * 0.6);
  sky.addColorStop(0, '#451a03');
  sky.addColorStop(0.4, '#78350f');
  sky.addColorStop(0.8, '#b45309');
  sky.addColorStop(1, '#f59e0b');
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, w, h * 0.65);

  // Giant Solar Disc
  const sunX = w * 0.5;
  const sunY = h * 0.22 + Math.sin(time * 0.5) * 4;
  const sunGrad = ctx.createRadialGradient(sunX, sunY, 10, sunX, sunY, 65);
  sunGrad.addColorStop(0, '#fef08a');
  sunGrad.addColorStop(0.4, '#fde047');
  sunGrad.addColorStop(0.8, '#f59e0b');
  sunGrad.addColorStop(1, 'rgba(245, 158, 11, 0)');
  ctx.fillStyle = sunGrad;
  ctx.beginPath();
  ctx.arc(sunX, sunY, 65, 0, Math.PI * 2);
  ctx.fill();

  // Distant Golden Great Pyramid (Pharaoh Mario style)
  const pyrBaseY = h * 0.62;
  const pyrApexX = w * 0.5;
  const pyrApexY = h * 0.25;

  // Pyramid Lit Face (Golden Amber)
  ctx.fillStyle = '#d97706';
  ctx.beginPath();
  ctx.moveTo(pyrApexX, pyrApexY);
  ctx.lineTo(pyrApexX - 160, pyrBaseY);
  ctx.lineTo(pyrApexX, pyrBaseY);
  ctx.closePath();
  ctx.fill();

  // Pyramid Shadow Face (Darker Sand)
  ctx.fillStyle = '#92400e';
  ctx.beginPath();
  ctx.moveTo(pyrApexX, pyrApexY);
  ctx.lineTo(pyrApexX + 160, pyrBaseY);
  ctx.lineTo(pyrApexX, pyrBaseY);
  ctx.closePath();
  ctx.fill();

  // Glowing Electrum Capstone
  ctx.fillStyle = '#fef08a';
  ctx.beginPath();
  ctx.moveTo(pyrApexX, pyrApexY);
  ctx.lineTo(pyrApexX - 25, pyrApexY + 40);
  ctx.lineTo(pyrApexX + 25, pyrApexY + 40);
  ctx.closePath();
  ctx.fill();

  // Radiant Solar Eye in Capstone
  ctx.fillStyle = '#b45309';
  ctx.beginPath();
  ctx.arc(pyrApexX, pyrApexY + 22, 5 + Math.sin(time * 4) * 1.5, 0, Math.PI * 2);
  ctx.fill();

  // Layered Rolling Sand Dunes (Parallax Sine Waves)
  for (let d = 0; d < 3; d++) {
    const duneY = h * 0.58 + d * 45;
    ctx.fillStyle = d === 0 ? '#b45309' : d === 1 ? '#d97706' : '#f59e0b';
    ctx.beginPath();
    ctx.moveTo(0, h);
    ctx.lineTo(0, duneY);

    for (let x = 0; x <= w; x += 15) {
      const dy = Math.sin(x * 0.008 + d * 2 + time * 0.3) * (18 - d * 4);
      ctx.lineTo(x, duneY + dy);
    }
    ctx.lineTo(w, h);
    ctx.closePath();
    ctx.fill();
  }

  // Animated Crawling Scarab Slimes & Ka Wisps (from the concept art)
  for (let s = 0; s < 4; s++) {
    const scarabSpeed = 25 + s * 8;
    const sx = (time * scarabSpeed + s * 180) % (w + 60) - 30;
    const sy = h * 0.78 + Math.sin(time * 3 + s) * 6 + s * 14;

    // Glowing Scarab / Ka Slime body
    ctx.fillStyle = s % 2 === 0 ? '#38bdf8' : '#eab308';
    ctx.beginPath();
    ctx.ellipse(sx, sy, 12, 8, 0, 0, Math.PI * 2);
    ctx.fill();

    // Golden Scarab Shell / Eye
    ctx.fillStyle = '#0f172a';
    ctx.beginPath();
    ctx.arc(sx + 3, sy - 2, 2.5, 0, Math.PI * 2);
    ctx.fill();

    // Ka Spirit Aura
    ctx.strokeStyle = s % 2 === 0 ? 'rgba(56, 189, 248, 0.4)' : 'rgba(234, 179, 8, 0.4)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(sx, sy, 16 + Math.sin(time * 5 + s) * 3, 0, Math.PI * 2);
    ctx.stroke();
  }

  // Floating Golden Sand Glimmer Particles
  for (let p = 0; p < 25; p++) {
    const px = (p * 35 + time * 30) % w;
    const py = (h * 0.4 + (p * 27 + Math.sin(time * 2 + p) * 20)) % (h * 0.6);
    ctx.fillStyle = 'rgba(254, 240, 138, 0.8)';
    ctx.fillRect(px, py, 2.5, 2.5);
  }

  // Heat Shimmer distortion on bottom horizon
  if (mouse.x && mouse.y) {
    ctx.beginPath();
    ctx.arc(mouse.x, mouse.y, 28, 0, Math.PI * 2);
    ctx.strokeStyle = '#fde047';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }
}

function renderCosmicPsiRift(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  t: number,
  epoch: EpochEra,
  mouse: { x: number; y: number; isDown: boolean }
) {
  const time = t * 0.001;
  // EarthBound psychedelic background raster wave
  const rows = epoch === '8bit' ? 32 : 64;
  const rowHeight = h / rows;

  for (let i = 0; i < rows; i++) {
    const waveOffset = Math.sin(time * 2 + i * 0.2) * (mouse.isDown ? 40 : 20);
    const hue = (time * 40 + i * 5) % 360;
    ctx.fillStyle = `hsl(${hue}, 70%, 15%)`;
    ctx.fillRect(0, i * rowHeight, w, rowHeight);

    // Sine scanlines
    ctx.fillStyle = `hsla(${(hue + 60) % 360}, 80%, 35%, 0.4)`;
    ctx.fillRect(waveOffset, i * rowHeight, w, rowHeight * 0.5);
  }

  // Central Cosmic Vortex
  const cx = w / 2;
  const cy = h / 2;
  const spiralCount = epoch === 'ultra' ? 8 : 4;

  for (let s = 0; s < spiralCount; s++) {
    ctx.beginPath();
    ctx.strokeStyle = s % 2 === 0 ? 'rgba(244, 63, 94, 0.7)' : 'rgba(168, 85, 247, 0.7)';
    ctx.lineWidth = epoch === '8bit' ? 4 : 2;

    for (let a = 0; a < Math.PI * 6; a += 0.1) {
      const radius = (a * 15 + Math.sin(time * 3 + a) * 10) * (mouse.isDown ? 1.2 : 1);
      const angle = a + time * 0.8 + (s * Math.PI * 2) / spiralCount;
      const x = cx + Math.cos(angle) * radius;
      const y = cy + Math.sin(angle) * radius;
      if (a === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }

  // Cursor distortion ripple
  if (mouse.x && mouse.y) {
    ctx.beginPath();
    ctx.arc(mouse.x, mouse.y, 25 + Math.sin(time * 6) * 8, 0, Math.PI * 2);
    ctx.strokeStyle = '#f43f5e';
    ctx.lineWidth = 2;
    ctx.stroke();
  }
}

function renderCyberArchaeology(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  t: number,
  epoch: EpochEra,
  mouse: { x: number; y: number; isDown: boolean }
) {
  const time = t * 0.001;

  // Vector Phosphor deep CRT background
  ctx.fillStyle = '#02130d';
  ctx.fillRect(0, 0, w, h);

  const cx = w * 0.5;
  const cy = h * 0.5;
  const fov = 260;

  // =========================================================================
  // LAYER 1: DEEP SUBTERRANEAN WIREFRAME TERRAIN (Curves back into the sky)
  // =========================================================================
  const subRadius = Math.min(w, h) * 0.75;
  const subSegments = 28;
  const subTracks = 9;

  ctx.lineWidth = 1;
  for (let track = 0; track < subTracks; track++) {
    const trackXRatio = (track - (subTracks - 1) / 2) / ((subTracks - 1) / 2);
    const baseX = trackXRatio * (w * 0.7);

    ctx.beginPath();
    ctx.strokeStyle = `rgba(6, 182, 212, ${0.18 + (1 - Math.abs(trackXRatio)) * 0.25})`;

    let firstPoint = true;
    for (let i = 0; i <= subSegments; i++) {
      // Loop angle around the cylindrical world
      const angle = (i / subSegments) * Math.PI * 2 + (time * 0.4) % (Math.PI * 2);
      
      // Undulating digital terrain heightmap
      const terrainHeight =
        Math.sin(angle * 4 + track * 1.2 + time) * 14 +
        Math.cos(angle * 7 - track) * 8;

      const currentR = subRadius + terrainHeight + 35;
      const worldY = Math.sin(angle) * currentR;
      const worldZ = Math.cos(angle) * currentR + subRadius + 40;

      if (worldZ > 15) {
        const scale = fov / (fov + worldZ);
        const screenX = cx + baseX * scale * 1.4;
        const screenY = cy + worldY * scale;

        if (firstPoint) {
          ctx.moveTo(screenX, screenY);
          firstPoint = false;
        } else {
          ctx.lineTo(screenX, screenY);
        }
      }
    }
    ctx.stroke();
  }

  // =========================================================================
  // LAYER 2: PRIMARY CYBER GRID FLOOR (Curving backwards onto itself like an O'Neill cylinder)
  // =========================================================================
  const gridRadius = Math.min(w, h) * 0.55;
  const rings = 32;
  const longitudinalLanes = 12;

  // Longitudinal grid lines running along the loop
  for (let lane = 0; lane <= longitudinalLanes; lane++) {
    const laneRatio = (lane - longitudinalLanes / 2) / (longitudinalLanes / 2);
    const laneX = laneRatio * (w * 0.55);

    ctx.beginPath();
    const isCenter = Math.abs(laneRatio) < 0.15;
    ctx.strokeStyle = isCenter
      ? 'rgba(52, 211, 153, 0.75)'
      : `rgba(16, 185, 129, ${0.25 + (1 - Math.abs(laneRatio)) * 0.35})`;
    ctx.lineWidth = isCenter ? 2 : 1.2;

    let hasStarted = false;
    for (let r = 0; r <= rings * 2; r++) {
      const angle = (r / rings) * Math.PI + (time * 0.7) % (Math.PI * 2);
      const worldY = Math.sin(angle) * gridRadius;
      const worldZ = Math.cos(angle) * gridRadius + gridRadius + 20;

      if (worldZ > 10) {
        const scale = fov / (fov + worldZ);
        const screenX = cx + laneX * scale * 1.35;
        const screenY = cy + worldY * scale;

        if (!hasStarted) {
          ctx.moveTo(screenX, screenY);
          hasStarted = true;
        } else {
          ctx.lineTo(screenX, screenY);
        }
      }
    }
    ctx.stroke();
  }

  // Latitudinal rings sliding along the loop into the distance and overhead
  const ringSpeed = (time * 1.2) % 1;
  for (let ringIdx = 0; ringIdx < 24; ringIdx++) {
    const ringAngle = ((ringIdx + ringSpeed) / 24) * Math.PI * 2;
    const worldY = Math.sin(ringAngle) * gridRadius;
    const worldZ = Math.cos(ringAngle) * gridRadius + gridRadius + 20;

    if (worldZ > 10) {
      const scale = fov / (fov + worldZ);
      const ringY = cy + worldY * scale;
      const ringHalfWidth = (w * 0.55) * scale * 1.35;

      const alpha = Math.max(0.1, Math.min(0.85, 1.2 - worldZ / 400));
      ctx.strokeStyle = `rgba(16, 185, 129, ${alpha})`;
      ctx.lineWidth = 1;

      ctx.beginPath();
      ctx.moveTo(cx - ringHalfWidth, ringY);
      ctx.lineTo(cx + ringHalfWidth, ringY);
      ctx.stroke();

      // Glowing vertex node markers on intersections
      if (ringIdx % 2 === 0) {
        for (let l = 0; l <= longitudinalLanes; l += 3) {
          const lRatio = (l - longitudinalLanes / 2) / (longitudinalLanes / 2);
          const ptX = cx + lRatio * ringHalfWidth;
          ctx.fillStyle = '#34d399';
          ctx.fillRect(ptX - 1.5, ringY - 1.5, 3, 3);
        }
      }
    }
  }

  // =========================================================================
  // LAYER 3: STEPPED CURVED CHUTES & TIER BRIDGES (Connecting upper & lower loop)
  // =========================================================================
  for (let chute = 0; chute < 2; chute++) {
    const chuteSide = chute === 0 ? -1 : 1;
    ctx.beginPath();
    ctx.strokeStyle = 'rgba(245, 158, 11, 0.7)';
    ctx.lineWidth = 2.5;

    for (let step = 0; step <= 20; step++) {
      const tProgress = step / 20;
      const chuteAngle = -Math.PI * 0.2 + tProgress * Math.PI * 0.8 + time * 0.3;
      const cRadius = gridRadius * (0.8 + Math.sin(tProgress * Math.PI) * 0.2);
      const cWorldY = Math.sin(chuteAngle) * cRadius;
      const cWorldZ = Math.cos(chuteAngle) * cRadius + gridRadius + 30;

      if (cWorldZ > 10) {
        const scale = fov / (fov + cWorldZ);
        const cX = cx + (chuteSide * (w * 0.35) + Math.sin(tProgress * 4 + time * 2) * 15) * scale;
        const cY = cy + cWorldY * scale;

        if (step === 0) ctx.moveTo(cX, cY);
        else ctx.lineTo(cX, cY);

        // Chute rungs / ladder bars
        if (step % 3 === 0) {
          ctx.fillStyle = '#fbbf24';
          ctx.fillRect(cX - 4, cY - 1, 8, 2);
        }
      }
    }
    ctx.stroke();
  }

  // Mini Inset Moving Picture Data Frames (vector holographic tiles)
  for (let f = 0; f < 3; f++) {
    const frameAngle = (f * (Math.PI * 2 / 3) + time * 0.4) % (Math.PI * 2);
    const fWorldY = Math.sin(frameAngle) * (gridRadius * 0.9);
    const fWorldZ = Math.cos(frameAngle) * (gridRadius * 0.9) + gridRadius + 25;

    if (fWorldZ > 15) {
      const fScale = fov / (fov + fWorldZ);
      const fX = cx + ((f - 1) * (w * 0.28)) * fScale;
      const fY = cy + fWorldY * fScale;

      const fw = 42 * fScale;
      const fh = 30 * fScale;

      // Frame Border
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1.5;
      ctx.strokeRect(fX - fw / 2, fY - fh / 2, fw, fh);
      ctx.fillStyle = 'rgba(15, 23, 42, 0.7)';
      ctx.fillRect(fX - fw / 2, fY - fh / 2, fw, fh);

      // Micro moving oscilloscope wave inside picture frame
      ctx.beginPath();
      ctx.strokeStyle = f === 0 ? '#34d399' : f === 1 ? '#f59e0b' : '#38bdf8';
      ctx.lineWidth = 1;
      for (let mx = 0; mx < fw; mx += 3) {
        const my = Math.sin(mx * 0.3 + time * 5 + f) * (fh * 0.3);
        if (mx === 0) ctx.moveTo(fX - fw / 2 + mx, fY + my);
        else ctx.lineTo(fX - fw / 2 + mx, fY + my);
      }
      ctx.stroke();
    }
  }

  // =========================================================================
  // LAYER 4: FLOATING / HOVERING 3D TESSERACT HYPERCUBE FLOATERIZING ALL AROUND
  // =========================================================================
  // Dynamic 3D path: weaves and bobs smoothly across the curved chamber
  const cubeBaseX = cx + Math.sin(time * 1.4) * (w * 0.24) + Math.cos(time * 0.7) * 25;
  const cubeBaseY = cy + Math.cos(time * 1.1) * (h * 0.2) + Math.sin(time * 2.3) * 15;
  const cubeBaseZ = Math.sin(time * 0.9) * 60; // moves forward and backward

  // Reactive hover influence from mouse
  const targetCubeX = mouse.x && mouse.y ? cubeBaseX * 0.7 + mouse.x * 0.3 : cubeBaseX;
  const targetCubeY = mouse.x && mouse.y ? cubeBaseY * 0.7 + mouse.y * 0.3 : cubeBaseY;

  const cubeSize = (55 + Math.sin(time * 2.5) * 6) * (fov / (fov + cubeBaseZ + 100));

  // Outer Cube Vertices
  const outerPoints = [
    { x: -1, y: -1, z: -1 },
    { x: 1, y: -1, z: -1 },
    { x: 1, y: 1, z: -1 },
    { x: -1, y: 1, z: -1 },
    { x: -1, y: -1, z: 1 },
    { x: 1, y: -1, z: 1 },
    { x: 1, y: 1, z: 1 },
    { x: -1, y: 1, z: 1 },
  ];

  // Inner Core Tesseract Cube Vertices
  const innerScaleRatio = 0.52 + Math.sin(time * 3) * 0.08;
  const innerPoints = outerPoints.map((p) => ({
    x: p.x * innerScaleRatio,
    y: p.y * innerScaleRatio,
    z: p.z * innerScaleRatio,
  }));

  const rotAngleX = time * 0.95 + (mouse.isDown ? 1.5 : 0);
  const rotAngleY = time * 1.35;
  const rotAngleZ = time * 0.6;

  const project3D = (p: { x: number; y: number; z: number }, size: number) => {
    // 3D Euler Rotations
    // Rotate Y
    let x1 = p.x * Math.cos(rotAngleY) + p.z * Math.sin(rotAngleY);
    let z1 = -p.x * Math.sin(rotAngleY) + p.z * Math.cos(rotAngleY);
    // Rotate X
    let y2 = p.y * Math.cos(rotAngleX) - z1 * Math.sin(rotAngleX);
    let z2 = p.y * Math.sin(rotAngleX) + z1 * Math.cos(rotAngleX);
    // Rotate Z
    let x3 = x1 * Math.cos(rotAngleZ) - y2 * Math.sin(rotAngleZ);
    let y3 = x1 * Math.sin(rotAngleZ) + y2 * Math.cos(rotAngleZ);

    const pScale = fov / (fov + z2 * 45 + 90);
    return {
      x: targetCubeX + x3 * size * pScale,
      y: targetCubeY + y3 * size * pScale,
    };
  };

  const projOuter = outerPoints.map((p) => project3D(p, cubeSize));
  const projInner = innerPoints.map((p) => project3D(p, cubeSize));

  const cubeEdges = [
    [0, 1], [1, 2], [2, 3], [3, 0],
    [4, 5], [5, 6], [6, 7], [7, 4],
    [0, 4], [1, 5], [2, 6], [3, 7],
  ];

  // Draw Outer Cube Edges with Emerald Glow
  ctx.strokeStyle = '#10b981';
  ctx.lineWidth = 2.2;
  cubeEdges.forEach(([i, j]) => {
    ctx.beginPath();
    ctx.moveTo(projOuter[i].x, projOuter[i].y);
    ctx.lineTo(projOuter[j].x, projOuter[j].y);
    ctx.stroke();
  });

  // Draw Inner Core Cube with Cyan Glow
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 1.6;
  cubeEdges.forEach(([i, j]) => {
    ctx.beginPath();
    ctx.moveTo(projInner[i].x, projInner[i].y);
    ctx.lineTo(projInner[j].x, projInner[j].y);
    ctx.stroke();
  });

  // Draw 4D Hypercube Struts connecting outer and inner vertices
  ctx.strokeStyle = 'rgba(251, 191, 36, 0.85)';
  ctx.lineWidth = 1.2;
  for (let i = 0; i < 8; i++) {
    ctx.beginPath();
    ctx.moveTo(projOuter[i].x, projOuter[i].y);
    ctx.lineTo(projInner[i].x, projInner[i].y);
    ctx.stroke();
  }

  // Floating Gyroscopic Energy Ring around the Cube
  ctx.beginPath();
  ctx.strokeStyle = 'rgba(52, 211, 153, 0.6)';
  ctx.lineWidth = 1.5;
  ctx.ellipse(
    targetCubeX,
    targetCubeY,
    cubeSize * 1.4,
    cubeSize * 0.5,
    time * 1.5,
    0,
    Math.PI * 2
  );
  ctx.stroke();

  // Floating Data Bit Dust around the hovering cube
  for (let b = 0; b < 12; b++) {
    const bitAngle = b * (Math.PI / 6) + time * 2;
    const bitDist = cubeSize * (1.1 + Math.sin(time * 3 + b) * 0.3);
    const bx = targetCubeX + Math.cos(bitAngle) * bitDist;
    const by = targetCubeY + Math.sin(bitAngle) * bitDist * 0.7;

    ctx.fillStyle = b % 2 === 0 ? '#34d399' : '#f59e0b';
    ctx.fillRect(bx - 1.5, by - 1.5, 3, 3);
  }

  // Phosphor Telemetry Code Overlay in corner
  ctx.font = '10px monospace';
  ctx.fillStyle = 'rgba(52, 211, 153, 0.7)';
  ctx.fillText(`CYL-TORUS LOOP: ${(gridRadius).toFixed(0)}m`, 15, h - 35);
  ctx.fillText(`TESSERACT POS: [${targetCubeX.toFixed(0)}, ${targetCubeY.toFixed(0)}]`, 15, h - 20);
}

function renderSkyCitadel(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  t: number,
  epoch: EpochEra,
  ringAngles: [number, number, number],
  mouse: { x: number; y: number }
) {
  const time = t * 0.001;
  // Sky Gradient
  const skyGrad = ctx.createLinearGradient(0, 0, 0, h);
  skyGrad.addColorStop(0, '#0c4a6e');
  skyGrad.addColorStop(0.6, '#38bdf8');
  skyGrad.addColorStop(1, '#bae6fd');
  ctx.fillStyle = skyGrad;
  ctx.fillRect(0, 0, w, h);

  // Parallax Drifting Clouds
  for (let c = 0; c < 5; c++) {
    const cloudSpeed = 15 + c * 10;
    const cx = ((time * cloudSpeed + c * 160) % (w + 200)) - 100;
    const cy = 60 + c * 45;
    ctx.fillStyle = `rgba(255, 255, 255, ${0.3 + c * 0.1})`;
    ctx.beginPath();
    ctx.ellipse(cx, cy, 70 + c * 15, 25 + c * 8, 0, 0, Math.PI * 2);
    ctx.fill();
  }

  // Floating Island of Zeal
  const islandX = w / 2;
  const islandY = h * 0.55 + Math.sin(time * 1.5) * 8;

  // Island Body
  ctx.fillStyle = '#1e293b';
  ctx.beginPath();
  ctx.moveTo(islandX - 120, islandY);
  ctx.lineTo(islandX + 120, islandY);
  ctx.lineTo(islandX + 40, islandY + 80);
  ctx.lineTo(islandX, islandY + 110);
  ctx.lineTo(islandX - 50, islandY + 70);
  ctx.closePath();
  ctx.fill();

  // Green grass top & golden spires
  ctx.fillStyle = '#10b981';
  ctx.fillRect(islandX - 120, islandY - 4, 240, 8);

  // Golden Citadel Spire
  ctx.fillStyle = '#fbbf24';
  ctx.beginPath();
  ctx.moveTo(islandX - 25, islandY);
  ctx.lineTo(islandX, islandY - 65);
  ctx.lineTo(islandX + 25, islandY);
  ctx.fill();

  // Concentric Celestial Harmonization Rings
  const [r1, r2, r3] = ringAngles;
  const radii = [45, 65, 85];
  const angles = [r1, r2, r3];

  angles.forEach((ang, idx) => {
    const radius = radii[idx];
    ctx.beginPath();
    ctx.arc(islandX, islandY - 30, radius, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(251, 191, 36, 0.4)';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Solar Crest Marker
    const rad = (ang * Math.PI) / 180;
    const markerX = islandX + Math.cos(rad) * radius;
    const markerY = islandY - 30 + Math.sin(rad) * radius;

    ctx.beginPath();
    ctx.arc(markerX, markerY, 5, 0, Math.PI * 2);
    ctx.fillStyle = '#f59e0b';
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.stroke();
  });
}

function renderLavaFoundry(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  t: number,
  epoch: EpochEra,
  magmaCrystals: number,
  mouse: { x: number; y: number }
) {
  const time = t * 0.001;
  // Dark Molten Cavern Background
  ctx.fillStyle = '#1c0a06';
  ctx.fillRect(0, 0, w, h);

  // Molten Magma River
  const lavaY = h * 0.65;
  const grad = ctx.createLinearGradient(0, lavaY, 0, h);
  grad.addColorStop(0, '#f97316');
  grad.addColorStop(0.5, '#dc2626');
  grad.addColorStop(1, '#7f1d1d');
  ctx.fillStyle = grad;
  ctx.fillRect(0, lavaY, w, h - lavaY);

  // Lava Bubbles
  for (let b = 0; b < 12; b++) {
    const bx = (b * 65 + Math.sin(time + b) * 20) % w;
    const by = lavaY + 20 + Math.cos(time * 2 + b * 2) * 25;
    const radius = 6 + Math.sin(time * 3 + b) * 4;
    ctx.beginPath();
    ctx.arc(bx, by, Math.max(2, radius), 0, Math.PI * 2);
    ctx.fillStyle = '#fde047';
    ctx.fill();
  }

  // Smelting Core Forge Anvil
  const anvilX = w / 2;
  const anvilY = lavaY - 30;

  ctx.fillStyle = '#334155';
  ctx.fillRect(anvilX - 60, anvilY, 120, 40);

  // Radiant Primordial Core Crystal (harvestable)
  const crystalGlow = 1 + magmaCrystals * 0.4;
  ctx.fillStyle = '#ffedd5';
  ctx.beginPath();
  ctx.arc(anvilX, anvilY - 20, 15 * crystalGlow, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = '#ea580c';
  ctx.lineWidth = 3;
  ctx.stroke();

  // Floating Ember Particles
  for (let p = 0; p < 24; p++) {
    const px = (p * 32 + time * 40) % w;
    const py = ((h - (p * 18 + time * 60)) % h) + (p % 2 === 0 ? 0 : 40);
    ctx.fillStyle = 'rgba(251, 146, 60, 0.8)';
    ctx.fillRect(px, py, 3, 3);
  }
}

function renderEpochMatrix(
  ctx: CanvasRenderingContext2D,
  w: number,
  h: number,
  t: number,
  epoch: EpochEra,
  mouse: { x: number; y: number }
) {
  const time = t * 0.001;
  ctx.fillStyle = '#050510';
  ctx.fillRect(0, 0, w, h);

  // Dynamic geometric matrix comparing historical render pipeline capabilities
  const cx = w / 2;
  const cy = h / 2;

  if (epoch === '8bit') {
    // 8-bit NES: Limited 4-color palette dither, low resolution blocks
    const blockSize = 16;
    for (let x = 0; x < w; x += blockSize) {
      for (let y = 0; y < h; y += blockSize) {
        const val = Math.sin(x * 0.05 + time * 2) * Math.cos(y * 0.05 + time * 2);
        ctx.fillStyle = val > 0.5 ? '#ffffff' : val > 0 ? '#eab308' : val > -0.5 ? '#ca8a04' : '#000000';
        ctx.fillRect(x, y, blockSize - 1, blockSize - 1);
      }
    }
  } else if (epoch === '16bit') {
    // 16-bit SNES: Mode 7 rotating pseudo-3D tile plane
    for (let r = 0; r < 14; r++) {
      const radius = 20 + r * 16;
      ctx.beginPath();
      ctx.arc(cx, cy, radius, time * 0.5, time * 0.5 + Math.PI * 1.5);
      ctx.strokeStyle = `hsl(${(time * 40 + r * 20) % 360}, 85%, 60%)`;
      ctx.lineWidth = 6;
      ctx.stroke();
    }
  } else if (epoch === '32bit') {
    // 32-bit PS1: Gouraud shaded affine polygon fan with vertex jitter
    for (let p = 0; p < 18; p++) {
      const angle = (p * Math.PI * 2) / 18 + time;
      const jitter = (Math.random() - 0.5) * 3;
      const x1 = cx + Math.cos(angle) * (110 + jitter);
      const y1 = cy + Math.sin(angle) * (110 + jitter);

      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(x1, y1);
      ctx.lineTo(cx + Math.cos(angle + 0.3) * 110, cy + Math.sin(angle + 0.3) * 110);
      ctx.closePath();
      ctx.fillStyle = `rgba(56, 189, 248, ${0.4 + (p % 3) * 0.2})`;
      ctx.fill();
    }
  } else {
    // Ultra: Raymarched Sine Particle Nebula
    for (let i = 0; i < 70; i++) {
      const angle = time * 0.7 + i * 0.15;
      const dist = 50 + Math.sin(time * 2 + i) * 60 + i * 2;
      const px = cx + Math.cos(angle) * dist;
      const py = cy + Math.sin(angle) * dist;

      ctx.beginPath();
      ctx.arc(px, py, 4 + Math.sin(time * 4 + i) * 2, 0, Math.PI * 2);
      ctx.fillStyle = i % 2 === 0 ? '#eab308' : '#38bdf8';
      ctx.shadowColor = '#eab308';
      ctx.shadowBlur = 10;
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }
}

function applyEpochPostFX(ctx: CanvasRenderingContext2D, w: number, h: number, epoch: EpochEra) {
  if (epoch === '8bit' || epoch === '16bit') {
    // CRT Scanlines
    ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
    for (let y = 0; y < h; y += 4) {
      ctx.fillRect(0, y, w, 2);
    }
    // Phosphor Vignette
    const vig = ctx.createRadialGradient(w / 2, h / 2, w * 0.3, w / 2, h / 2, w * 0.65);
    vig.addColorStop(0, 'rgba(0,0,0,0)');
    vig.addColorStop(1, 'rgba(0,0,0,0.5)');
    ctx.fillStyle = vig;
    ctx.fillRect(0, 0, w, h);
  }
}
