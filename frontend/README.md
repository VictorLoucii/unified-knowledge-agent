# 💻 Unified Knowledge Agent: Next.js Frontend Client

This is the Next.js frontend client for the **Unified Knowledge Agent**. It provides a real-time chat interface to interact with the internal knowledge base, featuring markdown rendering, metadata sanitization, and Human-in-the-Loop (HITL) approval states.

---

## 🌟 Key Features

*   **Human-in-the-Loop (HITL) Interface:** Visually intercepts heavy tool calls (the "Yellow Card" protocol) using LangGraph interrupts. Users can approve or deny actions directly from the chat UI.
*   **Fidelity Markdown Rendering:** Renders technical bug logs, tabular data, code snippets, and inline highlights using `react-markdown` and `remark-gfm`.
*   **Regex Sanitization Firewall:** Dynamically cleanses outputs to strip system anchors, internal document links, and hidden metadata tag blocks (e.g., `<END OF PROBLEM>`, `<!-- RETRIEVED_PROBLEM_IDS -->`) before displaying them to the user.
*   **Streaming Chat Hooks:** Uses custom React hooks to manage server-sent events (SSE) and stream responses back seamlessly.

---

## 📂 Directory Layout

*   `src/app/`: Next.js App Router setup (layout and page views).
*   `src/components/`: Modular UI elements including:
    *   `ChatInput`: User message inputs and controls.
    *   `MessageList`: Message bubble rendering (user vs. assistant/agent) with markdown formatting.
    *   `Sidebar`: Active thread listing and navigation.
    *   `HITLPanel`: Prompt box rendering the interrupt state for active tool approval.
*   `src/hooks/`: Custom state management (e.g., `useChatStream.ts`).

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Node.js (v18+) installed.

### 1. Install Dependencies

```bash
npm install
# or
yarn install
# or
pnpm install
```

### 2. Configure Environment Variables

Create a `.env.local` file in this directory and specify the backend endpoint:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

### 3. Start the Development Server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the interface.

---

## 🐳 Docker Deployment

The frontend is Dockerized. You can build it standalone or orchestrate it through the main directory's `docker-compose.yml`.

To build the standalone Docker image:
```bash
docker build -t uka-frontend -f frontend.Dockerfile .
```
