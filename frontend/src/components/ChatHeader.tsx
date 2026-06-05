// frontend/src/components/ChatHeader.tsx
"use client";

import React from "react";

interface ChatHeaderProps {
  isStreaming?: boolean;
  onToggleSidebar?: () => void;
}

export default function ChatHeader({
  isStreaming = false,
  onToggleSidebar = () => {},
}: ChatHeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm flex items-center justify-between">
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="p-1 rounded-md text-gray-500 hover:bg-gray-100 md:hidden focus:outline-none"
          aria-label="Toggle sidebar"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
        <h1 className="text-xl font-semibold text-gray-800">
          Agentic AI Streaming Bridge
        </h1>
      </div>
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