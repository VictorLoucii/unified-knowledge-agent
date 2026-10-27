// frontend/src/lib/browserId.ts
// A random id created once per browser and kept in localStorage. The backend
// reads it from the X-Browser-Id header and shows each browser only its own threads.

const STORAGE_KEY = "agent_browser_id";
let memoryId: string | null = null;

const createId = (): string => {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  // crypto.randomUUID needs a secure context; getRandomValues does not
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
};

export const getBrowserId = (): string => {
  try {
    let id = localStorage.getItem(STORAGE_KEY);
    if (!id) {
      id = createId();
      localStorage.setItem(STORAGE_KEY, id);
    }
    return id;
  } catch (error) {
    // Storage blocked (privacy settings): keep one id for this page load
    console.warn("localStorage unavailable, using an in-memory browser id:", error);
    if (!memoryId) memoryId = createId();
    return memoryId;
  }
};

export const browserIdHeaders = (): Record<string, string> => ({
  "X-Browser-Id": getBrowserId(),
});
