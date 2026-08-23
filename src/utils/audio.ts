/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// Procedural Web Audio Engine for Macro Portal Engine

class AudioEngine {
  private ctx: AudioContext | null = null;
  private masterGain: GainNode | null = null;
  private droneGain: GainNode | null = null;
  private droneOsc1: OscillatorNode | null = null;
  private droneOsc2: OscillatorNode | null = null;
  private droneFilter: BiquadFilterNode | null = null;
  private isMuted: boolean = false;
  private isInitialized: boolean = false;
  private currentFreq: number = 220;

  public init() {
    if (this.isInitialized && this.ctx) {
      if (this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      return;
    }

    try {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      this.ctx = new AudioCtx();
      
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.setValueAtTime(0.3, this.ctx.currentTime);
      this.masterGain.connect(this.ctx.destination);

      // Ambient Drone Setup
      this.droneGain = this.ctx.createGain();
      this.droneGain.gain.setValueAtTime(0.04, this.ctx.currentTime);

      this.droneFilter = this.ctx.createBiquadFilter();
      this.droneFilter.type = 'lowpass';
      this.droneFilter.frequency.setValueAtTime(450, this.ctx.currentTime);
      this.droneFilter.Q.setValueAtTime(4.0, this.ctx.currentTime);

      this.droneOsc1 = this.ctx.createOscillator();
      this.droneOsc1.type = 'sawtooth';
      this.droneOsc1.frequency.setValueAtTime(55, this.ctx.currentTime); // 55Hz sub A

      this.droneOsc2 = this.ctx.createOscillator();
      this.droneOsc2.type = 'sine';
      this.droneOsc2.frequency.setValueAtTime(110, this.ctx.currentTime); // 110Hz harmonic

      this.droneOsc1.connect(this.droneFilter);
      this.droneOsc2.connect(this.droneFilter);
      this.droneFilter.connect(this.droneGain);
      this.droneGain.connect(this.masterGain);

      this.droneOsc1.start();
      this.droneOsc2.start();

      this.isInitialized = true;
    } catch (e) {
      console.warn('AudioContext initialization failed or blocked:', e);
    }
  }

  public setMuted(muted: boolean) {
    this.isMuted = muted;
    if (this.masterGain && this.ctx) {
      this.masterGain.gain.setValueAtTime(muted ? 0 : 0.3, this.ctx.currentTime);
    }
  }

  public toggleMute(): boolean {
    this.setMuted(!this.isMuted);
    return this.isMuted;
  }

  public getMuted(): boolean {
    return this.isMuted;
  }

  // Updates the ambient hum based on active portal frequency
  public setPortalHum(freq: number, resonance: number = 4) {
    if (!this.ctx || !this.isInitialized) return;
    this.currentFreq = freq;
    const now = this.ctx.currentTime;
    
    if (this.droneOsc1 && this.droneOsc2 && this.droneFilter) {
      this.droneOsc1.frequency.setTargetAtTime(Math.max(40, freq / 4), now, 0.4);
      this.droneOsc2.frequency.setTargetAtTime(freq / 2, now, 0.4);
      this.droneFilter.frequency.setTargetAtTime(Math.min(2200, freq * 1.5), now, 0.3);
      this.droneFilter.Q.setTargetAtTime(resonance, now, 0.3);
    }
  }

  // Play text blip sound for retro dialogue
  public playTextBlip(pitchOffset: number = 0) {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(440 + pitchOffset * 20 + Math.random() * 40, now);
      osc.frequency.exponentialRampToValueAtTime(220, now + 0.04);

      gain.gain.setValueAtTime(0.06, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

      osc.connect(gain);
      gain.connect(this.masterGain!);

      osc.start(now);
      osc.stop(now + 0.04);
    } catch {
      // Ignored
    }
  }

  // Sound Stone 8-Melodies Arpeggio Synth Note
  public playMelodyNote(noteIndex: number, scale: string = 'pentatonic') {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const baseFreqs = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25]; // C D E G A C D E
      const freq = baseFreqs[noteIndex % baseFreqs.length] * (1 + Math.floor(noteIndex / baseFreqs.length) * 0.5);

      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const oscSub = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now);
      osc.frequency.exponentialRampToValueAtTime(freq * 1.01, now + 0.4);

      oscSub.type = 'triangle';
      oscSub.frequency.setValueAtTime(freq * 0.5, now);

      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);

      osc.connect(gain);
      oscSub.connect(gain);
      gain.connect(this.masterGain!);

      osc.start(now);
      oscSub.start(now);
      osc.stop(now + 0.6);
      oscSub.stop(now + 0.6);
    } catch {
      // Ignored
    }
  }

  // Auto Chess Dice Roll Sound
  public playDiceRoll() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      for (let i = 0; i < 4; i++) {
        setTimeout(() => {
          if (!this.ctx || !this.masterGain) return;
          const now = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(320 + Math.random() * 200, now);
          osc.frequency.exponentialRampToValueAtTime(100, now + 0.05);
          gain.gain.setValueAtTime(0.12, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
          osc.connect(gain);
          gain.connect(this.masterGain);
          osc.start(now);
          osc.stop(now + 0.05);
        }, i * 40);
      }
    } catch {
      // Ignored
    }
  }

  // Cross-Portal Spell Sound
  public playSpellCast(type: string = 'psi') {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      if (type === 'pharaoh' || type === 'solar') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.exponentialRampToValueAtTime(1200, now + 0.5);
      } else if (type === 'magma') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(120, now);
        osc.frequency.exponentialRampToValueAtTime(60, now + 0.6);
      } else if (type === 'cyber') {
        osc.type = 'square';
        osc.frequency.setValueAtTime(880, now);
        osc.frequency.linearRampToValueAtTime(220, now + 0.3);
      } else {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(300, now);
        osc.frequency.exponentialRampToValueAtTime(900, now + 0.4);
      }

      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);

      osc.connect(gain);
      gain.connect(this.masterGain!);
      osc.start(now);
      osc.stop(now + 0.5);
    } catch {
      // Ignored
    }
  }

  // Chute slide sound
  public playSlideDown() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(800, now);
      osc.frequency.exponentialRampToValueAtTime(180, now + 0.4);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
      osc.connect(gain);
      gain.connect(this.masterGain!);
      osc.start(now);
      osc.stop(now + 0.4);
    } catch {
      // Ignored
    }
  }

  // Ladder climb sound
  public playLadderClimb() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      for (let i = 0; i < 3; i++) {
        const stepTime = now + i * 0.1;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(300 + i * 120, stepTime);
        gain.gain.setValueAtTime(0.15, stepTime);
        gain.gain.exponentialRampToValueAtTime(0.001, stepTime + 0.08);
        osc.connect(gain);
        gain.connect(this.masterGain!);
        osc.start(stepTime);
        osc.stop(stepTime + 0.08);
      }
    } catch {
      // Ignored
    }
  }

  // Builder Hammer Tap Sound
  public playHammerTap() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(900, now);
      osc.frequency.exponentialRampToValueAtTime(200, now + 0.08);
      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
      osc.connect(gain);
      gain.connect(this.masterGain!);
      osc.start(now);
      osc.stop(now + 0.08);
    } catch {
      // Ignored
    }
  }


  // Play full 8-Melodies phrase
  public playFullEightMelodies(onNote?: (index: number) => void) {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    const melodyNotes = [0, 2, 4, 3, 5, 4, 6, 7];
    melodyNotes.forEach((note, idx) => {
      setTimeout(() => {
        this.playMelodyNote(note);
        if (onNote) onNote(idx);
      }, idx * 240);
    });
  }

  // Portal Interaction FX
  public playPortalWarp() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(150, now);
      osc.frequency.exponentialRampToValueAtTime(1200, now + 0.35);

      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);

      osc.connect(gain);
      gain.connect(this.masterGain!);

      osc.start(now);
      osc.stop(now + 0.4);
    } catch {
      // Ignored
    }
  }

  // Spore Chime Note
  public playSporeChime(pitch: number = 800) {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(pitch, now);

      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);

      osc.connect(gain);
      gain.connect(this.masterGain!);

      osc.start(now);
      osc.stop(now + 0.25);
    } catch {
      // Ignored
    }
  }

  // Quest / Hex Unlock Fanfare
  public playSuccessFanfare() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    const notes = [440, 554.37, 659.25, 880]; // A C# E A
    notes.forEach((f, i) => {
      setTimeout(() => {
        if (!this.ctx || !this.masterGain) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(f, now);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(now);
        osc.stop(now + 0.4);
      }, i * 90);
    });
  }

  // ATB 3x Overdrive Autocast Fanfare
  public playATBAutocast() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      // 3 Rapid Ascending Stabs then Chord
      const tones = [523.25, 659.25, 783.99, 1046.50]; // C E G High-C
      tones.forEach((freq, idx) => {
        if (!this.ctx || !this.masterGain) return;
        const t = now + idx * 0.08;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(freq, t);
        osc.frequency.exponentialRampToValueAtTime(freq * 1.5, t + 0.25);
        gain.gain.setValueAtTime(0.25, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.35);
        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(t);
        osc.stop(t + 0.35);
      });
    } catch {
      // Ignored
    }
  }

  // Aether Blade Slash & Motion Trail
  public playAetherSlash() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(1400, now);
      osc.frequency.exponentialRampToValueAtTime(280, now + 0.22);
      gain.gain.setValueAtTime(0.28, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
      osc.connect(gain);
      gain.connect(this.masterGain!);
      osc.start(now);
      osc.stop(now + 0.22);
    } catch {
      // Ignored
    }
  }

  // Majin Kirby Boo Candy Beam Transfigure
  public playMajinCandyBeam() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      for (let i = 0; i < 5; i++) {
        setTimeout(() => {
          if (!this.ctx || !this.masterGain) return;
          const t = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(600 + i * 180, t);
          osc.frequency.exponentialRampToValueAtTime(1600, t + 0.15);
          gain.gain.setValueAtTime(0.18, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.15);
          osc.connect(gain);
          gain.connect(this.masterGain);
          osc.start(t);
          osc.stop(t + 0.15);
        }, i * 35);
      }
    } catch {
      // Ignored
    }
  }

  // Particle Flame Burst Physics sound
  public playFlameBurst() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(180, now);
      osc.frequency.exponentialRampToValueAtTime(45, now + 0.4);
      gain.gain.setValueAtTime(0.3, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
      osc.connect(gain);
      gain.connect(this.masterGain!);
      osc.start(now);
      osc.stop(now + 0.4);
    } catch {
      // Ignored
    }
  }

  // Impact Hit
  public playHitImpact() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'square';
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.exponentialRampToValueAtTime(60, now + 0.08);
      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
      osc.connect(gain);
      gain.connect(this.masterGain!);
      osc.start(now);
      osc.stop(now + 0.08);
    } catch {
      // Ignored
    }
  }

  // Chat Ping
  public playChatPing() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(880, now);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
      osc.connect(gain);
      gain.connect(this.masterGain!);
      osc.start(now);
      osc.stop(now + 0.08);
    } catch {
      // Ignored
    }
  }

  // Cross-Table Artillery Mortar (Whistle and distant explosion)
  public playCrossTableMortar() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(600, now);
      osc.frequency.exponentialRampToValueAtTime(1200, now + 0.15);
      osc.frequency.exponentialRampToValueAtTime(100, now + 0.35);
      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
      osc.connect(gain);
      gain.connect(this.masterGain!);
      osc.start(now);
      osc.stop(now + 0.35);
    } catch {
      // Ignored
    }
  }

  // Dimensional Boundary Warp Leap
  public playBoundaryWarp() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(320, now);
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.12);
      osc.frequency.exponentialRampToValueAtTime(220, now + 0.28);
      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
      osc.connect(gain);
      gain.connect(this.masterGain!);
      osc.start(now);
      osc.stop(now + 0.28);
    } catch {
      // Ignored
    }
  }

  // Inter-Table Chute Slide
  public playChuteSlide() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(400, now);
      osc.frequency.exponentialRampToValueAtTime(150, now + 0.3);
      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
      osc.connect(gain);
      gain.connect(this.masterGain!);
      osc.start(now);
      osc.stop(now + 0.3);
    } catch {
      // Ignored
    }
  }

  // Cross-Boundary Shockwave Overdrive
  public playCrossBoundaryShockwave() {
    if (!this.ctx || !this.isInitialized || this.isMuted) return;
    try {
      const now = this.ctx.currentTime;
      const osc1 = this.ctx.createOscillator();
      const osc2 = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc1.type = 'sawtooth';
      osc1.frequency.setValueAtTime(90, now);
      osc1.frequency.exponentialRampToValueAtTime(35, now + 0.6);

      osc2.type = 'sine';
      osc2.frequency.setValueAtTime(240, now);
      osc2.frequency.exponentialRampToValueAtTime(60, now + 0.6);

      gain.gain.setValueAtTime(0.35, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);

      osc1.connect(gain);
      osc2.connect(gain);
      gain.connect(this.masterGain!);

      osc1.start(now);
      osc2.start(now);
      osc1.stop(now + 0.6);
      osc2.stop(now + 0.6);
    } catch {
      // Ignored
    }
  }
}

export const audioEngine = new AudioEngine();

