// frontend/src/types/agent.ts :

// This represents the raw event emitted by LangGraph's astream_events(version="v2")
export interface AgentStreamEvent {
  event: string; // e.g., "on_chat_model_stream", "on_tool_start", "on_tool_end"
  name: string;  // e.g., "ChatOpenAI", "TavilySearchResults"
  run_id: string; // Unique ID for the specific node execution
  tags?: string[]; // Useful for filtering specific graph nodes
  data: {
    chunk?: {
      content: string | null;
      // Other metadata depending on your LLM provider
    };
    output?: any; 
    input?: any;
  };
}

// This represents the parsed state we will actually use in the React UI
export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";  
  content: string;
  isThinking?: boolean;
  currentTool?: string | null; // e.g., "Searching the web..."
}