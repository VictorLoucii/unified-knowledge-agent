// src/app/page.tsx
'use client';

import { useState, useRef, useEffect } from 'react';
import { useChatStream } from '../hooks/useChatStream';

export default function ChatUI() {
  const { messages, sendMessage, isStreaming } = useChatStream();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to the latest message as the stream arrives
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    sendMessage(input);
    setInput('');
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-800">Agentic AI Streaming Bridge</h1>
        <span className="text-xs text-red-500">Streaming: {isStreaming ? "YES" : "NO"}</span>
        <div className="flex items-center gap-2">
          <span className={`h-2.5 w-2.5 rounded-full ${isStreaming ? 'bg-green-500 animate-pulse' : 'bg-gray-300'}`}></span>
          <span className="text-sm text-gray-500 font-medium">
            {isStreaming ? 'Connection Active' : 'Idle'}
          </span>
        </div>
      </header>

      {/* Message History Area */}
      <main className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 ? (
          <div className="flex h-full items-center justify-center text-gray-400">
            <p>Send a message to initialize the LangGraph reasoning engine.</p>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-5 py-3 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-br-none shadow-md'
                    : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm'
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
                    <svg className="animate-spin h-4 w-4 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>{msg.currentTool ? msg.currentTool : 'Agent is reasoning...'}</span>
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
              placeholder={isStreaming ? "Wait for response..." : "Ask the agent anything..."}
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
  );
}