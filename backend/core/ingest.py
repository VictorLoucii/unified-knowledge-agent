# backend/core/ingest.py
import os
import json
import re
from langchain_text_splitters import MarkdownHeaderTextSplitter
from backend.core.config import retriever, store, parent_splitter, get_data_file_paths

def get_manifest_path() -> str:
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_dir, "..", "..", "data", ".manifest.json")

def load_manifest() -> dict:
    manifest_path = get_manifest_path()
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"ingested_files": []}

def save_manifest(manifest: dict):
    manifest_path = get_manifest_path()
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

def initialize_rag():
    print("🧠 Checking Vector Database state...")
    manifest = load_manifest()
    
    # 1. Check if the docstore already has data (using yield_keys to avoid loading everything)
    try:
        first_key = next(store.yield_keys(), None)
        if first_key is not None:
            print("✅ Vector Database & DocStore populated.")
    except Exception as e:
        print(f"⚠️ Error checking docstore: {e}")

    # 2. Resolve exact paths
    try:
        data_files = get_data_file_paths()
    except FileNotFoundError as e:
        print(f"🚨 ERROR: {e}")
        return

    files_to_ingest = []
    for data_file in data_files:
        basename = os.path.basename(data_file)
        if basename not in manifest.get("ingested_files", []):
            files_to_ingest.append((data_file, basename))
            
    if not files_to_ingest:
        print("✅ Vector Database & DocStore up to date. Proceeding with existing index.")
        return
        
    print(f"⚠️ Vector Database missing {len(files_to_ingest)} files. Initiating Incremental Auto-Ingestion...")

    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on
    )
    
    for data_file, basename in files_to_ingest:
        print(f"📄 Loading and splitting markdown data for {basename}...")
        with open(data_file, "r", encoding="utf-8") as f:
            markdown_document = f.read()

        # [Pandoc Fix] Scrub any lingering Pandoc media tags (e.g. ![](something){width=something})
        markdown_document = re.sub(r'!\[.*?\]\(.*?\)(\{.*?\})?', '', markdown_document)

        md_header_splits = markdown_splitter.split_text(markdown_document)

        # Prepend headers to page_content and add source_file metadata
        for doc in md_header_splits:
            doc.metadata["source_file"] = basename
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
            f"⚙️ Adding {len(safe_splits)} safe parent documents to the Retriever in batches for {basename}..."
        )

        BATCH_SIZE = 100
        for i in range(0, len(safe_splits), BATCH_SIZE):
            batch = safe_splits[i : i + BATCH_SIZE]
            print(
                f"📦 Processing batch {i//BATCH_SIZE + 1} (Documents {i} to {i + len(batch)})..."
            )
            retriever.add_documents(batch)
            
        manifest.setdefault("ingested_files", []).append(basename)
        save_manifest(manifest)

    print("✅ Auto-Ingestion complete. The Agent's memory is hydrated.")
