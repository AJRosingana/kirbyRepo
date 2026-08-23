/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { OracleMessage, QuestNode } from '../types';
import { audioEngine } from '../utils/audio';
import { Sparkles, Send, Music, MessageSquare, Volume2, ShieldCheck } from 'lucide-react';

interface SoundStoneOracleProps {
  questNodes: QuestNode[];
  activePortalId: string;
  onSelectPortalById?: (portalId: string) => void;
}

export const SoundStoneOracle: React.FC<SoundStoneOracleProps> = ({
  questNodes,
  activePortalId,
  onSelectPortalById,
}) => {
  const [messages, setMessages] = useState<OracleMessage[]>([
    {
      id: 'init_1',
      sender: 'oracle',
      text: '...Greetings, traveler of the Macro Hall. I am the Sound Stone Oracle. The ancient melodies of our universe were shattered across dimensions.',
      timestamp: Date.now() - 4000,
    },
    {
      id: 'init_2',
      sender: 'oracle',
      text: 'Align the PSI frequencies, unlock archaic vector ciphers (0x9F4B), smelt the fire crystal, and harmonize the rings of Zeal to restore the Eight Melodies.',
      timestamp: Date.now() - 2000,
    },
  ]);

  const [inputVal, setInputVal] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeMelodyIndex, setActiveMelodyIndex] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const completedCount = questNodes.filter((q) => q.completed).length;
  const isFullMelodyUnlocked = completedCount >= 4;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputVal.trim() || isLoading) return;

    const userText = inputVal.trim();
    setInputVal('');

    const newMsg: OracleMessage = {
      id: 'msg_' + Date.now(),
      sender: 'traveler',
      text: userText,
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, newMsg]);
    setIsLoading(true);
    audioEngine.playTextBlip(4);

    try {
      const completedIds = questNodes.filter((q) => q.completed).map((q) => q.id);
      const res = await fetch('/api/oracle/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userText,
          history: messages.slice(-4).map((m) => ({ role: m.sender, text: m.text })),
          currentActivePortalId: activePortalId,
          completedQuests: completedIds,
        }),
      });

      const data = await res.json();
      const oracleReply: OracleMessage = {
        id: 'reply_' + Date.now(),
        sender: 'oracle',
        text: data.response || '...The sound stone hums silently.',
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, oracleReply]);

      // Retro speech sound effect
      for (let i = 0; i < Math.min(oracleReply.text.length, 12); i++) {
        setTimeout(() => audioEngine.playTextBlip(i % 3), i * 45);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: 'err_' + Date.now(),
          sender: 'oracle',
          text: '...The cosmic static is heavy. Seek the resonance within the portal walls.',
          timestamp: Date.now(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlaySoundStone = () => {
    audioEngine.playFullEightMelodies((noteIdx) => {
      setActiveMelodyIndex(noteIdx);
    });
    setTimeout(() => setActiveMelodyIndex(null), 2500);
  };

  const handlePlaySingleNote = (index: number) => {
    audioEngine.playMelodyNote(index);
    setActiveMelodyIndex(index);
    setTimeout(() => setActiveMelodyIndex(null), 600);
  };

  return (
    <div className="w-full rounded-2xl bg-slate-900/60 border border-slate-800/80 p-4 sm:p-5 backdrop-blur-xl shadow-2xl flex flex-col gap-4">
      {/* Sound Stone Header & 8 Melodies Visualizer */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-800/60">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h3 className="text-sm sm:text-base font-bold text-white flex items-center gap-2">
              The Sound Stone Oracle
              <span className="text-[11px] font-mono text-amber-400/90 font-normal">
                ({completedCount}/4 Melodies Gathered)
              </span>
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              Cosmic Resonance & Persona Guidance
            </p>
          </div>
        </div>

        {/* 8-Melodies Play Chorus Button */}
        <button
          onClick={handlePlaySoundStone}
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-amber-600 to-rose-600 hover:from-amber-500 hover:to-rose-500 text-white font-mono text-xs font-semibold shadow-lg shadow-amber-900/40 transition-all active:scale-95"
        >
          <Music className="w-3.5 h-3.5 animate-bounce" />
          <span>Synthesize 8 Melodies</span>
        </button>
      </div>

      {/* 8 Melody Sound Stone Prisms */}
      <div className="grid grid-cols-8 gap-1.5 sm:gap-2 bg-slate-950/70 p-2.5 rounded-xl border border-slate-800/80">
        {[0, 1, 2, 3, 4, 5, 6, 7].map((noteIdx) => {
          // Check if associated quest is completed
          const isCollected = isFullMelodyUnlocked || noteIdx < completedCount * 2;
          const isPlaying = activeMelodyIndex === noteIdx;

          return (
            <button
              key={noteIdx}
              onClick={() => handlePlaySingleNote(noteIdx)}
              className={`h-12 rounded-lg flex flex-col items-center justify-center transition-all duration-200 border ${
                isPlaying
                  ? 'bg-amber-400 text-slate-950 border-white scale-105 shadow-[0_0_16px_#f59e0b]'
                  : isCollected
                  ? 'bg-amber-950/40 border-amber-500/40 text-amber-300 hover:bg-amber-800/50'
                  : 'bg-slate-900/40 border-slate-800 text-slate-600 hover:border-slate-700'
              }`}
              title={`Melody Note ${noteIdx + 1}`}
            >
              <span className="text-[10px] font-mono font-bold">#{noteIdx + 1}</span>
              <div
                className={`w-1.5 h-1.5 rounded-full mt-1 ${
                  isCollected ? 'bg-amber-400 animate-ping' : 'bg-slate-700'
                }`}
              />
            </button>
          );
        })}
      </div>

      {/* Retro Oracle Dialogue Message Feed */}
      <div className="h-44 sm:h-52 overflow-y-auto pr-1 flex flex-col gap-2.5 font-sans text-xs scrollbar-thin scrollbar-thumb-slate-700">
        {messages.map((m) => {
          const isOracle = m.sender === 'oracle';
          return (
            <div
              key={m.id}
              className={`p-3 rounded-xl max-w-[88%] leading-relaxed ${
                isOracle
                  ? 'self-start bg-slate-950/90 border border-amber-500/30 text-amber-100 shadow-md'
                  : 'self-end bg-sky-950/80 border border-sky-500/30 text-sky-100'
              }`}
            >
              <div className="flex items-center gap-1.5 mb-1 font-mono text-[10px] opacity-70">
                {isOracle ? (
                  <>
                    <Sparkles className="w-3 h-3 text-amber-400" />
                    <span className="text-amber-300 font-semibold">SOUND STONE SAGE</span>
                  </>
                ) : (
                  <>
                    <MessageSquare className="w-3 h-3 text-sky-400" />
                    <span className="text-sky-300 font-semibold">TRAVELER</span>
                  </>
                )}
              </div>
              <p className="whitespace-pre-wrap">{m.text}</p>
            </div>
          );
        })}
        {isLoading && (
          <div className="self-start bg-slate-950/80 border border-amber-500/20 text-amber-300/70 p-2.5 rounded-xl font-mono text-[11px] flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping" />
            <span>The Sound Stone vibrates with forgotten lore...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Oracle Input Form */}
      <form onSubmit={handleSendMessage} className="flex items-center gap-2">
        <input
          type="text"
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          placeholder="Consult the Oracle on ciphers, lore, or memories..."
          className="flex-1 bg-slate-950/80 border border-slate-700/80 rounded-xl px-3.5 py-2 text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-amber-400 font-sans"
        />
        <button
          type="submit"
          disabled={isLoading || !inputVal.trim()}
          className="bg-amber-600 hover:bg-amber-500 disabled:opacity-40 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs flex items-center gap-1.5 transition-colors font-mono"
        >
          <span>SPEAK</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
};
