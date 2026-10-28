// frontend/src/hooks/useIngestionState.ts
import { useState, useEffect } from "react";
import { API_BASE_URL } from "./useChatStream";

export type IngestionState = "not_started" | "running" | "done" | "failed";

// Poll fast while loading. Poll slowly after "done" or "failed": the tab outlives
// the backend process, so it must still see the next restart and its outcome.
const POLL_LOADING_MS = 3000;
const POLL_SETTLED_MS = 30000;

// Returns the backend's ingestion_state from /health, or null before the first answer
export const useIngestionState = () => {
  const [ingestionState, setIngestionState] = useState<IngestionState | null>(null);

  useEffect(() => {
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let lastState: IngestionState | null = null;

    const poll = () => {
      let reached = false;
      fetch(`${API_BASE_URL}/health`)
        .then((res) => res.json())
        .then((data) => {
          if (cancelled) return;
          reached = true;
          lastState = data.ingestion_state ?? null;
          setIngestionState(lastState);
        })
        // A restarting backend refuses connections; keep the last state and poll again soon
        .catch((err) => console.error("Failed to fetch /health:", err))
        .finally(() => {
          if (cancelled) return;
          const settled = lastState === "done" || lastState === "failed";
          const delay = reached && settled ? POLL_SETTLED_MS : POLL_LOADING_MS;
          timer = setTimeout(poll, delay);
        });
    };

    poll();
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, []);

  return ingestionState;
};
