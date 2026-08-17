// frontend/src/components/ChatInput.tsx
"use client";

import React from "react";
import { useVoiceRecording } from "../hooks/useVoiceRecording";
import { useAudioVisualizer } from "../hooks/useAudioVisualizer";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:7860";

interface ChatInputProps {
  input?: string;
  setInput?: (val: string) => void;
  handleSubmit?: (e: React.FormEvent, overrideInput?: string) => void;
  isStreaming?: boolean;
  isWaitingForApproval?: boolean; // <-- [PHASE 7 NEW] Optional prop for backward compatibility
  onStop?: () => void; // <-- [NEW] Optional stop callback
}

export default function ChatInput({
  input = "",
  setInput = () => {},
  handleSubmit = (e) => e.preventDefault(),
  isStreaming = false,
  isWaitingForApproval = false, // <-- [PHASE 7 NEW] Default value
  onStop = () => {}, // <-- [NEW] Default handler
}: ChatInputProps) {
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);
  const ignoreVoiceUpdatesRef = React.useRef(false);

  const { transcript, isListening, startRecording, stopRecording, resetTranscript, browserSupportsSpeechRecognition } = useVoiceRecording();
  const audioData = useAudioVisualizer(isListening, 20);
  const [inputBeforeRecording, setInputBeforeRecording] = React.useState("");
  const [mounted, setMounted] = React.useState(false);
  const [isRefining, setIsRefining] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  React.useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    // Reset height to calculate scrollHeight correctly
    textarea.style.height = "auto";
    // Set height based on scrollHeight, cap at 200px
    textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
  }, [input, isListening]);

  React.useEffect(() => {
    console.log("[ChatInput Debug] useEffect triggered | isListening:", isListening, "| transcript:", transcript, "| ignoreVoice:", ignoreVoiceUpdatesRef.current);
    if (ignoreVoiceUpdatesRef.current) {
      if (!isListening && !transcript) {
        ignoreVoiceUpdatesRef.current = false;
      }
      return;
    }
    if (isListening || transcript) { // <-- allow updating even if isListening just became false
      const newText = inputBeforeRecording ? `${inputBeforeRecording} ${transcript}` : transcript;
      console.log("[ChatInput Debug] Setting input to:", newText);
      setInput(newText);
    }
  }, [transcript, isListening, inputBeforeRecording, setInput]);

  const handleStartRecording = () => {
    console.log("[ChatInput Debug] Starting recording");
    ignoreVoiceUpdatesRef.current = false;
    setInputBeforeRecording(input);
    startRecording();
  };

  const handleStopRecordingLocal = async (): Promise<string | null> => {
    console.log("[ChatInput Debug] Stopping recording");
    stopRecording();
    
    const currentTranscript = transcript;
    if (!currentTranscript.trim()) return null;

    setIsRefining(true);
    ignoreVoiceUpdatesRef.current = true; // Stop real-time updates

    let finalRefinedText = currentTranscript;
    try {
      const response = await fetch(`${API_BASE_URL}/refine_transcript`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript: currentTranscript }),
      });
      const data = await response.json();
      
      const refinedText = data.refined_transcript || currentTranscript;
      finalRefinedText = inputBeforeRecording ? `${inputBeforeRecording} ${refinedText}` : refinedText;
      setInput(finalRefinedText);
    } catch (err) {
      console.error("Failed to refine transcript:", err);
      finalRefinedText = inputBeforeRecording ? `${inputBeforeRecording} ${currentTranscript}` : currentTranscript;
      setInput(finalRefinedText);
    } finally {
      setIsRefining(false);
      resetTranscript();
    }
    return finalRefinedText;
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (input.trim() && !isStreaming && !isWaitingForApproval && !isListening) {
        const form = e.currentTarget.form;
        if (form) {
          form.requestSubmit();
        }
      }
    }
  };

  const onFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isListening) {
      console.log("[ChatInput Debug] Stopping recording on send");
      const refinedText = await handleStopRecordingLocal();
      if (refinedText && !isStreaming && !isWaitingForApproval) {
        ignoreVoiceUpdatesRef.current = true;
        handleSubmit(e, refinedText);
        setInputBeforeRecording("");
      }
      return;
    }
    if (input.trim() && !isStreaming && !isWaitingForApproval) {
      ignoreVoiceUpdatesRef.current = true;
      handleSubmit(e);
      // Clear the internal transcript so it doesn't re-populate the input on the next render
      resetTranscript(); 
      setInputBeforeRecording("");
    }
  };

  return (
    <footer className="bg-white border-t border-gray-200 p-4">
      <div className="max-w-4xl mx-auto">
        <form onSubmit={onFormSubmit} className="flex gap-2 items-end">
          {isListening ? (
            <div className="flex-1 flex items-center px-4 h-[48px] bg-gray-50 rounded-2xl border border-gray-200 overflow-hidden">
              <div className="flex gap-1 items-center h-full">
                {audioData.map((height, i) => (
                  <div 
                    key={i} 
                    className="w-1.5 bg-blue-400 rounded-full opacity-70 transition-all duration-75 ease-out" 
                    style={{ height: `${height}%` }}
                  ></div>
                ))}
              </div>
              <span className="ml-4 text-sm text-gray-500 font-medium">Listening...</span>
            </div>
          ) : (
            <textarea
              ref={textareaRef}
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isStreaming || isWaitingForApproval || isRefining}
              placeholder={
                isRefining
                  ? "Refining text..."
                  : isWaitingForApproval
                  ? "Agent is waiting for approval..."
                  : isStreaming
                  ? "Wait for response..."
                  : "Ask the agent anything..."
              }
              className="flex-1 rounded-2xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:text-gray-400 transition-colors resize-none overflow-y-auto min-h-[48px] max-h-[200px] leading-relaxed"
            />
          )}

          {!isStreaming && !isWaitingForApproval && mounted && browserSupportsSpeechRecognition && (
            <button
              type="button"
              disabled={isRefining}
              onClick={isListening ? handleStopRecordingLocal : handleStartRecording}
              className={`flex-shrink-0 w-[48px] h-[48px] rounded-2xl flex items-center justify-center transition-all ${
                isRefining ? 'bg-gray-100 opacity-50 cursor-not-allowed' : 'active:scale-95'
              } ${
                isListening 
                  ? 'bg-red-50 border-2 border-blue-500' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
              title={isListening ? "Pause recording" : "Start recording"}
            >
              {isListening ? (
                <div className="w-3.5 h-3.5 bg-red-600 rounded-[2px]"></div>
              ) : (
                <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5-3c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
                </svg>
              )}
            </button>
          )}

          {isStreaming ? (
            <button
              type="button"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                if (onStop) onStop();
              }}
              className="bg-red-600 text-white px-6 py-3 rounded-2xl font-medium hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all active:scale-95 flex items-center gap-2 h-[48px]"
            >
              <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                <rect x="6" y="6" width="12" height="12" rx="1.5" />
              </svg>
              Stop
            </button>
          ) : (
            <button
              type="submit"
              disabled={(!input.trim() && !isListening) || isWaitingForApproval || isRefining}
              className="flex-shrink-0 w-[48px] h-[48px] rounded-2xl flex items-center justify-center bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-blue-300 disabled:opacity-50 transition-all active:scale-95"
            >
              <svg className="w-6 h-6 fill-current" viewBox="0 0 24 24">
                <path d="M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z" />
              </svg>
            </button>
          )}
        </form>
      </div>
    </footer>
  );
}