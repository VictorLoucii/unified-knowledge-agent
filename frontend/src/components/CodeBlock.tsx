// frontend/src/components/CodeBlock.tsx
"use client";

import React, { useState } from "react";

interface CodeBlockProps {
  language?: string;
  codeText: string;
  children: React.ReactNode;
}

export default function CodeBlock({ language, codeText, children }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    const cleanText = codeText.replace(/\n$/, "");
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard
        .writeText(cleanText)
        .then(() => {
          setCopied(true);
          setTimeout(() => setCopied(false), 2000);
        })
        .catch((err) => {
          console.error("Failed to copy code: ", err);
          fallbackCopyTextToClipboard(cleanText);
        });
    } else {
      fallbackCopyTextToClipboard(cleanText);
    }
  };

  const fallbackCopyTextToClipboard = (text: string) => {
    try {
      const textArea = document.createElement("textarea");
      textArea.value = text;
      textArea.style.position = "fixed";
      textArea.style.left = "-9999px";
      textArea.style.top = "0";
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      const successful = document.execCommand("copy");
      document.body.removeChild(textArea);
      if (successful) {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
    } catch (err) {
      console.error("Fallback copy failed: ", err);
    }
  };

  return (
    <div className="relative border border-gray-800 rounded-lg my-4 overflow-hidden shadow-sm bg-gray-900">
      {/* Code Header */}
      <div className="flex justify-between items-center bg-gray-800 text-gray-400 px-4 py-1.5 text-xs font-sans select-none border-b border-gray-700/50">
        <span className="font-medium lowercase">{language || "code"}</span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 text-gray-400 hover:text-gray-200 transition-colors focus:outline-none cursor-pointer"
          title="Copy code"
        >
          {copied ? (
            <>
              <svg
                className="w-3.5 h-3.5 text-green-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2.5}
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <span className="text-green-400 font-medium">Copied!</span>
            </>
          ) : (
            <>
              <svg
                className="w-3.5 h-3.5"
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
              <span>Copy code</span>
            </>
          )}
        </button>
      </div>
      {/* Code Content */}
      <pre className="bg-gray-900 text-gray-100 p-4 overflow-x-auto text-sm font-mono m-0">
        {children}
      </pre>
    </div>
  );
}
