import re
import os
import json
from langchain_core.tools import tool
from langchain_text_splitters import MarkdownHeaderTextSplitter
from backend.core.config import get_data_file_paths

@tool
def get_internship_stats() -> str:
    """Returns the total number of unique problems and the number of knowledge base files scanned as a JSON string."""
    unique_problems = set()
    try:
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on
        )
        
        data_files = get_data_file_paths()
        for filepath in data_files:
            if not (filepath.endswith(".md") or filepath.endswith(".docx")):
                continue
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Pandoc scrub
            content = re.sub(r'!\[.*?\]\(.*?\)(\{.*?\})?', '', content)
            
            splits = markdown_splitter.split_text(content)
            for doc in splits:
                headers_text = " ".join(
                    [str(val) for k, val in doc.metadata.items() if "Header" in k]
                )
                full_text = headers_text + "\n" + str(doc.page_content)
                
                matches = re.findall(r"(?i)problem\s*:?\s*(\d+)", full_text)
                if matches:
                    for num in matches:
                        unique_problems.add(num)
                    
        problem_count = len(unique_problems)
        total_files = len(data_files)

        return json.dumps({
            "unique_problems_count": problem_count,
            "total_knowledge_files_scanned": total_files
        })
    except Exception as e:
        return json.dumps({"error": f"Could not determine stats: {e}"})
