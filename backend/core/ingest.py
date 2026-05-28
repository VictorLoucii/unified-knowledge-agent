# backend/core/ingest.py
import os
from langchain_text_splitters import MarkdownHeaderTextSplitter
from backend.core.config import retriever, store, parent_splitter, get_data_file_path


def initialize_rag():
    print("🧠 Checking Vector Database state...")

    # 1. Check if the docstore already has data (using yield_keys to avoid loading everything)
    try:
        # yield_keys returns a generator, so we check if it has at least one item
        first_key = next(store.yield_keys(), None)
        if first_key is not None:
            print(
                "✅ Vector Database & DocStore populated. Proceeding with existing index."
            )
            return
    except Exception as e:
        print(f"⚠️ Error checking docstore: {e}")

    print("⚠️ Vector Database empty. Initiating Cold-Start Auto-Ingestion...")

    # 2. Resolve exact paths
    try:
        DATA_FILE = get_data_file_path()
    except FileNotFoundError as e:
        print(f"🚨 ERROR: {e}")
        return

    # 3. Read and split the markdown specifically by headers
    print("📄 Loading and splitting markdown data by headers...")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        markdown_document = f.read()

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    md_header_splits = markdown_splitter.split_text(markdown_document)

    # Prepend headers to page_content so vector embeddings include them
    for doc in md_header_splits:
        header_parts = []
        if "Header 1" in doc.metadata:
            header_parts.append(f"# {doc.metadata['Header 1']}")
        if "Header 2" in doc.metadata:
            header_parts.append(f"## {doc.metadata['Header 2']}")
        if "Header 3" in doc.metadata:
            header_parts.append(f"### {doc.metadata['Header 3']}")
        if header_parts:
            doc.page_content = "\n".join(header_parts) + "\n\n" + doc.page_content

    # ==========================================
    # Pre-split these header sections so no single document
    # overflows the Langchain -> ChromaDB transaction limit.
    # ==========================================
    safe_splits = parent_splitter.split_documents(md_header_splits)

    print(
        f"⚙️ Adding {len(safe_splits)} safe parent documents to the Retriever in batches..."
    )

    BATCH_SIZE = 100
    for i in range(0, len(safe_splits), BATCH_SIZE):
        batch = safe_splits[i : i + BATCH_SIZE]
        print(
            f"📦 Processing batch {i//BATCH_SIZE + 1} (Documents {i} to {i + len(batch)})..."
        )
        retriever.add_documents(batch)

    print("✅ Auto-Ingestion complete. The Agent's memory is hydrated.")
