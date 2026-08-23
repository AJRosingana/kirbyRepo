/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useRef, useState } from 'react';
import { SporeCreature, SporeMushroom } from '../types';
import { audioEngine } from '../utils/audio';
import { Plus, Sparkles, Sprout, Wind, Play } from 'lucide-react';

interface SporeNetworkSimProps {
  isActive: boolean;
  onQuestComplete?: () => void;
}

export const SporeNetworkSim: React.FC<SporeNetworkSimProps> = ({ isActive, onQuestComplete }) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [sporeEnergy, setSporeEnergy] = useState(120);
  const [workerCount, setWorkerCount] = useState(4);
  const [mushroomsCount, setMushroomsCount] = useState(3);

  const mushroomsRef = useRef<SporeMushroom[]>([
    { id: 'm1', x: 160, y: 180, radius: 26, color: '#a855f7', glowPhase: 0, sporesGenerated: 0 },
    { id: 'm2', x: 520, y: 150, radius: 32, color: '#38bdf8', glowPhase: 2, sporesGenerated: 0 },
    { id: 'm3', x: 360, y: 340, radius: 38, color: '#ec4899', glowPhase: 4, sporesGenerated: 0 },
  ]);

  const creaturesRef = useRef<SporeCreature[]>([
    { id: 1, x: 160, y: 180, targetX: 520, targetY: 150, speed: 1.8, color: '#c084fc', energy: 10, carryingSpore: true },
    { id: 2, x: 520, y: 150, targetX: 360, targetY: 340, speed: 1.5, color: '#7dd3fc', energy: 10, carryingSpore: false },
    { id: 3, x: 360, y: 340, targetX: 160, targetY: 180, speed: 2.0, color: '#f472b6', energy: 10, carryingSpore: true },
    { id: 4, x: 300, y: 220, targetX: 520, targetY: 150, speed: 1.6, color: '#34d399', energy: 10, carryingSpore: false },
  ]);

  // Click on canvas to plant mushroom or harvest
  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = (e.clientX - rect.left) * (e.currentTarget.width / rect.width);
    const clickY = (e.clientY - rect.top) * (e.currentTarget.height / rect.height);

    // Check if clicked an existing mushroom
    const clickedMushroom = mushroomsRef.current.find((m) => {
      const dist = Math.hypot(m.x - clickX, m.y - clickY);
      return dist <= m.radius + 15;
    });

    if (clickedMushroom) {
      // Release spores
      clickedMushroom.glowPhase += 2;
      setSporeEnergy((prev) => prev + 25);
      audioEngine.playSporeChime(500 + Math.random() * 400);
      return;
    }

    // Otherwise plant a new mushroom if energy permits
    if (sporeEnergy >= 30) {
      setSporeEnergy((prev) => prev - 30);
      const colors = ['#a855f7', '#38bdf8', '#ec4899', '#34d399', '#facc15'];
      const newMushroom: SporeMushroom = {
        id: 'm_' + Date.now(),
        x: clickX,
        y: clickY,
        radius: 20 + Math.random() * 14,
        color: colors[mushroomsRef.current.length % colors.length],
        glowPhase: Math.random() * Math.PI,
        sporesGenerated: 0,
      };
      mushroomsRef.current.push(newMushroom);
      setMushroomsCount(mushroomsRef.current.length);
      audioEngine.playMelodyNote(mushroomsRef.current.length);

      if (mushroomsRef.current.length >= 6 && onQuestComplete) {
        onQuestComplete();
      }
    } else {
      audioEngine.playTextBlip(-4);
    }
  };

  const handleSpawnWorker = () => {
    if (sporeEnergy >= 40) {
      setSporeEnergy((prev) => prev - 40);
      const m1 = mushroomsRef.current[Math.floor(Math.random() * mushroomsRef.current.length)];
      const m2 = mushroomsRef.current[Math.floor(Math.random() * mushroomsRef.current.length)];
      const newWorker: SporeCreature = {
        id: Date.now(),
        x: m1.x,
        y: m1.y,
        targetX: m2.x,
        targetY: m2.y,
        speed: 1.4 + Math.random() * 1.2,
        color: m1.color,
        energy: 10,
        carryingSpore: true,
      };
      creaturesRef.current.push(newWorker);
      setWorkerCount(creaturesRef.current.length);
      audioEngine.playSporeChime(700);
    }
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId: number;
    let lastEnergyTick = performance.now();

    const loop = (now: number) => {
      const w = canvas.width;
      const h = canvas.height;
      const t = now * 0.001;

      // Dark bioluminescent forest floor
      ctx.fillStyle = '#030712';
      ctx.fillRect(0, 0, w, h);

      // Draw glowing mycelium bridges connecting all mushrooms
      const mushrooms = mushroomsRef.current;
      for (let i = 0; i < mushrooms.length; i++) {
        for (let j = i + 1; j < mushrooms.length; j++) {
          const m1 = mushrooms[i];
          const m2 = mushrooms[j];
          const dist = Math.hypot(m1.x - m2.x, m1.y - m2.y);

          ctx.beginPath();
          ctx.moveTo(m1.x, m1.y);
          // Organic curved vine bridge
          const midX = (m1.x + m2.x) / 2 + Math.sin(t + i + j) * 15;
          const midY = (m1.y + m2.y) / 2 + Math.cos(t + i + j) * 15;
          ctx.quadraticCurveTo(midX, midY, m2.x, m2.y);

          ctx.strokeStyle = 'rgba(168, 85, 247, 0.25)';
          ctx.lineWidth = 2;
          ctx.stroke();

          // Flowing pulse packet along bridge
          const pulseProgress = (t * 0.4 + (i + j) * 0.2) % 1;
          const px = (1 - pulseProgress) * m1.x + pulseProgress * m2.x;
          const py = (1 - pulseProgress) * m1.y + pulseProgress * m2.y;
          ctx.fillStyle = '#a855f7';
          ctx.beginPath();
          ctx.arc(px, py, 3, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // Update and Draw Mushrooms
      mushrooms.forEach((m, idx) => {
        const pulse = Math.sin(t * 2 + m.glowPhase) * 4;
        const currentRadius = m.radius + pulse;

        // Radiant glow halo
        const grad = ctx.createRadialGradient(m.x, m.y, 4, m.x, m.y, currentRadius * 2.2);
        grad.addColorStop(0, m.color);
        grad.addColorStop(0.6, 'rgba(168, 85, 247, 0.15)');
        grad.addColorStop(1, 'rgba(0, 0, 0, 0)');

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(m.x, m.y, currentRadius * 2.2, 0, Math.PI * 2);
        ctx.fill();

        // Mushroom Cap
        ctx.fillStyle = m.color;
        ctx.beginPath();
        ctx.arc(m.x, m.y, currentRadius, 0, Math.PI * 2);
        ctx.fill();

        // Stalk
        ctx.fillStyle = '#1e1b4b';
        ctx.fillRect(m.x - 4, m.y + currentRadius * 0.4, 8, 14);

        // Cap spots
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(m.x - 6, m.y - 6, 3, 0, Math.PI * 2);
        ctx.arc(m.x + 8, m.y + 2, 4, 0, Math.PI * 2);
        ctx.arc(m.x + 2, m.y - 10, 2.5, 0, Math.PI * 2);
        ctx.fill();
      });

      // Update and Draw Worker Creatures
      const creatures = creaturesRef.current;
      creatures.forEach((c) => {
        const dx = c.targetX - c.x;
        const dy = c.targetY - c.y;
        const dist = Math.hypot(dx, dy);

        if (dist < 8) {
          // Reached target mushroom - pick another target
          const targetMushroom = mushrooms[Math.floor(Math.random() * mushrooms.length)];
          c.targetX = targetMushroom.x;
          c.targetY = targetMushroom.y;
          c.carryingSpore = !c.carryingSpore;
          if (c.carryingSpore) {
            setSporeEnergy((prev) => prev + 2);
          }
        } else {
          c.x += (dx / dist) * c.speed;
          c.y += (dy / dist) * c.speed;
        }

        // Draw cute mini worker sprite with antenna
        ctx.fillStyle = c.color;
        ctx.beginPath();
        ctx.arc(c.x, c.y, 5, 0, Math.PI * 2);
        ctx.fill();

        // Spore cargo
        if (c.carryingSpore) {
          ctx.fillStyle = '#fde047';
          ctx.beginPath();
          ctx.arc(c.x, c.y - 7, 3, 0, Math.PI * 2);
          ctx.fill();
        }
      });

      // Passive energy accumulation
      if (now - lastEnergyTick > 1000) {
        setSporeEnergy((prev) => prev + mushrooms.length * 2);
        lastEnergyTick = now;
      }

      animId = requestAnimationFrame(loop);
    };

    animId = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(animId);
  }, []);

  return (
    <div className="relative w-full h-full">
      <canvas
        ref={canvasRef}
        width={720}
        height={480}
        onClick={handleCanvasClick}
        className="w-full h-full object-cover cursor-pointer"
      />

      {/* Spore HUD */}
      <div className="absolute top-4 left-4 flex items-center gap-3 bg-slate-950/85 backdrop-blur-md border border-purple-500/30 rounded-lg p-2.5 text-xs font-mono text-purple-200 shadow-xl">
        <div className="flex items-center gap-1.5 text-amber-300 font-bold">
          <Sparkles className="w-4 h-4 text-amber-400 animate-spin" />
          <span>{sporeEnergy} SPORES</span>
        </div>
        <div className="h-4 w-px bg-slate-700" />
        <div className="flex items-center gap-1 text-purple-300">
          <Sprout className="w-3.5 h-3.5" />
          <span>{mushroomsCount} Mushrooms</span>
        </div>
        <div className="h-4 w-px bg-slate-700" />
        <div className="flex items-center gap-1 text-sky-300">
          <Wind className="w-3.5 h-3.5" />
          <span>{workerCount} Workers</span>
        </div>
      </div>

      {/* Control Buttons */}
      <div className="absolute bottom-4 right-4 flex items-center gap-2">
        <button
          onClick={handleSpawnWorker}
          disabled={sporeEnergy < 40}
          className="bg-purple-900/80 hover:bg-purple-700 disabled:opacity-40 text-purple-200 border border-purple-500/40 rounded-lg px-3 py-1.5 text-xs font-mono flex items-center gap-1.5 transition-colors shadow-lg"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Spawn Worker (40)</span>
        </button>
      </div>

      <div className="absolute bottom-4 left-4 bg-slate-950/70 backdrop-blur-md rounded px-2.5 py-1 text-[10px] font-mono text-slate-400">
        💡 Click empty soil to plant mushroom (30) • Click mushroom to harvest chime
      </div>
    </div>
  );
};
