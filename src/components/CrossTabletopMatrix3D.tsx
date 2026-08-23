/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  ATBHero,
  CustomBattlefield,
  CrossTableProjectile,
  CrossTableLeap,
  VFXParticle,
  TabletopLayer,
  MultiplayerRoomState,
} from '../types';
import { INITIAL_HERO_ROSTER, RAID_BOSSES } from '../data/heroes';
import { audioEngine } from '../utils/audio';
import { multiplayerEngine } from '../utils/multiplayerEngine';
import {
  Layers,
  Rotate3d,
  Sparkles,
  Zap,
  Swords,
  Crosshair,
  ArrowUpRight,
  Shield,
  RefreshCw,
  Flame,
  Volume2,
  VolumeX,
  Play,
  Pause,
  Maximize2,
  Sliders,
  Send,
  Eye,
  Hammer,
} from 'lucide-react';
import confetti from 'canvas-confetti';

interface CrossTabletopMatrix3DProps {
  onOpenBuilder?: () => void;
  onExit?: () => void;
}

export const CrossTabletopMatrix3D: React.FC<CrossTabletopMatrix3DProps> = ({
  onOpenBuilder,
  onExit,
}) => {
  // 3D Camera & Matrix Layout
  const [cameraPitch, setCameraPitch] = useState<number>(28); // Angle in degrees
  const [cameraYaw, setCameraYaw] = useState<number>(-15); // Orbit yaw
  const [tableSpacingZ, setTableSpacingZ] = useState<number>(260); // Gap between tables along Z
  const [tableElevationY, setTableElevationY] = useState<number>(75); // Height difference between tables
  const [zoom, setZoom] = useState<number>(0.9);
  const [isAutoRotate, setIsAutoRotate] = useState<boolean>(false);
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const dragStartRef = useRef<{ x: number; y: number; yaw: number; pitch: number }>({
    x: 0,
    y: 0,
    yaw: 0,
    pitch: 0,
  });

  // Tabletop Layers (Table 0: Foreground, Table 1: Midground, Table 2: Background)
  const [tables, setTables] = useState<TabletopLayer[]>([
    {
      id: 'table_0_foreground',
      tableIndex: 0,
      name: 'Table 0: Frontline Toy Box',
      theme: 'Kirby Stepped Arena & Chutes',
      accentColor: '#f472b6',
      depthZ: 0,
      elevationY: 0,
      hazardState: 'calm',
      forcefieldActive: false,
      battlefield: {
        id: 'field_0',
        name: 'Toy Box Frontline',
        theme: 'Candy & Chutes',
        gridSize: 6,
        accentColor: '#f472b6',
        tiles: [
          { x: 1, y: 1, tier: 1, type: 'candy_bush', color: '#fb7185' },
          { x: 2, y: 2, tier: 2, type: 'star_block', color: '#facc15' },
          { x: 4, y: 1, tier: 1, type: 'chute', color: '#38bdf8' },
          { x: 3, y: 4, tier: 1, type: 'hazard_spore', color: '#a855f7' },
        ],
        chutes: [{ topX: 4, topY: 1, botX: 1, botY: 4 }],
        ladders: [{ startX: 2, startY: 2, endX: 3, endY: 3 }],
        creator: 'Foreman Kirby',
        createdAt: Date.now(),
      },
      units: [
        { ...INITIAL_HERO_ROSTER[0], x: 1, y: 1, tier: 0 }, // Majin Kirby
        { ...INITIAL_HERO_ROSTER[3], x: 4, y: 2, tier: 1 }, // Foreman Kirby
      ],
    },
    {
      id: 'table_1_midground',
      tableIndex: 1,
      name: 'Table 1: Aether Citadel',
      theme: 'Floating Mesh Citadel & Lasers',
      accentColor: '#38bdf8',
      depthZ: 260,
      elevationY: 75,
      hazardState: 'charged',
      forcefieldActive: false,
      battlefield: {
        id: 'field_1',
        name: 'Aether Floating Citadel',
        theme: 'Subdivision Mesh Platforms',
        gridSize: 6,
        accentColor: '#38bdf8',
        tiles: [
          { x: 2, y: 2, tier: 2, type: 'mesh_spire', color: '#38bdf8' },
          { x: 1, y: 4, tier: 1, type: 'laser_relay', color: '#818cf8' },
          { x: 4, y: 3, tier: 1, type: 'warp_pad', color: '#06b6d4' },
        ],
        chutes: [{ topX: 4, topY: 3, botX: 2, botY: 5 }],
        ladders: [{ startX: 1, startY: 1, endX: 2, endY: 2 }],
        creator: 'Aether Scribe',
        createdAt: Date.now(),
      },
      units: [
        { ...INITIAL_HERO_ROSTER[1], x: 2, y: 2, tier: 2 }, // Aether Knight
        { ...INITIAL_HERO_ROSTER[2], x: 3, y: 1, tier: 1 }, // Bézier Adventurer
      ],
    },
    {
      id: 'table_2_background',
      tableIndex: 2,
      name: 'Table 2: Void Colossus Core',
      theme: 'Hyper-Vector Pharaoh Altar',
      accentColor: '#f59e0b',
      depthZ: 520,
      elevationY: 150,
      hazardState: 'erupting',
      forcefieldActive: true,
      battlefield: {
        id: 'field_2',
        name: 'Pharaoh Sun Altar',
        theme: 'Solar Colossus Sanctum',
        gridSize: 6,
        accentColor: '#f59e0b',
        tiles: [
          { x: 2, y: 2, tier: 2, type: 'solar_obelisk', color: '#f59e0b' },
          { x: 3, y: 2, tier: 2, type: 'solar_obelisk', color: '#f59e0b' },
          { x: 1, y: 1, tier: 1, type: 'pyramid_step', color: '#eab308' },
          { x: 4, y: 4, tier: 1, type: 'pyramid_step', color: '#eab308' },
        ],
        chutes: [{ topX: 2, topY: 2, botX: 4, botY: 4 }],
        ladders: [{ startX: 1, startY: 1, endX: 2, endY: 2 }],
        creator: 'Pharaoh Architect',
        createdAt: Date.now(),
      },
      units: [
        { ...RAID_BOSSES[0], x: 2, y: 2, tier: 2 }, // Hyper-Vector Tesseract Boss
        { ...RAID_BOSSES[1], x: 3, y: 3, tier: 2 }, // Pharaoh Colossus
      ],
    },
  ]);

  // Cross-Boundary Active Interactions
  const [projectiles, setProjectiles] = useState<CrossTableProjectile[]>([]);
  const [leaps, setLeaps] = useState<CrossTableLeap[]>([]);
  const [particles, setParticles] = useState<VFXParticle[]>([]);
  const [crossTableLogs, setCrossTableLogs] = useState<
    { id: string; time: string; text: string; type: 'mortar' | 'leap' | 'overdrive' | 'chute' }[]
  >([
    {
      id: 'log_init',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
      text: '3D Cross-Table Matrix initialized. 3 tabletop worlds linked across dimensional boundaries.',
      type: 'overdrive',
    },
  ]);

  // Selected Unit & Targeting
  const [selectedUnit, setSelectedUnit] = useState<{ tableIndex: number; heroId: string } | null>({
    tableIndex: 0,
    heroId: INITIAL_HERO_ROSTER[0].id,
  });
  const [targetTableIndex, setTargetTableIndex] = useState<number>(2); // Default target Table 2 (Background)

  // Simulation running state
  const [isRunning, setIsRunning] = useState<boolean>(true);
  const [isMuted, setIsMuted] = useState<boolean>(audioEngine.getMuted());
  const [screenShake, setScreenShake] = useState<number>(0);
  const [activeOverdriveBanner, setActiveOverdriveBanner] = useState<{
    casterName: string;
    skillName: string;
    avatar: string;
    color: string;
    desc: string;
  } | null>(null);

  const canvasRef = useRef<HTMLCanvasElement>(null);
  const logsEndRef = useRef<HTMLDivElement>(null);

  // Available custom battlefields
  const savedBattlefields = multiplayerEngine.getBattlefields();

  // Scroll logs to bottom
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [crossTableLogs]);

  // Add a cross-table combat log entry
  const addLog = useCallback(
    (text: string, type: 'mortar' | 'leap' | 'overdrive' | 'chute') => {
      setCrossTableLogs((prev) => [
        ...prev.slice(-40),
        {
          id: `log_${Date.now()}_${Math.random()}`,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
          text,
          type,
        },
      ]);
    },
    []
  );

  // Camera Orbit Animation Loop
  useEffect(() => {
    if (!isAutoRotate || isDragging) return;
    const interval = setInterval(() => {
      setCameraYaw((prev) => (prev + 0.2) % 360);
    }, 30);
    return () => clearInterval(interval);
  }, [isAutoRotate, isDragging]);

  // Launch Cross-Table Artillery Mortar (Table A -> Table B)
  const launchCrossTableMortar = useCallback(
    (
      fromTable: number,
      toTable: number,
      caster: ATBHero,
      target: ATBHero,
      isAutocast: boolean = false
    ) => {
      audioEngine.init();
      audioEngine.playCrossTableMortar();

      const projId = `proj_${Date.now()}_${Math.random()}`;
      let pType: CrossTableProjectile['type'] = 'star_mortar';
      let pColor = '#f472b6';
      let pDmg = Math.round(caster.atk * (isAutocast ? 3.2 : 1.4) + Math.random() * 40);

      if (caster.characterClass === 'majin_kirby') {
        pType = isAutocast ? 'transmute_bubble' : 'star_mortar';
        pColor = '#f472b6';
      } else if (caster.characterClass === 'aether_knight') {
        pType = 'aether_beam';
        pColor = '#38bdf8';
      } else if (caster.characterClass === 'adventurer') {
        pType = 'bezier_fireball';
        pColor = '#f97316';
      } else if (caster.characterClass === 'kirb_builder') {
        pType = 'anvil_bomb';
        pColor = '#fbbf24';
      } else {
        pType = 'tesseract_laser';
        pColor = '#a855f7';
      }

      const newProj: CrossTableProjectile = {
        id: projId,
        casterId: caster.id,
        casterName: caster.name,
        targetId: target.id,
        targetName: target.name,
        fromTableIndex: fromTable,
        toTableIndex: toTable,
        fromX: caster.x,
        fromY: caster.y,
        toX: target.x,
        toY: target.y,
        progress: 0,
        speed: 0.015,
        arcHeight: 120 + Math.abs(toTable - fromTable) * 60,
        type: pType,
        color: pColor,
        damage: pDmg,
        isAutocast,
      };

      setProjectiles((prev) => [...prev, newProj]);

      const distEst = Math.round(Math.hypot(toTable - fromTable, target.x - caster.x, target.y - caster.y) * 10);
      addLog(
        `💥 [Table ${fromTable} ➔ Table ${toTable}] ${caster.name} launched ${isAutocast ? '🌟 3X OVERDRIVE MORTAR' : '🚀 Cross-Boundary Shell'} at ${target.name} (Trajectory Arc: ${newProj.arcHeight}px, Distance: ${distEst}m)`,
        'mortar'
      );
    },
    [addLog]
  );

  // Trigger Cross-Boundary Dimensional Leap (Hero leaps from Table A -> Table B)
  const triggerCrossTableLeap = useCallback(
    (fromTable: number, toTable: number, unitId: string, isChute: boolean = false) => {
      audioEngine.init();
      if (isChute) {
        audioEngine.playChuteSlide();
      } else {
        audioEngine.playBoundaryWarp();
      }

      const sourceTable = tables.find((t) => t.tableIndex === fromTable);
      const unit = sourceTable?.units.find((u) => u.id === unitId);
      if (!unit) return;

      const targetX = Math.floor(Math.random() * 5);
      const targetY = Math.floor(Math.random() * 5);

      const leap: CrossTableLeap = {
        id: `leap_${Date.now()}_${Math.random()}`,
        unitId: unit.id,
        unitName: unit.name,
        fromTableIndex: fromTable,
        toTableIndex: toTable,
        startX: unit.x,
        startY: unit.y,
        targetX,
        targetY,
        progress: 0,
        isChuteSlide: isChute,
        color: unit.color,
      };

      setLeaps((prev) => [...prev, leap]);

      addLog(
        `🌌 [BOUNDARY CROSSING] ${unit.name} ${
          isChute ? 'slid down Inter-Table Copper Chute' : 'performed Dimensional Boundary Leap'
        } from Table ${fromTable} into Table ${toTable} (Coords: [${targetX}, ${targetY}])!`,
        isChute ? 'chute' : 'leap'
      );
    },
    [tables, addLog]
  );

  // Trigger Multi-Table 3X Autocast Cascade (Overdrive shockwave across all tables)
  const triggerMultiTableOverdriveCascade = useCallback(
    (caster: ATBHero, fromTableIndex: number) => {
      audioEngine.init();
      audioEngine.playCrossBoundaryShockwave();

      setScreenShake(14);
      setTimeout(() => setScreenShake(0), 800);
      confetti({ particleCount: 90, spread: 100, origin: { y: 0.4 } });

      setActiveOverdriveBanner({
        casterName: caster.name,
        skillName: caster.skills.charge3Autocast.name,
        avatar: caster.avatar,
        color: caster.color,
        desc: `Cross-Boundary 3X Overdrive wave ripping through Tables 0, 1, and 2!`,
      });
      setTimeout(() => setActiveOverdriveBanner(null), 3200);

      // Launch barrage of cross-table projectiles to every other table
      tables.forEach((t) => {
        if (t.tableIndex !== fromTableIndex && t.units.length > 0) {
          const targetUnit = t.units[Math.floor(Math.random() * t.units.length)];
          launchCrossTableMortar(fromTableIndex, t.tableIndex, caster, targetUnit, true);
        }
      });

      addLog(
        `⚡⚡⚡ [3X MULTI-TABLE CASCADE] ${caster.name} unleashed ${caster.skills.charge3Autocast.name}! Dimensional shockwave reverberates across all tabletop boundaries!`,
        'overdrive'
      );
    },
    [tables, launchCrossTableMortar, addLog]
  );

  // Main 3D Canvas Render & Physics Loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId: number;

    const renderLoop = () => {
      const width = canvas.width;
      const height = canvas.height;
      const cx = width / 2;
      const cy = height / 2 + 30;

      ctx.clearRect(0, 0, width, height);

      // Save canvas state for screen shake
      ctx.save();
      if (screenShake > 0) {
        const sx = (Math.random() - 0.5) * screenShake;
        const sy = (Math.random() - 0.5) * screenShake;
        ctx.translate(sx, sy);
      }

      // Background Void Starfield & Spatial Depth Grid
      const pitchRad = (cameraPitch * Math.PI) / 180;
      const yawRad = (cameraYaw * Math.PI) / 180;

      // Draw Spatial Horizon & Grid
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.08)';
      ctx.lineWidth = 1;
      for (let g = -10; g <= 10; g++) {
        ctx.beginPath();
        ctx.moveTo(cx + g * 80 * zoom, 0);
        ctx.lineTo(cx + g * 140 * zoom, height);
        ctx.stroke();
      }

      // 3D Projection Math Helper: (x, y, z) in world units -> (screenX, screenY, scale)
      const project3D = (worldX: number, worldY: number, worldZ: number) => {
        // Rotate around Y (Yaw)
        const cosY = Math.cos(yawRad);
        const sinY = Math.sin(yawRad);
        const rx = worldX * cosY - worldZ * sinY;
        const rz = worldX * sinY + worldZ * cosY;

        // Rotate around X (Pitch)
        const cosP = Math.cos(pitchRad);
        const sinP = Math.sin(pitchRad);
        const ry = worldY * cosP - rz * sinP;
        const finalZ = worldY * sinP + rz * cosP;

        // Perspective division
        const fov = 750;
        const distance = fov + finalZ;
        const scale = (fov / Math.max(80, distance)) * zoom;

        const screenX = cx + rx * scale;
        const screenY = cy + ry * scale;

        return { x: screenX, y: screenY, scale, z: finalZ };
      };

      // Draw Inter-Table Boundary Conduits / Chutes / Bridges between tables
      const numTables = tables.length;
      for (let i = 0; i < numTables - 1; i++) {
        const tA = tables[i];
        const tB = tables[i + 1];

        const zA = tA.depthZ;
        const yA = -tA.elevationY;
        const zB = tB.depthZ;
        const yB = -tB.elevationY;

        // Draw Inter-Table Energy Bridge (Connecting borders)
        const pA_L = project3D(-120, yA, zA + 90);
        const pA_R = project3D(120, yA, zA + 90);
        const pB_L = project3D(-120, yB, zB - 90);
        const pB_R = project3D(120, yB, zB - 90);

        ctx.fillStyle = 'rgba(99, 102, 241, 0.07)';
        ctx.beginPath();
        ctx.moveTo(pA_L.x, pA_L.y);
        ctx.lineTo(pA_R.x, pA_R.y);
        ctx.lineTo(pB_R.x, pB_R.y);
        ctx.lineTo(pB_L.x, pB_L.y);
        ctx.closePath();
        ctx.fill();

        ctx.strokeStyle = 'rgba(168, 85, 247, 0.35)';
        ctx.setLineDash([4, 4]);
        ctx.stroke();
        ctx.setLineDash([]);

        // Pulsing Energy Conduit Centerline
        const pulse = (Math.sin(Date.now() * 0.005 + i) + 1) * 0.5;
        const midA = project3D(0, yA, zA + 90);
        const midB = project3D(0, yB, zB - 90);

        ctx.strokeStyle = `rgba(56, 189, 248, ${0.4 + pulse * 0.4})`;
        ctx.lineWidth = 2.5 * midA.scale;
        ctx.beginPath();
        ctx.moveTo(midA.x, midA.y);
        // Quadratic curve in 3D projection
        const midMid = project3D(0, (yA + yB) / 2 - 30, (zA + zB) / 2);
        ctx.quadraticCurveTo(midMid.x, midMid.y, midB.x, midB.y);
        ctx.stroke();

        // Label on Inter-Table Chute
        ctx.font = `bold ${Math.max(9, Math.round(11 * midMid.scale))}px monospace`;
        ctx.fillStyle = '#c084fc';
        ctx.textAlign = 'center';
        ctx.fillText(`⚡ BOUNDARY BRIDGE [T${i} ➔ T${i + 1}]`, midMid.x, midMid.y - 8);
      }

      // Render Each Tabletop Layer in Depth Order (Background to Foreground)
      const sortedTables = [...tables].sort((a, b) => b.depthZ - a.depthZ);

      sortedTables.forEach((table) => {
        const tableZ = table.depthZ;
        const tableY = -table.elevationY; // negative is higher
        const gridSize = table.battlefield.gridSize || 6;
        const tileSize = 36;
        const tableWidth = gridSize * tileSize;
        const halfWidth = tableWidth / 2;

        // Base slab projection
        const pTopLeft = project3D(-halfWidth, tableY, tableZ - halfWidth);
        const pTopRight = project3D(halfWidth, tableY, tableZ - halfWidth);
        const pBotRight = project3D(halfWidth, tableY, tableZ + halfWidth);
        const pBotLeft = project3D(-halfWidth, tableY, tableZ + halfWidth);

        // Table Slab Base Drop Shadow & Extrusion
        const slabDepth = 22;
        const pExtLeft = project3D(-halfWidth, tableY + slabDepth, tableZ + halfWidth);
        const pExtRight = project3D(halfWidth, tableY + slabDepth, tableZ + halfWidth);

        ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
        ctx.beginPath();
        ctx.moveTo(pBotLeft.x, pBotLeft.y);
        ctx.lineTo(pBotRight.x, pBotRight.y);
        ctx.lineTo(pExtRight.x, pExtRight.y);
        ctx.lineTo(pExtLeft.x, pExtLeft.y);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = table.accentColor;
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Tabletop Surface Polygon
        const grad = ctx.createLinearGradient(pTopLeft.x, pTopLeft.y, pBotRight.x, pBotRight.y);
        grad.addColorStop(0, '#1e293b');
        grad.addColorStop(1, '#0f172a');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.moveTo(pTopLeft.x, pTopLeft.y);
        ctx.lineTo(pTopRight.x, pTopRight.y);
        ctx.lineTo(pBotRight.x, pBotRight.y);
        ctx.lineTo(pBotLeft.x, pBotLeft.y);
        ctx.closePath();
        ctx.fill();

        // Accent Glowing Border
        ctx.strokeStyle = table.accentColor;
        ctx.lineWidth = 2 * pBotRight.scale;
        ctx.stroke();

        // Grid Lines on Tabletop
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = 1;
        for (let gx = 0; gx <= gridSize; gx++) {
          const xPos = -halfWidth + gx * tileSize;
          const startP = project3D(xPos, tableY, tableZ - halfWidth);
          const endP = project3D(xPos, tableY, tableZ + halfWidth);
          ctx.beginPath();
          ctx.moveTo(startP.x, startP.y);
          ctx.lineTo(endP.x, endP.y);
          ctx.stroke();
        }
        for (let gy = 0; gy <= gridSize; gy++) {
          const zPos = tableZ - halfWidth + gy * tileSize;
          const startP = project3D(-halfWidth, tableY, zPos);
          const endP = project3D(halfWidth, tableY, zPos);
          ctx.beginPath();
          ctx.moveTo(startP.x, startP.y);
          ctx.lineTo(endP.x, endP.y);
          ctx.stroke();
        }

        // Render Battlefield Custom Tiles & Voxels
        table.battlefield.tiles.forEach((tile) => {
          const tileWorldX = -halfWidth + (tile.x + 0.5) * tileSize;
          const tileWorldZ = tableZ - halfWidth + (tile.y + 0.5) * tileSize;
          const tileWorldY = tableY - tile.tier * 16;

          const proj = project3D(tileWorldX, tileWorldY, tileWorldZ);
          const radius = Math.max(4, 10 * proj.scale);

          ctx.fillStyle = tile.color || '#38bdf8';
          ctx.beginPath();
          ctx.arc(proj.x, proj.y, radius, 0, Math.PI * 2);
          ctx.fill();
          ctx.strokeStyle = '#ffffff';
          ctx.lineWidth = 1;
          ctx.stroke();
        });

        // Boundary Forcefield Wall (if active)
        if (table.forcefieldActive) {
          const wallTopL = project3D(-halfWidth, tableY - 60, tableZ - halfWidth);
          const wallTopR = project3D(halfWidth, tableY - 60, tableZ - halfWidth);
          ctx.fillStyle = 'rgba(245, 158, 11, 0.12)';
          ctx.beginPath();
          ctx.moveTo(pTopLeft.x, pTopLeft.y);
          ctx.lineTo(pTopRight.x, pTopRight.y);
          ctx.lineTo(wallTopR.x, wallTopR.y);
          ctx.lineTo(wallTopL.x, wallTopL.y);
          ctx.closePath();
          ctx.fill();
          ctx.strokeStyle = 'rgba(245, 158, 11, 0.6)';
          ctx.stroke();
        }

        // Table Header Tag in 3D space
        const tagProj = project3D(0, tableY - 45, tableZ - halfWidth);
        ctx.font = `bold ${Math.max(10, Math.round(13 * tagProj.scale))}px sans-serif`;
        ctx.fillStyle = table.accentColor;
        ctx.textAlign = 'center';
        ctx.fillText(`TABLE ${table.tableIndex}: ${table.name.toUpperCase()}`, tagProj.x, tagProj.y);

        // Render Units on this Table
        table.units.forEach((unit) => {
          const unitWorldX = -halfWidth + (unit.x + 0.5) * tileSize;
          const unitWorldZ = tableZ - halfWidth + (unit.y + 0.5) * tileSize;
          const unitWorldY = tableY - unit.tier * 16 - 18;

          const proj = project3D(unitWorldX, unitWorldY, unitWorldZ);
          const size = Math.max(14, 28 * proj.scale);

          const isSelected = selectedUnit?.tableIndex === table.tableIndex && selectedUnit.heroId === unit.id;

          // Unit Shadow on the tile below
          const shadowProj = project3D(unitWorldX, tableY - unit.tier * 16, unitWorldZ);
          ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
          ctx.beginPath();
          ctx.ellipse(shadowProj.x, shadowProj.y, size * 0.6, size * 0.3, 0, 0, Math.PI * 2);
          ctx.fill();

          // Selection Ring
          if (isSelected) {
            ctx.strokeStyle = '#facc15';
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.ellipse(shadowProj.x, shadowProj.y, size * 0.9, size * 0.45, 0, 0, Math.PI * 2);
            ctx.stroke();
          }

          // Unit Avatar & Halo
          ctx.fillStyle = unit.color;
          ctx.beginPath();
          ctx.arc(proj.x, proj.y, size / 2, 0, Math.PI * 2);
          ctx.fill();
          ctx.strokeStyle = isSelected ? '#facc15' : '#ffffff';
          ctx.lineWidth = isSelected ? 3 : 1.5;
          ctx.stroke();

          // Emoji Icon
          ctx.font = `${Math.round(size * 0.65)}px sans-serif`;
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(unit.avatar, proj.x, proj.y);

          // Name Tag & HP Bar
          ctx.font = `bold ${Math.max(8, Math.round(10 * proj.scale))}px sans-serif`;
          ctx.fillStyle = '#ffffff';
          ctx.fillText(unit.name, proj.x, proj.y - size / 2 - 12);

          // 3-Tier ATB Bar (0-300)
          const barW = Math.max(24, 44 * proj.scale);
          const barH = Math.max(3, 5 * proj.scale);
          const barX = proj.x - barW / 2;
          const barY = proj.y - size / 2 - 6;

          ctx.fillStyle = '#1e293b';
          ctx.fillRect(barX, barY, barW, barH);

          const atbPercent = Math.min(1, unit.atbGauge / 300);
          const atbColor = unit.atbGauge >= 300 ? '#f59e0b' : unit.atbGauge >= 200 ? '#ec4899' : '#38bdf8';
          ctx.fillStyle = atbColor;
          ctx.fillRect(barX, barY, barW * atbPercent, barH);
        });
      });

      // Render Cross-Table Projectiles in 3D Parabolic Trajectories
      projectiles.forEach((p) => {
        const fromT = tables.find((t) => t.tableIndex === p.fromTableIndex) || tables[0];
        const toT = tables.find((t) => t.tableIndex === p.toTableIndex) || tables[1];

        const tileSize = 36;
        const halfWidth = (fromT.battlefield.gridSize * tileSize) / 2;

        const startWX = -halfWidth + (p.fromX + 0.5) * tileSize;
        const startWZ = fromT.depthZ - halfWidth + (p.fromY + 0.5) * tileSize;
        const startWY = -fromT.elevationY - 18;

        const targetWX = -halfWidth + (p.toX + 0.5) * tileSize;
        const targetWZ = toT.depthZ - halfWidth + (p.toY + 0.5) * tileSize;
        const targetWY = -toT.elevationY - 18;

        // Current interpolated 3D position
        const t = p.progress;
        const curWX = startWX + (targetWX - startWX) * t;
        const curWZ = startWZ + (targetWZ - startWZ) * t;
        // Parabolic arc Y: Y(t) = Y_linear(t) - 4 * arcHeight * t * (1 - t)
        const arcY = Math.sin(t * Math.PI) * p.arcHeight;
        const curWY = startWY + (targetWY - startWY) * t - arcY;

        const projScreen = project3D(curWX, curWY, curWZ);
        const shadowScreen = project3D(curWX, startWY + (targetWY - startWY) * t, curWZ);

        // Projectile Ground Shadow
        ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
        ctx.beginPath();
        ctx.ellipse(shadowScreen.x, shadowScreen.y, 8 * shadowScreen.scale, 4 * shadowScreen.scale, 0, 0, Math.PI * 2);
        ctx.fill();

        // Parabolic Flight Ribbon Trail
        ctx.strokeStyle = p.color;
        ctx.lineWidth = Math.max(2, 4 * projScreen.scale);
        ctx.beginPath();
        // Trace back a few steps for motion blur trail
        for (let step = 0; step <= 10; step++) {
          const st = Math.max(0, t - step * 0.02);
          const sWX = startWX + (targetWX - startWX) * st;
          const sWZ = startWZ + (targetWZ - startWZ) * st;
          const sArcY = Math.sin(st * Math.PI) * p.arcHeight;
          const sWY = startWY + (targetWY - startWY) * st - sArcY;
          const pStep = project3D(sWX, sWY, sWZ);
          if (step === 0) ctx.moveTo(pStep.x, pStep.y);
          else ctx.lineTo(pStep.x, pStep.y);
        }
        ctx.stroke();

        // Projectile Head
        const pSize = Math.max(6, (p.isAutocast ? 18 : 12) * projScreen.scale);
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(projScreen.x, projScreen.y, pSize, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Glowing Star / Flame Icon
        ctx.font = `${Math.round(pSize * 1.2)}px sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(p.type === 'transmute_bubble' ? '🍬' : p.type === 'star_mortar' ? '⭐' : p.type === 'anvil_bomb' ? '🔨' : '🔥', projScreen.x, projScreen.y);
      });

      // Render Cross-Table Unit Leaps
      leaps.forEach((l) => {
        const fromT = tables.find((t) => t.tableIndex === l.fromTableIndex) || tables[0];
        const toT = tables.find((t) => t.tableIndex === l.toTableIndex) || tables[1];

        const tileSize = 36;
        const halfWidth = (fromT.battlefield.gridSize * tileSize) / 2;

        const startWX = -halfWidth + (l.startX + 0.5) * tileSize;
        const startWZ = fromT.depthZ - halfWidth + (l.startY + 0.5) * tileSize;
        const startWY = -fromT.elevationY - 18;

        const targetWX = -halfWidth + (l.targetX + 0.5) * tileSize;
        const targetWZ = toT.depthZ - halfWidth + (l.targetY + 0.5) * tileSize;
        const targetWY = -toT.elevationY - 18;

        const t = l.progress;
        const curWX = startWX + (targetWX - startWX) * t;
        const curWZ = startWZ + (targetWZ - startWZ) * t;
        const arcY = Math.sin(t * Math.PI) * (l.isChuteSlide ? 20 : 160);
        const curWY = startWY + (targetWY - startWY) * t - arcY;

        const projScreen = project3D(curWX, curWY, curWZ);

        // Unit Leaping Sprite
        ctx.fillStyle = l.color;
        const lSize = Math.max(14, 28 * projScreen.scale);
        ctx.beginPath();
        ctx.arc(projScreen.x, projScreen.y, lSize / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#facc15';
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.font = `bold ${Math.max(9, Math.round(11 * projScreen.scale))}px sans-serif`;
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.fillText(l.isChuteSlide ? '🌪️ SLIDING!' : '🚀 LEAPING!', projScreen.x, projScreen.y - lSize / 2 - 8);
      });

      // Render Floating Particles & Text in 3D
      particles.forEach((pt) => {
        ctx.save();
        ctx.globalAlpha = Math.max(0, pt.life / pt.maxLife);

        if (pt.type === 'text' && pt.text) {
          ctx.font = 'black 14px sans-serif';
          ctx.fillStyle = pt.color;
          ctx.textAlign = 'center';
          ctx.fillText(pt.text, pt.x, pt.y);
        } else {
          ctx.fillStyle = pt.color;
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, pt.size, 0, Math.PI * 2);
          ctx.fill();
        }
        ctx.restore();
      });

      ctx.restore(); // Screen shake restore

      // Physics State Update (Continuous simulation)
      if (isRunning) {
        // Update Projectiles
        setProjectiles((prev) => {
          const next: CrossTableProjectile[] = [];
          prev.forEach((p) => {
            const nextProg = p.progress + p.speed;
            if (nextProg >= 1) {
              // Impact hit on target table!
              audioEngine.playHitImpact();
              const toT = tables.find((t) => t.tableIndex === p.toTableIndex);
              const target = toT?.units.find((u) => u.id === p.targetId);

              if (target) {
                target.hp = Math.max(0, target.hp - p.damage);
                // Create Floating Combat Text at target position
                const tileSize = 36;
                const halfWidth = (toT!.battlefield.gridSize * tileSize) / 2;
                const targetWX = -halfWidth + (p.toX + 0.5) * tileSize;
                const targetWZ = toT!.depthZ - halfWidth + (p.toY + 0.5) * tileSize;
                const targetWY = -toT!.elevationY - 18;
                const targetScreen = project3D(targetWX, targetWY, targetWZ);

                setParticles((part) => [
                  ...part,
                  {
                    x: targetScreen.x + (Math.random() - 0.5) * 20,
                    y: targetScreen.y - 15,
                    vx: (Math.random() - 0.5) * 2,
                    vy: -2.5,
                    ax: 0,
                    ay: 0.05,
                    life: 40,
                    maxLife: 40,
                    size: 12,
                    color: p.isAutocast ? '#facc15' : '#ef4444',
                    type: 'text',
                    text: `-${p.damage} DMG!`,
                  },
                ]);

                addLog(
                  `💥 [IMPACT] Projectile from ${p.casterName} struck ${target.name} on Table ${p.toTableIndex} for ${p.damage} damage!`,
                  'mortar'
                );
              }
            } else {
              next.push({ ...p, progress: nextProg });
            }
          });
          return next;
        });

        // Update Leaps
        setLeaps((prev) => {
          const next: CrossTableLeap[] = [];
          prev.forEach((l) => {
            const nextProg = l.progress + (l.isChuteSlide ? 0.025 : 0.018);
            if (nextProg >= 1) {
              // Land unit on target table
              setTables((curTables) => {
                const sourceT = curTables.find((t) => t.tableIndex === l.fromTableIndex);
                const targetT = curTables.find((t) => t.tableIndex === l.toTableIndex);
                if (!sourceT || !targetT) return curTables;

                const movingUnit = sourceT.units.find((u) => u.id === l.unitId);
                if (!movingUnit) return curTables;

                sourceT.units = sourceT.units.filter((u) => u.id !== l.unitId);
                targetT.units = [
                  ...targetT.units,
                  { ...movingUnit, x: l.targetX, y: l.targetY },
                ];

                return [...curTables];
              });
              audioEngine.playHitImpact();
              addLog(
                `🏁 [LANDING] ${l.unitName} landed safely on Table ${l.toTableIndex} at [${l.targetX}, ${l.targetY}]!`,
                'leap'
              );
            } else {
              next.push({ ...l, progress: nextProg });
            }
          });
          return next;
        });

        // Update Particles
        setParticles((prev) =>
          prev
            .map((pt) => ({
              ...pt,
              x: pt.x + pt.vx,
              y: pt.y + pt.vy,
              vx: pt.vx + pt.ax,
              vy: pt.vy + pt.ay,
              life: pt.life - 1,
            }))
            .filter((pt) => pt.life > 0)
        );

        // Continuous ATB Gauge Increment & Autonomous Cross-Table Autocasting
        setTables((curTables) => {
          curTables.forEach((t) => {
            t.units.forEach((unit) => {
              if (unit.hp > 0) {
                unit.atbGauge = Math.min(300, unit.atbGauge + (unit.atbSpeed || 25) * 0.04);
                // Autonomous 3X Autocast Trigger
                if (unit.atbGauge >= 300 && Math.random() < 0.03) {
                  unit.atbGauge = 0;
                  // Choose target on another table
                  const otherTables = curTables.filter((ot) => ot.tableIndex !== t.tableIndex);
                  const targetTable = otherTables[Math.floor(Math.random() * otherTables.length)];
                  if (targetTable && targetTable.units.length > 0) {
                    const targetUnit = targetTable.units[Math.floor(Math.random() * targetTable.units.length)];
                    launchCrossTableMortar(t.tableIndex, targetTable.tableIndex, unit, targetUnit, true);
                  }
                }
              }
            });
          });
          return [...curTables];
        });
      }

      animId = requestAnimationFrame(renderLoop);
    };

    animId = requestAnimationFrame(renderLoop);
    return () => cancelAnimationFrame(animId);
  }, [
    tables,
    projectiles,
    leaps,
    particles,
    cameraPitch,
    cameraYaw,
    zoom,
    screenShake,
    isRunning,
    selectedUnit,
    launchCrossTableMortar,
    addLog,
  ]);

  // Mouse Drag Handlers for 3D Camera Orbit
  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    dragStartRef.current = {
      x: e.clientX,
      y: e.clientY,
      yaw: cameraYaw,
      pitch: cameraPitch,
    };
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    const dx = e.clientX - dragStartRef.current.x;
    const dy = e.clientY - dragStartRef.current.y;
    setCameraYaw(dragStartRef.current.yaw + dx * 0.4);
    setCameraPitch(Math.max(5, Math.min(75, dragStartRef.current.pitch + dy * 0.3)));
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Assign Custom Battlefield to a Table Slot
  const handleAssignBattlefield = (tableIndex: number, field: CustomBattlefield) => {
    audioEngine.playSporeChime(500);
    setTables((prev) =>
      prev.map((t) =>
        t.tableIndex === tableIndex
          ? {
              ...t,
              name: `Table ${tableIndex}: ${field.name}`,
              theme: field.theme,
              accentColor: field.accentColor || t.accentColor,
              battlefield: field,
            }
          : t
      )
    );
    addLog(`🗺️ Assigned world "${field.name}" to Table ${tableIndex}!`, 'chute');
  };

  // Find currently selected hero object
  const currentHeroObj = selectedUnit
    ? tables
        .find((t) => t.tableIndex === selectedUnit.tableIndex)
        ?.units.find((u) => u.id === selectedUnit.heroId)
    : null;

  return (
    <div className="w-full flex flex-col gap-4 text-slate-100">
      {/* Top Header & Cross-Table Status Banner */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-4 rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950/80 to-slate-900 border border-indigo-500/30 shadow-[0_0_30px_rgba(79,70,229,0.2)]">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-indigo-500/20 border border-indigo-500/40 shadow-[0_0_15px_rgba(99,102,241,0.4)]">
            <Rotate3d className="w-6 h-6 text-indigo-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="font-black text-lg text-white tracking-wide">
                3D CROSS-INTERACTIONARY TABLETOP MATRIX
              </h2>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-black bg-indigo-500/30 text-indigo-300 border border-indigo-500/40">
                DEPTH LINKED
              </span>
            </div>
            <p className="text-xs text-indigo-200/70">
              Interactive multi-world tabletop cascade with cross-boundary ballistics, inter-table chutes, and 3X Overdrive shockwaves
            </p>
          </div>
        </div>

        {/* Quick Actions & Sound Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsRunning(!isRunning)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
              isRunning
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
            }`}
          >
            {isRunning ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            <span>{isRunning ? 'RUNNING' : 'PAUSED'}</span>
          </button>

          <button
            onClick={() => {
              const muted = audioEngine.toggleMute();
              setIsMuted(muted);
            }}
            className="p-2 rounded-xl bg-slate-800/80 border border-slate-700 text-slate-300 hover:text-white"
          >
            {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4 text-emerald-400" />}
          </button>

          {onOpenBuilder && (
            <button
              onClick={onOpenBuilder}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-400 hover:to-rose-400 text-white font-bold text-xs shadow-[0_0_15px_rgba(244,114,182,0.4)]"
            >
              <Hammer className="w-3.5 h-3.5" />
              <span>BUILD WORLD</span>
            </button>
          )}
        </div>
      </div>

      {/* Main 3D Canvas Stage + Interactive Tactical Overlay */}
      <div className="relative w-full h-[520px] rounded-2xl overflow-hidden bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 border border-slate-800 shadow-2xl">
        <canvas
          ref={canvasRef}
          width={1000}
          height={520}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          className="w-full h-full cursor-grab active:cursor-grabbing block"
        />

        {/* 3X Overdrive Cinematic Overlay Banner */}
        {activeOverdriveBanner && (
          <div className="absolute top-6 left-1/2 -translate-x-1/2 z-30 flex items-center gap-3 px-6 py-3 rounded-2xl bg-gradient-to-r from-indigo-950/95 via-purple-950/95 to-pink-950/95 border-2 border-pink-400/80 shadow-[0_0_40px_rgba(236,72,153,0.7)] animate-bounce">
            <span className="text-3xl">{activeOverdriveBanner.avatar}</span>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-black px-2 py-0.5 rounded-full bg-pink-500 text-white animate-pulse">
                  3X AUTOCAST CASCADE
                </span>
                <span className="text-sm font-black text-amber-300">
                  {activeOverdriveBanner.casterName}
                </span>
              </div>
              <h3 className="text-lg font-black text-white tracking-wide">
                {activeOverdriveBanner.skillName}
              </h3>
              <p className="text-xs text-pink-200">{activeOverdriveBanner.desc}</p>
            </div>
          </div>
        )}

        {/* 3D Camera Controls Floating Palette */}
        <div className="absolute top-4 left-4 z-20 flex flex-col gap-2 p-3 rounded-xl bg-slate-900/85 backdrop-blur-md border border-slate-700/60 text-xs shadow-lg max-w-[200px]">
          <div className="flex items-center justify-between text-slate-300 font-bold">
            <span className="flex items-center gap-1">
              <Eye className="w-3.5 h-3.5 text-indigo-400" /> 3D Orbit Cam
            </span>
            <button
              onClick={() => setIsAutoRotate(!isAutoRotate)}
              className={`px-1.5 py-0.5 rounded text-[10px] ${
                isAutoRotate ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400'
              }`}
            >
              {isAutoRotate ? 'AUTO' : 'MANUAL'}
            </button>
          </div>

          <div className="flex flex-col gap-1 text-[11px]">
            <label className="flex justify-between text-slate-400">
              <span>Pitch: {Math.round(cameraPitch)}°</span>
            </label>
            <input
              type="range"
              min="5"
              max="70"
              value={cameraPitch}
              onChange={(e) => setCameraPitch(Number(e.target.value))}
              className="accent-indigo-500 h-1 bg-slate-700 rounded-lg cursor-pointer"
            />

            <label className="flex justify-between text-slate-400 mt-1">
              <span>Table Spacing (Z)</span>
            </label>
            <input
              type="range"
              min="160"
              max="380"
              value={tableSpacingZ}
              onChange={(e) => {
                const val = Number(e.target.value);
                setTableSpacingZ(val);
                setTables((prev) =>
                  prev.map((t) => ({ ...t, depthZ: t.tableIndex * val }))
                );
              }}
              className="accent-pink-500 h-1 bg-slate-700 rounded-lg cursor-pointer"
            />

            <label className="flex justify-between text-slate-400 mt-1">
              <span>Table Elevation (Y)</span>
            </label>
            <input
              type="range"
              min="20"
              max="140"
              value={tableElevationY}
              onChange={(e) => {
                const val = Number(e.target.value);
                setTableElevationY(val);
                setTables((prev) =>
                  prev.map((t) => ({ ...t, elevationY: t.tableIndex * val }))
                );
              }}
              className="accent-amber-500 h-1 bg-slate-700 rounded-lg cursor-pointer"
            />
          </div>

          {/* Camera Presets */}
          <div className="grid grid-cols-2 gap-1 mt-1">
            <button
              onClick={() => {
                setCameraPitch(28);
                setCameraYaw(-15);
                setZoom(0.9);
              }}
              className="px-1.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-[10px] text-slate-300"
            >
              Perspective 3D
            </button>
            <button
              onClick={() => {
                setCameraPitch(58);
                setCameraYaw(0);
                setZoom(0.85);
              }}
              className="px-1.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-[10px] text-slate-300"
            >
              Top Cascade
            </button>
          </div>
        </div>

        {/* Real-Time Cross-Boundary Action Controls (Bottom Floating Bar) */}
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-20 flex flex-wrap items-center gap-2 px-4 py-2.5 rounded-2xl bg-slate-900/90 backdrop-blur-md border border-indigo-500/40 shadow-2xl">
          {currentHeroObj ? (
            <div className="flex items-center gap-2 pr-3 border-r border-slate-700">
              <span className="text-xl">{currentHeroObj.avatar}</span>
              <div>
                <div className="text-xs font-black text-white">{currentHeroObj.name}</div>
                <div className="text-[10px] text-indigo-300">
                  Stationed on Table {selectedUnit?.tableIndex}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-xs text-slate-400 pr-3 border-r border-slate-700">
              Select a Unit on any table
            </div>
          )}

          {/* Cross-Table Target Selector */}
          <div className="flex items-center gap-1 text-xs">
            <span className="text-slate-400 font-bold">Target Table:</span>
            {[0, 1, 2].map((tIdx) => (
              <button
                key={tIdx}
                onClick={() => setTargetTableIndex(tIdx)}
                className={`px-2.5 py-1 rounded-lg font-bold text-xs transition-all ${
                  targetTableIndex === tIdx
                    ? 'bg-indigo-600 text-white shadow-[0_0_10px_rgba(99,102,241,0.5)]'
                    : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                Table {tIdx}
              </button>
            ))}
          </div>

          {/* Action Trigger Buttons */}
          <div className="flex items-center gap-2 pl-2">
            <button
              onClick={() => {
                if (!currentHeroObj || selectedUnit === null) return;
                const toT = tables.find((t) => t.tableIndex === targetTableIndex);
                if (!toT || toT.units.length === 0) return;
                const targetU = toT.units[0];
                launchCrossTableMortar(
                  selectedUnit.tableIndex,
                  targetTableIndex,
                  currentHeroObj,
                  targetU,
                  false
                );
              }}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-rose-500 to-amber-500 hover:from-rose-400 hover:to-amber-400 text-slate-950 font-black text-xs shadow-[0_0_15px_rgba(244,63,94,0.4)] transition-all active:scale-95"
            >
              <Crosshair className="w-3.5 h-3.5" />
              <span>CROSS-TABLE MORTAR</span>
            </button>

            <button
              onClick={() => {
                if (!currentHeroObj || selectedUnit === null) return;
                triggerCrossTableLeap(
                  selectedUnit.tableIndex,
                  targetTableIndex,
                  currentHeroObj.id,
                  false
                );
              }}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold text-xs shadow-[0_0_15px_rgba(6,182,212,0.4)] transition-all active:scale-95"
            >
              <ArrowUpRight className="w-3.5 h-3.5" />
              <span>BOUNDARY LEAP</span>
            </button>

            <button
              onClick={() => {
                if (!currentHeroObj || selectedUnit === null) return;
                triggerCrossTableLeap(
                  selectedUnit.tableIndex,
                  targetTableIndex,
                  currentHeroObj.id,
                  true
                );
              }}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-slate-950 font-black text-xs shadow-[0_0_15px_rgba(245,158,11,0.4)] transition-all active:scale-95"
            >
              <Zap className="w-3.5 h-3.5" />
              <span>CHUTE SLIDE</span>
            </button>

            <button
              onClick={() => {
                if (!currentHeroObj || selectedUnit === null) return;
                triggerMultiTableOverdriveCascade(currentHeroObj, selectedUnit.tableIndex);
              }}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 hover:from-purple-500 hover:to-rose-500 text-white font-black text-xs shadow-[0_0_20px_rgba(236,72,153,0.5)] transition-all active:scale-95"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>3X OVERDRIVE CASCADE</span>
            </button>
          </div>
        </div>
      </div>

      {/* Lower Row: Table Slot Management & Live Telemetry Cross-Boundary Logs */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Table Management Cards (Table 0, Table 1, Table 2) */}
        <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-3 gap-3">
          {tables.map((tbl) => (
            <div
              key={tbl.id}
              className="p-3.5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 flex flex-col justify-between gap-3 shadow-lg"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span
                    className="text-[11px] font-black px-2 py-0.5 rounded-full"
                    style={{
                      backgroundColor: `${tbl.accentColor}25`,
                      color: tbl.accentColor,
                      border: `1px solid ${tbl.accentColor}50`,
                    }}
                  >
                    TABLE {tbl.tableIndex} ({tbl.tableIndex === 0 ? 'FOREGROUND' : tbl.tableIndex === 1 ? 'MIDGROUND' : 'BACKGROUND'})
                  </span>
                  <button
                    onClick={() => {
                      setTables((prev) =>
                        prev.map((t) =>
                          t.tableIndex === tbl.tableIndex
                            ? { ...t, forcefieldActive: !t.forcefieldActive }
                            : t
                        )
                      );
                      audioEngine.playTextBlip(15);
                    }}
                    className={`p-1 rounded-lg ${
                      tbl.forcefieldActive ? 'text-amber-400 bg-amber-500/20' : 'text-slate-500 bg-slate-800'
                    }`}
                    title="Toggle Forcefield"
                  >
                    <Shield className="w-3.5 h-3.5" />
                  </button>
                </div>

                <h4 className="font-bold text-sm text-white mt-1.5">{tbl.name}</h4>
                <p className="text-[11px] text-slate-400">{tbl.theme}</p>

                {/* Stationed Units */}
                <div className="mt-2.5 flex flex-col gap-1.5">
                  <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                    Stationed Units ({tbl.units.length})
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {tbl.units.map((u) => {
                      const isSel = selectedUnit?.tableIndex === tbl.tableIndex && selectedUnit.heroId === u.id;
                      return (
                        <button
                          key={u.id}
                          onClick={() => {
                            setSelectedUnit({ tableIndex: tbl.tableIndex, heroId: u.id });
                            audioEngine.playTextBlip();
                          }}
                          className={`flex items-center gap-1.5 px-2 py-1 rounded-xl text-xs font-bold transition-all ${
                            isSel
                              ? 'bg-indigo-600 text-white shadow-[0_0_12px_rgba(99,102,241,0.5)] ring-1 ring-indigo-300'
                              : 'bg-slate-800/90 text-slate-300 hover:bg-slate-700'
                          }`}
                        >
                          <span>{u.avatar}</span>
                          <span>{u.name.split(' ')[0]}</span>
                          <span className="text-[9px] text-amber-300">
                            {Math.round(u.atbGauge)}
                          </span>
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Map Switcher for this slot */}
              <div className="pt-2 border-t border-slate-800/80">
                <label className="text-[10px] text-slate-400 font-semibold block mb-1">
                  Deploy Custom Map:
                </label>
                <select
                  value={tbl.battlefield.id}
                  onChange={(e) => {
                    const field = savedBattlefields.find((f) => f.id === e.target.value);
                    if (field) handleAssignBattlefield(tbl.tableIndex, field);
                  }}
                  className="w-full bg-slate-950 border border-slate-700/80 rounded-lg px-2 py-1 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                >
                  {savedBattlefields.map((f) => (
                    <option key={f.id} value={f.id}>
                      {f.name} ({f.creator})
                    </option>
                  ))}
                </select>
              </div>
            </div>
          ))}
        </div>

        {/* Live Cross-Boundary Telemetry Log */}
        <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex flex-col justify-between gap-3 shadow-lg">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-400" />
              <span className="font-bold text-xs text-white uppercase tracking-wider">
                Cross-Boundary Telemetry
              </span>
            </div>
            <span className="px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 text-[10px] font-black">
              LIVE 3D RADAR
            </span>
          </div>

          <div className="flex-1 overflow-y-auto max-h-[160px] flex flex-col gap-1.5 text-[11px] font-mono pr-1">
            {crossTableLogs.map((log) => (
              <div
                key={log.id}
                className={`p-1.5 rounded-lg border ${
                  log.type === 'overdrive'
                    ? 'bg-purple-950/40 border-purple-800/60 text-purple-200'
                    : log.type === 'mortar'
                    ? 'bg-rose-950/30 border-rose-900/50 text-rose-200'
                    : log.type === 'chute'
                    ? 'bg-amber-950/30 border-amber-900/50 text-amber-200'
                    : 'bg-slate-950/40 border-slate-800 text-slate-300'
                }`}
              >
                <span className="text-[9px] text-slate-500 mr-1.5">[{log.time}]</span>
                <span>{log.text}</span>
              </div>
            ))}
            <div ref={logsEndRef} />
          </div>

          <div className="text-[10px] text-slate-500 text-center italic">
            Ballistics calculate 3D parabolic trajectories: $Y(t) = Y_0 + v_0 t - \frac{1}{2}gt^2$
          </div>
        </div>
      </div>
    </div>
  );
};
