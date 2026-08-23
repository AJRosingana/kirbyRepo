/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Sparkles, Wand2, Volume2, VolumeX, RefreshCw } from 'lucide-react';
import { audioEngine } from '../utils/audio';

interface NavbarProps {
  onOpenPromptStudio: () => void;
  isMuted: boolean;
  onToggleMute: () => void;
  onResetQuests: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenPromptStudio,
  isMuted,
  onToggleMute,
  onResetQuests,
}) => {
  return (
    <header className="w-full border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-xl sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-600 via-indigo-600 to-rose-500 p-0.5 shadow-lg shadow-indigo-900/30 flex items-center justify-center">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-sky-400 animate-pulse" />
            </div>
          </div>
          <div>
            <h1 className="text-base sm:text-lg font-extrabold tracking-tight text-white flex items-center gap-2">
              Macro Portal Engine
              <span className="text-[10px] bg-sky-500/10 text-sky-400 border border-sky-500/30 px-2 py-0.5 rounded-full font-mono font-normal">
                AI Studio Intro
              </span>
            </h1>
            <p className="text-[11px] text-slate-400 font-mono hidden sm:block">
              Multimodal Generative World & Procedural Synth
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2.5">
          {/* Mute toggle */}
          <button
            onClick={() => {
              audioEngine.init();
              onToggleMute();
            }}
            className="p-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700/80 text-slate-300 transition-colors"
            title={isMuted ? 'Unmute Procedural Audio' : 'Mute Audio'}
          >
            {isMuted ? <VolumeX className="w-4 h-4 text-rose-400" /> : <Volume2 className="w-4 h-4 text-emerald-400" />}
          </button>

          {/* Reset Quests */}
          <button
            onClick={onResetQuests}
            className="hidden md:flex items-center gap-1 px-3 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700/80 text-slate-300 text-xs font-mono transition-colors"
            title="Reset Sound Stone Quests"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Reset Lore</span>
          </button>

          {/* Spawn AI Portal Button */}
          <button
            onClick={onOpenPromptStudio}
            className="flex items-center gap-2 bg-gradient-to-r from-sky-500 via-indigo-500 to-purple-600 hover:from-sky-400 hover:to-purple-500 text-white font-mono font-semibold px-3.5 sm:px-4 py-2 rounded-xl text-xs shadow-lg shadow-indigo-900/40 transition-all active:scale-95"
          >
            <Wand2 className="w-4 h-4" />
            <span className="hidden sm:inline">AI Studio Portal Creator</span>
            <span className="sm:hidden">Create</span>
          </button>
        </div>
      </div>
    </header>
  );
};
