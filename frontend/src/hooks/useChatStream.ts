// src/hooks/useChatStream.ts
import { useState } from 'react';
import { ChatMessage, AgentStreamEvent } from '../types/agent';

export const useChatStream = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = async (userText: string) => {
    // 1. Instantly show the user's message
    const userMsg: ChatMessage = { 
      id: Date.now().toString(), 
      role: 'user', 
      content: userText 
    };
    
    // 2. Setup the empty assistant message with the "Thinking" state
    const assistantId = (Date.now() + 1).toString();
    const initialAssistantMsg: ChatMessage = { 
      id: assistantId, 
      role: 'assistant', 
      content: '', 
      isThinking: true 
    };

    setMessages((prev) => [...prev, userMsg, initialAssistantMsg]);
    setIsStreaming(true);

    try {
      // Note: Update this URL to match your actual FastAPI local port
      const response = await fetch('http://localhost:8000/chat_stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userText }), 
      });

      if (!response.body) throw new Error('No readable stream available');

      // 3. Attach a reader to the stream
      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let done = false;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        
        if (value) {
          // Decode the Uint8Array chunk into a string
          const chunkString = decoder.decode(value, { stream: true });
          
          // SSE chunks are separated by newlines and prefixed with "data: "
          const lines = chunkString.split('\n');
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const dataStr = line.slice(6).trim();
              
              if (!dataStr || dataStr === '[DONE]') continue;

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
        prev.map(msg => msg.id === assistantId ? { ...msg, isThinking: false } : msg)
      );
    }
  };

  // 4. The Event Router: Updates state based on LangGraph astream_events
  const processGraphEvent = (event: AgentStreamEvent, assistantId: string) => {
    setMessages((prev) => prev.map((msg) => {
      if (msg.id !== assistantId) return msg;

      const updatedMsg = { ...msg };

      // Route based on the specific LangGraph event type
      switch (event.event) {
        case 'on_tool_start':
          updatedMsg.currentTool = `Using tool: ${event.name}...`;
          updatedMsg.isThinking = true;
          break;
        case 'on_tool_end':
          updatedMsg.currentTool = null;
          break;
        case 'on_chat_model_stream':
          if (event.data.chunk?.content) {
            updatedMsg.content += event.data.chunk.content;
            updatedMsg.isThinking = false; // Turn off thinking once tokens flow
          }
          break;
      }

      return updatedMsg;
    }));
  };

  return { messages, sendMessage, isStreaming };
};