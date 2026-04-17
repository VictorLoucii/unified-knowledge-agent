// frontend/src/components/MessageList.tsx
"use client";

import React from "react";

interface MessageListProps {
  messages?: any[];
  isStreaming?: boolean;
  handleSuggestedQuery?: (query: string) => void;
  scrollContainerRef?: React.RefObject<HTMLElement | null>;
  handleScroll?: () => void;
  messagesEndRef?: React.RefObject<HTMLDivElement | null>;
  copiedId?: string | null;
  handleCopy?: (id: string, content: string) => void;
}

export default function MessageList({
  messages = [],
  isStreaming = false,
  handleSuggestedQuery = () => {},
  scrollContainerRef,
  handleScroll = () => {},
  messagesEndRef,
  copiedId = null,
  handleCopy = () => {},
}: MessageListProps) {
  return (
    <main
      ref={scrollContainerRef as any}
      onScroll={handleScroll}
      className="flex-1 overflow-y-auto p-6 space-y-6"
    >
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
              Your personal Second Brain for the Nexteir Internship. Ask about
              debugging, architecture, or specific problem IDs.
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
            className={`flex flex-col ${
              msg.role === "user" ? "items-end" : "items-start"
            }`}
          >
            <div
              className={`relative max-w-[80%] rounded-2xl px-5 py-3 pb-8 ${
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-br-none shadow-md"
                  : "bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm"
              }`}
            >
              {msg.content && (
                <div className="whitespace-pre-wrap leading-relaxed">
                  {msg.content}
                </div>
              )}

              {msg.content && !msg.isThinking && (
                <button
                  onClick={() => handleCopy(msg.id, msg.content)}
                  className={`absolute bottom-2 flex items-center gap-1 text-xs transition-colors ${
                    msg.role === "user"
                      ? "right-4 text-blue-200 hover:text-white"
                      : "left-4 text-gray-400 hover:text-gray-600"
                  }`}
                  title="Copy message"
                >
                  {copiedId === msg.id ? (
                    <>
                      <svg
                        className={`w-4 h-4 ${
                          msg.role === "user" ? "text-white" : "text-green-500"
                        }`}
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                      <span
                        className={`font-medium ${
                          msg.role === "user" ? "text-white" : "text-green-500"
                        }`}
                      >
                        Copied!
                      </span>
                    </>
                  ) : (
                    <>
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
                          d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                        />
                      </svg>
                      <span>Copy</span>
                    </>
                  )}
                </button>
              )}

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
                    {msg.currentTool ? msg.currentTool : "Agent is reasoning..."}
                  </span>
                </div>
              )}
            </div>
          </div>
        ))
      )}
      <div ref={messagesEndRef as any} />
    </main>
  );
}