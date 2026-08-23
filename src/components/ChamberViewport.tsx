/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { PortalSurface, EpochEra, CustomBattlefield } from '../types';
import { PortalCanvas } from './PortalCanvas';
import { PortalFrame } from './PortalFrame';
import { Overworld3DStage } from './Overworld3DStage';
import { AutoChessArena3D } from './AutoChessArena3D';
import { WorldBuilderStudio } from './WorldBuilderStudio';
import { ATBMultiplayerArena } from './ATBMultiplayerArena';
import { CrossTabletopMatrix3D } from './CrossTabletopMatrix3D';
import {
  ChevronLeft,
  ChevronRight,
  Maximize2,
  Radio,
  Sparkles,
  Volume2,
  Layers,
  Compass,
  ArrowLeft,
  Swords,
  Hammer,
  Zap,
  Rotate3d,
} from 'lucide-react';
import { audioEngine } from '../utils/audio';

interface ChamberViewportProps {
  portals: PortalSurface[];
  activePortal: PortalSurface;
  epoch: EpochEra;
  onSelectPortal: (portal: PortalSurface) => void;
  onQuestProgress?: (nodeId: string, value?: any) => void;
  completedQuestIds: string[];
  onDeployWorld?: (portal: PortalSurface) => void;
}

export const ChamberViewport: React.FC<ChamberViewportProps> = ({
  portals,
  activePortal,
  epoch,
  onSelectPortal,
  onQuestProgress,
  completedQuestIds,
  onDeployWorld,
}) => {
  // Mode: 'cross_matrix' | 'atb_multiplayer' | 'overworld' | 'focused' | 'autochess' | 'builder'
  const [viewMode, setViewMode] = useState<
    'cross_matrix' | 'atb_multiplayer' | 'overworld' | 'focused' | 'autochess' | 'builder'
  >('cross_matrix');
  const [isFullscreen, setIsFullscreen] = useState(false);

  const activeIndex = portals.findIndex((p) => p.id === activePortal.id);

  const handlePrev = () => {
    const nextIdx = (activeIndex - 1 + portals.length) % portals.length;
    onSelectPortal(portals[nextIdx]);
    audioEngine.playPortalWarp();
  };

  const handleNext = () => {
    const nextIdx = (activeIndex + 1) % portals.length;
    onSelectPortal(portals[nextIdx]);
    audioEngine.playPortalWarp();
  };

  const handleStepThrough = (portal: PortalSurface) => {
    onSelectPortal(portal);
    setViewMode('focused');
  };

  const handleWorldDeployed = (newPortal: PortalSurface) => {
    if (onDeployWorld) {
      onDeployWorld(newPortal);
    }
    onSelectPortal(newPortal);
    setViewMode('cross_matrix');
  };

  const handleDeployToMultiplayer = (_battlefield: CustomBattlefield) => {
    setViewMode('cross_matrix');
  };

  return (
    <div className="w-full flex flex-col gap-4">
      {/* Top View Mode Switcher Banner */}
      <div className="flex flex-wrap items-center justify-between gap-3 bg-slate-900/60 p-2.5 sm:p-3 rounded-2xl border border-slate-800/80 backdrop-blur-xl shadow-lg">
        <div className="flex flex-wrap items-center gap-2">
          {/* 3D Cross-Table Matrix (Cross-boundary inter-tableplay) */}
          <button
            onClick={() => {
              setViewMode('cross_matrix');
              audioEngine.playCrossTableMortar();
            }}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl font-black text-xs transition-all ${
              viewMode === 'cross_matrix'
                ? 'bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white shadow-[0_0_22px_rgba(168,85,247,0.5)] ring-1 ring-pink-300'
                : 'bg-slate-800/80 text-purple-300 hover:text-white border border-purple-500/30'
            }`}
          >
            <Rotate3d className="w-4 h-4 text-pink-300" />
            <span>3D CROSS-TABLE MATRIX</span>
          </button>

          {/* ATB Multiplayer Arena (3X Autocasting) */}
          <button
            onClick={() => {
              setViewMode('atb_multiplayer');
              audioEngine.playATBAutocast();
            }}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl font-black text-xs transition-all ${
              viewMode === 'atb_multiplayer'
                ? 'bg-gradient-to-r from-amber-500 via-rose-500 to-indigo-600 text-white shadow-[0_0_20px_rgba(244,63,94,0.4)] ring-1 ring-amber-300'
                : 'bg-slate-800/80 text-amber-300 hover:text-white border border-amber-500/30'
            }`}
          >
            <Zap className="w-4 h-4 text-amber-300 fill-amber-300" />
            <span>3X ATB MULTIPLAYER RAID</span>
          </button>

          {/* 3D Overworld Realm */}
          <button
            onClick={() => {
              setViewMode('overworld');
              audioEngine.playSporeChime(400);
            }}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl font-bold text-xs transition-all ${
              viewMode === 'overworld'
                ? 'bg-gradient-to-r from-sky-500 to-indigo-600 text-white shadow-[0_0_15px_rgba(56,189,248,0.3)]'
                : 'bg-slate-800/80 text-slate-400 hover:text-slate-200 border border-slate-700/60'
            }`}
          >
            <Compass className="w-4 h-4" />
            <span>3D OVERWORLD REALM</span>
          </button>

          {/* Kirby World Builder Studio */}
          <button
            onClick={() => {
              setViewMode('builder');
              audioEngine.playHammerTap();
            }}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl font-bold text-xs transition-all ${
              viewMode === 'builder'
                ? 'bg-gradient-to-r from-pink-500 to-emerald-500 text-slate-950 font-black shadow-[0_0_15px_rgba(244,114,182,0.4)]'
                : 'bg-slate-800/80 text-pink-400 hover:text-pink-200 border border-slate-700/60'
            }`}
          >
            <Hammer className="w-4 h-4" />
            <span>WORLD BUILDER STUDIO</span>
          </button>

          {/* 3D Auto Chess Arena */}
          <button
            onClick={() => {
              setViewMode('autochess');
              audioEngine.playDiceRoll();
            }}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl font-bold text-xs transition-all ${
              viewMode === 'autochess'
                ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-bold shadow-[0_0_15px_rgba(6,182,212,0.4)]'
                : 'bg-slate-800/80 text-slate-400 hover:text-slate-200 border border-slate-700/60'
            }`}
          >
            <Swords className="w-4 h-4" />
            <span>3D AUTO-CHESS</span>
          </button>

          {/* Focused Gateway */}
          <button
            onClick={() => {
              setViewMode('focused');
              audioEngine.playSporeChime(550);
            }}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl font-bold text-xs transition-all ${
              viewMode === 'focused'
                ? 'bg-gradient-to-r from-teal-500 to-emerald-600 text-white shadow-[0_0_15px_rgba(20,184,166,0.3)]'
                : 'bg-slate-800/80 text-slate-400 hover:text-slate-200 border border-slate-700/60'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>GATEWAY FOCUS</span>
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => audioEngine.playMelodyNote(activeIndex % 8)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-xs font-mono border border-slate-700 transition-colors"
            title="Resonate with Active Portal Frequency"
          >
            <Volume2 className="w-3.5 h-3.5 text-amber-400" />
            <span>{activePortal.ambientFrequency} Hz</span>
          </button>
        </div>
      </div>

      {/* Primary Stage Switcher */}
      {viewMode === 'cross_matrix' ? (
        <CrossTabletopMatrix3D
          onOpenBuilder={() => setViewMode('builder')}
          onExit={() => setViewMode('atb_multiplayer')}
        />
      ) : viewMode === 'atb_multiplayer' ? (
        <ATBMultiplayerArena
          onOpenBuilder={() => setViewMode('builder')}
          onExit={() => setViewMode('cross_matrix')}
        />
      ) : viewMode === 'overworld' ? (
        <Overworld3DStage
          portals={portals}
          activePortal={activePortal}
          epoch={epoch}
          onSelectPortal={onSelectPortal}
          onStepThrough={handleStepThrough}
          completedQuestIds={completedQuestIds}
          onQuestProgress={onQuestProgress}
        />
      ) : viewMode === 'autochess' ? (
        <AutoChessArena3D
          portals={portals}
          onSelectPortal={onSelectPortal}
        />
      ) : viewMode === 'builder' ? (
        <WorldBuilderStudio
          onDeployWorld={handleWorldDeployed}
          onDeployToMultiplayer={handleDeployToMultiplayer}
          onClose={() => setViewMode('cross_matrix')}
        />
      ) : (

        /* Focused Gateway Chamber with Ornate Portal Frame & Quest Tools */
        <div className="relative w-full rounded-2xl bg-slate-900/60 border border-slate-800/80 p-3 sm:p-5 shadow-2xl backdrop-blur-xl transition-all duration-300">
          {/* Stage Header Info */}
          <div className="flex flex-wrap items-center justify-between gap-3 mb-3 pb-3 border-b border-slate-800/60">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setViewMode('overworld')}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-sky-400 text-xs font-mono border border-slate-700 transition-colors"
                title="Return to 3D Overworld"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                <span>Return to Overworld</span>
              </button>

              <div>
                <h2 className="text-lg sm:text-xl font-bold tracking-tight text-white flex items-center gap-2">
                  {activePortal.name}
                  {activePortal.isGenerated && (
                    <span className="text-[10px] bg-sky-500/20 text-sky-400 border border-sky-500/30 px-2 py-0.5 rounded-full font-mono font-normal">
                      AI Multimodal
                    </span>
                  )}
                </h2>
                <p className="text-xs text-slate-400 font-mono">{activePortal.subtitle}</p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsFullscreen(!isFullscreen)}
                className="p-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-colors"
                title="Toggle View Mode"
              >
                <Maximize2 className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Live Canvas Viewport Stage encased in Ornate Portal Frame */}
          <div className={`relative w-full ${isFullscreen ? 'h-[620px]' : 'h-[440px] sm:h-[500px]'} transition-all duration-300 p-3 sm:p-5`}>
            <PortalFrame portal={activePortal} isFocused={true} className="w-full h-full">
              <PortalCanvas
                portal={activePortal}
                epoch={epoch}
                isActive={true}
                onQuestProgress={onQuestProgress}
                isQuestCompleted={activePortal.questNodeId ? completedQuestIds.includes(activePortal.questNodeId) : false}
              />
            </PortalFrame>

            {/* Chamber Nav Navigation Chevrons */}
            <button
              onClick={handlePrev}
              className="absolute left-1 sm:left-2 top-1/2 -translate-y-1/2 p-2.5 rounded-full bg-slate-950/80 hover:bg-slate-900 text-slate-200 border border-slate-700/80 shadow-2xl backdrop-blur-md transition-transform hover:scale-110 active:scale-95 z-30"
              title="Previous Portal Wall (Left)"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>

            <button
              onClick={handleNext}
              className="absolute right-1 sm:right-2 top-1/2 -translate-y-1/2 p-2.5 rounded-full bg-slate-950/80 hover:bg-slate-900 text-slate-200 border border-slate-700/80 shadow-2xl backdrop-blur-md transition-transform hover:scale-110 active:scale-95 z-30"
              title="Next Portal Wall (Right)"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>

          {/* Portal Lore Narrative Banner */}
          <div className="mt-3.5 p-3 rounded-xl bg-slate-950/70 border border-slate-800/60 text-xs text-slate-300 font-sans leading-relaxed flex items-start gap-2.5">
            <Radio className="w-4 h-4 text-sky-400 shrink-0 mt-0.5 animate-pulse" />
            <div>
              <span className="font-semibold text-slate-100 mr-1.5 font-mono text-[11px]">PORTAL TELEMETRY:</span>
              {activePortal.lore}
            </div>
          </div>
        </div>
      )}

      {/* 3D Macro Hall Portal Carousel Selector */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-2.5">
        {portals.map((portal, idx) => {
          const isSelected = portal.id === activePortal.id;
          const isCompleted = portal.questNodeId && completedQuestIds.includes(portal.questNodeId);

          return (
            <button
              key={portal.id}
              onClick={() => {
                onSelectPortal(portal);
                audioEngine.playPortalWarp();
              }}
              className={`text-left p-3 rounded-xl transition-all duration-200 border relative group overflow-hidden ${
                isSelected
                  ? 'bg-slate-800/90 border-sky-400 shadow-[0_0_20px_rgba(56,189,248,0.2)] scale-[1.02]'
                  : 'bg-slate-900/40 hover:bg-slate-800/60 border-slate-800 hover:border-slate-700'
              }`}
            >
              {/* Accent Glow Top Rim */}
              <div
                className="absolute top-0 left-0 right-0 h-1 transition-opacity"
                style={{
                  backgroundColor: portal.accentColor,
                  opacity: isSelected ? 1 : 0.4,
                }}
              />

              <div className="flex items-center justify-between mb-1 mt-1">
                <span className="text-[10px] font-mono text-slate-400">WALL 0{idx + 1}</span>
                {isCompleted ? (
                  <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]" />
                ) : (
                  <span
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: portal.accentColor }}
                  />
                )}
              </div>

              <h4 className="text-xs font-bold text-slate-100 truncate group-hover:text-white">
                {portal.name}
              </h4>
              <p className="text-[10px] text-slate-400 truncate font-mono mt-0.5">
                {portal.theme}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
};


