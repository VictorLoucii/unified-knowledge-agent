# backend/evals/eval_corpus_growth.py
import json
import os
import sys
import re
import time
from pathlib import Path

# Ensure project root is in sys.path
project_root = str(Path(__file__).parent.parent.parent.resolve())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from langchain_chroma import Chroma
from langchain_classic.storage import InMemoryStore, create_kv_docstore
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_text_splitters import MarkdownHeaderTextSplitter
from backend.core.config import get_data_file_path, embeddings, parent_splitter, child_splitter

def run_corpus_growth_eval():
    dataset_path = os.path.join(os.path.dirname(__file__), "qa_dataset.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        qa_dataset = json.load(f)
        
    data_file = get_data_file_path()
    with open(data_file, "r", encoding="utf-8") as f:
        full_text = f.read()

    # Extract all problems using the standard regex
    all_header_matches = list(re.finditer(r"(?im)^\s*(?:#|//)\s*problem\s*:?\s*(\d+)", full_text))
    
    problems = []
    for i, match in enumerate(all_header_matches):
        prob_num = match.group(1)
        start_idx = match.start()
        end_idx = all_header_matches[i + 1].start() if i + 1 < len(all_header_matches) else len(full_text)
        block = full_text[start_idx:end_idx].strip()
        
        # Normalize header
        if not block.startswith(f"# Problem {prob_num}"):
            first_line_end = block.find("\n")
            if first_line_end != -1:
                block = f"# Problem {prob_num}" + block[first_line_end:]
            else:
                block = f"# Problem {prob_num}"
                
        problems.append({"id": prob_num, "content": block})

    total_problems = len(problems)
    print(f"Total problems found in master markdown: {total_problems}")
    
    # Define test slices (adjust as needed)
    slices = [10, 30, 50, 100, 150, total_problems]
    # Filter slices to not exceed total_problems, and deduplicate
    slices = sorted(list(set([s for s in slices if s < total_problems] + [total_problems])))

    results = []

    for slice_size in slices:
        print(f"\n--- Testing Corpus Size: {slice_size} Problems ---")
        slice_problems = problems[:slice_size]
        slice_ids = [p["id"] for p in slice_problems]
        
        # Build ephemeral markdown document
        slice_markdown = "\n\n".join([p["content"] for p in slice_problems])
        
        # Split markdown by headers
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(slice_markdown)
        
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

        # Initialize Ephemeral Vectorstore and Docstore
        ephemeral_vectorstore = Chroma(
            collection_name=f"temp_eval_{slice_size}_{int(time.time())}",
            embedding_function=embeddings,
        )
        ephemeral_store = create_kv_docstore(InMemoryStore())
        
        retriever = ParentDocumentRetriever(
            vectorstore=ephemeral_vectorstore,
            docstore=ephemeral_store,
            child_splitter=child_splitter,
            parent_splitter=parent_splitter,
            search_kwargs={"k": 40},
        )
        
        print("Ingesting data to ephemeral retriever...")
        safe_splits = parent_splitter.split_documents(md_header_splits)
        BATCH_SIZE = 100
        for i in range(0, len(safe_splits), BATCH_SIZE):
            retriever.add_documents(safe_splits[i: i + BATCH_SIZE])
            
        print("Evaluating Recall@k...")
        recall_hits = 0
        total_targets = 0
        
        for test in qa_dataset:
            target_id = test.get("target_problem_id")
            if target_id is None:
                continue
            
            # Only test if this target_id is actually in our current slice
            if str(target_id) not in slice_ids:
                continue
                
            total_targets += 1
            query = test["query"]
            
            # Retrieve documents
            retrieved_docs = retriever.invoke(query)
            
            # Check if target_id is in any of the retrieved docs
            is_hit = False
            for doc in retrieved_docs:
                h1 = doc.metadata.get("Header 1", "")
                if f"Problem {target_id}" in h1:
                    is_hit = True
                    break
                
                # Fallback check
                if re.search(rf"(?im)^\s*(?:#|//)\s*problem\s*:?\s*{target_id}\b", doc.page_content):
                    is_hit = True
                    break
                    
            if is_hit:
                recall_hits += 1

        if total_targets > 0:
            recall_score = (recall_hits / total_targets) * 100
            print(f"Slice {slice_size}: Recall@k = {recall_hits}/{total_targets} ({recall_score:.1f}%)")
            results.append({"size": slice_size, "score": recall_score, "hits": recall_hits, "total": total_targets})
        else:
            print(f"Slice {slice_size}: No test targets fell into this slice.")
            results.append({"size": slice_size, "score": None, "hits": 0, "total": 0})
            
    print("\n===========================================")
    print("📈 RECALL VS. CORPUS GROWTH REPORT")
    print("===========================================")
    print(f"{'Corpus Size (Problems)':<25} | {'Recall@k Score':<15}")
    print("-" * 43)
    for res in results:
        if res["score"] is not None:
            print(f"{res['size']:<25} | {res['score']:.1f}% ({res['hits']}/{res['total']})")
        else:
            print(f"{res['size']:<25} | N/A")
    print("===========================================")

if __name__ == "__main__":
    run_corpus_growth_eval()
