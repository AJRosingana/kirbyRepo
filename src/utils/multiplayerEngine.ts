/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { MultiplayerPlayer, MultiplayerRoomState, CustomBattlefield } from '../types';
import { DEFAULT_BATTLEFIELDS } from '../data/heroes';

const STORAGE_KEY_PROFILE = 'macro_portal_player_profile';
const STORAGE_KEY_BATTLEFIELDS = 'macro_portal_custom_battlefields';
const STORAGE_KEY_STATS = 'macro_portal_player_stats';

export interface PersistentProfile {
  id: string;
  name: string;
  avatar: string;
  level: number;
  xp: number;
  multiverseShards: number;
  unlockedHeroClasses: string[];
}

export interface PlayerStats {
  battlesWon: number;
  battlesPlayed: number;
  totalAutocastsTriggered: number;
  totalDamageDealt: number;
  worldsCreated: number;
}

class MultiplayerEngine {
  private channel: BroadcastChannel | null = null;
  private currentRoom: MultiplayerRoomState | null = null;
  private profile: PersistentProfile;
  private stats: PlayerStats;
  private customBattlefields: CustomBattlefield[] = [];
  private listeners: Array<(room: MultiplayerRoomState) => void> = [];
  private chatListeners: Array<(msg: MultiplayerRoomState['chatMessages'][0]) => void> = [];

  constructor() {
    this.profile = this.loadProfile();
    this.stats = this.loadStats();
    this.customBattlefields = this.loadBattlefields();
    this.initBroadcast();
  }

  private loadProfile(): PersistentProfile {
    try {
      const stored = localStorage.getItem(STORAGE_KEY_PROFILE);
      if (stored) {
        return JSON.parse(stored);
      }
    } catch {
      // Ignored
    }
    const defaultProfile: PersistentProfile = {
      id: 'player_' + Math.random().toString(36).substring(2, 8),
      name: 'Traveler-' + Math.floor(Math.random() * 900 + 100),
      avatar: '⚔️',
      level: 4,
      xp: 320,
      multiverseShards: 1250,
      unlockedHeroClasses: ['aether_knight', 'majin_kirby', 'adventurer', 'kirb_builder', 'pharaoh_scarab', 'cyber_tesseract'],
    };
    this.saveProfile(defaultProfile);
    return defaultProfile;
  }

  public saveProfile(profile: Partial<PersistentProfile>) {
    this.profile = { ...this.profile, ...profile };
    try {
      localStorage.setItem(STORAGE_KEY_PROFILE, JSON.stringify(this.profile));
    } catch {
      // Ignored
    }
  }

  public getProfile(): PersistentProfile {
    return this.profile;
  }

  private loadStats(): PlayerStats {
    try {
      const stored = localStorage.getItem(STORAGE_KEY_STATS);
      if (stored) return JSON.parse(stored);
    } catch {
      // Ignored
    }
    const defStats: PlayerStats = {
      battlesWon: 7,
      battlesPlayed: 9,
      totalAutocastsTriggered: 24,
      totalDamageDealt: 18450,
      worldsCreated: 2,
    };
    this.saveStats(defStats);
    return defStats;
  }

  public saveStats(stats: Partial<PlayerStats>) {
    this.stats = { ...this.stats, ...stats };
    try {
      localStorage.setItem(STORAGE_KEY_STATS, JSON.stringify(this.stats));
    } catch {
      // Ignored
    }
  }

  public getStats(): PlayerStats {
    return this.stats;
  }

  public addAutocastStat(dmg: number) {
    this.stats.totalAutocastsTriggered += 1;
    this.stats.totalDamageDealt += dmg;
    this.profile.xp += Math.round(dmg / 10);
    this.profile.multiverseShards += 50;
    if (this.profile.xp >= this.profile.level * 200) {
      this.profile.level += 1;
      this.profile.xp = 0;
    }
    this.saveStats(this.stats);
    this.saveProfile(this.profile);
  }

  public recordVictory() {
    this.stats.battlesWon += 1;
    this.stats.battlesPlayed += 1;
    this.profile.multiverseShards += 200;
    this.saveStats(this.stats);
    this.saveProfile(this.profile);
  }

  private loadBattlefields(): CustomBattlefield[] {
    try {
      const stored = localStorage.getItem(STORAGE_KEY_BATTLEFIELDS);
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch {
      // Ignored
    }
    return DEFAULT_BATTLEFIELDS;
  }

  public saveBattlefield(field: CustomBattlefield) {
    const existingIdx = this.customBattlefields.findIndex((f) => f.id === field.id);
    if (existingIdx >= 0) {
      this.customBattlefields[existingIdx] = field;
    } else {
      this.customBattlefields.unshift(field);
    }
    this.stats.worldsCreated += 1;
    try {
      localStorage.setItem(STORAGE_KEY_BATTLEFIELDS, JSON.stringify(this.customBattlefields));
    } catch {
      // Ignored
    }
  }

  public getBattlefields(): CustomBattlefield[] {
    return this.customBattlefields;
  }

  // Cross-Tab BroadcastChannel Setup
  private initBroadcast() {
    try {
      if (typeof window !== 'undefined' && 'BroadcastChannel' in window) {
        this.channel = new BroadcastChannel('macro_portal_multiplayer_bus');
        this.channel.onmessage = (event) => {
          this.handleBroadcastMessage(event.data);
        };
      }
    } catch {
      // BroadcastChannel unavailable in some sandbox environments
    }
  }

  private handleBroadcastMessage(data: { type: string; payload: unknown }) {
    if (!data) return;
    if (data.type === 'SYNC_ROOM' && data.payload) {
      const room = data.payload as MultiplayerRoomState;
      if (this.currentRoom && this.currentRoom.roomId === room.roomId) {
        this.currentRoom = room;
        this.notifyListeners();
      }
    } else if (data.type === 'NEW_CHAT' && data.payload) {
      const msg = data.payload as MultiplayerRoomState['chatMessages'][0];
      if (this.currentRoom) {
        this.currentRoom.chatMessages.push(msg);
        this.notifyChatListeners(msg);
        this.notifyListeners();
      }
    }
  }

  public createRoom(roomName: string, gameMode: MultiplayerRoomState['gameMode'] = 'coop_boss_raid'): MultiplayerRoomState {
    const roomId = 'MP-' + Math.random().toString(36).substring(2, 6).toUpperCase();
    const hostPlayer: MultiplayerPlayer = {
      id: this.profile.id,
      name: this.profile.name,
      avatar: this.profile.avatar,
      isReady: true,
      heroClass: 'aether_knight',
      level: this.profile.level,
      ping: 28,
      isHost: true,
    };

    // Add 1-2 Simulated Co-op Party members for instant engaging multiplayer feel
    const ally1: MultiplayerPlayer = {
      id: 'peer_buu_' + Math.random().toString(36).substring(2, 5),
      name: 'Mallow-Spark',
      avatar: '🍬',
      isReady: true,
      heroClass: 'majin_kirby',
      level: 6,
      ping: 42,
    };

    const ally2: MultiplayerPlayer = {
      id: 'peer_foreman_' + Math.random().toString(36).substring(2, 5),
      name: 'VoxelForeman',
      avatar: '👷',
      isReady: true,
      heroClass: 'kirb_builder',
      level: 5,
      ping: 35,
    };

    const newRoom: MultiplayerRoomState = {
      roomId,
      roomName: roomName || `Multiverse Nexus #${roomId}`,
      hostId: this.profile.id,
      players: [hostPlayer, ally1, ally2],
      gameMode,
      battlefieldId: this.customBattlefields[0]?.id || 'field_dreamland_citadel',
      round: 1,
      isActive: true,
      maxPlayers: 4,
      chatMessages: [
        {
          id: 'm1',
          sender: 'SYSTEM',
          text: `Room ${roomId} created! Connected to 3D Multiverse Synchronizer.`,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          type: 'system',
        },
        {
          id: 'm2',
          sender: 'Mallow-Spark',
          text: '🍬 Ready for the raid! Charging up 3X Chocolate Nova!',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          type: 'chat',
        },
      ],
    };

    this.currentRoom = newRoom;
    this.broadcast({ type: 'SYNC_ROOM', payload: newRoom });
    this.notifyListeners();
    return newRoom;
  }

  public joinRoom(roomId: string): MultiplayerRoomState {
    if (this.currentRoom && this.currentRoom.roomId === roomId.toUpperCase()) {
      return this.currentRoom;
    }
    const joined = this.createRoom(`Chamber ${roomId.toUpperCase()}`);
    joined.roomId = roomId.toUpperCase();
    this.currentRoom = joined;
    this.notifyListeners();
    return joined;
  }

  public getCurrentRoom(): MultiplayerRoomState {
    if (!this.currentRoom) {
      return this.createRoom('Alpha Nexus Co-op Raid');
    }
    return this.currentRoom;
  }

  public sendChatMessage(text: string, type: 'chat' | 'autocast' | 'cast' | 'system' = 'chat') {
    if (!this.currentRoom) return;
    const newMsg: MultiplayerRoomState['chatMessages'][0] = {
      id: 'msg_' + Date.now() + '_' + Math.random().toString(36).substring(2, 5),
      sender: type === 'system' ? 'SYSTEM' : this.profile.name,
      text,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
      type,
    };
    this.currentRoom.chatMessages.push(newMsg);
    if (this.currentRoom.chatMessages.length > 50) {
      this.currentRoom.chatMessages.shift();
    }
    this.broadcast({ type: 'NEW_CHAT', payload: newMsg });
    this.broadcast({ type: 'SYNC_ROOM', payload: this.currentRoom });
    this.notifyChatListeners(newMsg);
    this.notifyListeners();
  }

  public selectHero(heroClass: MultiplayerPlayer['heroClass']) {
    if (!this.currentRoom) return;
    const p = this.currentRoom.players.find((pl) => pl.id === this.profile.id);
    if (p) {
      p.heroClass = heroClass;
      this.broadcast({ type: 'SYNC_ROOM', payload: this.currentRoom });
      this.notifyListeners();
    }
  }

  public setBattlefield(fieldId: string) {
    if (!this.currentRoom) return;
    this.currentRoom.battlefieldId = fieldId;
    this.sendChatMessage(`Host updated the battlefield terrain map to ${fieldId}`, 'system');
    this.broadcast({ type: 'SYNC_ROOM', payload: this.currentRoom });
    this.notifyListeners();
  }

  private broadcast(data: { type: string; payload: unknown }) {
    try {
      if (this.channel) {
        this.channel.postMessage(data);
      }
    } catch {
      // Ignored
    }
  }

  public subscribe(cb: (room: MultiplayerRoomState) => void) {
    this.listeners.push(cb);
    return () => {
      this.listeners = this.listeners.filter((l) => l !== cb);
    };
  }

  public subscribeChat(cb: (msg: MultiplayerRoomState['chatMessages'][0]) => void) {
    this.chatListeners.push(cb);
    return () => {
      this.chatListeners = this.chatListeners.filter((l) => l !== cb);
    };
  }

  private notifyListeners() {
    if (this.currentRoom) {
      this.listeners.forEach((cb) => cb(this.currentRoom!));
    }
  }

  private notifyChatListeners(msg: MultiplayerRoomState['chatMessages'][0]) {
    this.chatListeners.forEach((cb) => cb(msg));
  }
}

export const multiplayerEngine = new MultiplayerEngine();
