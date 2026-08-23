/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useCallback } from 'react';
import { PortalSurface, QuestNode, EpochEra } from './types';
import { INITIAL_PORTALS, INITIAL_QUEST_NODES } from './data/portalPresets';
import { Navbar } from './components/Navbar';
import { ChamberViewport } from './components/ChamberViewport';
import { SoundStoneOracle } from './components/SoundStoneOracle';
import { QuestTracker } from './components/QuestTracker';
import { EpochControls } from './components/EpochControls';
import { PromptStudioModal } from './components/PromptStudioModal';
import { audioEngine } from './utils/audio';

export default function App() {
  const [portals, setPortals] = useState<PortalSurface[]>(() => {
    const saved = localStorage.getItem('macro_portals');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return INITIAL_PORTALS;
      }
    }
    return INITIAL_PORTALS;
  });

  const [activePortal, setActivePortal] = useState<PortalSurface>(portals[0]);
  const [epoch, setEpoch] = useState<EpochEra>('16bit');
  const [questNodes, setQuestNodes] = useState<QuestNode[]>(() => {
    const saved = localStorage.getItem('macro_quests');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return INITIAL_QUEST_NODES;
      }
    }
    return INITIAL_QUEST_NODES;
  });

  const [isPromptStudioOpen, setIsPromptStudioOpen] = useState(false);
  const [isMuted, setIsMuted] = useState(false);

  // Initialize audio engine on first click
  useEffect(() => {
    const handleFirstClick = () => {
      audioEngine.init();
      audioEngine.setPortalHum(activePortal.ambientFrequency);
      window.removeEventListener('click', handleFirstClick);
    };
    window.addEventListener('click', handleFirstClick);
    return () => window.removeEventListener('click', handleFirstClick);
  }, [activePortal]);

  // Update dynamic portal audio hum whenever active portal changes
  useEffect(() => {
    audioEngine.setPortalHum(activePortal.ambientFrequency);
  }, [activePortal]);

  // Save portals to local storage
  useEffect(() => {
    localStorage.setItem('macro_portals', JSON.stringify(portals));
  }, [portals]);

  // Save quests to local storage
  useEffect(() => {
    localStorage.setItem('macro_quests', JSON.stringify(questNodes));
  }, [questNodes]);

  const handleSelectPortal = (portal: PortalSurface) => {
    setActivePortal(portal);
  };

  const handleSelectPortalById = (portalId: string) => {
    const target = portals.find((p) => p.id === portalId);
    if (target) {
      setActivePortal(target);
    }
  };

  const handleQuestProgress = useCallback((nodeId: string, value?: any) => {
    setQuestNodes((prev) =>
      prev.map((q) => {
        if (q.id === nodeId) {
          return { ...q, completed: true };
        }
        return q;
      })
    );
  }, []);

  const handleResetQuests = () => {
    setQuestNodes(INITIAL_QUEST_NODES);
    localStorage.removeItem('macro_quests');
    audioEngine.playTextBlip(-6);
  };

  const handlePortalCreated = (newPortal: PortalSurface) => {
    setPortals((prev) => [newPortal, ...prev]);
    setActivePortal(newPortal);
  };

  const completedQuestIds = questNodes.filter((q) => q.completed).map((q) => q.id);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-sky-500 selection:text-white flex flex-col">
      {/* Navigation Header */}
      <Navbar
        onOpenPromptStudio={() => setIsPromptStudioOpen(true)}
        isMuted={isMuted}
        onToggleMute={() => {
          const muted = audioEngine.toggleMute();
          setIsMuted(muted);
        }}
        onResetQuests={handleResetQuests}
      />

      {/* Main Chamber Stage */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-6 flex flex-col gap-6">
        {/* Top Section: 3D Chamber Viewport & Live Canvas Wall */}
        <ChamberViewport
          portals={portals}
          activePortal={activePortal}
          epoch={epoch}
          onSelectPortal={handleSelectPortal}
          onQuestProgress={handleQuestProgress}
          completedQuestIds={completedQuestIds}
          onDeployWorld={handlePortalCreated}
        />

        {/* Lower Grid: Epoch Shifter, Quest Chain & The Sound Stone Oracle */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Epoch Shifter & Quest Chain */}
          <div className="lg:col-span-2 flex flex-col gap-6">
            <EpochControls
              currentEpoch={epoch}
              onChangeEpoch={setEpoch}
              isMuted={isMuted}
              onToggleMute={() => {
                const muted = audioEngine.toggleMute();
                setIsMuted(muted);
              }}
              currentFrequency={activePortal.ambientFrequency}
            />

            <QuestTracker
              questNodes={questNodes}
              onSelectPortalById={handleSelectPortalById}
              activePortalId={activePortal.id}
            />
          </div>

          {/* Right Column: The Sound Stone Oracle */}
          <div className="lg:col-span-1 flex flex-col">
            <SoundStoneOracle
              questNodes={questNodes}
              activePortalId={activePortal.id}
              onSelectPortalById={handleSelectPortalById}
            />
          </div>
        </div>
      </main>

      {/* AI Studio Generative Prompt & Tool Modal */}
      <PromptStudioModal
        isOpen={isPromptStudioOpen}
        onClose={() => setIsPromptStudioOpen(false)}
        onPortalCreated={handlePortalCreated}
      />

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-4 px-6 text-center text-xs font-mono text-slate-500">
        Google AI Studio Intro Architecture • Multimodal Portal Engine & Procedural Sound Stone
      </footer>
    </div>
  );
}
