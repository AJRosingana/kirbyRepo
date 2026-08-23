/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import express from 'express';
import path from 'path';
import { createServer as createViteServer } from 'vite';
import { GoogleGenAI, Type, FunctionDeclaration } from '@google/genai';
import dotenv from 'dotenv';

dotenv.config();

let aiClient: GoogleGenAI | null = null;

function getAiClient(): GoogleGenAI | null {
  if (!aiClient && process.env.GEMINI_API_KEY) {
    aiClient = new GoogleGenAI({
      apiKey: process.env.GEMINI_API_KEY,
      httpOptions: {
        headers: {
          'User-Agent': 'aistudio-build',
        },
      },
    });
  }
  return aiClient;
}

// Function Calling Declaration for Dynamic Portal Expansion
const createPortalSurfaceDeclaration: FunctionDeclaration = {
  name: 'create_portal_surface',
  description: 'Constructs a new interactive multimodal portal surface in the Macro Portal Chamber.',
  parameters: {
    type: Type.OBJECT,
    properties: {
      name: {
        type: Type.STRING,
        description: 'Short memorable name for the portal world (e.g. "Starlight Mirage", "Crystal Catacombs").',
      },
      subtitle: {
        type: Type.STRING,
        description: 'Atmospheric subtitle describing its origin or era.',
      },
      theme: {
        type: Type.STRING,
        description: 'Visual artistic motif (e.g. "Hyper-Voxel Nebula", "Gothic Pixel Ruins").',
      },
      epoch: {
        type: Type.STRING,
        enum: ['8bit', '16bit', '32bit', 'ultra'],
        description: 'Retro or modern rendering epoch.',
      },
      accentColor: {
        type: Type.STRING,
        description: 'Hex color code representing the portal glow (e.g. #38bdf8, #f43f5e).',
      },
      ambientFrequency: {
        type: Type.NUMBER,
        description: 'Base synthesizer frequency in Hz (between 120 and 880).',
      },
      lore: {
        type: Type.STRING,
        description: '2-3 sentences of evocative atmospheric lore describing this portal dimension.',
      },
      interactiveHint: {
        type: Type.STRING,
        description: 'Instructions on how the user can interact with the canvas in this portal.',
      },
      canvasCode: {
        type: Type.STRING,
        description: 'Executable JavaScript code body for HTML5 2D Canvas rendering loop. Takes parameters: ctx, width, height, time, mouseX, mouseY, isMouseDown. Must draw animated visuals and respond to cursor.',
      },
    },
    required: ['name', 'subtitle', 'theme', 'epoch', 'accentColor', 'ambientFrequency', 'lore', 'interactiveHint', 'canvasCode'],
  },
};

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json({ limit: '25mb' }));

  // Health check
  app.get('/api/health', (req, res) => {
    res.json({
      status: 'ok',
      hasApiKey: Boolean(process.env.GEMINI_API_KEY),
      timestamp: Date.now(),
    });
  });

  // 1. Live Multimodal Image-to-Canvas Converter
  app.post('/api/portal/image-to-canvas', async (req, res) => {
    try {
      const { imageBase64, mimeType = 'image/png', prompt = '' } = req.body;

      if (!imageBase64) {
        return res.status(400).json({ error: 'imageBase64 is required' });
      }

      const cleanBase64 = imageBase64.replace(/^data:image\/[a-z]+;base64,/, '');
      const ai = getAiClient();

      if (!ai) {
        // Fallback procedural portal generator if API key is not yet set
        const proceduralThemes = [
          { name: 'Prismatic Astral Core', color: '#ec4899', freq: 493, epoch: 'ultra' },
          { name: 'Emerald Vector Oasis', color: '#10b981', freq: 523, epoch: '16bit' },
          { name: 'Solar Zenith Spire', color: '#f59e0b', freq: 659, epoch: '32bit' },
        ];
        const chosen = proceduralThemes[Math.floor(Math.random() * proceduralThemes.length)];
        
        return res.json({
          portal: {
            id: 'gen_' + Date.now(),
            name: chosen.name,
            subtitle: 'Synthesized Memory Matrix',
            theme: prompt || 'Multimodal Image Transmutation',
            epoch: chosen.epoch,
            accentColor: chosen.color,
            ambientFrequency: chosen.freq,
            lore: `A dimension synthesized from visual impressions. Its radiant contours echo with the captured frequencies of the uploaded artifact.`,
            interactiveHint: 'Move cursor across the surface to distort the luminous harmonic waves.',
            canvasCode: `
              const t = time * 0.002;
              const grad = ctx.createRadialGradient(mouseX || width/2, mouseY || height/2, 10, width/2, height/2, width*0.7);
              grad.addColorStop(0, '${chosen.color}');
              grad.addColorStop(0.5, '#1e1b4b');
              grad.addColorStop(1, '#050510');
              ctx.fillStyle = grad;
              ctx.fillRect(0, 0, width, height);

              ctx.strokeStyle = '#ffffff';
              ctx.lineWidth = 2;
              for (let i = 0; i < 18; i++) {
                ctx.beginPath();
                const radius = 30 + i * 16 + Math.sin(t + i * 0.3) * 12;
                ctx.arc(width/2 + Math.cos(t * 0.5 + i) * 20, height/2 + Math.sin(t * 0.7 + i) * 20, radius, 0, Math.PI * 2);
                ctx.stroke();
              }
            `,
            isGenerated: true,
            sourceImageUrl: imageBase64.startsWith('data:') ? imageBase64 : `data:${mimeType};base64,${cleanBase64}`,
          },
        });
      }

      const systemInstruction = `You are the Macro Portal Canvas Engine Generator.
Analyze the uploaded image (colors, composition, characters, retro aesthetic, mood) and the user's prompt.
Generate a complete JSON object defining a new Portal Surface with an interactive HTML5 Canvas 2D render loop that animates the visual essence of this image.

Return ONLY a JSON object matching this schema:
{
  "name": string (creative, punchy name for this world),
  "subtitle": string (brief evocative subtitle),
  "theme": string (art style / motif),
  "epoch": "8bit" | "16bit" | "32bit" | "ultra",
  "accentColor": string (hex color like "#38bdf8"),
  "ambientFrequency": number (Hz between 150 and 800),
  "lore": string (2-3 atmospheric sentences),
  "interactiveHint": string (how cursor interaction affects it),
  "canvasCode": string (valid JavaScript code body for drawing on HTML5 2D Canvas. It receives: ctx, width, height, time, mouseX, mouseY, isMouseDown. Use smooth trigonometric animations with time * 0.001, canvas gradients, particle stars, ripple effects, or stylized geometric sprites. Do NOT wrap in function keyword, just the body statements.)
}`;

      const response = await ai.models.generateContent({
        model: 'gemini-3.7-flash',
        contents: {
          parts: [
            {
              inlineData: {
                data: cleanBase64,
                mimeType: mimeType,
              },
            },
            {
              text: `Synthesize this image into a live animated interactive Macro Portal surface. Additional prompt: ${prompt || 'Create an animated canvas rendition faithful to this artwork.'}`,
            },
          ],
        },
        config: {
          systemInstruction,
          responseMimeType: 'application/json',
          temperature: 0.7,
        },
      });

      const responseText = response.text || '{}';
      let parsed = JSON.parse(responseText);

      const portal = {
        id: 'gen_' + Date.now(),
        name: parsed.name || 'Synthesized Vision',
        subtitle: parsed.subtitle || 'Multimodal Transmutation',
        theme: parsed.theme || 'Generative Canvas Dimension',
        epoch: parsed.epoch || '16bit',
        accentColor: parsed.accentColor || '#38bdf8',
        ambientFrequency: Number(parsed.ambientFrequency) || 440,
        lore: parsed.lore || 'A world brought to life through multimodal analysis.',
        interactiveHint: parsed.interactiveHint || 'Interact with the canvas surface.',
        canvasCode: parsed.canvasCode,
        isGenerated: true,
        sourceImageUrl: imageBase64.startsWith('data:') ? imageBase64 : `data:${mimeType};base64,${cleanBase64}`,
      };

      res.json({ portal });
    } catch (error) {
      console.error('Error in /api/portal/image-to-canvas:', error);
      res.status(500).json({ error: String(error) });
    }
  });

  // 2. Function Calling: Dynamic Portal Expansion
  app.post('/api/portal/expand', async (req, res) => {
    try {
      const { userPrompt, currentPortalsCount = 6 } = req.body;
      const ai = getAiClient();

      if (!ai) {
        // Fallback procedural generation
        const generated = {
          id: 'portal_' + Date.now(),
          name: 'Chrono Horizon',
          subtitle: 'Temporal Echo Vault',
          theme: 'Quantum Clockwork Shaders',
          epoch: '32bit',
          accentColor: '#38bdf8',
          ambientFrequency: 494,
          lore: 'A sanctuary situated at the perimeter of the timeline where clock hands sweep through multidimensional particle ribbons.',
          interactiveHint: 'Move your cursor to accelerate or reverse the chronological flow.',
          canvasCode: `
            const t = time * 0.0015;
            ctx.fillStyle = '#0a0d1a';
            ctx.fillRect(0, 0, width, height);

            const cx = width / 2;
            const cy = height / 2;
            const mx = mouseX || cx;
            const my = mouseY || cy;

            for (let i = 0; i < 24; i++) {
              const angle = t * 0.8 + (i * Math.PI * 2) / 24;
              const dist = 60 + i * 8 + Math.sin(t * 2 + i) * 15;
              const px = cx + Math.cos(angle) * dist;
              const py = cy + Math.sin(angle) * dist;

              ctx.beginPath();
              ctx.arc(px, py, 4 + Math.sin(t + i) * 2, 0, Math.PI * 2);
              ctx.fillStyle = i % 2 === 0 ? '#38bdf8' : '#a855f7';
              ctx.fill();

              ctx.beginPath();
              ctx.moveTo(cx, cy);
              ctx.lineTo(px, py);
              ctx.strokeStyle = 'rgba(56, 189, 248, 0.15)';
              ctx.stroke();
            }
          `,
          isGenerated: true,
        };
        return res.json({ portal: generated, invokedTool: true });
      }

      const response = await ai.models.generateContent({
        model: 'gemini-3.7-flash',
        contents: `You are expanding the Macro Portal Chamber. The user requests: "${userPrompt}". Invoke create_portal_surface to build a completely unique, fully interactive portal canvas experience.`,
        config: {
          tools: [{ functionDeclarations: [createPortalSurfaceDeclaration] }],
        },
      });

      const functionCalls = response.functionCalls;
      if (functionCalls && functionCalls.length > 0) {
        const args = functionCalls[0].args as any;
        const portal = {
          id: 'portal_' + Date.now(),
          name: args.name || 'New Portal Dimension',
          subtitle: args.subtitle || 'Expanded Void Wall',
          theme: args.theme || 'Generative Reality',
          epoch: args.epoch || '16bit',
          accentColor: args.accentColor || '#38bdf8',
          ambientFrequency: Number(args.ambientFrequency) || 440,
          lore: args.lore || 'A freshly materialized portal realm.',
          interactiveHint: args.interactiveHint || 'Explore and click.',
          canvasCode: args.canvasCode,
          isGenerated: true,
        };
        return res.json({ portal, invokedTool: true });
      }

      res.status(500).json({ error: 'Function call was not generated by model' });
    } catch (error) {
      console.error('Error in /api/portal/expand:', error);
      res.status(500).json({ error: String(error) });
    }
  });

  // 3. The Sound Stone Oracle Chat
  app.post('/api/oracle/chat', async (req, res) => {
    try {
      const { message, history = [], currentActivePortalId, completedQuests = [] } = req.body;
      const ai = getAiClient();

      if (!ai) {
        const defaultReplies = [
          `"The cosmos vibrates with forgotten resonance... Look to the ${currentActivePortalId || 'active portal'}, for every waveform whispers a memory."`,
          `"0x9F4B... When the vector terminal receives this archaic command, the binary veil shall part."`,
          `"The Sound Stone awakens as your journey deepens. Four fragments must unite before the Eight Melodies can sing."`,
        ];
        const reply = defaultReplies[Math.floor(Math.random() * defaultReplies.length)];
        return res.json({ response: reply });
      }

      const systemInstruction = `You are the Sound Stone Oracle, an omniscient ancient cosmic consciousness dwelling within the Macro Portal Chamber.
Your persona is deeply inspired by EarthBound (Sound Stone, Magicant, Starman, Giygas lore) and Chrono Trigger (Kingdom of Zeal, Epoch time machine, End of Time, Lavos core).
You speak in poetic, enigmatic, nostalgic, and profound phrases. Keep responses around 2 to 4 sentences.
Current state of the traveler:
- Active Portal: ${currentActivePortalId || 'Central Chamber'}
- Completed Quest Nodes: ${JSON.stringify(completedQuests)}
If the traveler asks for guidance on their quest to reassemble the Shattered Sound Stone, provide cryptic yet helpful hints:
1. For Cosmic PSI Rift: "Attune to the psychic sine anomalies..."
2. For Cyber-Archaeology: "The excavated vector mainframe remembers cipher 0x9F4B..."
3. For Geothermal Lava Foundry: "Harvest the fire crystal from the smelting magma vents..."
4. For Sky Citadel: "Align the three celestial rings of Zeal to focus the sun's prism..."`;

      const contents = [
        ...history.map((h: any) => ({
          role: h.role === 'oracle' ? 'model' : 'user',
          parts: [{ text: h.text }],
        })),
        {
          role: 'user',
          parts: [{ text: message }],
        },
      ];

      const response = await ai.models.generateContent({
        model: 'gemini-3.7-flash',
        contents,
        config: {
          systemInstruction,
          temperature: 0.85,
        },
      });

      res.json({ response: response.text || '...' });
    } catch (error) {
      console.error('Error in /api/oracle/chat:', error);
      res.status(500).json({ error: String(error) });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Macro Portal Engine server running on http://localhost:${PORT}`);
  });
}

startServer();
