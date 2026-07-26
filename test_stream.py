import asyncio
from backend.core.agents import workflow
from langchain_core.messages import HumanMessage
import json
import logging

logging.getLogger("langchain").setLevel(logging.CRITICAL)
logging.getLogger("langchain_core").setLevel(logging.CRITICAL)

async def test():
    graph = workflow.compile()
    inputs = {"messages": [HumanMessage(content="what kind of internship logs?")]}
    config = {"configurable": {"thread_id": "test_1"}}
    async for event in graph.astream_events(inputs, config, version="v2"):
        if event["name"] in ["fast_path_node", "route_input_node"]:
            print(f"Event: {event['event']} | Node: {event['name']}")
            if event["event"] == "on_chain_end":
                print(f"Output keys: {event['data']['output'].keys() if isinstance(event['data']['output'], dict) else 'Not a dict'}")
                if isinstance(event['data']['output'], dict) and "messages" in event['data']['output']:
                    msgs = event['data']['output']['messages']
                    print(f"Messages count: {len(msgs)}")
                    for m in msgs:
                        print(f"  - {m.__class__.__name__}: {m.content[:50]}...")

if __name__ == "__main__":
    asyncio.run(test())
