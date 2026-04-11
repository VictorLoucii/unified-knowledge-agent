// frontend/src/app/page.tsx
"use client";

import { useState, useRef, useEffect } from "react";
import { useChatStream } from "../hooks/useChatStream";

export default function ChatUI() {
  //  Added deleteThread and current threadId from the hook
  const {
    messages,
    sendMessage,
    isStreaming,
    loadThread,
    deleteThread,
    threadId: currentThreadId,
  } = useChatStream() as any;
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // [PHASE 5] Sidebar State (Updated to handle objects)
  const [threads, setThreads] = useState<any[]>([]);

  // [PHASE 5] Fetch Thread History on Mount
  useEffect(() => {
    fetch("http://localhost:8000/history")
      .then((res) => res.json())
      .then((data) => {
        if (data.threads) setThreads(data.threads);
      })
      .catch((err) => console.error("Failed to fetch history:", err));
  }, []);

  // Auto-scroll to the latest message as the stream arrives
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    sendMessage(input);
    setInput("");
  };

  return (
    <div className="flex h-screen w-full bg-white">
      {/* [PHASE 5] Sidebar */}
      <aside className="w-64 bg-gray-100 border-r border-gray-200 flex flex-col hidden md:flex">
        <div className="p-4 border-b border-gray-200 bg-white">
          <h2 className="text-lg font-semibold text-gray-800">Chat History</h2>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {threads.length === 0 ? (
            <p className="text-sm text-gray-500 p-2 text-center mt-4">
              No history yet.
            </p>
          ) : (
            threads.map((thread: any) => (
              <div
                key={thread.id}
                className={`group relative flex items-center ${currentThreadId === thread.id ? "bg-gray-200 rounded-lg" : ""}`}
              >
                <button
                  className="w-full text-left p-3 rounded-lg text-sm text-gray-700 hover:bg-gray-200 transition-colors truncate border border-transparent hover:border-gray-300 pr-10"
                  onClick={() => {
                    if (loadThread) loadThread(thread.id);
                  }}
                >
                  {/* Safely handle older threads that might not have a title yet */}
                  {thread.title?.startsWith("thread_")
                    ? `Session: ${thread.title.replace("thread_", "")}`
                    : thread.title}
                </button>

                {/* Delete Button (Visible on hover) */}
                <button
                  className="absolute right-2 p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-md opacity-0 group-hover:opacity-100 transition-all"
                  title="Delete chat"
                  onClick={async (e) => {
                    e.stopPropagation(); // Prevents the loadThread click from firing
                    if (
                      window.confirm(
                        "Are you sure you want to delete this chat session?",
                      )
                    ) {
                      const success = await deleteThread(thread.id);
                      if (success) {
                        // Remove it from the sidebar state immediately
                        setThreads((prev) =>
                          prev.filter((t: any) => t.id !== thread.id),
                        );
                      }
                    }
                  }}
                >
                  <svg
                    className="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>
            ))
          )}
        </div>
      </aside>

      {/* Main Chat Area (Original styles preserved) */}
      <div className="flex flex-col flex-1 h-screen bg-gray-50 text-gray-900 overflow-hidden">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm flex items-center justify-between">
          <h1 className="text-xl font-semibold text-gray-800">
            Agentic AI Streaming Bridge
          </h1>
          <span className="text-xs text-red-500">
            Streaming: {isStreaming ? "YES" : "NO"}
          </span>
          <div className="flex items-center gap-2">
            <span
              className={`h-2.5 w-2.5 rounded-full ${isStreaming ? "bg-green-500 animate-pulse" : "bg-gray-300"}`}
            ></span>
            <span className="text-sm text-gray-500 font-medium">
              {isStreaming ? "Connection Active" : "Idle"}
            </span>
          </div>
        </header>

        {/* Message History Area */}
        <main className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.length === 0 ? (
            <div className="flex h-full items-center justify-center text-gray-400">
              <p>
                Send a message to initialize the LangGraph reasoning engine.
              </p>
            </div>
          ) : (
            messages.map((msg: any) => (
              <div
                key={msg.id}
                className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-5 py-3 ${
                    msg.role === "user"
                      ? "bg-blue-600 text-white rounded-br-none shadow-md"
                      : "bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm"
                  }`}
                >
                  {/* 1. Content Rendering */}
                  {msg.content && (
                    <div className="whitespace-pre-wrap leading-relaxed">
                      {msg.content}
                    </div>
                  )}

                  {/* 2. Tool & Thinking State UI */}
                  {(msg.isThinking || msg.currentTool) && (
                    <div className="mt-2 flex items-center gap-2 text-sm text-blue-600 font-medium bg-blue-50/50 p-2 rounded-lg border border-blue-100">
                      <svg
                        className="animate-spin h-4 w-4 text-blue-600"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        ></circle>
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        ></path>
                      </svg>
                      <span>
                        {msg.currentTool
                          ? msg.currentTool
                          : "Agent is reasoning..."}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          {/* Invisible div to anchor the auto-scroll */}
          <div ref={messagesEndRef} />
        </main>

        {/* Input Form */}
        <footer className="bg-white border-t border-gray-200 p-4">
          <div className="max-w-4xl mx-auto">
            <form onSubmit={handleSubmit} className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={isStreaming}
                placeholder={
                  isStreaming
                    ? "Wait for response..."
                    : "Ask the agent anything..."
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
      </div>
    </div>
  );
}
