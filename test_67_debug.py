import asyncio
from backend.core.agents import workflow
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

async def test():
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    inputs = {"messages": [HumanMessage(content='What is the `eval()` function used for in JavaScript?')]}
    config = {"configurable": {"thread_id": "test"}}
    print("STARTING WORKFLOW...")
    async for event in app.astream(inputs, config=config):
        for node, state in event.items():
            print(f"--- NODE: {node} ---")
            if "messages" in state:
                print("LAST MSG:", state["messages"][-1])

if __name__ == '__main__':
    asyncio.run(test())
