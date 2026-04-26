// frontend/src/hooks/useChatStream.ts
import { useState, useRef } from "react";
import { ChatMessage, AgentStreamEvent } from "../types/agent";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:7860";

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
      const response = await fetch(`${API_BASE_URL}/history/${id}`);
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

  // --- REUSABLE STREAM READER ---
  const readStream = async (response: Response, assistantId: string) => {
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
            if (event.data.chunk?.content) {
              updatedMsg.content += event.data.chunk.content;
              updatedMsg.isThinking = false;
            }
            break;
          case "on_agent_interrupt":
            updatedMsg.isThinking = false;
            updatedMsg.currentTool = "Action Required: Pending approval.";
            break;
        }

        return updatedMsg;
      }),
    );
  };

  const sendMessage = async (userText: string, onFinish?: () => void) => {    
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

    try {
      const response = await fetch(`${API_BASE_URL}/chat_stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText, thread_id: threadId }),
      });

      await readStream(response, assistantId);

    } catch (error) {
      console.error("Stream connection failed:", error);
    } finally {
      // Only clear streaming if we aren't waiting for the user to click approve
      setIsStreaming((prev) => isWaitingForApproval ? true : false);
      
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantId && !isWaitingForApproval 
            ? { ...msg, isThinking: false } 
            : msg,
        ),
      );
      if (onFinish && !isWaitingForApproval) onFinish();
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
          headers: { "Content-Type": "application/json" },
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

    try {
      const response = await fetch(`${API_BASE_URL}/chat_approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ thread_id: threadId, approve: true }),
      });

      await readStream(response, targetAssistantId);

    } catch (err) {
      console.error("Stream resumption failed:", err);
    } finally {
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
  };
};