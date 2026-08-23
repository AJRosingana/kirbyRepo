/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { PortalSurface } from '../types';

interface PortalFrameProps {
  portal: PortalSurface;
  children: React.ReactNode;
  isFocused?: boolean;
  className?: string;
  onFrameClick?: () => void;
  showLabels?: boolean;
}

export const PortalFrame: React.FC<PortalFrameProps> = ({
  portal,
  children,
  isFocused = false,
  className = '',
  onFrameClick,
  showLabels = true,
}) => {
  const style = portal.frameStyle || 'custom';

  return (
    <div
      onClick={onFrameClick}
      className={`relative group rounded-2xl transition-all duration-300 ${className} ${
        isFocused ? 'ring-2 ring-sky-400 shadow-[0_0_35px_rgba(56,189,248,0.35)]' : ''
      }`}
    >
      {/* ========================================================================= */}
      {/* FRAME ARCHITECTURE 1: EGYPTIAN PHARAOH GOLDEN SUN STELE */}
      {/* ========================================================================= */}
      {style === 'pharaoh' && (
        <div className="absolute -inset-3.5 sm:-inset-4 pointer-events-none z-20 flex flex-col justify-between">
          {/* Top Winged Solar Disc & Lapis Lazuli Arch */}
          <div className="relative w-full flex items-center justify-center -top-2">
            <div className="bg-gradient-to-r from-amber-700 via-amber-400 to-amber-700 px-4 py-1 rounded-t-xl border-t border-x border-amber-300 shadow-[0_0_15px_rgba(245,158,11,0.5)] flex items-center gap-2">
              <span className="text-[10px] text-amber-950 font-black tracking-widest uppercase">𓇯 RA SOLAR GATE 𓊹</span>
              <div className="w-3.5 h-3.5 rounded-full bg-gradient-to-br from-amber-200 to-amber-500 shadow-[0_0_8px_#fde047] border border-amber-900" />
              <span className="text-[10px] text-amber-950 font-black tracking-widest uppercase">𓇯 SCARAB 𓊹</span>
            </div>
          </div>

          {/* Left & Right Hieroglyphic Pillar Borders */}
          <div className="w-full flex-1 flex justify-between px-0.5">
            <div className="w-2.5 bg-gradient-to-b from-amber-500 via-amber-700 to-amber-900 rounded-l border-y border-l border-amber-400/60 shadow-md flex flex-col justify-around items-center py-4">
              <span className="text-[8px] text-amber-200 font-bold opacity-80 select-none">𓀀</span>
              <span className="text-[8px] text-amber-200 font-bold opacity-80 select-none">𓃭</span>
              <span className="text-[8px] text-amber-200 font-bold opacity-80 select-none">𓆣</span>
              <span className="text-[8px] text-amber-200 font-bold opacity-80 select-none">𓋹</span>
            </div>
            <div className="w-2.5 bg-gradient-to-b from-amber-500 via-amber-700 to-amber-900 rounded-r border-y border-r border-amber-400/60 shadow-md flex flex-col justify-around items-center py-4">
              <span className="text-[8px] text-amber-200 font-bold opacity-80 select-none">𓋹</span>
              <span className="text-[8px] text-amber-200 font-bold opacity-80 select-none">𓆣</span>
              <span className="text-[8px] text-amber-200 font-bold opacity-80 select-none">𓃭</span>
              <span className="text-[8px] text-amber-200 font-bold opacity-80 select-none">𓀀</span>
            </div>
          </div>

          {/* Bottom Golden Sand Pedestal */}
          <div className="relative w-full flex items-center justify-center -bottom-2">
            <div className="bg-gradient-to-r from-amber-900 via-amber-600 to-amber-900 px-6 py-0.5 rounded-b-xl border-b border-x border-amber-400/80 shadow-lg text-[9px] font-mono text-amber-200">
              PYRAMID DIORAMA MATRIX
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* FRAME ARCHITECTURE 2: COSMIC PSI RIFT MONOLITH */}
      {/* ========================================================================= */}
      {style === 'cosmic' && (
        <div className="absolute -inset-3 sm:-inset-3.5 pointer-events-none z-20 flex flex-col justify-between">
          {/* Top Mystic Star Obelisk */}
          <div className="w-full flex items-center justify-center -top-1.5">
            <div className="bg-gradient-to-r from-rose-950 via-rose-600 to-purple-950 px-4 py-0.5 rounded-t-lg border-t border-x border-rose-400/60 shadow-[0_0_20px_rgba(244,63,94,0.4)] flex items-center gap-1.5">
              <span className="text-[9px] text-rose-100 font-mono tracking-wider">✦ MAGICANT PSI MONOLITH ✦</span>
            </div>
          </div>

          {/* Lateral Energy Conduits */}
          <div className="w-full flex-1 flex justify-between px-0.5">
            <div className="w-1.5 bg-gradient-to-b from-rose-500 via-purple-600 to-rose-700 rounded-l shadow-[0_0_10px_#f43f5e] animate-pulse" />
            <div className="w-1.5 bg-gradient-to-b from-purple-700 via-rose-500 to-purple-600 rounded-r shadow-[0_0_10px_#a855f7] animate-pulse" />
          </div>

          {/* Bottom Wave Baseline */}
          <div className="w-full flex items-center justify-center -bottom-1.5">
            <div className="bg-slate-950 px-4 py-0.5 rounded-b-lg border-b border-x border-rose-500/40 text-[9px] font-mono text-rose-300">
              440 Hz HARMONIC WAVELENGTH
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* FRAME ARCHITECTURE 3: CYBER 1983 PHOSPHOR CRT BEZEL */}
      {/* ========================================================================= */}
      {style === 'cyber' && (
        <div className="absolute -inset-3 sm:-inset-3.5 pointer-events-none z-20 flex flex-col justify-between">
          {/* CRT Monitor Top Bar */}
          <div className="w-full flex items-center justify-between px-3 -top-2 bg-slate-900 rounded-t-xl border-t-2 border-x-2 border-emerald-500/60 py-0.5 shadow-[0_0_15px_rgba(16,185,129,0.3)]">
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span className="text-[9px] font-mono text-emerald-400 font-bold">CRT-VECT 0x9F4B</span>
            </div>
            <span className="text-[8px] font-mono text-emerald-600">60Hz NTSC</span>
          </div>

          {/* CRT Lateral Metal Frames */}
          <div className="w-full flex-1 flex justify-between">
            <div className="w-2 bg-slate-900 border-l-2 border-emerald-500/40" />
            <div className="w-2 bg-slate-900 border-r-2 border-emerald-500/40" />
          </div>

          {/* Bottom CRT Terminal Vents */}
          <div className="w-full flex items-center justify-between px-3 -bottom-2 bg-slate-900 rounded-b-xl border-b-2 border-x-2 border-emerald-500/60 py-0.5">
            <div className="flex gap-1">
              <div className="w-1.5 h-1 bg-emerald-800 rounded-sm" />
              <div className="w-1.5 h-1 bg-emerald-800 rounded-sm" />
              <div className="w-1.5 h-1 bg-emerald-800 rounded-sm" />
            </div>
            <span className="text-[8px] font-mono text-emerald-400">MAINFRAME REPO</span>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* FRAME ARCHITECTURE 4: SKY CITADEL ZEAL TORUS */}
      {/* ========================================================================= */}
      {style === 'sky' && (
        <div className="absolute -inset-3 sm:-inset-3.5 pointer-events-none z-20 flex flex-col justify-between">
          <div className="w-full flex items-center justify-center -top-2">
            <div className="bg-gradient-to-r from-sky-800 via-sky-500 to-sky-800 px-4 py-0.5 rounded-t-xl border-t border-x border-sky-300 shadow-[0_0_15px_rgba(56,189,248,0.4)] flex items-center gap-1.5">
              <span className="text-[9px] text-white font-serif tracking-widest">★ KINGDOM OF ZEAL ★</span>
            </div>
          </div>
          <div className="w-full flex-1 flex justify-between px-0.5">
            <div className="w-1.5 bg-gradient-to-b from-sky-400 via-sky-600 to-sky-900 rounded-l shadow-[0_0_8px_#38bdf8]" />
            <div className="w-1.5 bg-gradient-to-b from-sky-400 via-sky-600 to-sky-900 rounded-r shadow-[0_0_8px_#38bdf8]" />
          </div>
          <div className="w-full flex items-center justify-center -bottom-1.5">
            <div className="bg-slate-950 px-4 py-0.5 rounded-b-xl border-b border-x border-sky-400/40 text-[9px] font-mono text-sky-200">
              HARMONIC STRATOSPHERE
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* FRAME ARCHITECTURE 5: GEOTHERMAL LAVA BASALT FORGE */}
      {/* ========================================================================= */}
      {style === 'magma' && (
        <div className="absolute -inset-3 sm:-inset-3.5 pointer-events-none z-20 flex flex-col justify-between">
          <div className="w-full flex items-center justify-center -top-2">
            <div className="bg-gradient-to-r from-stone-900 via-orange-700 to-stone-900 px-4 py-0.5 rounded-t-xl border-t border-x border-orange-500 shadow-[0_0_20px_rgba(249,115,22,0.4)] flex items-center gap-1.5">
              <span className="text-[9px] text-orange-200 font-bold tracking-wider">▲ SUB-TERRA FORGE ▲</span>
            </div>
          </div>
          <div className="w-full flex-1 flex justify-between px-0.5">
            <div className="w-2 bg-gradient-to-b from-orange-500 via-stone-800 to-red-600 rounded-l border-l border-orange-500/50 shadow-md" />
            <div className="w-2 bg-gradient-to-b from-red-600 via-stone-800 to-orange-500 rounded-r border-r border-orange-500/50 shadow-md" />
          </div>
          <div className="w-full flex items-center justify-center -bottom-1.5">
            <div className="bg-stone-950 px-4 py-0.5 rounded-b-xl border-b border-x border-orange-600 text-[9px] font-mono text-orange-300">
              180 Hz CORE RESONANCE
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* FRAME ARCHITECTURE 6: BIOLUMINESCENT SPORE MYCELIUM ARBOR */}
      {/* ========================================================================= */}
      {style === 'spore' && (
        <div className="absolute -inset-3 sm:-inset-3.5 pointer-events-none z-20 flex flex-col justify-between">
          <div className="w-full flex items-center justify-center -top-2">
            <div className="bg-gradient-to-r from-purple-950 via-purple-700 to-fuchsia-950 px-4 py-0.5 rounded-t-xl border-t border-x border-purple-400 shadow-[0_0_20px_rgba(168,85,247,0.4)] flex items-center gap-1.5">
              <span className="text-[9px] text-purple-200 font-sans font-semibold">🍄 LIVING SPORE ARBOR 🍄</span>
            </div>
          </div>
          <div className="w-full flex-1 flex justify-between px-0.5">
            <div className="w-1.5 bg-gradient-to-b from-fuchsia-500 via-purple-700 to-cyan-500 rounded-l shadow-[0_0_8px_#c084fc]" />
            <div className="w-1.5 bg-gradient-to-b from-cyan-500 via-purple-700 to-fuchsia-500 rounded-r shadow-[0_0_8px_#38bdf8]" />
          </div>
          <div className="w-full flex items-center justify-center -bottom-1.5">
            <div className="bg-slate-950 px-4 py-0.5 rounded-b-xl border-b border-x border-purple-400/50 text-[9px] font-mono text-purple-300">
              MYCELIAL LIGHT CHANNELS
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* FRAME ARCHITECTURE 7: EPOCH / CUSTOM GENERATIVE MATRIX */}
      {/* ========================================================================= */}
      {(style === 'matrix' || style === 'custom') && (
        <div className="absolute -inset-2.5 pointer-events-none z-20 flex flex-col justify-between">
          <div className="w-full flex items-center justify-center -top-2">
            <div
              className="px-3 py-0.5 rounded-t-lg border-t border-x shadow-md flex items-center gap-1.5 text-[9px] font-mono"
              style={{
                backgroundColor: '#0f172a',
                borderColor: portal.accentColor,
                color: portal.accentColor,
              }}
            >
              <span>◈ {portal.epoch.toUpperCase()} PORTAL FRAME ◈</span>
            </div>
          </div>
          <div className="w-full flex-1 flex justify-between">
            <div className="w-1 rounded-l" style={{ backgroundColor: portal.accentColor, opacity: 0.7 }} />
            <div className="w-1 rounded-r" style={{ backgroundColor: portal.accentColor, opacity: 0.7 }} />
          </div>
          <div className="w-full flex items-center justify-center -bottom-1.5">
            <div
              className="px-3 py-0.5 rounded-b-lg border-b border-x text-[8px] font-mono bg-slate-950"
              style={{ borderColor: portal.accentColor, color: portal.accentColor }}
            >
              {portal.theme}
            </div>
          </div>
        </div>
      )}

      {/* The Live Inner Portal Canvas Viewport */}
      <div className="relative w-full h-full rounded-xl overflow-hidden bg-slate-950 z-10">
        {children}
      </div>

      {/* Optional Top Floating Label */}
      {showLabels && (
        <div className="absolute top-2 left-2 z-30 pointer-events-none bg-slate-950/80 backdrop-blur-md px-2 py-0.5 rounded border border-slate-700/60 flex items-center gap-1.5 text-[10px] font-mono text-slate-200">
          <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: portal.accentColor }} />
          <span>{portal.name}</span>
        </div>
      )}
    </div>
  );
};
