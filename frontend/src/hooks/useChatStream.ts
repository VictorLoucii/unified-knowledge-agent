// frontend/src/hooks/useChatStream.ts
import { useState } from "react";
import { ChatMessage, AgentStreamEvent } from "../types/agent";

// Added optional initialThreadId to ensure backward compatibility
export const useChatStream = (initialThreadId?: string) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  // Initialize a stable thread ID for this session (Fallback to Date.now() if crypto is unavailable)
  const [threadId, setThreadId] = useState<string>(
    () =>
      initialThreadId ||
      (typeof crypto !== "undefined" && crypto.randomUUID
        ? crypto.randomUUID()
        : `thread_${Date.now()}`),
  );

  // [PHASE 5] Load historical messages from the backend
  const loadThread = async (id: string) => {
    setIsStreaming(true); // Show a loading state if desired
    setThreadId(id);

    try {
      const response = await fetch(`http://localhost:8000/history/${id}`);
      const data = await response.json();

      if (data.messages) {
        // Map simple backend messages to the UI's ChatMessage format
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

  const sendMessage = async (userText: string) => {
    // 1. Instantly show the user's message
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: userText,
    };

    // 2. Setup the empty assistant message with the "Thinking" state
    const assistantId = (Date.now() + 1).toString();
    const initialAssistantMsg: ChatMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
      isThinking: true,
    };

    setMessages((prev) => [...prev, userMsg, initialAssistantMsg]);
    setIsStreaming(true);

    try {
      // Note: Update this URL to match your actual FastAPI local port
      const response = await fetch("http://localhost:8000/chat_stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // Added thread_id to link messages in the Postgres checkpointer
        body: JSON.stringify({ message: userText, thread_id: threadId }),
      });

      if (!response.body) throw new Error("No readable stream available");

      // 3. Attach a reader to the stream
      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let done = false;

      let buffer = "";

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;

        if (value) {
          // Decode the Uint8Array chunk and append it to our buffer
          buffer += decoder.decode(value, { stream: true });

          // Split by newlines, just like before
          const lines = buffer.split("\n");

          // [FIX] Pop the last element off and keep it in the buffer.
          // If the network chunk cut off mid-JSON, it will wait here for the next packet.
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
    } catch (error) {
      console.error("Stream connection failed:", error);
    } finally {
      setIsStreaming(false);
      // Ensure the thinking state is turned off when the stream closes
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantId ? { ...msg, isThinking: false } : msg,
        ),
      );
    }
  };

  // 4. The Event Router: Updates state based on LangGraph astream_events
  const processGraphEvent = (event: AgentStreamEvent, assistantId: string) => {
    setMessages((prev) =>
      prev.map((msg) => {
        if (msg.id !== assistantId) return msg;

        const updatedMsg = { ...msg };

        // Route based on the specific LangGraph event type
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
              updatedMsg.isThinking = false; // Turn off thinking once tokens flow
            }
            break;
        }

        return updatedMsg;
      }),
    );
  };
  // [NEW] Add the delete logic here
  const deleteThread = async (id: string) => {
    try {
      const response = await fetch(`http://localhost:8000/history/${id}`, {
        method: "DELETE",
      });
      if (response.ok) {
        // If we deleted the currently active thread, clear the screen
        if (id === threadId) {
          setMessages([]);
        }
        return true;
      }
    } catch (err) {
      console.error("Failed to delete thread:", err);
    }
    return false;
  };

  return {
    messages,
    sendMessage,
    isStreaming,
    loadThread,
    threadId,
    deleteThread,
  };
};
