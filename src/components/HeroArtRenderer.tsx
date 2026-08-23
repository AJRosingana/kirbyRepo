/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useRef, useState } from 'react';
import { ATBHero } from '../types';

interface HeroArtRendererProps {
  hero: ATBHero;
  size?: number;
  showMeshToggle?: boolean;
  isAttacking?: boolean;
  isAutocasting?: boolean;
  isDamaged?: boolean;
  className?: string;
}

export const HeroArtRenderer: React.FC<HeroArtRendererProps> = ({
  hero,
  size = 96,
  showMeshToggle = false,
  isAttacking = false,
  isAutocasting = false,
  isDamaged = false,
  className = '',
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [renderMode, setRenderMode] = useState<'sprite' | 'mesh3d' | 'equations'>(
    hero.spriteStyle === 'mesh_3d_wire' ? 'mesh3d' : 'sprite'
  );
  const animationFrameRef = useRef<number | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let time = 0;

    const render = () => {
      time += 0.05;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const w = canvas.width;
      const h = canvas.height;
      const cx = w / 2;
      const cy = h / 2;

      // Glow or shake on autocast/damage
      if (isAutocasting) {
        ctx.save();
        const radGlow = ctx.createRadialGradient(cx, cy, 5, cx, cy, w * 0.48);
        radGlow.addColorStop(0, hero.color + '88');
        radGlow.addColorStop(0.6, '#fbbf2444');
        radGlow.addColorStop(1, 'transparent');
        ctx.fillStyle = radGlow;
        ctx.beginPath();
        ctx.arc(cx, cy, w * 0.48, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }

      ctx.save();
      if (isDamaged) {
        ctx.translate((Math.random() - 0.5) * 6, (Math.random() - 0.5) * 6);
      }
      if (isAttacking) {
        const attackLunge = Math.sin(time * 8) * 8;
        ctx.translate(hero.team === 'player' || hero.team === 'ally_multiplayer' ? attackLunge : -attackLunge, 0);
      }

      // Render based on character class and selected mode
      if (renderMode === 'mesh3d' || hero.characterClass === 'cyber_tesseract') {
        render3DMesh(ctx, hero, time, cx, cy, size * 0.4);
      } else if (renderMode === 'equations') {
        renderEquationOverlay(ctx, hero, time, w, h);
      } else {
        // Standard Character Sprites
        switch (hero.characterClass) {
          case 'majin_kirby':
            renderMajinKirbyBoo(ctx, time, cx, cy, size * 0.42, isAutocasting);
            break;
          case 'aether_knight':
            renderAetherKnightSprite(ctx, time, cx, cy, size * 0.42, isAutocasting);
            break;
          case 'adventurer':
            renderAdventurerSprite(ctx, time, cx, cy, size * 0.42, isAutocasting);
            break;
          case 'kirb_builder':
            renderKirbBuilderSprite(ctx, time, cx, cy, size * 0.42, isAutocasting);
            break;
          case 'pharaoh_scarab':
            renderPharaohColossus(ctx, time, cx, cy, size * 0.42, isAutocasting);
            break;
          default:
            renderGenericHero(ctx, hero, time, cx, cy, size * 0.4);
        }
      }

      ctx.restore();

      animationFrameRef.current = requestAnimationFrame(render);
    };

    animationFrameRef.current = requestAnimationFrame(render);

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [hero, renderMode, isAttacking, isAutocasting, isDamaged, size]);

  return (
    <div className={`relative inline-flex flex-col items-center select-none ${className}`}>
      <canvas
        ref={canvasRef}
        width={size}
        height={size}
        className="drop-shadow-md"
      />
      {showMeshToggle && (
        <div className="flex gap-1 mt-1 text-[10px]">
          <button
            onClick={(e) => {
              e.stopPropagation();
              setRenderMode('sprite');
            }}
            className={`px-1.5 py-0.5 rounded border transition-colors ${
              renderMode === 'sprite' ? 'bg-cyan-500/20 text-cyan-300 border-cyan-400' : 'bg-slate-800 text-slate-400 border-slate-700'
            }`}
          >
            Sprite
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              setRenderMode('mesh3d');
            }}
            className={`px-1.5 py-0.5 rounded border transition-colors ${
              renderMode === 'mesh3d' ? 'bg-pink-500/20 text-pink-300 border-pink-400' : 'bg-slate-800 text-slate-400 border-slate-700'
            }`}
          >
            3D Mesh
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              setRenderMode('equations');
            }}
            className={`px-1.5 py-0.5 rounded border transition-colors ${
              renderMode === 'equations' ? 'bg-amber-500/20 text-amber-300 border-amber-400' : 'bg-slate-800 text-slate-400 border-slate-700'
            }`}
          >
            Math VFX
          </button>
        </div>
      )}
    </div>
  );
};

// 1. Majin Kirby Boo Renderer (From Image 1: Pink genie body, M-belt, fluffy pants, tentacle curl, tongue out)
function renderMajinKirbyBoo(
  ctx: CanvasRenderingContext2D,
  time: number,
  cx: number,
  cy: number,
  r: number,
  isAutocasting: boolean
) {
  const bob = Math.sin(time * 3) * 3;
  const y = cy + bob;

  // Head Tentacle / Antenna (Curling back like Majin Buu)
  ctx.save();
  ctx.fillStyle = '#f472b6';
  ctx.strokeStyle = '#db2777';
  ctx.lineWidth = 2.5;

  ctx.beginPath();
  ctx.moveTo(cx - 3, y - r * 0.8);
  const curlX = cx + Math.sin(time * 2) * 6 + 18;
  const curlY = y - r * 1.6 + Math.cos(time * 2) * 4;
  ctx.quadraticCurveTo(cx + 8, y - r * 1.5, curlX, curlY);
  ctx.quadraticCurveTo(cx + 15, y - r * 0.7, cx + 5, y - r * 0.8);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // Tentacle Tip Bulb
  ctx.beginPath();
  ctx.arc(curlX, curlY, 5, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Genie Puffy White Pants
  ctx.fillStyle = '#f8fafc';
  ctx.strokeStyle = '#cbd5e1';
  ctx.beginPath();
  ctx.ellipse(cx, y + r * 0.65, r * 0.75, r * 0.45, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Little Black/Brown Boots
  ctx.fillStyle = '#1e293b';
  ctx.beginPath();
  ctx.ellipse(cx - r * 0.4, y + r * 1.0, 6, 4, 0, 0, Math.PI * 2);
  ctx.ellipse(cx + r * 0.4, y + r * 1.0, 6, 4, 0, 0, Math.PI * 2);
  ctx.fill();

  // Gold Belt with 'M' (Majin / Mario emblem)
  ctx.fillStyle = '#fbbf24';
  ctx.strokeStyle = '#b45309';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.ellipse(cx, y + r * 0.35, r * 0.55, 6, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // 'M' Symbol on gold buckle
  ctx.fillStyle = '#7f1d1d';
  ctx.font = 'bold 9px monospace';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('M', cx, y + r * 0.36);

  // Pink Round Body / Head (Kirby / Boo form)
  ctx.fillStyle = '#f472b6';
  ctx.strokeStyle = '#be185d';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.arc(cx, y - r * 0.1, r * 0.75, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Pink Nubby Arms
  ctx.beginPath();
  ctx.ellipse(cx - r * 0.75, y + Math.sin(time * 4) * 4, 8, 7, -0.4, 0, Math.PI * 2);
  ctx.ellipse(cx + r * 0.75, y - Math.sin(time * 4) * 4, 8, 7, 0.4, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Cute Eyes (Closed happy arches or big oval pupils)
  ctx.fillStyle = '#0f172a';
  ctx.beginPath();
  ctx.ellipse(cx - r * 0.28, y - r * 0.2, 3.5, 6, 0, 0, Math.PI * 2);
  ctx.ellipse(cx + r * 0.28, y - r * 0.2, 3.5, 6, 0, 0, Math.PI * 2);
  ctx.fill();

  // Eye Gleam
  ctx.fillStyle = '#ffffff';
  ctx.beginPath();
  ctx.arc(cx - r * 0.28, y - r * 0.25, 1.5, 0, Math.PI * 2);
  ctx.arc(cx + r * 0.28, y - r * 0.25, 1.5, 0, Math.PI * 2);
  ctx.fill();

  // Rosy Blushing Cheeks
  ctx.fillStyle = '#fda4af';
  ctx.beginPath();
  ctx.arc(cx - r * 0.45, y - r * 0.05, 5, 0, Math.PI * 2);
  ctx.arc(cx + r * 0.45, y - r * 0.05, 5, 0, Math.PI * 2);
  ctx.fill();

  // Cheeky Tongue Sticking Out (From image 1 panel)
  ctx.fillStyle = '#be123c';
  ctx.beginPath();
  ctx.arc(cx, y + 2, 4, 0, Math.PI);
  ctx.fill();
  ctx.fillStyle = '#fb7185';
  ctx.beginPath();
  ctx.arc(cx + 1, y + 5, 3.5, 0, Math.PI);
  ctx.fill();

  // Floating Candy Stars on Autocast
  if (isAutocasting) {
    ctx.fillStyle = '#fef08a';
    for (let i = 0; i < 4; i++) {
      const starAngle = time * 3 + (i * Math.PI) / 2;
      const sx = cx + Math.cos(starAngle) * (r * 1.2);
      const sy = y + Math.sin(starAngle) * (r * 1.2);
      ctx.beginPath();
      ctx.arc(sx, sy, 3.5, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  ctx.restore();
}

// 2. Aether Knight Sprite Renderer (Image 2: Pixel paladin with glowing cyan energy sword)
function renderAetherKnightSprite(
  ctx: CanvasRenderingContext2D,
  time: number,
  cx: number,
  cy: number,
  r: number,
  isAutocasting: boolean
) {
  const bob = Math.sin(time * 4) * 2;
  const y = cy + bob;

  ctx.save();
  // Flowing Blue Cape behind
  ctx.fillStyle = '#1e3a8a';
  ctx.beginPath();
  ctx.moveTo(cx - 10, y - r * 0.4);
  ctx.lineTo(cx - 18 + Math.sin(time * 3) * 6, y + r * 0.8);
  ctx.lineTo(cx + 18 + Math.cos(time * 3) * 6, y + r * 0.8);
  ctx.lineTo(cx + 10, y - r * 0.4);
  ctx.closePath();
  ctx.fill();

  // Silver/Blue Plated Armor Chest
  ctx.fillStyle = '#38bdf8';
  ctx.strokeStyle = '#0284c7';
  ctx.lineWidth = 2;
  ctx.fillRect(cx - 10, y - r * 0.2, 20, 18);
  ctx.strokeRect(cx - 10, y - r * 0.2, 20, 18);

  // Helmet / Visor
  ctx.fillStyle = '#e0f2fe';
  ctx.beginPath();
  ctx.arc(cx, y - r * 0.55, 12, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Glowing Visor Line
  ctx.fillStyle = '#06b6d4';
  ctx.fillRect(cx - 8, y - r * 0.58, 16, 4);

  // Glowing Aether Energy Blade
  const bladeAngle = Math.PI / 4 + Math.sin(time * 5) * 0.2;
  ctx.save();
  ctx.translate(cx + 12, y + 2);
  ctx.rotate(bladeAngle);

  // Sword Hilt
  ctx.fillStyle = '#d97706';
  ctx.fillRect(-3, -2, 6, 4);

  // Cyan Laser Blade with Alpha Glow
  ctx.shadowColor = '#06b6d4';
  ctx.shadowBlur = isAutocasting ? 16 : 8;
  ctx.fillStyle = '#67e8f9';
  ctx.fillRect(-2, -28, 4, 26);
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(-1, -26, 2, 22);
  ctx.restore();

  ctx.restore();
}

// 3. Adventurer Sprite (Image 3: 32x32 Runner with fire physics)
function renderAdventurerSprite(
  ctx: CanvasRenderingContext2D,
  time: number,
  cx: number,
  cy: number,
  r: number,
  isAutocasting: boolean
) {
  const bob = Math.sin(time * 6) * 3;
  const y = cy + bob;

  ctx.save();
  // Brown hair & red headband
  ctx.fillStyle = '#78350f';
  ctx.fillRect(cx - 8, y - r * 0.8, 16, 12);
  ctx.fillStyle = '#ef4444';
  ctx.fillRect(cx - 9, y - r * 0.7, 18, 3);

  // Adventurer Face
  ctx.fillStyle = '#fde68a';
  ctx.fillRect(cx - 7, y - r * 0.55, 14, 10);
  ctx.fillStyle = '#0f172a';
  ctx.fillRect(cx - 4, y - r * 0.5, 2, 3);
  ctx.fillRect(cx + 2, y - r * 0.5, 2, 3);

  // Blue Tunic
  ctx.fillStyle = '#2563eb';
  ctx.fillRect(cx - 9, y - r * 0.25, 18, 16);

  // Leather Belt & Dagger
  ctx.fillStyle = '#b45309';
  ctx.fillRect(cx - 9, y - r * 0.05, 18, 4);

  // Boots
  ctx.fillStyle = '#451a03';
  ctx.fillRect(cx - 8, y + r * 0.35, 6, 8);
  ctx.fillRect(cx + 2, y + r * 0.35, 6, 8);

  // Flame trail particles
  if (isAutocasting) {
    ctx.fillStyle = '#f97316';
    for (let i = 0; i < 5; i++) {
      const px = cx - 15 - Math.random() * 10;
      const py = y + (Math.random() - 0.5) * 20;
      ctx.beginPath();
      ctx.arc(px, py, 2 + Math.random() * 3, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  ctx.restore();
}

// 4. Kirby Builder Foreman
function renderKirbBuilderSprite(
  ctx: CanvasRenderingContext2D,
  time: number,
  cx: number,
  cy: number,
  r: number,
  _isAutocasting: boolean
) {
  const bob = Math.sin(time * 3) * 2;
  const y = cy + bob;

  ctx.save();
  // Round Pink Body
  ctx.fillStyle = '#f472b6';
  ctx.strokeStyle = '#be185d';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.arc(cx, y, r * 0.7, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Yellow Construction Hardhat
  ctx.fillStyle = '#fbbf24';
  ctx.strokeStyle = '#d97706';
  ctx.beginPath();
  ctx.arc(cx, y - r * 0.45, r * 0.7, Math.PI, 0);
  ctx.fill();
  ctx.stroke();
  ctx.fillRect(cx - r * 0.8, y - r * 0.45, r * 1.6, 5);

  // Eyes & Blush
  ctx.fillStyle = '#0f172a';
  ctx.beginPath();
  ctx.arc(cx - 6, y - 2, 2.5, 0, Math.PI * 2);
  ctx.arc(cx + 6, y - 2, 2.5, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#fda4af';
  ctx.beginPath();
  ctx.arc(cx - 10, y + 4, 4, 0, Math.PI * 2);
  ctx.arc(cx + 10, y + 4, 4, 0, Math.PI * 2);
  ctx.fill();

  // Builder Hammer in hand
  ctx.save();
  ctx.translate(cx + 16, y);
  ctx.rotate(Math.sin(time * 6) * 0.4);
  ctx.fillStyle = '#78350f';
  ctx.fillRect(-2, -4, 4, 18);
  ctx.fillStyle = '#94a3b8';
  ctx.fillRect(-7, -10, 14, 8);
  ctx.restore();

  ctx.restore();
}

// 5. Pharaoh Sentinel
function renderPharaohColossus(
  ctx: CanvasRenderingContext2D,
  time: number,
  cx: number,
  cy: number,
  r: number,
  _isAutocasting: boolean
) {
  const y = cy + Math.sin(time * 2) * 2;
  ctx.save();
  // Gold Monolith Headdress
  ctx.fillStyle = '#eab308';
  ctx.strokeStyle = '#a16207';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(cx, y - r * 0.9);
  ctx.lineTo(cx + r * 0.8, y + r * 0.6);
  ctx.lineTo(cx - r * 0.8, y + r * 0.6);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // Glowing Eye of Horus
  ctx.fillStyle = '#38bdf8';
  ctx.beginPath();
  ctx.arc(cx, y - r * 0.1, 7, 0, Math.PI * 2);
  ctx.fill();

  ctx.restore();
}

// 6. 3D Wireframe Mesh Renderer with real-time rotational transformation
function render3DMesh(
  ctx: CanvasRenderingContext2D,
  hero: ATBHero,
  time: number,
  cx: number,
  cy: number,
  radius: number
) {
  ctx.save();

  // 3D Cube / Polyhedron Vertices
  const rotX = time * 0.8;
  const rotY = time * 1.2;

  const vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
  ];

  const edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
  ];

  // Rotate & Project
  const projected = vertices.map(([x, y, z]) => {
    // Rot Y
    let x1 = x * Math.cos(rotY) - z * Math.sin(rotY);
    let z1 = x * Math.sin(rotY) + z * Math.cos(rotY);
    // Rot X
    let y1 = y * Math.cos(rotX) - z1 * Math.sin(rotX);
    let z2 = y * Math.sin(rotX) + z1 * Math.cos(rotX);

    const fov = 3.5;
    const pz = fov / (fov + z2);
    return {
      x: cx + x1 * radius * pz,
      y: cy + y1 * radius * pz,
      z: z2,
    };
  });

  // Draw wireframe edges
  ctx.strokeStyle = hero.color || '#38bdf8';
  ctx.lineWidth = 2;
  edges.forEach(([i, j]) => {
    const p1 = projected[i];
    const p2 = projected[j];
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();
  });

  // Draw Vertex Points
  ctx.fillStyle = '#ffffff';
  projected.forEach((p) => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
    ctx.fill();
  });

  // Subtitle formula
  ctx.fillStyle = '#94a3b8';
  ctx.font = '8px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('V_mesh = R·T·V_base', cx, cy + radius + 14);

  ctx.restore();
}

// 7. Equation VFX Overlay (Mathematical Shader Visualizer)
function renderEquationOverlay(
  ctx: CanvasRenderingContext2D,
  hero: ATBHero,
  _time: number,
  w: number,
  h: number
) {
  ctx.save();
  ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
  ctx.fillRect(0, 0, w, h);

  ctx.fillStyle = hero.color || '#38bdf8';
  ctx.font = 'bold 9px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('VFX MATH SHADER', w / 2, 16);

  ctx.fillStyle = '#e2e8f0';
  ctx.font = '8px monospace';
  const eq = hero.skills.charge3Autocast.equationSnippet || 'P(t) = P0 + v0·t + 1/2·a·t²';
  const parts = eq.split('|');
  parts.forEach((line, i) => {
    ctx.fillText(line.trim(), w / 2, 34 + i * 14);
  });

  ctx.restore();
}

function renderGenericHero(
  ctx: CanvasRenderingContext2D,
  hero: ATBHero,
  _time: number,
  cx: number,
  cy: number,
  r: number
) {
  ctx.save();
  ctx.fillStyle = hero.color;
  ctx.beginPath();
  ctx.arc(cx, cy, r * 0.75, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#ffffff';
  ctx.font = `${Math.round(r * 0.8)}px sans-serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(hero.avatar, cx, cy);
  ctx.restore();
}
