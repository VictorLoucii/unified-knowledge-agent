// frontend/src/components/MessageList.tsx
"use client";

import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MessageListProps {
  messages?: any[];
  isStreaming?: boolean;
  isWaitingForApproval?: boolean;
  handleApproval?: (approved: boolean) => void;
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
  isWaitingForApproval = false,
  handleApproval,
  handleSuggestedQuery = () => {},
  scrollContainerRef,
  handleScroll = () => {},
  messagesEndRef,
  copiedId = null,
  handleCopy = () => {},
}: MessageListProps) {
  // Helper to strip metadata tags AND the END OF PROBLEM marker
  const sanitizeContent = (content: string) => {
    if (!content) return "";
    return content
      .replace(/<!--[\s\S]*?(?:-->|$)/g, "") // Hides HTML comments
      .replace(/<END OF PROBLEM>/g, ""); // Hides the end tag
  };

  //Check if the user has already requested a post-mortem in this thread
  const hasRequestedPostMortem = messages.some(
    (msg: any) =>
      msg.role === "user" &&
      msg.content.includes(
        "Synthesize this conversation into a structured technical Post-Mortem report",
      ),
  );

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
              Your internal knowledge base for your internship. Ask about
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
        messages.map((msg: any) => {
          if (msg.role === "system") {
            return (
              <div key={msg.id} className="flex justify-center my-4">
                <div className="bg-gray-100 text-gray-600 text-xs px-4 py-2 rounded-full border border-gray-200">
                  {msg.content}
                </div>
              </div>
            );
          }

          const cleanContent = sanitizeContent(msg.content);

          return (
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
                {/* Replaced raw div with ReactMarkdown */}
                {cleanContent && (
                  <div className="leading-relaxed">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      components={{
                        // 1. Style the block wrapper (the dark box)
                        pre({ node, children, ...props }: any) {
                          return (
                            <pre
                              className="bg-gray-900 text-gray-100 rounded-lg p-4 overflow-x-auto my-4 text-sm"
                              {...props}
                            >
                              {children}
                            </pre>
                          );
                        },
                        // 2. Style the text inside (inline vs block text)
                        code({ node, className, children, ...props }: any) {
                          // Block code usually gets a language class like "language-js"
                          // If it doesn't have one, we treat it as an inline ` snippet
                          const isInline = !className;

                          return (
                            <code
                              className={`${className || ""} ${
                                isInline
                                  ? "bg-gray-100 text-gray-800 rounded px-1.5 py-0.5 font-mono text-sm"
                                  : ""
                              }`}
                              {...props}
                            >
                              {children}
                            </code>
                          );
                        },
                      }}
                    >
                      {cleanContent}
                    </ReactMarkdown>
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
                          className={`w-4 h-4 ${msg.role === "user" ? "text-white" : "text-green-500"}`}
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
                          className={`font-medium ${msg.role === "user" ? "text-white" : "text-green-500"}`}
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
                    {msg.isThinking && (
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
                    )}
                    <span>
                      {msg.currentTool
                        ? msg.currentTool
                        : "Agent is reasoning..."}
                    </span>
                  </div>
                )}
              </div>
            </div>
          );
        })
      )}

      {/* --- HITL APPROVAL COMPONENT --- */}
      {isWaitingForApproval && handleApproval && (
        <div className="flex flex-col items-center justify-center p-6 mt-4 border-2 border-yellow-400 bg-yellow-50 rounded-2xl shadow-sm animate-in slide-in-from-bottom-4">
          <div className="flex items-center gap-2 mb-4">
            <svg
              className="w-6 h-6 text-yellow-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <span className="text-yellow-800 font-bold text-lg">
              Action Required
            </span>
          </div>
          <p className="text-sm text-yellow-700 mb-6 text-center max-w-md">
            The agent is requesting permission to execute a tool. Do you want to
            proceed?
          </p>
          <div className="flex gap-4 w-full justify-center">
            <button
              onClick={() => handleApproval(true)}
              className="flex-1 max-w-[140px] px-4 py-2.5 bg-green-500 text-white font-medium rounded-xl hover:bg-green-600 transition shadow-sm hover:shadow active:scale-95"
            >
              Approve ✅
            </button>
            <button
              onClick={() => handleApproval(false)}
              className="flex-1 max-w-[140px] px-4 py-2.5 bg-white border-2 border-red-200 text-red-600 font-medium rounded-xl hover:bg-red-50 hover:border-red-300 transition shadow-sm hover:shadow active:scale-95"
            >
              Reject ❌
            </button>
          </div>
        </div>
      )}

      {/* --- POST-MORTEM BONUS TRIGGER --- */}
      {messages.length > 4 &&
        !isStreaming &&
        !isWaitingForApproval &&
        !hasRequestedPostMortem && (
          <div className="flex justify-center mt-10 pt-6 border-t border-gray-100">
            <button
              onClick={() =>
                handleSuggestedQuery(
                  "Synthesize this conversation into a structured technical Post-Mortem report (Root Cause, Fix, Lessons Learned).",
                )
              }
              className="px-6 py-2.5 bg-gray-800 text-white text-sm font-medium rounded-full hover:bg-gray-700 transition shadow-sm flex items-center gap-2 group"
            >
              <svg
                className="w-4 h-4 text-gray-400 group-hover:text-white transition-colors"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              Generate Post-Mortem
            </button>
          </div>
        )}

      <div ref={messagesEndRef as any} />
    </main>
  );
}
