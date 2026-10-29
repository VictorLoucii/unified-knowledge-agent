// frontend/src/hooks/useChatStream.ts
import { useState, useRef } from "react";
import { ChatMessage, AgentStreamEvent } from "../types/agent";
import { browserIdHeaders } from "../lib/browserId";

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:7860";

// The one wording shown when a request fails; the backend never sends exception text
const ERROR_MESSAGE = "Something went wrong on our side. Please try again in a moment.";

// Keep any partial answer and put the error message below it
const withErrorMessage = (content: string, message: string = ERROR_MESSAGE) =>
  content ? `${content}\n\n${message}` : message;

// A 429 from the rate limit; its message is the backend's fixed line
class RateLimitedError extends Error {}

const errorText = (error: unknown) =>
  error instanceof RateLimitedError ? error.message : ERROR_MESSAGE;

const getSessionId = () => {
  if (typeof window === "undefined") {
    return `thread_${Date.now()}`;
  }
  
  let sessionId = sessionStorage.getItem("agent_session_id");
  if (!sessionId) {
    sessionId = typeof crypto !== "undefined" && crypto.randomUUID
      ? crypto.randomUUID()
      : `thread_${Date.now()}`;
    sessionStorage.setItem("agent_session_id", sessionId);
  }
  return sessionId;
};

export const useChatStream = (initialThreadId?: string) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isWaitingForApproval, setIsWaitingForApproval] = useState(false);
  
  // Track the current assistant message ID to reliably resume streams
  const latestAssistantIdRef = useRef<string | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null); // <-- [NEW] Abort controller ref
  const isSubmittingRef = useRef<boolean>(false); // <-- [FIX] Prevent double-submissions

  const [threadId, setThreadId] = useState<string>(() => {
    if (initialThreadId) return initialThreadId;
    return getSessionId();
  });

  const loadThread = async (id: string) => {
    setIsStreaming(true); 
    setThreadId(id);
    
    if (typeof window !== "undefined") {
      sessionStorage.setItem("agent_session_id", id);
    }
    
    setMessages([]);

    try {
      const response = await fetch(`${API_BASE_URL}/history/${id}`, {
        headers: browserIdHeaders(),
      });
      const data = await response.json();

      if (data.messages) {
        const formattedMessages: ChatMessage[] = data.messages.map(
          (m: any, index: number) => ({
            id: `${id}-${index}`,
            role: m.role,
            content: m.content,
            isThinking: false,
          }),
        );
        setMessages(formattedMessages);
      }
    } catch (err) {
      console.error("Failed to load thread history:", err);
    } finally {
      setIsStreaming(false);
    }
  };

  const showErrorMessage = (assistantId: string, message: string = ERROR_MESSAGE) => {
    setMessages((prev) =>
      prev.map((msg) =>
        msg.id === assistantId && !msg.isError
          ? { ...msg, content: withErrorMessage(msg.content, message), isThinking: false, currentTool: null, isError: true }
          : msg
      )
    );
  };

  // --- REUSABLE STREAM READER ---
  const readStream = async (response: Response, assistantId: string) => {
    if (response.status === 429) {
      // Another layer (HF's proxy) could also answer 429; then the body is not ours
      const body: { error?: unknown } | null = await response.json().catch(() => null);
      throw new RateLimitedError(typeof body?.error === "string" ? body.error : ERROR_MESSAGE);
    }
    if (!response.ok) throw new Error(`Request failed with status ${response.status}`);
    if (!response.body) throw new Error("No readable stream available");
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;
    let buffer = "";

    while (!done) {
      const { value, done: readerDone } = await reader.read();
      done = readerDone;

      if (value) {
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const dataStr = line.slice(6).trim();
            if (!dataStr || dataStr === "[DONE]") continue;

            try {
              const event: AgentStreamEvent = JSON.parse(dataStr);
              processGraphEvent(event, assistantId);
            } catch (err) {
              console.error("Failed to parse stream event:", err, dataStr);
            }
          }
        }
      }
    }
  };

  const processGraphEvent = (event: AgentStreamEvent, assistantId: string) => {
    // 1. Catch the interrupt and lock the UI
    if (event.event === "on_agent_interrupt") {
      setIsWaitingForApproval(true);
    }

    setMessages((prev) =>
      prev.map((msg) => {
        if (msg.id !== assistantId) return msg;

        const updatedMsg = { ...msg };

        switch (event.event) {
          case "on_tool_start":
            updatedMsg.currentTool = `Using tool: ${event.name}...`;
            updatedMsg.isThinking = true;
            break;
          case "on_tool_end":
            updatedMsg.currentTool = null;
            break;
          case "on_chat_model_stream":
            // The backend still appends its latency line after an error; keep the error message last
            if (updatedMsg.isError) break;
            if (event.data.chunk?.content) {
              updatedMsg.content += event.data.chunk.content;
              updatedMsg.isThinking = false;
            }
            break;
          case "on_agent_interrupt":
            updatedMsg.isThinking = false;
            updatedMsg.currentTool = "Action Required: Pending approval.";
            break;
          case "on_error":
            updatedMsg.content = withErrorMessage(updatedMsg.content);
            updatedMsg.isThinking = false;
            updatedMsg.currentTool = null;
            updatedMsg.isError = true;
            break;
        }

        return updatedMsg;
      }),
    );
  };

  const sendMessage = async (userText: string, onFinish?: () => void) => {    
    if (isSubmittingRef.current || isStreaming) return; // Prevent double clicks
    isSubmittingRef.current = true;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: userText,
    };

    const assistantId = (Date.now() + 1).toString();
    latestAssistantIdRef.current = assistantId; // Store for resumption

    const initialAssistantMsg: ChatMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
      isThinking: true,
    };

    setMessages((prev) => [...prev, userMsg, initialAssistantMsg]);
    setIsStreaming(true);
    setIsWaitingForApproval(false); // Reset lock on new message

    // Create abort controller for streaming cancellation
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      const response = await fetch(`${API_BASE_URL}/chat_stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...browserIdHeaders() },
        body: JSON.stringify({ message: userText, thread_id: threadId }),
        signal: controller.signal,
      });

      await readStream(response, assistantId);

    } catch (error: unknown) {
      if (error instanceof Error && error.name === "AbortError") {
        console.log("Stream connection stopped by user.");
      } else {
        console.error("Stream connection failed:", error);
        showErrorMessage(assistantId, errorText(error));
      }
    } finally {
      if (abortControllerRef.current === controller) {
        abortControllerRef.current = null;
      }
      setMessages((prev) => {
        const targetMsg = prev.find((m) => m.id === assistantId);
        const isInterrupted = targetMsg?.currentTool === "Action Required: Pending approval.";
        
        if (isInterrupted) {
          isSubmittingRef.current = false;
          return prev;
        } else {
          setIsStreaming(false);
          isSubmittingRef.current = false;
          if (onFinish) onFinish();
          return prev.map((msg) =>
            msg.id === assistantId ? { ...msg, isThinking: false } : msg
          );
        }
      });
    }
  };

  // --- THE SAFETY VALVE LOGIC ---
  const handleApproval = async (approved: boolean) => {
    setIsWaitingForApproval(false);
    const targetAssistantId = latestAssistantIdRef.current || "";

    if (!approved) {
      try {
        await fetch(`${API_BASE_URL}/chat_approve`, {
          method: "POST",
          headers: { "Content-Type": "application/json", ...browserIdHeaders() },
          body: JSON.stringify({ thread_id: threadId, approve: false }),
        });
        
        // Inject a localized rejection message
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now().toString(),
            role: "system",
            content: "❌ Action cancelled. What would you like to do instead?",
          },
        ]);
      } catch (err) {
        console.error("Failed to reject action:", err);
      } finally {
        setIsStreaming(false);
      }
      return;
    }

    // User Approved: Resume the stream
    setIsStreaming(true);
    
    // Visually reset the active assistant message to a thinking state
    setMessages((prev) =>
      prev.map((msg) =>
        msg.id === targetAssistantId 
          ? { ...msg, isThinking: true, currentTool: "Executing approved action..." } 
          : msg
      )
    );

    // Create abort controller for streaming cancellation
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      const response = await fetch(`${API_BASE_URL}/chat_approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...browserIdHeaders() },
        body: JSON.stringify({ thread_id: threadId, approve: true }),
        signal: controller.signal,
      });

      await readStream(response, targetAssistantId);

    } catch (err: unknown) {
      if (err instanceof Error && err.name === "AbortError") {
        console.log("Stream resumption stopped by user.");
      } else {
        console.error("Stream resumption failed:", err);
        showErrorMessage(targetAssistantId, errorText(err));
      }
    } finally {
      if (abortControllerRef.current === controller) {
        abortControllerRef.current = null;
      }
      setIsStreaming(false);
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === targetAssistantId 
            ? { ...msg, isThinking: false, currentTool: null } 
            : msg
        )
      );
    }
  };

  const deleteThread = async (id: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}/history/${id}`, {
        method: "DELETE",
        headers: browserIdHeaders(),
      });
      if (response.ok) {
        if (id === threadId) setMessages([]);
        return true;
      }
    } catch (err) {
      console.error("Failed to delete thread:", err);
    }
    return false;
  };

  const createNewChat = () => {
    setMessages([]);
    const newId = typeof crypto !== "undefined" && crypto.randomUUID
      ? crypto.randomUUID()
      : `thread_${Date.now()}`;
      
    setThreadId(newId);
    
    if (typeof window !== "undefined") {
      sessionStorage.setItem("agent_session_id", newId);
      window.history.pushState(null, '', window.location.pathname);
    }
  };

  const stopResponse = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setIsStreaming(false);
  };

  return {
    messages,
    sendMessage,
    isStreaming,
    isWaitingForApproval,
    handleApproval,
    loadThread,
    threadId,
    deleteThread,
    createNewChat,
    stopResponse, // <-- [NEW] Expose stopResponse
  };
};