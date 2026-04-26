// frontend/src/components/ChatHeader.tsx
"use client";

import React from "react";

interface ChatHeaderProps {
  isStreaming?: boolean;
}

export default function ChatHeader({ isStreaming = false }: ChatHeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm flex items-center justify-between">
      <h1 className="text-xl font-semibold text-gray-800">
        Agentic AI Streaming Bridge
      </h1>
      <span className="text-xs text-red-500">
        Streaming: {isStreaming ? "YES" : "NO"}
      </span>
      <div className="flex items-center gap-2">
        <span
          className={`h-2.5 w-2.5 rounded-full ${
            isStreaming ? "bg-green-500 animate-pulse" : "bg-gray-300"
          }`}
        ></span>
        <span className="text-sm text-gray-500 font-medium">
          {isStreaming ? "Connection Active" : "Idle"}
        </span>
      </div>
    </header>
  );
}