from backend.core.config import retriever

def test_query(query):
    print(f"\n--- QUERY: {query} ---")
    docs = retriever.invoke(query)
    for i, doc in enumerate(docs[:3]):
        print(f"[{i}] source_file: {doc.metadata.get('source_file')}")
        print(f"Content preview: {doc.page_content[:200]}...\n")

test_query("how am i using docker in my unified knowledge agent project?")
test_query("what is my tech stack in unified knowledge agent?")
