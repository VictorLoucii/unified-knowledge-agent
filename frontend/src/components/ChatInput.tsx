// frontend/src/components/ChatInput.tsx
"use client";

import React from "react";

interface ChatInputProps {
  input?: string;
  setInput?: (val: string) => void;
  handleSubmit?: (e: React.FormEvent) => void;
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

  React.useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    // Reset height to calculate scrollHeight correctly
    textarea.style.height = "auto";
    // Set height based on scrollHeight, cap at 200px
    textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
  }, [input]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (input.trim() && !isStreaming && !isWaitingForApproval) {
        const form = e.currentTarget.form;
        if (form) {
          form.requestSubmit();
        }
      }
    }
  };

  return (
    <footer className="bg-white border-t border-gray-200 p-4">
      <div className="max-w-4xl mx-auto">
        <form onSubmit={handleSubmit} className="flex gap-3 items-end">
          <textarea
            ref={textareaRef}
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isStreaming || isWaitingForApproval} // <-- [PHASE 7 NEW] Lock if waiting
            placeholder={
              isWaitingForApproval
                ? "Agent is waiting for approval..." // <-- [PHASE 7 NEW] UX feedback
                : isStreaming
                ? "Wait for response..."
                : "Ask the agent anything..."
            }
            className="flex-1 rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:text-gray-400 transition-colors resize-none overflow-y-auto min-h-[48px] max-h-[200px] leading-relaxed"
          />
          {isStreaming ? (
            <button
              type="button"
              onClick={onStop}
              className="bg-red-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all active:scale-95 flex items-center gap-2 h-[48px]"
            >
              <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                <rect x="6" y="6" width="12" height="12" rx="1.5" />
              </svg>
              Stop
            </button>
          ) : (
            <button
              type="submit"
              disabled={!input.trim() || isWaitingForApproval} // <-- [PHASE 7 NEW] Lock if waiting
              className="bg-blue-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-blue-300 transition-all active:scale-95 h-[48px]"
            >
              Send
            </button>
          )}
        </form>
      </div>
    </footer>
  );
}