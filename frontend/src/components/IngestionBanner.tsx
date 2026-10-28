// frontend/src/components/IngestionBanner.tsx
"use client";

import React from "react";
import { IngestionState } from "../hooks/useIngestionState";

interface IngestionBannerProps {
  ingestionState?: IngestionState | null;
}

// Shown while /health reports the knowledge base as not loaded; hidden once "done"
export default function IngestionBanner({
  ingestionState = null,
}: IngestionBannerProps) {
  if (ingestionState === null || ingestionState === "done") return null;

  const failed = ingestionState === "failed";
  return (
    <div
      role="status"
      className={`px-6 py-2 text-sm border-b ${
        failed
          ? "bg-red-50 text-red-700 border-red-200"
          : "bg-amber-50 text-amber-800 border-amber-200"
      }`}
    >
      {failed
        ? "The knowledge base did not load. The chat cannot answer right now."
        : "The knowledge base is loading after a restart. Answers start when it finishes."}
    </div>
  );
}
