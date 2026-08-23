/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { QuestNode } from '../types';
import { audioEngine } from '../utils/audio';
import { CheckCircle2, Circle, Compass, Sparkles, Music, ArrowUpRight } from 'lucide-react';

interface QuestTrackerProps {
  questNodes: QuestNode[];
  onSelectPortalById: (portalId: string) => void;
  activePortalId: string;
}

export const QuestTracker: React.FC<QuestTrackerProps> = ({
  questNodes,
  onSelectPortalById,
  activePortalId,
}) => {
  const completedCount = questNodes.filter((q) => q.completed).length;
  const isAllComplete = completedCount === questNodes.length;

  return (
    <div className="w-full rounded-2xl bg-slate-900/60 border border-slate-800/80 p-4 sm:p-5 backdrop-blur-xl shadow-2xl flex flex-col gap-3.5">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800/60">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400">
            <Compass className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm sm:text-base font-bold text-white flex items-center gap-2">
              The Shattered Sound Stone
              <span className="text-[11px] font-mono text-rose-400 font-normal">
                ({completedCount}/{questNodes.length} Restored)
              </span>
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              Multiverse Quest Chain • Gather the 4 Melodies
            </p>
          </div>
        </div>

        {isAllComplete && (
          <div className="flex items-center gap-1.5 bg-amber-500/20 text-amber-300 border border-amber-500/40 px-3 py-1 rounded-full text-xs font-mono font-bold animate-pulse">
            <Sparkles className="w-3.5 h-3.5" />
            <span>OMNIVERSE HARMONIZED</span>
          </div>
        )}
      </div>

      {/* Quest Nodes List */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        {questNodes.map((node) => {
          const isTargetActive = activePortalId === node.portalId;

          return (
            <div
              key={node.id}
              onClick={() => {
                onSelectPortalById(node.portalId);
                audioEngine.playPortalWarp();
              }}
              className={`p-3 rounded-xl border transition-all duration-200 cursor-pointer flex flex-col justify-between gap-2 group ${
                node.completed
                  ? 'bg-emerald-950/20 border-emerald-500/30 hover:border-emerald-500/60'
                  : isTargetActive
                  ? 'bg-slate-800/80 border-sky-500/50 shadow-md'
                  : 'bg-slate-950/50 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  {node.completed ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  ) : (
                    <Circle className="w-4 h-4 text-slate-500 shrink-0 group-hover:text-sky-400" />
                  )}
                  <span className={`text-xs font-bold ${node.completed ? 'text-emerald-200' : 'text-slate-200'}`}>
                    {node.title}
                  </span>
                </div>
                <ArrowUpRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-slate-300 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
              </div>

              <p className="text-[11px] text-slate-400 font-sans leading-relaxed">
                {node.objective}
              </p>

              <div className="flex items-center justify-between pt-1 border-t border-slate-800/60 text-[10px] font-mono">
                <span className="text-amber-400/90 flex items-center gap-1">
                  <Music className="w-3 h-3" />
                  <span>Melody #{node.melodyNote + 1}</span>
                </span>
                <span className="text-slate-400 uppercase">{node.completed ? 'RESTORED' : 'PENDING'}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
