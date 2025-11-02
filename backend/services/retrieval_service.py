import chromadb
from chromadb.config import Settings
from sklearn.feature_extraction.text import TfidfVectorizer # Import TfidfVectorizer
import uuid
import os

# Ensure the database directory exists
os.makedirs("db/chroma_store", exist_ok=True)

client = chromadb.Client(Settings(persist_directory="db/chroma_store"))
collection = client.get_or_create_collection("quiz_context")

# Initialize TfidfVectorizer
# We need to fit this vectorizer when we store chunks, and reuse it for retrieval
vectorizer = TfidfVectorizer()

def store_text_chunks(text_iterator, source_name: str, chunk_size: int = 1000, batch_size: int = 32):
    """Split the text into chunks and store embeddings in batches"""
    all_chunks = []
    for page_text in text_iterator:
        all_chunks.extend([page_text[i:i+chunk_size] for i in range(0, len(page_text), chunk_size)])

    if not all_chunks:
        return

    # Fit and transform the vectorizer with all chunks
    # Note: For production, you might want to save/load the fitted vectorizer
    global vectorizer # Access the global vectorizer instance
    # If the vectorizer has not been fitted, fit it. Otherwise, only transform.
    # This simplified approach assumes the vectorizer should learn from all data.
    # A more robust solution would involve persisting the vectorizer.
    if not hasattr(vectorizer, 'vocabulary_') or not vectorizer.vocabulary_:
        chunk_embeddings = vectorizer.fit_transform(all_chunks)
    else:
        chunk_embeddings = vectorizer.transform(all_chunks)

    # Convert sparse TF-IDF matrix to dense list for ChromaDB
    dense_embeddings = chunk_embeddings.toarray().tolist()

    for i in range(0, len(all_chunks), batch_size):
        batch_chunks = all_chunks[i:i+batch_size]
        if not batch_chunks:  # Skip if batch is empty
            continue
        
        # Get corresponding embeddings for the batch
        batch_embeddings = dense_embeddings[i : i + len(batch_chunks)]

        ids = [str(uuid.uuid4()) for _ in batch_chunks]
        metadatas = [{"source": source_name}] * len(batch_chunks)

        collection.add(
            documents=batch_chunks,
            embeddings=batch_embeddings,
            ids=ids,
            metadatas=metadatas
        )

def retrieve_context(query: str, top_k: int = 3) -> str:
    """Retrieve top matching chunks for the query"""
    global vectorizer # Access the global vectorizer instance
    # Ensure vectorizer has been fitted before transforming the query
    if not hasattr(vectorizer, 'vocabulary_') or not vectorizer.vocabulary_:
        # If vectorizer is not fitted, we cannot retrieve meaningful context.
        # This scenario should ideally not happen if store_text_chunks is called first.
        # For now, return empty or raise an error.
        print("Warning: TfidfVectorizer not fitted. Cannot retrieve context.")
        return ""

    query_embedding = vectorizer.transform([query]).toarray().tolist()[0] # Transform query and convert to list
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    docs = [d for doclist in results["documents"] for d in doclist]
    return "\n".join(docs)
