// frontend/src/app/page.tsx
"use client";

import { useState, useRef, useEffect } from "react";
import { useChatStream } from "../hooks/useChatStream";
import Sidebar from "../components/Sidebar";
import ChatHeader from "../components/ChatHeader";
import MessageList from "../components/MessageList";
import ChatInput from "../components/ChatInput";

export default function ChatUI() {
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

  const [threads, setThreads] = useState<any[]>([]);
  const [selectedThreads, setSelectedThreads] = useState<Set<string>>(
    new Set(),
  );
  const scrollContainerRef = useRef<HTMLElement>(null);
  const isAutoScrollPaused = useRef(false);

  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const LIMIT = 20;

  const [pinnedThreads, setPinnedThreads] = useState<Set<string>>(new Set());
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const handleScroll = () => {
    const container = scrollContainerRef.current;
    if (!container) return;
    const { scrollTop, scrollHeight, clientHeight } = container;
    const isAtBottom = scrollHeight - scrollTop - clientHeight < 10;
    isAutoScrollPaused.current = !isAtBottom;
  };

  useEffect(() => {
    const savedPins = localStorage.getItem("pinnedThreads");
    if (savedPins) {
      setPinnedThreads(new Set(JSON.parse(savedPins)));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(
      "pinnedThreads",
      JSON.stringify(Array.from(pinnedThreads)),
    );
  }, [pinnedThreads]);

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

  useEffect(() => {
    fetchHistory(true);
    if (typeof window !== "undefined") {
      const urlParams = new URLSearchParams(window.location.search);
      const urlThreadId = urlParams.get("thread");
      if (urlThreadId && loadThread) {
        loadThread(urlThreadId);
      }
    }
  }, []);

  useEffect(() => {
    if (!isAutoScrollPaused.current) {
      messagesEndRef.current?.scrollIntoView({ behavior: "auto" });
    }
  }, [messages]);

  const handleSelectAll = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.checked) {
      setSelectedThreads(new Set(threads.map((t: any) => t.id)));
    } else {
      setSelectedThreads(new Set());
    }
  };

  const toggleThreadSelection = (
    id: string,
    e: React.ChangeEvent<HTMLInputElement>,
  ) => {
    e.stopPropagation();
    const newSet = new Set(selectedThreads);
    if (newSet.has(id)) newSet.delete(id);
    else newSet.add(id);
    setSelectedThreads(newSet);
  };

  const handleBulkDelete = async () => {
    if (selectedThreads.size === 0) return;
    if (
      !window.confirm(
        `Are you sure you want to delete ${selectedThreads.size} selected chat(s)?`,
      )
    )
      return;

    const idsToDelete = Array.from(selectedThreads);
    await Promise.all(idsToDelete.map((id) => deleteThread(id)));

    setThreads((prev) => prev.filter((t: any) => !selectedThreads.has(t.id)));
    setSelectedThreads(new Set());

    setPinnedThreads((prev) => {
      const newSet = new Set(prev);
      idsToDelete.forEach((id) => newSet.delete(id));
      return newSet;
    });

    if (idsToDelete.includes(currentThreadId) && createNewChat) {
      createNewChat();
    }
  };

  const togglePin = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setPinnedThreads((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(id)) newSet.delete(id);
      else newSet.add(id);
      return newSet;
    });
  };

  const handleCopy = (id: string, content: string) => {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard
        .writeText(content)
        .then(() => {
          setCopiedId(id);
          setTimeout(() => setCopiedId(null), 2000);
        })
        .catch((err) => {
          console.error("Modern copy failed, trying fallback: ", err);
          fallbackCopyTextToClipboard(id, content);
        });
    } else {
      fallbackCopyTextToClipboard(id, content);
    }
  };

  const fallbackCopyTextToClipboard = (id: string, content: string) => {
    try {
      const textArea = document.createElement("textarea");
      textArea.value = content;
      textArea.style.position = "fixed";
      textArea.style.left = "-9999px";
      textArea.style.top = "0";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();

      const successful = document.execCommand("copy");
      document.body.removeChild(textArea);

      if (successful) {
        setCopiedId(id);
        setTimeout(() => setCopiedId(null), 2000);
      }
    } catch (err) {
      console.error("Fallback copy failed: ", err);
    }
  };

  const handleSuggestedQuery = (query: string) => {
    if (isStreaming) return;
    isAutoScrollPaused.current = false;

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
    isAutoScrollPaused.current = false;

    const isNewThread = !threads.some((t: any) => t.id === currentThreadId);
    if (isNewThread) {
      const optimisticTitle =
        input.length > 40 ? input.slice(0, 40) + "..." : input;
      setThreads((prev) => [
        { id: currentThreadId, title: optimisticTitle },
        ...prev,
      ]);
      window.history.pushState(null, "", `?thread=${currentThreadId}`);
    }
    sendMessage(input, () => fetchHistory(true));
    setInput("");
  };

  return (
    <div className="flex h-screen w-full bg-white">
      <Sidebar
        threads={threads}
        pinnedThreads={pinnedThreads}
        selectedThreads={selectedThreads}
        currentThreadId={currentThreadId}
        hasMore={hasMore}
        createNewChat={createNewChat}
        handleSelectAll={handleSelectAll}
        handleBulkDelete={handleBulkDelete}
        toggleThreadSelection={toggleThreadSelection}
        loadThread={loadThread}
        togglePin={togglePin}
        deleteThread={deleteThread}
        setThreads={setThreads}
        setSelectedThreads={setSelectedThreads}
        setPinnedThreads={setPinnedThreads}
        fetchHistory={fetchHistory}
      />

      <div className="flex flex-col flex-1 h-screen bg-gray-50 text-gray-900 overflow-hidden">
        <ChatHeader isStreaming={isStreaming} />

        <MessageList
          messages={messages}
          isStreaming={isStreaming}
          handleSuggestedQuery={handleSuggestedQuery}
          scrollContainerRef={scrollContainerRef}
          handleScroll={handleScroll}
          messagesEndRef={messagesEndRef}
          copiedId={copiedId}
          handleCopy={handleCopy}
        />

        <ChatInput
          input={input}
          setInput={setInput}
          handleSubmit={handleSubmit}
          isStreaming={isStreaming}
        />
      </div>
    </div>
  );
}
