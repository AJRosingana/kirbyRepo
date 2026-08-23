/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export type EpochEra = '8bit' | '16bit' | '32bit' | 'ultra';

export type PortalFrameStyle = 'pharaoh' | 'cosmic' | 'cyber' | 'sky' | 'magma' | 'spore' | 'matrix' | 'custom';

export interface PortalSurface {
  id: string;
  name: string;
  subtitle: string;
  theme: string;
  epoch: EpochEra;
  accentColor: string;
  ambientFrequency: number;
  lore: string;
  interactiveHint: string;
  frameStyle?: PortalFrameStyle;
  canvasCode?: string; // Custom runnable JS/Canvas script for dynamic portals
  isGenerated?: boolean;
  sourceImageUrl?: string;
  questNodeId?: string;
}

export interface QuestNode {
  id: string;
  title: string;
  portalId: string;
  description: string;
  objective: string;
  completed: boolean;
  codeSnippet?: string;
  targetValue?: string | number;
  melodyNote: number; // Hz or index
  loreFragment: string;
}

export interface OracleMessage {
  id: string;
  sender: 'oracle' | 'traveler' | 'system';
  text: string;
  timestamp: number;
  associatedPortalId?: string;
  isSpecialCipher?: boolean;
}

export interface SporeCreature {
  id: number;
  x: number;
  y: number;
  targetX: number;
  targetY: number;
  speed: number;
  color: string;
  energy: number;
  carryingSpore: boolean;
}

export interface SporeMushroom {
  id: string;
  x: number;
  y: number;
  radius: number;
  color: string;
  glowPhase: number;
  sporesGenerated: number;
}

export type ChessUnitType =
  | 'knight'
  | 'bishop'
  | 'rook'
  | 'pawn'
  | 'kirb_builder'
  | 'scarab'
  | 'tesseract'
  | 'mimic';

export interface ChessUnit {
  id: string;
  name: string;
  type: ChessUnitType;
  team: 'player' | 'enemy';
  tier: 0 | 1 | 2; // 0: Lower ground, 1: Middle terrace, 2: Upper plateau
  x: number; // 0-7
  y: number; // 0-7
  hp: number;
  maxHp: number;
  attack: number;
  range: number;
  mana: number;
  maxMana: number;
  color: string;
  isMoving?: boolean;
}

export interface CrossPortalSpell {
  id: string;
  name: string;
  portalId: string;
  portalName: string;
  icon: string;
  color: string;
  manaCost: number;
  description: string;
  targetTier?: number;
  effect: 'damage_all' | 'heal_team' | 'stun_tier' | 'chute_slide' | 'elevate_ladder' | 'confuse';
}

export interface BuilderVoxel {
  id: string;
  x: number;
  y: number;
  zone: 'foundation' | 'assembly' | 'canopy';
  type: 'kirb_worker' | 'crane' | 'question_block' | 'chute' | 'ladder' | 'portal_frame' | 'sand_dune' | 'magma_pipe' | 'spore_cap';
  color: string;
  label?: string;
  rotation?: number;
}

export type ATBCharacterClass =
  | 'aether_knight'
  | 'adventurer'
  | 'majin_kirby'
  | 'kirb_builder'
  | 'pharaoh_scarab'
  | 'cyber_tesseract';

export interface ATBSkill {
  name: string;
  cost: number; // 100, 200, or 300 ATB
  desc: string;
  icon: string;
  vfxType: string;
  equationSnippet?: string;
  damageMultiplier?: number;
  healMultiplier?: number;
  aoe?: boolean;
}

export interface ATBHero {
  id: string;
  name: string;
  title: string;
  characterClass: ATBCharacterClass;
  team: 'player' | 'ally_multiplayer' | 'enemy_boss' | 'enemy_mob';
  ownerId: string; // 'local_player', 'peer_1', 'bot', etc.
  hp: number;
  maxHp: number;
  mp: number;
  maxMp: number;
  atbGauge: number; // 0 to 300 (100 = 1x, 200 = 2x, 300 = 3x AUTOCAST)
  atbSpeed: number; // charge per second
  atk: number;
  def: number;
  spd: number;
  tier: 0 | 1 | 2; // elevation tier
  x: number;
  y: number;
  targetId?: string;
  isAutocasting?: boolean;
  autocastTimer?: number;
  color: string;
  spriteStyle: 'pixel_2d' | 'mesh_3d_wire' | 'toon_vector';
  avatar: string;
  lore: string;
  skills: {
    charge1: ATBSkill;
    charge2: ATBSkill;
    charge3Autocast: ATBSkill;
  };
  kills: number;
  damageDealt: number;
}

export interface MultiplayerPlayer {
  id: string;
  name: string;
  avatar: string;
  isReady: boolean;
  heroClass: ATBCharacterClass;
  level: number;
  ping: number;
  isHost?: boolean;
}

export interface MultiplayerRoomState {
  roomId: string;
  roomName: string;
  hostId: string;
  players: MultiplayerPlayer[];
  gameMode: 'coop_boss_raid' | 'atb_duel' | 'endless_gauntlet' | 'custom_builder_war';
  battlefieldId: string;
  round: number;
  isActive: boolean;
  maxPlayers: number;
  chatMessages: {
    id: string;
    sender: string;
    text: string;
    time: string;
    type?: 'system' | 'chat' | 'cast' | 'autocast';
  }[];
}

export interface CustomBattlefield {
  id: string;
  name: string;
  theme: string;
  gridSize: number;
  accentColor: string;
  tiles: { x: number; y: number; tier: 0 | 1 | 2; type: string; color: string; hazard?: string }[];
  chutes: { topX: number; topY: number; botX: number; botY: number }[];
  ladders: { startX: number; startY: number; endX: number; endY: number }[];
  creator: string;
  createdAt: number;
  bossType?: string;
}

export interface VFXParticle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  ax: number;
  ay: number;
  life: number;
  maxLife: number;
  size: number;
  color: string;
  type: 'flame' | 'smoke' | 'aether_blade' | 'aether_trail' | 'candy_star' | 'gaussian_bloom' | 'shockwave' | 'text' | 'spore' | 'boundary_rift' | 'laser_beam';
  text?: string;
  blurRadius?: number;
  alpha?: number;
  z?: number;
}

export interface TabletopLayer {
  id: string;
  tableIndex: number; // 0 = Foreground, 1 = Midground, 2 = Background
  name: string;
  theme: string;
  accentColor: string;
  depthZ: number; // 3D depth position
  elevationY: number; // 3D vertical step
  battlefield: CustomBattlefield;
  units: ATBHero[];
  hazardState: 'calm' | 'charged' | 'erupting';
  forcefieldActive: boolean;
}

export interface CrossTableProjectile {
  id: string;
  casterId: string;
  casterName: string;
  targetId: string;
  targetName: string;
  fromTableIndex: number;
  toTableIndex: number;
  fromX: number;
  fromY: number;
  toX: number;
  toY: number;
  progress: number; // 0 to 1
  speed: number;
  arcHeight: number;
  type: 'star_mortar' | 'aether_beam' | 'bezier_fireball' | 'tesseract_laser' | 'anvil_bomb' | 'transmute_bubble';
  color: string;
  damage: number;
  isAutocast?: boolean;
}

export interface CrossTableLeap {
  id: string;
  unitId: string;
  unitName: string;
  fromTableIndex: number;
  toTableIndex: number;
  startX: number;
  startY: number;
  targetX: number;
  targetY: number;
  progress: number; // 0 to 1
  isChuteSlide: boolean;
  color: string;
}

