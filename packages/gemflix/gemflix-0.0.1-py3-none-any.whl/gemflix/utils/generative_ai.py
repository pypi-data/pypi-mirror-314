from typing import Any, Dict, List, Tuple
import os
import google.generativeai as genai


# Load environment variables
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")


def generate_embeddings(input_data: str) -> list:
    """Generate an embedding vector using Google API"""
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=input_data,
        task_type="retrieval_query",
    )
    return result["embedding"]
