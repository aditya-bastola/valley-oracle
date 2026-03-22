# utils/db.py
import os
from dotenv import load_dotenv
from supabase import Client, create_client
from langchain_core.documents import Document

load_dotenv()

def get_supabase_client() -> Client:
    """Return an authenticated Supabase client using env vars."""
    return create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )

def upsert_chunks(chunks: list[Document], embeddings: list[list[float]]) -> None:
    """Insert a batch of document chunks and their embeddings into Supabase."""
    client = get_supabase_client()
    rows = [
        {
            "content": chunk.page_content,
            "metadata": chunk.metadata,
            "embedding": embedding,
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]
    client.table("documents").upsert(rows).execute()