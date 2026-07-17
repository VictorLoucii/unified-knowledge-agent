from backend.core.config import cache_vectorstore

def clear_semantic_cache():
    try:
        cache_vectorstore.delete_collection()
        print("✅ Semantic cache cleared successfully!")
    except Exception as e:
        print(f"⚠️ Error clearing cache: {e}")

if __name__ == "__main__":
    clear_semantic_cache()
