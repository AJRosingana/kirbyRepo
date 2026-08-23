/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { EpochEra } from '../types';
import { audioEngine } from '../utils/audio';
import { Cpu, Sliders, Volume2, VolumeX, Sparkles, Activity } from 'lucide-react';

interface EpochControlsProps {
  currentEpoch: EpochEra;
  onChangeEpoch: (epoch: EpochEra) => void;
  isMuted: boolean;
  onToggleMute: () => void;
  currentFrequency: number;
}

export const EpochControls: React.FC<EpochControlsProps> = ({
  currentEpoch,
  onChangeEpoch,
  isMuted,
  onToggleMute,
  currentFrequency,
}) => {
  const epochs: { id: EpochEra; label: string; desc: string; color: string }[] = [
    { id: '8bit', label: '8-BIT NES', desc: '4-Color Dither & Raster Lines', color: '#eab308' },
    { id: '16bit', label: '16-BIT SNES', desc: 'Mode-7 Affine & Copper Palette', color: '#f43f5e' },
    { id: '32bit', label: '32-BIT PS1', desc: 'Gouraud Polygon & Jitter Matrix', color: '#38bdf8' },
    { id: 'ultra', label: 'ULTRA SHADER', desc: 'Raymarched Sine & Glow FX', color: '#a855f7' },
  ];

  return (
    <div className="w-full rounded-2xl bg-slate-900/60 border border-slate-800/80 p-4 sm:p-5 backdrop-blur-xl shadow-2xl flex flex-col gap-3.5">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800/60">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm sm:text-base font-bold text-white flex items-center gap-2">
              Bit-Shift Epoch Shifter
              <span className="text-[11px] font-mono text-amber-400 font-normal">
                (Global Pipeline)
              </span>
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              Chrono-Visual Transmutation Matrix
            </p>
          </div>
        </div>

        {/* Mute & Frequency Meter */}
        <div className="flex items-center gap-2">
          <button
            onClick={onToggleMute}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-mono transition-colors ${
              isMuted
                ? 'bg-rose-950/40 border-rose-500/40 text-rose-300'
                : 'bg-slate-800 border-slate-700 text-slate-200 hover:bg-slate-700'
            }`}
          >
            {isMuted ? <VolumeX className="w-3.5 h-3.5 text-rose-400" /> : <Volume2 className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />}
            <span>{isMuted ? 'MUTED' : 'SYNTH ON'}</span>
          </button>
        </div>
      </div>

      {/* Epoch Era Buttons */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
        {epochs.map((ep) => {
          const isSelected = currentEpoch === ep.id;
          return (
            <button
              key={ep.id}
              onClick={() => {
                onChangeEpoch(ep.id);
                audioEngine.playTextBlip(ep.id === '8bit' ? -2 : ep.id === '16bit' ? 0 : ep.id === '32bit' ? 2 : 4);
              }}
              className={`p-3 rounded-xl border text-left transition-all duration-200 flex flex-col justify-between ${
                isSelected
                  ? 'bg-slate-800/90 border-amber-400 shadow-[0_0_15px_rgba(234,179,8,0.2)] scale-[1.02]'
                  : 'bg-slate-950/40 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: ep.color }}
                />
                <span className={`text-[10px] font-mono ${isSelected ? 'text-amber-300 font-bold' : 'text-slate-500'}`}>
                  {ep.id.toUpperCase()}
                </span>
              </div>
              <h4 className="text-xs font-bold text-slate-100">{ep.label}</h4>
              <p className="text-[10px] text-slate-400 font-mono mt-0.5">{ep.desc}</p>
            </button>
          );
        })}
      </div>
    </div>
  );
};
