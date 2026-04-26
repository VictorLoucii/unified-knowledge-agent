// frontend/src/components/Sidebar.tsx
"use client";

import React from "react";

interface SidebarProps {
  threads?: any[];
  pinnedThreads?: Set<string>;
  selectedThreads?: Set<string>;
  currentThreadId?: string;
  hasMore?: boolean;
  createNewChat?: () => void;
  handleSelectAll?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  handleBulkDelete?: () => Promise<void>;
  toggleThreadSelection?: (
    id: string,
    e: React.ChangeEvent<HTMLInputElement>
  ) => void;
  loadThread?: (id: string) => void;
  togglePin?: (id: string, e: React.MouseEvent) => void;
  deleteThread?: (id: string) => Promise<boolean>;
  setThreads?: React.Dispatch<React.SetStateAction<any[]>>;
  setSelectedThreads?: React.Dispatch<React.SetStateAction<Set<string>>>;
  setPinnedThreads?: React.Dispatch<React.SetStateAction<Set<string>>>;
  fetchHistory?: (isReset?: boolean) => void;
}

export default function Sidebar({
  threads = [],
  pinnedThreads = new Set(),
  selectedThreads = new Set(),
  currentThreadId = "",
  hasMore = false,
  createNewChat = () => {},
  handleSelectAll = () => {},
  handleBulkDelete = async () => {},
  toggleThreadSelection = () => {},
  loadThread = () => {},
  togglePin = () => {},
  deleteThread = async () => false,
  setThreads = () => {},
  setSelectedThreads = () => {},
  setPinnedThreads = () => {},
  fetchHistory = () => {},
}: SidebarProps) {
  const sortedThreads = [...threads].sort((a, b) => {
    const aPinned = pinnedThreads.has(a.id);
    const bPinned = pinnedThreads.has(b.id);
    if (aPinned && !bPinned) return -1;
    if (!aPinned && bPinned) return 1;
    return 0;
  });

  return (
    <aside className="w-64 bg-gray-100 border-r border-gray-200 flex flex-col hidden md:flex">
      <div className="p-4 border-b border-gray-200 bg-white flex flex-col gap-3">
        <h2 className="text-lg font-semibold text-gray-800">Chat History</h2>

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

        {threads.length > 0 && (
          <div className="flex items-center justify-between mt-1 px-1">
            <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer hover:text-gray-800 transition-colors">
              <input
                type="checkbox"
                checked={
                  selectedThreads.size === threads.length && threads.length > 0
                }
                onChange={handleSelectAll}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 w-4 h-4 cursor-pointer"
              />
              Select All
            </label>
            {selectedThreads.size > 0 && (
              <button
                onClick={handleBulkDelete}
                className="text-xs text-red-600 hover:text-red-700 font-medium hover:bg-red-50 px-2 py-1 rounded transition-colors"
              >
                Delete ({selectedThreads.size})
              </button>
            )}
          </div>
        )}
      </div>
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {sortedThreads.length === 0 ? (
          <p className="text-sm text-gray-500 p-2 text-center mt-4">
            No history yet.
          </p>
        ) : (
          sortedThreads.map((thread: any) => (
            <div
              key={thread.id}
              className="group relative flex items-center mb-1 px-1 gap-2"
            >
              <input
                type="checkbox"
                checked={selectedThreads.has(thread.id)}
                onChange={(e) => toggleThreadSelection(thread.id, e)}
                onClick={(e) => e.stopPropagation()}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 w-4 h-4 cursor-pointer flex-shrink-0"
              />

              <button
                className={`w-full text-left p-3 rounded-lg text-sm transition-all truncate border pr-14 flex-1 ${
                  currentThreadId === thread.id
                    ? "bg-blue-50 border-blue-200 text-blue-700 font-semibold shadow-sm"
                    : "text-gray-700 border-transparent hover:bg-gray-200 hover:border-gray-300"
                }`}
                onClick={() => {
                  if (loadThread) {
                    loadThread(thread.id);
                    window.history.pushState(null, "", `?thread=${thread.id}`);
                  }
                }}
              >
                {thread.title?.startsWith("thread_")
                  ? `Session: ${thread.title.replace("thread_", "")}`
                  : thread.title}
              </button>

              <div className="absolute right-3 flex items-center gap-1">
                <button
                  className={`p-1.5 rounded-md transition-all ${
                    pinnedThreads.has(thread.id)
                      ? "text-blue-600 opacity-100"
                      : "text-gray-400 opacity-0 group-hover:opacity-100 hover:text-blue-600 hover:bg-blue-50"
                  }`}
                  title={
                    pinnedThreads.has(thread.id) ? "Unpin chat" : "Pin chat"
                  }
                  onClick={(e) => togglePin(thread.id, e)}
                >
                  <svg
                    className="h-4 w-4"
                    fill={
                      pinnedThreads.has(thread.id) ? "currentColor" : "none"
                    }
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"
                    />
                  </svg>
                </button>

                <button
                  className="p-1.5 text-gray-400 opacity-0 group-hover:opacity-100 hover:text-red-600 hover:bg-red-50 rounded-md transition-all"
                  title="Delete chat"
                  onClick={async (e) => {
                    e.stopPropagation();
                    if (
                      window.confirm(
                        "Are you sure you want to delete this chat session?"
                      )
                    ) {
                      const success = await deleteThread(thread.id);
                      if (success) {
                        setThreads((prev) =>
                          prev.filter((t: any) => t.id !== thread.id)
                        );
                        setSelectedThreads((prev) => {
                          const newSet = new Set(prev);
                          newSet.delete(thread.id);
                          return newSet;
                        });
                        setPinnedThreads((prev) => {
                          const newSet = new Set(prev);
                          newSet.delete(thread.id);
                          return newSet;
                        });

                        if (currentThreadId === thread.id && createNewChat) {
                          createNewChat();
                        }
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
            </div>
          ))
        )}

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
  );
}