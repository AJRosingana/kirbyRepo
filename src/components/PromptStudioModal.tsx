/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { PortalSurface } from '../types';
import { audioEngine } from '../utils/audio';
import { Sparkles, Upload, Code2, Image as ImageIcon, PlusCircle, ArrowRight, Wand2, X } from 'lucide-react';
import confetti from 'canvas-confetti';

interface PromptStudioModalProps {
  isOpen: boolean;
  onClose: () => void;
  onPortalCreated: (newPortal: PortalSurface) => void;
}

export const PromptStudioModal: React.FC<PromptStudioModalProps> = ({
  isOpen,
  onClose,
  onPortalCreated,
}) => {
  const [activeTab, setActiveTab] = useState<'multimodal' | 'function_call'>('multimodal');
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [customPrompt, setCustomPrompt] = useState('');
  const [functionPrompt, setFunctionPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationLog, setGenerationLog] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setImagePreview(event.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  // Sample quick templates for inspiration
  const samplePrompts = [
    {
      title: 'Vaporwave Sunset Highway',
      prompt: 'A retro 80s outrun grid with chrome palm trees and a neon magenta setting sun with drifting grid lines.',
    },
    {
      title: 'Crystal Catacombs Core',
      prompt: 'A subterranean cavern with pulsing amethyst geometric crystals floating in zero gravity.',
    },
    {
      title: 'Hyper-Voxel Nebula',
      prompt: 'Volumetric glowing voxels swirling around an event horizon with dynamic chromatic aberration.',
    },
  ];

  const handleGenerateMultimodal = async () => {
    if (!imagePreview && !customPrompt) return;
    setIsGenerating(true);
    setGenerationLog('Gemini 3.7 Flash: Analyzing image composition, color palettes & vector motion...');

    try {
      // If user didn't upload an image, generate a stylish SVG placeholder or color canvas
      let base64Data = imagePreview;
      if (!base64Data) {
        // Fallback default sample base64 canvas
        const offscreen = document.createElement('canvas');
        offscreen.width = 120;
        offscreen.height = 120;
        const octx = offscreen.getContext('2d');
        if (octx) {
          octx.fillStyle = '#1e1b4b';
          octx.fillRect(0, 0, 120, 120);
          octx.fillStyle = '#ec4899';
          octx.beginPath();
          octx.arc(60, 60, 40, 0, Math.PI * 2);
          octx.fill();
        }
        base64Data = offscreen.toDataURL('image/png');
      }

      const res = await fetch('/api/portal/image-to-canvas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          imageBase64: base64Data,
          prompt: customPrompt,
        }),
      });

      const data = await res.json();
      if (data.portal) {
        setGenerationLog('Canvas 2D render loop compiled successfully. Mounting portal wall...');
        audioEngine.playSuccessFanfare();
        confetti({ particleCount: 60, spread: 70 });
        setTimeout(() => {
          onPortalCreated(data.portal);
          onClose();
        }, 600);
      } else {
        setGenerationLog('Generation failed: ' + (data.error || 'Unknown error'));
      }
    } catch (err) {
      setGenerationLog('Error contacting server: ' + String(err));
    } finally {
      setIsGenerating(false);
    }
  };

  const handleGenerateFunctionCall = async () => {
    if (!functionPrompt) return;
    setIsGenerating(true);
    setGenerationLog('Executing create_portal_surface schema with Gemini Function Calling...');

    try {
      const res = await fetch('/api/portal/expand', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userPrompt: functionPrompt,
        }),
      });

      const data = await res.json();
      if (data.portal) {
        setGenerationLog('Structured function invocation complete. Materializing portal in Macro Hall...');
        audioEngine.playSuccessFanfare();
        confetti({ particleCount: 60, spread: 70 });
        setTimeout(() => {
          onPortalCreated(data.portal);
          onClose();
        }, 600);
      } else {
        setGenerationLog('Function calling error: ' + (data.error || 'Unknown error'));
      }
    } catch (err) {
      setGenerationLog('Error calling expand API: ' + String(err));
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="relative w-full max-w-2xl bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="flex items-center justify-between p-4 sm:p-5 border-b border-slate-800 bg-slate-950/60">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-sky-500/10 border border-sky-500/30 text-sky-400">
              <Wand2 className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                AI Studio Portal Generator
                <span className="text-[10px] bg-amber-500/20 text-amber-300 border border-amber-500/30 px-2 py-0.5 rounded-full font-mono font-normal">
                  Gemini Multimodal & Function Calling
                </span>
              </h2>
              <p className="text-xs text-slate-400 font-mono">
                Synthesize new interactive 3D portal surfaces on demand
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center border-b border-slate-800 bg-slate-950/40 px-4">
          <button
            onClick={() => setActiveTab('multimodal')}
            className={`px-4 py-3 text-xs font-mono font-semibold flex items-center gap-2 border-b-2 transition-all ${
              activeTab === 'multimodal'
                ? 'border-sky-400 text-sky-300'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <ImageIcon className="w-4 h-4" />
            <span>1. Multimodal Image-to-Canvas</span>
          </button>

          <button
            onClick={() => setActiveTab('function_call')}
            className={`px-4 py-3 text-xs font-mono font-semibold flex items-center gap-2 border-b-2 transition-all ${
              activeTab === 'function_call'
                ? 'border-sky-400 text-sky-300'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Code2 className="w-4 h-4" />
            <span>2. Function Calling Tool (`create_portal_surface`)</span>
          </button>
        </div>

        {/* Tab 1: Multimodal Image-to-Canvas Converter */}
        {activeTab === 'multimodal' && (
          <div className="p-5 flex flex-col gap-4 overflow-y-auto">
            <p className="text-xs text-slate-300 leading-relaxed font-sans">
              Drop any retro game screenshot, pixel art, or concept sketch. Gemini analyzes the layout, colors, and key elements to write an executable 60 FPS HTML5 Canvas rendering script.
            </p>

            {/* Image Dropzone / Picker */}
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <label className="flex-1 w-full flex flex-col items-center justify-center h-36 border-2 border-dashed border-slate-700 hover:border-sky-500/60 rounded-xl bg-slate-950/60 hover:bg-slate-950 cursor-pointer transition-colors p-4 text-center">
                {imagePreview ? (
                  <img
                    src={imagePreview}
                    alt="Preview"
                    className="max-h-28 rounded object-contain"
                  />
                ) : (
                  <>
                    <Upload className="w-7 h-7 text-slate-400 mb-2" />
                    <span className="text-xs font-mono text-slate-300">
                      Click to upload screenshot or artwork
                    </span>
                    <span className="text-[10px] text-slate-500 font-mono mt-1">
                      PNG, JPG, WebP supported
                    </span>
                  </>
                )}
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </label>

              {imagePreview && (
                <button
                  onClick={() => setImagePreview(null)}
                  className="text-xs font-mono text-rose-400 hover:underline"
                >
                  Clear Image
                </button>
              )}
            </div>

            {/* Custom Prompt */}
            <div>
              <label className="block text-xs font-mono text-slate-300 mb-1.5">
                Stylistic Direction / Motion Guidance (Optional):
              </label>
              <input
                type="text"
                value={customPrompt}
                onChange={(e) => setCustomPrompt(e.target.value)}
                placeholder="e.g. Add swirling psychic spiral shaders, neon grid waves, or floating crystal particles..."
                className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-sky-400 font-sans"
              />
            </div>

            {/* Action Button */}
            <button
              onClick={handleGenerateMultimodal}
              disabled={isGenerating || (!imagePreview && !customPrompt)}
              className="w-full bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 disabled:opacity-40 text-white font-mono font-bold py-3 rounded-xl text-xs flex items-center justify-center gap-2 shadow-lg shadow-sky-900/40 transition-all active:scale-98"
            >
              <Sparkles className="w-4 h-4" />
              <span>{isGenerating ? 'Synthesizing Multimodal Portal...' : 'Synthesize Canvas Portal'}</span>
            </button>
          </div>
        )}

        {/* Tab 2: Function Calling Tool (`create_portal_surface`) */}
        {activeTab === 'function_call' && (
          <div className="p-5 flex flex-col gap-4 overflow-y-auto">
            <p className="text-xs text-slate-300 leading-relaxed font-sans">
              Provide natural language instructions. Gemini invokes the structured <code className="text-sky-300 bg-slate-950 px-1 py-0.5 rounded font-mono">create_portal_surface</code> tool to generate custom visual shaders, interactive mechanics, and procedural audio keys.
            </p>

            {/* Preset Prompt Pills */}
            <div className="flex flex-col gap-2">
              <span className="text-[11px] font-mono text-slate-400">Sample Concept Invocations:</span>
              <div className="flex flex-wrap gap-2">
                {samplePrompts.map((s, idx) => (
                  <button
                    key={idx}
                    onClick={() => setFunctionPrompt(s.prompt)}
                    className="text-[11px] bg-slate-950 hover:bg-slate-800 text-slate-300 border border-slate-800 hover:border-slate-600 px-2.5 py-1.5 rounded-lg transition-colors text-left"
                  >
                    ✦ {s.title}
                  </button>
                ))}
              </div>
            </div>

            {/* Prompt Textarea */}
            <div>
              <label className="block text-xs font-mono text-slate-300 mb-1.5">
                Portal World Concept & Mechanics:
              </label>
              <textarea
                rows={3}
                value={functionPrompt}
                onChange={(e) => setFunctionPrompt(e.target.value)}
                placeholder="Describe the environment, epoch style (8bit/16bit/32bit/ultra), ambient audio mood, and interactive canvas physics..."
                className="w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-sky-400 font-sans"
              />
            </div>

            {/* Action Button */}
            <button
              onClick={handleGenerateFunctionCall}
              disabled={isGenerating || !functionPrompt.trim()}
              className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 disabled:opacity-40 text-white font-mono font-bold py-3 rounded-xl text-xs flex items-center justify-center gap-2 shadow-lg shadow-emerald-900/40 transition-all active:scale-98"
            >
              <Code2 className="w-4 h-4" />
              <span>{isGenerating ? 'Invoking create_portal_surface...' : 'Execute Tool Invocation'}</span>
            </button>
          </div>
        )}

        {/* Live Terminal Log Banner */}
        {generationLog && (
          <div className="p-3 bg-slate-950 border-t border-slate-800 text-[11px] font-mono text-sky-400 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-sky-400 animate-ping" />
            <span>{generationLog}</span>
          </div>
        )}
      </div>
    </div>
  );
};
