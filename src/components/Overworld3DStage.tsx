/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { PortalSurface, EpochEra } from '../types';
import { PortalFrame } from './PortalFrame';
import { PortalCanvas } from './PortalCanvas';
import { audioEngine } from '../utils/audio';
import {
  Compass,
  Rotate3d,
  Maximize,
  ZoomIn,
  ZoomOut,
  Sparkles,
  ArrowRight,
  Play,
  Pause,
  Layers,
  Eye,
} from 'lucide-react';

interface Overworld3DStageProps {
  portals: PortalSurface[];
  activePortal: PortalSurface;
  epoch: EpochEra;
  onSelectPortal: (portal: PortalSurface) => void;
  onStepThrough: (portal: PortalSurface) => void;
  completedQuestIds: string[];
  onQuestProgress?: (nodeId: string, value?: any) => void;
}

export const Overworld3DStage: React.FC<Overworld3DStageProps> = ({
  portals,
  activePortal,
  epoch,
  onSelectPortal,
  onStepThrough,
  completedQuestIds,
  onQuestProgress,
}) => {
  // 3D Camera State
  const [rotationY, setRotationY] = useState(0);
  const [rotationX, setRotationX] = useState(12); // subtle downward tilt
  const [zoom, setZoom] = useState(1); // 0.6 (panoramic) to 1.4 (close)
  const [isAutoOrbit, setIsAutoOrbit] = useState(true);
  const [isDragging, setIsDragging] = useState(false);

  const dragStartRef = useRef<{ x: number; y: number; startRotY: number; startRotX: number }>({
    x: 0,
    y: 0,
    startRotY: 0,
    startRotX: 0,
  });

  const activeIndex = portals.findIndex((p) => p.id === activePortal.id);
  const totalPortals = portals.length;
  const angleStep = 360 / Math.max(1, totalPortals);

  // Auto-Orbit animation loop
  useEffect(() => {
    if (!isAutoOrbit || isDragging) return;

    const interval = setInterval(() => {
      setRotationY((prev) => (prev + 0.15) % 360);
    }, 30);

    return () => clearInterval(interval);
  }, [isAutoOrbit, isDragging]);

  // When active portal changes externally, snap camera angle to face it smoothly
  const snapToPortal = useCallback((index: number) => {
    const targetAngle = -index * angleStep;
    setRotationY(targetAngle);
  }, [angleStep]);

  // Mouse & Touch Drag Handlers for 3D Chamber Rotation
  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    dragStartRef.current = {
      x: e.clientX,
      y: e.clientY,
      startRotY: rotationY,
      startRotX: rotationX,
    };
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    const deltaX = e.clientX - dragStartRef.current.x;
    const deltaY = e.clientY - dragStartRef.current.y;

    setRotationY(dragStartRef.current.startRotY + deltaX * 0.4);
    setRotationX(Math.max(-10, Math.min(35, dragStartRef.current.startRotX - deltaY * 0.2)));
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Touch handlers for mobile/tablet 3D orbit
  const handleTouchStart = (e: React.TouchEvent) => {
    if (e.touches.length === 1) {
      setIsDragging(true);
      dragStartRef.current = {
        x: e.touches[0].clientX,
        y: e.touches[0].clientY,
        startRotY: rotationY,
        startRotX: rotationX,
      };
    }
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isDragging || e.touches.length !== 1) return;
    const deltaX = e.touches[0].clientX - dragStartRef.current.x;
    const deltaY = e.touches[0].clientY - dragStartRef.current.y;

    setRotationY(dragStartRef.current.startRotY + deltaX * 0.5);
    setRotationX(Math.max(-10, Math.min(35, dragStartRef.current.startRotX - deltaY * 0.25)));
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
  };

  // Calculate 3D Cylinder Radius based on count of portals
  const cylinderRadius = Math.max(380, totalPortals * 68);

  return (
    <div className="relative w-full h-[520px] sm:h-[580px] lg:h-[620px] rounded-2xl bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 border border-slate-800/80 shadow-2xl overflow-hidden select-none flex flex-col justify-between">
      {/* 3D Overworld Stage Header Controls */}
      <div className="relative z-30 p-3 sm:p-4 bg-slate-950/70 backdrop-blur-md border-b border-slate-800/60 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-sky-500/20 text-sky-400 border border-sky-500/30 shadow-[0_0_12px_rgba(56,189,248,0.3)]">
            <Layers className="w-4 h-4 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-sm font-bold text-white tracking-wide flex items-center gap-1.5">
                <span>3D OVERWORLD CHAMBER</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  {portals.length} Interconnected Realities
                </span>
              </h3>
            </div>
            <p className="text-[11px] font-mono text-slate-400">
              Drag stage to orbit 360° • Click any portal frame to focus or step through
            </p>
          </div>
        </div>

        {/* 3D Camera & Orbit Toolbar */}
        <div className="flex items-center gap-2">
          {/* Auto-Orbit Toggle */}
          <button
            onClick={() => setIsAutoOrbit(!isAutoOrbit)}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-mono border transition-all ${
              isAutoOrbit
                ? 'bg-sky-950/80 text-sky-300 border-sky-500/50 shadow-[0_0_10px_rgba(56,189,248,0.2)]'
                : 'bg-slate-900 text-slate-400 border-slate-700 hover:text-slate-200'
            }`}
            title="Toggle Auto-Orbit Camera Rotation"
          >
            {isAutoOrbit ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            <span>Auto Orbit</span>
          </button>

          {/* Zoom Out */}
          <button
            onClick={() => setZoom((z) => Math.max(0.65, z - 0.1))}
            className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 transition-colors"
            title="Zoom Out (Panoramic Overworld)"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>

          {/* Zoom In */}
          <button
            onClick={() => setZoom((z) => Math.min(1.3, z + 0.1))}
            className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 transition-colors"
            title="Zoom In (Close Portal Inspection)"
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </button>

          {/* Reset Camera */}
          <button
            onClick={() => {
              setRotationY(0);
              setRotationX(12);
              setZoom(1);
            }}
            className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 transition-colors"
            title="Reset 3D Camera"
          >
            <Rotate3d className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* 3D Viewport Stage Canvas & Orbit Ring */}
      <div
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
        className="relative flex-1 w-full flex items-center justify-center overflow-hidden cursor-grab active:cursor-grabbing"
        style={{
          perspective: '1200px',
        }}
      >
        {/* Background Ambient Starfield & Atmospheric Glow */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-sky-950/20 via-slate-950 to-black pointer-events-none" />

        {/* 3D Transforming World Container */}
        <div
          className="relative w-full h-full flex items-center justify-center transition-transform duration-75 ease-out pointer-events-none"
          style={{
            transformStyle: 'preserve-3d',
            transform: `scale(${zoom}) rotateX(${rotationX}deg) rotateY(${rotationY}deg)`,
          }}
        >
          {/* ========================================================================= */}
          {/* 3D FLOOR MATRIX & LEYLINES */}
          {/* ========================================================================= */}
          <div
            className="absolute rounded-full pointer-events-none border border-sky-500/20 shadow-[0_0_60px_rgba(56,189,248,0.15)] flex items-center justify-center"
            style={{
              width: `${cylinderRadius * 2.3}px`,
              height: `${cylinderRadius * 2.3}px`,
              transform: 'translateY(190px) rotateX(90deg)',
              background:
                'radial-gradient(circle, rgba(14,165,233,0.12) 0%, rgba(15,23,42,0.6) 50%, rgba(2,6,23,0.9) 100%)',
            }}
          >
            {/* Concentric Leyline Rings */}
            <div className="w-[75%] h-[75%] rounded-full border border-sky-400/25 animate-[spin_40s_linear_infinite]" />
            <div className="w-[50%] h-[50%] rounded-full border border-amber-400/30 animate-[spin_25s_linear_infinite_reverse]" />
            <div className="w-[25%] h-[25%] rounded-full border border-purple-400/40" />

            {/* Radiant Leylines projecting outward to each portal wall */}
            {portals.map((portal, idx) => {
              const angle = idx * angleStep;
              return (
                <div
                  key={`leyline-${portal.id}`}
                  className="absolute w-full h-0.5"
                  style={{
                    transform: `rotate(${angle}deg)`,
                    background: `linear-gradient(90deg, transparent 40%, ${portal.accentColor} 85%, transparent 100%)`,
                    opacity: portal.id === activePortal.id ? 0.9 : 0.4,
                  }}
                />
              );
            })}

            {/* Central Sound Stone Dais Pedestal */}
            <div className="absolute w-20 h-20 rounded-full bg-gradient-to-tr from-sky-500 via-amber-400 to-purple-500 shadow-[0_0_30px_#38bdf8] flex items-center justify-center animate-pulse">
              <Compass className="w-8 h-8 text-slate-950 font-bold" />
            </div>
          </div>

          {/* ========================================================================= */}
          {/* 3D PORTAL FRAMES STANDING IN CYLINDRICAL OVERWORLD SPACE */}
          {/* ========================================================================= */}
          {portals.map((portal, idx) => {
            const angle = idx * angleStep;
            const isSelected = portal.id === activePortal.id;
            const isCompleted = portal.questNodeId && completedQuestIds.includes(portal.questNodeId);

            return (
              <div
                key={portal.id}
                onClick={(e) => {
                  e.stopPropagation();
                  onSelectPortal(portal);
                  audioEngine.playPortalWarp();
                  snapToPortal(idx);
                }}
                className="absolute pointer-events-auto cursor-pointer transition-all duration-300 hover:scale-[1.05]"
                style={{
                  width: '260px',
                  height: '190px',
                  transformStyle: 'preserve-3d',
                  transform: `rotateY(${angle}deg) translateZ(${cylinderRadius}px)`,
                }}
              >
                {/* Ornate Portal Frame with Living Moving Picture Canvas */}
                <PortalFrame
                  portal={portal}
                  isFocused={isSelected}
                  showLabels={false}
                  className="w-full h-full shadow-2xl"
                >
                  <PortalCanvas
                    portal={portal}
                    epoch={epoch}
                    isActive={isSelected}
                    onQuestProgress={onQuestProgress}
                    isQuestCompleted={isCompleted}
                  />
                </PortalFrame>

                {/* Floating Pedestal Plinth Label */}
                <div
                  className={`mt-4 px-3 py-1.5 rounded-xl border backdrop-blur-md transition-all text-center flex flex-col items-center gap-0.5 ${
                    isSelected
                      ? 'bg-slate-900/95 border-sky-400 shadow-[0_0_20px_rgba(56,189,248,0.3)]'
                      : 'bg-slate-950/80 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center gap-1.5">
                    <span
                      className="w-2 h-2 rounded-full"
                      style={{ backgroundColor: portal.accentColor }}
                    />
                    <span className="text-[11px] font-bold text-white truncate max-w-[170px]">
                      {portal.name}
                    </span>
                  </div>
                  <span className="text-[9px] font-mono text-slate-400">{portal.theme}</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Center Crosshair / Drag Hint Overlay */}
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-20 pointer-events-none bg-slate-950/80 backdrop-blur-md px-3 py-1 rounded-full border border-slate-800 text-[10px] font-mono text-slate-400 flex items-center gap-2">
          <Eye className="w-3.5 h-3.5 text-sky-400 animate-pulse" />
          <span>Click any Portal Frame to approach • Drag anywhere to rotate Overworld</span>
        </div>
      </div>

      {/* Overworld Bottom Teleportation Dock */}
      <div className="relative z-30 p-3 bg-slate-950/80 backdrop-blur-md border-t border-slate-800/60 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <span
            className="w-3 h-3 rounded-full animate-ping"
            style={{ backgroundColor: activePortal.accentColor }}
          />
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-white font-mono uppercase">
                TARGET PORTAL: {activePortal.name}
              </span>
              <span className="text-[10px] font-mono px-2 py-0.2 rounded bg-slate-800 text-amber-400">
                {activePortal.ambientFrequency} Hz
              </span>
            </div>
            <p className="text-[11px] text-slate-400 line-clamp-1">{activePortal.lore}</p>
          </div>
        </div>

        {/* Step Through Button */}
        <button
          onClick={() => {
            onStepThrough(activePortal);
            audioEngine.playSuccessFanfare();
          }}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-bold text-xs shadow-[0_0_20px_rgba(56,189,248,0.4)] transition-all hover:scale-105 active:scale-95"
        >
          <Sparkles className="w-4 h-4" />
          <span>STEP INTO GATEWAY</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
