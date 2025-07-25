from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Initialize model
model = SentenceTransformer('intfloat/multilingual-e5-base')

# Initialize ChromaDB (local) using PersistentClient
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="bangla_rag_knowledge_base_v3")


# Load cleaned chunks
def load_chunks(file_path):
    chunks = []
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
        raw_chunks = data.split("=" * 50)
        for block in raw_chunks:
            if block.strip():
                chunks.append(block.strip())
    return chunks


# Embed and store chunks
def index_chunks(chunks):
    for idx, chunk in enumerate(chunks):
        embedding = model.encode(chunk)
        collection.add(
            ids=[f"chunk_{idx}"],
            documents=[chunk],
            embeddings=[embedding.tolist()]  # Convert numpy array to list
        )
        print(f"Indexed chunk_{idx}")


if __name__ == "__main__":
    chunks = load_chunks("data/merged.txt")
    index_chunks(chunks)
    print("Embedding & indexing completed.")
    
