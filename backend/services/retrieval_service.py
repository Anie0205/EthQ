import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
import os

# Ensure the database directory exists
os.makedirs("db/chroma_store", exist_ok=True)

client = chromadb.Client(Settings(persist_directory="db/chroma_store"))
collection = client.get_or_create_collection("quiz_context")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def store_text_chunks(file_text: str, source_name: str):
    """Split the text into chunks and store embeddings"""
    chunks = [file_text[i:i+1000] for i in range(0, len(file_text), 1000)]
    embeddings = embedder.encode(chunks)
    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"source": source_name}] * len(chunks)
    )

def retrieve_context(query: str, top_k: int = 3) -> str:
    """Retrieve top matching chunks for the query"""
    embedding = embedder.encode([query])[0]
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    docs = [d for doclist in results["documents"] for d in doclist]
    return "\n".join(docs)
