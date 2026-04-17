// frontend/src/components/ChatInput.tsx
"use client";

import React from "react";

interface ChatInputProps {
  input?: string;
  setInput?: (val: string) => void;
  handleSubmit?: (e: React.FormEvent) => void;
  isStreaming?: boolean;
}

export default function ChatInput({
  input = "",
  setInput = () => {},
  handleSubmit = (e) => e.preventDefault(),
  isStreaming = false,
}: ChatInputProps) {
  return (
    <footer className="bg-white border-t border-gray-200 p-4">
      <div className="max-w-4xl mx-auto">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isStreaming}
            placeholder={
              isStreaming ? "Wait for response..." : "Ask the agent anything..."
            }
            className="flex-1 rounded-xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:text-gray-400 transition-colors"
          />
          <button
            type="submit"
            disabled={!input.trim() || isStreaming}
            className="bg-blue-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-blue-300 transition-all active:scale-95"
          >
            Send
          </button>
        </form>
      </div>
    </footer>
  );
}