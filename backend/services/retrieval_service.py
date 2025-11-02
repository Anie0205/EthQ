import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
import os

# Ensure the database directory exists
os.makedirs("db/chroma_store", exist_ok=True)

client = chromadb.Client(Settings(persist_directory="db/chroma_store"))
collection = client.get_or_create_collection("quiz_context")

embedder = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2") # Corrected model name

def store_text_chunks(text_iterator, source_name: str, chunk_size: int = 1000, batch_size: int = 32):
    """Split the text into chunks and store embeddings in batches"""
    all_chunks = []
    for page_text in text_iterator:
        all_chunks.extend([page_text[i:i+chunk_size] for i in range(0, len(page_text), chunk_size)])

    for i in range(0, len(all_chunks), batch_size):
        batch_chunks = all_chunks[i:i+batch_size]
        if not batch_chunks:  # Skip if batch is empty
            continue
        
        embeddings = embedder.encode(batch_chunks).tolist() # .tolist() to ensure JSON serializable
        ids = [str(uuid.uuid4()) for _ in batch_chunks]
        metadatas = [{"source": source_name}] * len(batch_chunks)

        collection.add(
            documents=batch_chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

def retrieve_context(query: str, top_k: int = 3) -> str:
    """Retrieve top matching chunks for the query"""
    embedding = embedder.encode([query])[0]
    results = collection.query(query_embeddings=[embedding], n_results=top_k)
    docs = [d for doclist in results["documents"] for d in doclist]
    return "\n".join(docs)
