/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { PortalSurface, QuestNode } from '../types';

export const INITIAL_PORTALS: PortalSurface[] = [
  {
    id: 'pharaoh_tomb',
    name: "Pharaoh's Radiant Dune Gate",
    subtitle: 'Golden Pyramid & Scarab Slime Domain',
    theme: 'Egyptian Hieroglyphics & Solar Amulet',
    epoch: '16bit',
    accentColor: '#eab308',
    frameStyle: 'pharaoh',
    ambientFrequency: 392, // G4
    lore: 'An ancient pyramid gate guarding the sacred solar cartridge. Scarab slimes crawl along golden sand dunes while radiant Ka spirits refract celestial sunlight through lapis lazuli obelisks.',
    interactiveHint: 'Click radiant Ka energy spheres and guide wandering Scarab Slimes across the sands.',
    questNodeId: 'node_pharaoh',
  },
  {
    id: 'cosmic_psi_rift',
    name: 'Cosmic PSI Rift',
    subtitle: 'Magicant / Giygas Sine Matrix',
    theme: 'Psychotropic Cosmic Waveform',
    epoch: '16bit',
    accentColor: '#f43f5e',
    frameStyle: 'cosmic',
    ambientFrequency: 440,
    lore: 'A distortion in psychic spacetime reminiscent of Magicant. Sine waves warp reality as psychic energy coalesces into sound vibrations.',
    interactiveHint: 'Click to emit PSI resonance pulses and align the psychic nodes.',
    questNodeId: 'node_psi',
  },
  {
    id: 'cyber_archaeology',
    name: 'Cyber-Archaeology Grid',
    subtitle: 'Vector Matrix & Hex Vault',
    theme: '1983 Phosphor CRT Vector Wireframe',
    epoch: '8bit',
    accentColor: '#10b981',
    frameStyle: 'cyber',
    ambientFrequency: 520,
    lore: 'An unearthed mainframe from the dawn of digital computing. Decipher the archaic hex code 0x9F4B to restore the forgotten knowledge node.',
    interactiveHint: 'Interact with the 3D rotating vector core and input the access cipher.',
    questNodeId: 'node_cyber',
  },
  {
    id: 'sky_citadel',
    name: 'High-Altitude Sky Citadel',
    subtitle: 'Kingdom of Zeal Floating Island',
    theme: 'Aetheric Wind & Sun Flare Sanctuary',
    epoch: '16bit',
    accentColor: '#38bdf8',
    frameStyle: 'sky',
    ambientFrequency: 659,
    lore: 'Suspended in the stratosphere by ancient anti-gravity monoliths. Three golden concentric harmonic rings keep the islands from plummeting.',
    interactiveHint: 'Drag the rotating celestial rings to align their solar crests.',
    questNodeId: 'node_sky',
  },
  {
    id: 'lava_foundry',
    name: 'Geothermal Lava Foundry',
    subtitle: 'Sub-Terra Molten Core',
    theme: 'Smelting Magma & Anvil Sparks',
    epoch: '32bit',
    accentColor: '#f97316',
    frameStyle: 'magma',
    ambientFrequency: 180,
    lore: 'A subterranean forge fueled by liquid mantle. The intense heat refracts ambient light while heavy sub-bass vibrations shake the stone walls.',
    interactiveHint: 'Click bubbling magma veins to smelt and harvest the Primordial Fire Crystal.',
    questNodeId: 'node_foundry',
  },
  {
    id: 'spore_forest',
    name: 'Bioluminescent Spore Network',
    subtitle: 'Living Mycelium Simulation',
    theme: 'Luminescent Flora & Worker Sprites',
    epoch: 'ultra',
    accentColor: '#a855f7',
    frameStyle: 'spore',
    ambientFrequency: 330,
    lore: 'A thriving subterranean eco-system where mini spore workers ferry energy between giant glowing mushrooms across organic light-bridges.',
    interactiveHint: 'Click empty ground to plant glowing mushrooms; click mushrooms to release chime spores.',
    questNodeId: 'node_spore',
  },
  {
    id: 'epoch_matrix',
    name: 'Bit-Shift Epoch Shifter',
    subtitle: 'Chrono-Visual Time Transmutation',
    theme: 'Multi-Generation Render Pipeline',
    epoch: '8bit',
    accentColor: '#06b6d4',
    frameStyle: 'matrix',
    ambientFrequency: 587,
    lore: 'A reality synthesizer that seamlessly transmutates visual physics across 8-bit NES, 16-bit SNES Mode-7, 32-bit PS1 dither, and Ultra raymarched shaders.',
    interactiveHint: 'Switch era modes to transform the live visual pipeline and sound frequency.',
  },
];

export const INITIAL_QUEST_NODES: QuestNode[] = [
  {
    id: 'node_pharaoh',
    title: 'Solar Ka Awakening',
    portalId: 'pharaoh_tomb',
    description: 'Awaken the sacred golden pyramid by touching 3 radiant Ka sun orbs floating above the shifting dunes.',
    objective: 'Harmonize 3 Radiant Ka sun orbs in the Pharaoh Gate.',
    completed: false,
    melodyNote: 1, // Note 2
    loreFragment: 'The Pharaohs etched the primordial second chord into the gold capstone of the pyramid.',
  },
  {
    id: 'node_psi',
    title: 'PSI Harmonization',
    portalId: 'cosmic_psi_rift',
    description: 'Stabilize the psychic frequency by finding and activating 3 resonant PSI nodes within the cosmic rift.',
    objective: 'Click 3 pulsing psychic anomalies in the PSI Rift.',
    completed: false,
    melodyNote: 0, // Note 1
    loreFragment: 'The first melody echoes from the childhood memories of an alien world.',
  },
  {
    id: 'node_cyber',
    title: 'Vector Mainframe Decipher',
    portalId: 'cyber_archaeology',
    description: 'Input the excavated hex memory cipher 0x9F4B into the phosphor CRT vector terminal.',
    objective: 'Unlock the vector vault with hex code 0x9F4B.',
    completed: false,
    targetValue: '0x9F4B',
    melodyNote: 2, // Note 3
    loreFragment: 'The second melody was preserved in binary parity bits by ancient cyber-archaeologists.',
  },
  {
    id: 'node_foundry',
    title: 'Primordial Fire Crystal',
    portalId: 'lava_foundry',
    description: 'Smelt molten magma vents to forge the radiant Fire Crystal necessary to fuel the sound stone.',
    objective: 'Harvest 3 magma charge crystals from the foundry vents.',
    completed: false,
    melodyNote: 4, // Note 5
    loreFragment: 'The third melody burns with the heat of the planet’s unyielding core.',
  },
  {
    id: 'node_sky',
    title: 'Zeal Ring Alignment',
    portalId: 'sky_citadel',
    description: 'Align the 3 celestial concentric rings of the Sky Citadel to focus the sunlight into the Sound Stone prism.',
    objective: 'Align the concentric rings to 100% resonance.',
    completed: false,
    melodyNote: 7, // Note 8
    loreFragment: 'The final melody drifts down from the kingdom that once ruled the skies.',
  },
];

export const SAMPLE_ORACLE_RESPONSES = [
  "The Sound Stone remembers what time has scattered... Go forth, traveler, and seek the frequency of the rift.",
  "0x9F4B... An archaic hex instruction from a universe running on 8 bits. The vector grid yearns for its key.",
  "Can you hear the magma singing beneath your feet? Only when tempered in the forge will the stone resonate.",
  "When the three rings of Zeal align, the heavens open and the Eight Melodies become one.",
  "You hold a memory in your hands. Upload an artifact of old, and Gemini shall paint its soul across the portal chamber.",
];
