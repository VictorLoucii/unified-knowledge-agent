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
    createNewChat,
  } = useChatStream() as any;
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // [PHASE 5] Sidebar State (Updated to handle objects)
  const [threads, setThreads] = useState<any[]>([]);

  //  Pagination State
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const LIMIT = 20;

  // [PHASE 5] Reusable fetch function for history
  const fetchHistory = (isReset = false) => {
    const currentOffset = isReset ? 0 : offset;

    fetch(
      `http://localhost:8000/history?limit=${LIMIT}&offset=${currentOffset}`,
    )
      .then((res) => res.json())
      .then((data) => {
        if (data.threads) {
          if (isReset) {
            setThreads(data.threads);
          } else {
            // Append new threads, ensuring no duplicates
            setThreads((prev) => {
              const newThreads = data.threads.filter(
                (newT: any) => !prev.some((p) => p.id === newT.id),
              );
              return [...prev, ...newThreads];
            });
          }
          setOffset(currentOffset + LIMIT);
          setHasMore(data.has_more);
        }
      })
      .catch((err) => console.error("Failed to fetch history:", err));
  };

  // Fetch on mount and check URL for bookmarks
  useEffect(() => {
    fetchHistory(true); // Pass true to reset on initial load

    if (typeof window !== "undefined") {
      const urlParams = new URLSearchParams(window.location.search);
      const urlThreadId = urlParams.get("thread");
      if (urlThreadId && loadThread) {
        loadThread(urlThreadId);
      }
    }
  }, []);

  // Auto-scroll to the latest message as the stream arrives
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  //  Helper function to handle suggested queries
  const handleSuggestedQuery = (query: string) => {
    if (isStreaming) return;

    const isNewThread = !threads.some((t: any) => t.id === currentThreadId);
    if (isNewThread) {
      const optimisticTitle =
        query.length > 40 ? query.slice(0, 40) + "..." : query;
      setThreads((prev) => [
        { id: currentThreadId, title: optimisticTitle },
        ...prev,
      ]);
      window.history.pushState(null, "", `?thread=${currentThreadId}`);
    }

    sendMessage(query, () => fetchHistory(true));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;

    // [NEW] Optimistic UI: Instantly add to sidebar if it's a brand new chat
    const isNewThread = !threads.some((t: any) => t.id === currentThreadId);

    if (isNewThread) {
      // Create a title matching your backend logic (first 40 chars)
      const optimisticTitle =
        input.length > 40 ? input.slice(0, 40) + "..." : input;

      setThreads((prev) => [
        { id: currentThreadId, title: optimisticTitle },
        ...prev, // Put the new chat at the very top
      ]);

      // [NEW] Update the URL immediately so the new chat can be bookmarked
      window.history.pushState(null, "", `?thread=${currentThreadId}`);
    }

    // Start streaming. The fetchHistory callback will ensure DB sync when done.
    sendMessage(input, () => fetchHistory(true));
    setInput("");
  };

  return (
    <div className="flex h-screen w-full bg-white">
      {/* [PHASE 5] Sidebar */}
      <aside className="w-64 bg-gray-100 border-r border-gray-200 flex flex-col hidden md:flex">
        <div className="p-4 border-b border-gray-200 bg-white flex flex-col gap-3">
          <h2 className="text-lg font-semibold text-gray-800">Chat History</h2>

          {/* New Chat Button */}
          <button
            onClick={createNewChat}
            className="w-full bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors flex items-center justify-center gap-2 shadow-sm"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
            New Chat
          </button>
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
                className="group relative flex items-center mb-1"
              >
                <button
                  className={`w-full text-left p-3 rounded-lg text-sm transition-all truncate border pr-10 ${
                    currentThreadId === thread.id
                      ? "bg-blue-50 border-blue-200 text-blue-700 font-semibold shadow-sm"
                      : "text-gray-700 border-transparent hover:bg-gray-200 hover:border-gray-300"
                  }`}
                  onClick={() => {
                    if (loadThread) {
                      loadThread(thread.id);
                      window.history.pushState(
                        null,
                        "",
                        `?thread=${thread.id}`,
                      );
                    }
                  }}
                >
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

          {/* Pagination Button */}
          {hasMore && threads.length > 0 && (
            <button
              onClick={() => fetchHistory(false)}
              className="w-full mt-2 p-2 text-xs font-semibold text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors flex items-center justify-center gap-1"
            >
              Load Older Chats
              <svg
                className="w-3 h-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
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
            <div className="flex flex-col h-full items-center justify-center text-center space-y-8 animate-in fade-in duration-500">
              <div className="space-y-2">
                <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-sm">
                  <svg
                    className="w-8 h-8"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-gray-800">
                  Unified Knowledge Agent
                </h2>
                <p className="text-gray-500 max-w-md mx-auto">
                  Your personal Second Brain for the Nexteir Internship. Ask
                  about debugging, architecture, or specific problem IDs.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl px-4">
                {[
                  "What was the fix for the Chiiro loader?",
                  "Summarize the React Native Yarn vs NPM issue.",
                  "How do I handle the MultiSelect scrolling bug?",
                  "Find the solution for //problem82.",
                ].map((query, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSuggestedQuery(query)}
                    className="p-4 border border-gray-200 rounded-xl bg-white hover:border-blue-300 hover:shadow-md transition-all text-sm text-gray-700 text-left flex flex-col gap-2 group"
                  >
                    <span className="font-medium group-hover:text-blue-600 transition-colors">
                      {query}
                    </span>
                    <span className="text-xs text-gray-400">
                      Query Knowledge Base →
                    </span>
                  </button>
                ))}
              </div>
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
